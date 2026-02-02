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
- 📦 ~~**OBD-II Splitter Cable**~~ - ✅ Already have
- 🚨 **REQUIRED: Bidirectional Logic Level Shifter** - 4 or 5 channel, 3.3V ↔ 5V (~$5-15)
  - [Amazon Search: "bidirectional logic level shifter"](https://www.amazon.com/s?k=bidirectional+logic+level+shifter+5v+3.3v)
  - **SparkFun BOB-12009** or **Adafruit 757** recommended
  - **Must be bidirectional** (not just unidirectional buffer)

---

## ⚠️ CRITICAL: 5V Logic Level Warning

**Your HiLetgo MCP2515 modules with TJA1050 transceivers use 5V logic levels, which WILL DAMAGE the Raspberry Pi 5's 3.3V GPIO pins!**

### The Problem

The MCP2515 chip and most TJA1050-based modules operate at **5V logic levels**. When powered from the Pi's 5V pin, the MCP2515's SPI output pins (especially **MISO/SO**) will output **5V signals** to the Pi's GPIO pins, which are only rated for **3.3V maximum**.

**Result:** Immediate or gradual damage to the Raspberry Pi 5's GPIO pins.

### How to Identify Your Module's Logic Level

**HiLetgo MCP2515 with TJA1050 transceiver = 5V logic (NOT Pi-safe)**

Check your module:
- If it has a **TJA1050** transceiver chip → **5V logic** (needs level shifter)
- If it has a **SN65HVD230** transceiver chip → **3.3V logic** (Pi-safe)
- Look for "3.3V" or "5V" markings on the PCB

### Solution 1: Use a Logic Level Shifter (Recommended)

Use a **bidirectional 4-channel logic level shifter** between the Pi and MCP2515.

**You have: 4-Channel IIC I2C Level Converter Module (Bi-Directional, 5V ↔ 3.3V)**

**Required connections through level shifter:**
- CS (GPIO 8)
- MISO (GPIO 9) ← **Most critical - this outputs 5V from MCP2515**
- MOSI (GPIO 10)
- SCK (GPIO 11)
- INT (GPIO 25) ← *Optional: Can connect directly to Pi (see note below)*

**Level Shifter Module Pinout:**
Your modules have these pins:
- **HV** - High voltage power (5V)
- **LV** - Low voltage power (3.3V)
- **GND** - Common ground
- **HV1, HV2, HV3, HV4** - High voltage signals (5V side)
- **LV1, LV2, LV3, LV4** - Low voltage signals (3.3V side)

**Complete Wiring Diagram:**
```
Raspberry Pi 5              Level Shifter Module        MCP2515 Module
==============              ====================        ==============

Power Connections:
─────────────────
5V (Pin 2) ────────────────→ HV
                             GND ←───────────────────── GND
3.3V (Pin 1) ──────────────→ LV
GND (Pin 6) ───────────────→ GND

5V (Pin 2) ──────────────────────────────────────────→ VCC
GND (Pin 6) ─────────────────────────────────────────→ GND

SPI Signal Connections (through level shifter):
───────────────────────────────────────────────
GPIO 8  (Pin 24) ──────────→ LV1 ←→ HV1 ──────────────→ CS
GPIO 9  (Pin 21) ──────────→ LV2 ←→ HV2 ──────────────→ MISO (SO)
GPIO 10 (Pin 19) ──────────→ LV3 ←→ HV3 ──────────────→ MOSI (SI)
GPIO 11 (Pin 23) ──────────→ LV4 ←→ HV4 ──────────────→ SCK

Interrupt (Optional):
────────────────────
GPIO 25 (Pin 22) ──────────────────────────────────────→ INT
                  (Direct connection - INT is open-drain, safe at 3.3V)
```

**Note about INT pin:** The MCP2515's INT pin is **open-drain** (pulls to GND when active), so it's safe to connect directly to the Pi's 3.3V GPIO without a level shifter. You can use a 10kΩ pull-up resistor to 3.3V if needed, but the Pi's internal pull-up usually works fine.

**Your Level Shifter Modules:**
- ✅ 4-Channel IIC I2C Level Converter
- ✅ Bidirectional (MOSFETs, not just buffers)
- ✅ Presoldered and compact
- ✅ Perfect for this application

### Solution 2: Buy a 3.3V-Compatible Module (Alternative)

Replace your HiLetgo modules with **3.3V-compatible MCP2515 modules** that use the **SN65HVD230** CAN transceiver instead of TJA1050.

**Look for modules labeled:**
- "MCP2515 SN65HVD230"
- "3.3V/5V compatible"
- "Raspberry Pi compatible"

**Note:** These are less common than the 5V TJA1050 versions.

### DO NOT Connect Directly Without Protection!

**NEVER connect your HiLetgo MCP2515 (TJA1050) directly to Pi GPIO!** This is a "works until it doesn't" situation - you might get lucky initially, but it **will** damage your Pi5.

---

## Quick Start Checklist (When Level Shifters Arrive)

Use this checklist to wire everything correctly:

### Power Connections (5 wires):
- [ ] Pi Pin 2 (5V) → Level Shifter **HV**
- [ ] Pi Pin 1 (3.3V) → Level Shifter **LV**
- [ ] Pi Pin 6 (GND) → Level Shifter **GND**
- [ ] Pi Pin 2 (5V) → MCP2515 **VCC** (can share with level shifter wire)
- [ ] Pi Pin 6 (GND) → MCP2515 **GND** (can share with level shifter wire)

### SPI Signal Connections (8 wires through level shifter):
- [ ] Pi Pin 24 (GPIO 8) → Level Shifter **LV1** → Level Shifter **HV1** → MCP2515 **CS**
- [ ] Pi Pin 21 (GPIO 9) → Level Shifter **LV2** → Level Shifter **HV2** → MCP2515 **MISO/SO**
- [ ] Pi Pin 19 (GPIO 10) → Level Shifter **LV3** → Level Shifter **HV3** → MCP2515 **MOSI/SI**
- [ ] Pi Pin 23 (GPIO 11) → Level Shifter **LV4** → Level Shifter **HV4** → MCP2515 **SCK**

### Optional Interrupt (1 wire, direct):
- [ ] Pi Pin 22 (GPIO 25) → MCP2515 **INT** (direct connection, no level shifter needed)

### CAN Bus Connections (to OBD-II):
- [ ] MCP2515 **CAN-H** → OBD-II Pin 6
- [ ] MCP2515 **CAN-L** → OBD-II Pin 14
- [ ] MCP2515 **GND** → OBD-II Pin 4 or 5

### Verification:
- [ ] Double-check all connections match the diagrams above
- [ ] Verify level shifter HV is connected to 5V, LV to 3.3V
- [ ] Ensure NO direct connections between MCP2515 SPI pins and Pi GPIO
- [ ] All grounds are connected together (Pi, level shifter, MCP2515)

**Total wire count:** ~14 wires (5 power + 8 SPI through shifter + 1 INT)

---

## MCP2515 to Raspberry Pi 5 Wiring

**IMPORTANT: This wiring assumes you are using a logic level shifter as described above!**

The MCP2515 uses SPI to communicate with the Raspberry Pi.

### Pin Connections (WITH 4-Channel Level Shifter)

**Step-by-step wiring table:**

| Step | Component | Pin | Wire Color | Connects To | Component | Pin |
|------|-----------|-----|------------|-------------|-----------|-----|
| **POWER CONNECTIONS** |
| 1 | Raspberry Pi 5 | Pin 2 (5V) | Red | → | Level Shifter | HV |
| 2 | Raspberry Pi 5 | Pin 1 (3.3V) | Orange | → | Level Shifter | LV |
| 3 | Raspberry Pi 5 | Pin 6 (GND) | Black | → | Level Shifter | GND |
| 4 | Raspberry Pi 5 | Pin 2 (5V) | Red | → | MCP2515 | VCC |
| 5 | Raspberry Pi 5 | Pin 6 (GND) | Black | → | MCP2515 | GND |
| **SPI SIGNAL CONNECTIONS** (through level shifter) |
| 6 | Raspberry Pi 5 | Pin 24 (GPIO 8) | White | → | Level Shifter | LV1 |
| 7 | Level Shifter | HV1 | White | → | MCP2515 | CS |
| 8 | Raspberry Pi 5 | Pin 21 (GPIO 9) | Yellow | → | Level Shifter | LV2 |
| 9 | Level Shifter | HV2 | Yellow | → | MCP2515 | MISO (SO) |
| 10 | Raspberry Pi 5 | Pin 19 (GPIO 10) | Green | → | Level Shifter | LV3 |
| 11 | Level Shifter | HV3 | Green | → | MCP2515 | MOSI (SI) |
| 12 | Raspberry Pi 5 | Pin 23 (GPIO 11) | Blue | → | Level Shifter | LV4 |
| 13 | Level Shifter | HV4 | Blue | → | MCP2515 | SCK |
| **INTERRUPT (Optional)** |
| 14 | Raspberry Pi 5 | Pin 22 (GPIO 25) | Purple | → | MCP2515 | INT |

**Notes:**
- Wire colors are suggestions - use whatever you have available
- Steps 1-3: Power the level shifter from Pi (both 5V and 3.3V needed)
- Steps 4-5: Power the MCP2515 from Pi 5V
- Steps 6-13: SPI signals go through level shifter (Pi 3.3V ↔ MCP2515 5V)
- Step 14: INT can connect directly (open-drain, safe at 3.3V)

### Visual Wiring Diagram (WITH 4-Channel Level Shifter)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         COMPLETE WIRING DIAGRAM                         │
└─────────────────────────────────────────────────────────────────────────┘

    RASPBERRY PI 5              LEVEL SHIFTER             MCP2515 MODULE
    ==============              =============             ==============
    GPIO Header                 4-Ch Module               CAN Controller

    Pin 1  (3.3V) ────────────→ LV
    Pin 2  (5V)   ───┬────────→ HV          ┌──────────→ VCC
                     │                      │
    Pin 6  (GND)  ───┼────────→ GND ────────┼──────────→ GND
                     │                      │
                     └──────────────────────┘

    Pin 24 (GPIO 8)  ────────→ LV1 ←→ HV1 ───────────→ CS

    Pin 21 (GPIO 9)  ────────→ LV2 ←→ HV2 ───────────→ MISO (SO)
                                         ↑
                                         └─ CRITICAL: 5V → 3.3V conversion!

    Pin 19 (GPIO 10) ────────→ LV3 ←→ HV3 ───────────→ MOSI (SI)

    Pin 23 (GPIO 11) ────────→ LV4 ←→ HV4 ───────────→ SCK

    Pin 22 (GPIO 25) ─────────────────────────────────→ INT (direct)


┌─────────────────────────────────────────────────────────────────────────┐
│                    LEVEL SHIFTER MODULE PINOUT                          │
└─────────────────────────────────────────────────────────────────────────┘

Your 4-Channel IIC I2C Level Converter module looks like this:

        LV Side (3.3V)              HV Side (5V)
        ==============              ============

        [ LV4 ]                     [ HV4 ]  ← To MCP2515 SCK
        [ LV3 ]                     [ HV3 ]  ← To MCP2515 MOSI
        [ LV2 ]                     [ HV2 ]  ← To MCP2515 MISO
        [ LV1 ]                     [ HV1 ]  ← To MCP2515 CS
        [ GND ]  ← Common ground
        [ LV  ]  ← 3.3V from Pi
        [ HV  ]  ← 5V from Pi

        ↑                           ↑
        From Pi GPIO                To MCP2515


┌─────────────────────────────────────────────────────────────────────────┐
│                  RASPBERRY PI 5 GPIO HEADER                             │
└─────────────────────────────────────────────────────────────────────────┘

View from above (USB ports at bottom):

        3.3V [ 1] [ 2] 5V     ← To Level Shifter LV and HV, MCP2515 VCC
       GPIO2 [ 3] [ 4] 5V
       GPIO3 [ 5] [ 6] GND    ← Common GND (to Level Shifter & MCP2515)
       GPIO4 [ 7] [ 8] GPIO14
         GND [ 9] [10] GPIO15
      GPIO17 [11] [12] GPIO18
      GPIO27 [13] [14] GND
      GPIO22 [15] [16] GPIO23
        3.3V [17] [18] GPIO24
 MOSI/GPIO10 [19] [20] GND    ← To Level Shifter LV3
 MISO/GPIO9  [21] [22] GPIO25 ← To Level Shifter LV2 | To MCP2515 INT
 SCLK/GPIO11 [23] [24] GPIO8  ← To Level Shifter LV4 | To Level Shifter LV1
         GND [25] [26] GPIO7


┌─────────────────────────────────────────────────────────────────────────┐
│                      MCP2515 MODULE PINOUT                              │
└─────────────────────────────────────────────────────────────────────────┘

Typical HiLetgo MCP2515 module pin headers:

    [ VCC  ]  ← 5V from Pi Pin 2
    [ GND  ]  ← GND from Pi Pin 6
    [ CS   ]  ← From Level Shifter HV1
    [ SO   ]  ← To Level Shifter HV2 (MISO - outputs 5V!)
    [ SI   ]  ← From Level Shifter HV3 (MOSI)
    [ SCK  ]  ← From Level Shifter HV4
    [ INT  ]  ← To Pi GPIO 25 (optional, can be direct)

    [ CANH ]  ← To OBD-II Pin 6
    [ CANL ]  ← To OBD-II Pin 14


IMPORTANT: ALL 4 SPI signals (CS, MISO, MOSI, SCK) MUST go through the
level shifter. NEVER connect MCP2515 SPI pins directly to Pi GPIO!
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
