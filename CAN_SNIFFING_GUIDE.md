# CAN Bus Sniffing Guide for 2013 WRX

Guide for sniffing CAN bus data using Raspberry Pi 5 with OpenDash and MCP2515 module.

---

## Hardware Setup

### What You Have:
- ✅ Raspberry Pi 5 with OpenDash installed
- ✅ 2x MCP2515 CAN Bus Module (TJA1050 transceiver)
- ✅ Jumper wires
- ✅ 12V to 5V buck converter

### What You Need to Buy:
- 📦 **OBD-II Splitter Cable** - Male-to-Dual-Female Y-cable (~$15-25)
  - [Amazon Search](https://www.amazon.com/s?k=obd2+splitter+cable)

---

## MCP2515 to Raspberry Pi 5 Wiring

The MCP2515 uses SPI to communicate with the Raspberry Pi.

### Pin Connections

| MCP2515 Pin | Pi5 GPIO Pin | Pi5 Pin # | Notes |
|-------------|--------------|-----------|-------|
| **VCC** | 5V Power | Pin 2 or 4 | 5V power |
| **GND** | Ground | Pin 6, 9, 14, 20, etc | Common ground |
| **CS** | GPIO 8 (CE0) | Pin 24 | SPI Chip Select |
| **SO (MISO)** | GPIO 9 (MISO) | Pin 21 | SPI Data Out |
| **SI (MOSI)** | GPIO 10 (MOSI) | Pin 19 | SPI Data In |
| **SCK** | GPIO 11 (SCLK) | Pin 23 | SPI Clock |
| **INT** | GPIO 25 | Pin 22 | Interrupt (optional but recommended) |

### Visual Pinout

```
Raspberry Pi 5 GPIO Header (view from above):
        3.3V [ 1] [ 2] 5V     ← Connect VCC here
       GPIO2 [ 3] [ 4] 5V
       GPIO3 [ 5] [ 6] GND    ← Connect GND here
       GPIO4 [ 7] [ 8] GPIO14
         GND [ 9] [10] GPIO15
      GPIO17 [11] [12] GPIO18
      GPIO27 [13] [14] GND
      GPIO22 [15] [16] GPIO23
        3.3V [17] [18] GPIO24
 MOSI/GPIO10 [19] [20] GND
 MISO/GPIO9  [21] [22] GPIO25 ← Connect INT here
 SCLK/GPIO11 [23] [24] GPIO8  ← Connect CS here
         GND [25] [26] GPIO7
```

---

## MCP2515 to OBD-II Wiring

### OBD-II Pinout
```
        ___________________
       /                   \
      | 1  2  3  4  5  6  7  8 |
      |  9  10 11 12 13 14 15 16|
       \_______________________/

Pin 4:  Chassis Ground
Pin 5:  Signal Ground
Pin 6:  CAN High (CAN-H)     ← Connect to MCP2515 CAN-H
Pin 14: CAN Low (CAN-L)      ← Connect to MCP2515 CAN-L
Pin 16: Battery Positive (12V)
```

### Connections

| MCP2515 | OBD-II Pin | Typical Wire Color |
|---------|------------|-------------------|
| **CAN-H** | Pin 6 | Green or Yellow |
| **CAN-L** | Pin 14 | Green/White or Yellow/Black |
| **GND** | Pin 4 or 5 | Black |

**Note:** You'll use the OBD-II splitter to tap into these wires without cutting your main cable.

---

## Software Configuration

### Step 1: Enable SPI on Raspberry Pi

1. **SSH into your Pi5 or open terminal:**
```bash
ssh pi@opendash.local
# or use default user if different
```

2. **Enable SPI interface:**
```bash
sudo raspi-config
```
- Navigate to: `3 Interface Options`
- Select: `I4 SPI`
- Choose: `Yes` to enable
- Reboot: `sudo reboot`

### Step 2: Configure MCP2515 Overlay

1. **Edit boot config:**
```bash
sudo nano /boot/firmware/config.txt
```

2. **Add MCP2515 overlay at the end:**
```bash
# MCP2515 CAN Bus Configuration
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
# Use 16000000 if your module has 16MHz crystal
```

**Important:** Check your MCP2515 module for the crystal frequency:
- Most modules use **8MHz** (Y1 crystal marked "8.000")
- Some use **16MHz** (Y1 crystal marked "16.000")

3. **Save and exit:** `Ctrl+X`, then `Y`, then `Enter`

4. **Reboot:**
```bash
sudo reboot
```

### Step 3: Install CAN Utilities

```bash
sudo apt-get update
sudo apt-get install can-utils
```

### Step 4: Bring Up CAN Interface

1. **Manual startup (for testing):**
```bash
sudo ip link set can0 up type can bitrate 500000
```

**Note:** Most modern cars use 500kbps (500000). Older cars might use 250kbps.

2. **Auto-start on boot (recommended):**

Create a systemd service:
```bash
sudo nano /etc/systemd/system/can0.service
```

Add this content:
```ini
[Unit]
Description=CAN0 Interface
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/sbin/ip link set can0 up type can bitrate 500000
ExecStop=/sbin/ip link set can0 down

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable can0.service
sudo systemctl start can0.service
```

3. **Verify CAN interface is up:**
```bash
ifconfig can0
```

You should see something like:
```
can0: flags=193<UP,RUNNING,NOARP>  mtu 16
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 10  (UNSPEC)
```

---

## Sniffing CAN Bus Data

### Method 1: Using candump (Simple)

1. **Connect hardware:**
   - MCP2515 connected to Pi5 GPIO
   - OBD-II splitter plugged into car
   - MCP2515 CAN-H/CAN-L connected to splitter
   - Turn on ignition (engine can be off or running)

2. **Start sniffing:**
```bash
candump can0
```

**Output example:**
```
  can0  140   [8]  0F A0 12 34 00 00 00 00
  can0  360   [8]  5A 48 3C 00 00 00 00 00
  can0  0D1   [8]  00 3E 80 00 00 00 00 00
```

3. **Save to file:**
```bash
candump can0 -l
# Creates file: candump-YYYY-MM-DD_HHMMSS.log
```

### Method 2: Using cansniffer (Interactive)

```bash
cansniffer can0
```

**Features:**
- Shows only changing values (great for identifying RPM, speed, etc.)
- Highlights bytes that change
- Press `q` to quit

### Method 3: Using Python (Advanced)

Install python-can:
```bash
sudo apt-get install python3-pip
pip3 install python-can
```

Create a sniffing script:
```python
#!/usr/bin/env python3
import can
import time

# Initialize CAN bus
bus = can.interface.Bus(channel='can0', bustype='socketcan')

print("Sniffing CAN bus (Ctrl+C to stop)...")
print("ID      DLC  Data")
print("-" * 50)

unique_ids = set()

try:
    while True:
        msg = bus.recv(timeout=1.0)
        if msg:
            unique_ids.add(msg.arbitration_id)
            data_str = ' '.join(f'{byte:02X}' for byte in msg.data)
            print(f"0x{msg.arbitration_id:03X}  [{msg.dlc}]  {data_str}")

except KeyboardInterrupt:
    print("\n\nUnique CAN IDs seen:")
    for can_id in sorted(unique_ids):
        print(f"  0x{can_id:03X}")

bus.shutdown()
```

Save as `can_sniffer.py` and run:
```bash
chmod +x can_sniffer.py
./can_sniffer.py
```

### Method 4: Using OpenDash (GUI)

OpenDash already has SocketCAN support. You can:
1. Create a vehicle plugin that logs CAN data
2. Display real-time CAN data on the OpenDash UI
3. Use the existing OBD-II interface to request standard PIDs

Check the OpenDash vehicle plugin documentation for more details.

---

## Identifying CAN IDs for Your WRX

### What to Look For:

1. **Start engine and let it idle**
2. **Watch for changing values:**
   - **RPM:** Rev the engine - find ID where values increase/decrease with RPM
   - **Speed:** Drive the car - find ID that changes with vehicle speed
   - **Coolant Temp:** Watch for slowly increasing value as engine warms
   - **Throttle:** Press accelerator - find ID that changes with pedal position

3. **Common Subaru CAN IDs (Reference - verify on your car):**

| CAN ID | Likely Data | How to Verify |
|--------|-------------|---------------|
| 0x140 | Engine RPM | Changes with engine speed |
| 0x141 | Throttle Position | Changes with accelerator pedal |
| 0x144 | Wheel Speeds | Changes when driving |
| 0x0D0 | Steering Angle | Turn steering wheel |
| 0x0D1 | Vehicle Speed / Brake | Drive or press brake |
| 0x360 | Coolant / Oil Temp | Slowly changes as engine warms |
| 0x361 | Fuel System | May show fuel level/consumption |
| 0x7E8 | OBD-II ECU Response | Appears when requesting OBD PIDs |

4. **Document your findings:**
   - Create a spreadsheet or text file
   - Note the CAN ID, byte positions, and what they represent
   - Record scaling factors (e.g., RPM = (byte1 * 256 + byte2) / 4)

---

## Requesting OBD-II Data

### Using cansend

```bash
# Request RPM (PID 0x0C)
cansend can0 7DF#020C000000000000

# Request Speed (PID 0x0D)
cansend can0 7DF#020D000000000000

# Request Coolant Temp (PID 0x05)
cansend can0 7DF#0205000000000000
```

Watch for responses on ID `0x7E8` using `candump can0`

---

## Troubleshooting

### No CAN interface (can0 not found)
```bash
# Check if overlay is loaded
dmesg | grep mcp251x

# Should see something like:
# mcp251x spi0.0 can0: MCP2515 successfully initialized.
```

**Solutions:**
- Verify SPI is enabled: `ls /dev/spi*` (should show /dev/spidev0.0)
- Check wiring connections
- Verify oscillator frequency in config.txt matches your module

### CAN interface up but no messages
- Check CAN-H and CAN-L connections to OBD-II
- Verify car ignition is ON
- Try different bitrate: `sudo ip link set can0 down && sudo ip link set can0 up type can bitrate 250000`
- Check for proper termination (120Ω resistor)

### "No buffer space available" error
```bash
sudo ip link set can0 down
sudo ip link set can0 up type can bitrate 500000
```

### Too many messages / flooding
```bash
# Filter by specific ID
candump can0,140:7FF
# Shows only ID 0x140

# Filter range
candump can0,100:700
# Shows IDs 0x100-0x6FF
```

---

## Next Steps

1. **Sniff CAN bus** while driving to identify all relevant IDs
2. **Document byte positions** for each data point (RPM, speed, temp, etc.)
3. **Determine scaling factors** (how raw bytes convert to real values)
4. **Create a mapping table** for your digital dash implementation
5. **Integrate findings** into OpenDash or your custom dash code

---

## Safety Notes

⚠️ **Important:**
- CAN sniffing is **read-only** and won't affect your car's operation
- **DO NOT send random CAN messages** while driving - this can interfere with vehicle systems
- Test in a safe, stationary environment first
- Use OBD-II splitter to avoid disconnecting the factory ECU

---

## References

- [SocketCAN Documentation](https://www.kernel.org/doc/html/latest/networking/can.html)
- [MCP2515 Datasheet](http://ww1.microchip.com/downloads/en/DeviceDoc/MCP2515-Stand-Alone-CAN-Controller-with-SPI-20001801J.pdf)
- [Python-CAN Documentation](https://python-can.readthedocs.io/)
- [OpenDash Vehicle Plugins](https://github.com/openDsh/dash/tree/main/plugins/vehicle)
