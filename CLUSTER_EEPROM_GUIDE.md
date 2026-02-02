# Subaru Cluster EEPROM Guide

This guide covers reading and writing the EEPROM chip in the 2013 WRX instrument cluster for backup, mileage transfer, and modification purposes.

---

## Hardware Required

### CH341A USB EEPROM Programmer
**Product:** [CH341A USB Programmer](https://www.amazon.com/dp/B07VNVVXW6)

**Features:**
- USB interface for PC connection
- Support for 24xxx and 25xxx series EEPROM/Flash chips
- SOIC8 test clip included for in-circuit programming
- SPI pin headers for custom connections
- 500mA self-recovery fuse protection
- Programming/TTL conversion interface

**Included Accessories:**
- Main CH341A programmer board
- SOIC8 IC test clip (1.27mm pitch)
- Adapter boards for 8/16 pin chips
- USB cable

---

## CH341A Physical Setup Guide

### What's in the Box

Your CH341A programmer kit includes:
1. **Main CH341A programmer board** (black PCB with USB port)
2. **SOIC8 test clip** (black clip with spring-loaded pins)
3. **Ribbon cable** (gray/red wires connecting clip to adapter)
4. **Small green adapter boards** (150mil and 200mil SOIC8-to-DIP8 adapters)
5. **USB cable** (for connecting programmer to PC)

### Understanding the Components

#### Main CH341A Board
- Has a **ZIF socket** (Zero Insertion Force - the white socket that opens/closes)
- The ZIF socket accepts DIP8 chips or adapter boards
- **Important:** There's a small notch/mark on one end of the ZIF socket indicating Pin 1

#### SOIC8 Test Clip
- Spring-loaded clip that grabs onto surface-mount chips
- **Red wire = Pin 1** (this is critical!)
- 8 pins inside the clip match the 8 pins on the SOIC8 chip
- Works with 1.27mm pitch (standard SOIC8 spacing)

#### Adapter Boards
- Convert SOIC8 chips to DIP8 format
- Allow you to desolder the chip and insert it into an adapter
- Then insert the adapter into the CH341A ZIF socket

---

## Setup Method 1: Using the SOIC8 Test Clip (Recommended)

This method lets you read/write the EEPROM **without desoldering** it from the cluster PCB.

### Step 1: Connect the Clip to the CH341A Board

**Option A: Direct Connection (if your clip has a 8-pin header)**
1. Locate the **8-pin header** on the CH341A board (usually labeled with pin numbers)
2. The clip's ribbon cable should have a connector that plugs into this header
3. **Orientation matters:** The red wire must align with Pin 1 on the header

**Option B: Using the Green Adapter Board**
1. Take one of the small green adapter boards
2. Look for the ribbon cable connector on the adapter board
3. Plug the clip's ribbon cable into the adapter board
   - **Red wire = Pin 1** (there should be a marking)
4. Insert the adapter board into the CH341A ZIF socket
   - Open the ZIF lever
   - Insert adapter with Pin 1 aligned to the Pin 1 mark on the socket
   - Close the ZIF lever

### Step 2: Connect to Your Computer
1. Plug USB cable into the CH341A board
2. Connect the other end to your computer
3. Windows should detect the device (install drivers if prompted)

### Step 3: Connect Clip to the S93C76 Chip

**Before clipping onto the chip:**
1. **POWER OFF** the cluster completely
2. Locate the S93C76 chip on your cluster PCB
3. Find **Pin 1** on the chip:
   - Look for a small dot in one corner
   - Or a notch/chamfer on one edge
   - Pin 1 is typically top-left when chip text is readable

**Clipping onto the chip:**
1. Orient the test clip so the **red wire** will be at Pin 1 of the chip
2. Carefully open the clip
3. Align it over the chip - all 8 pins must line up
4. Gently release the clip to clamp onto the chip
5. **Verify:** Ensure all 8 pins are making contact

```
    View from above:

    ┌─────────────┐
    │ S93C76      │  ← Chip on PCB
    │ ●           │  ← Pin 1 dot
    └─────────────┘

    Red wire here ─→ ●─┐
                       ├─ Test Clip
                       │
                      ─┘
```

---

## Setup Method 2: Using Adapter Boards (Advanced)

Only use this if you're comfortable with SMD soldering and desoldering.

### Step 1: Desolder the S93C76
1. Use hot air station or fine-tip soldering iron
2. Carefully remove chip from cluster PCB
3. Clean the chip pins with isopropyl alcohol

### Step 2: Insert Chip into Adapter Board
1. Take a green adapter board
2. Identify Pin 1 position (marked on the adapter)
3. Carefully solder the S93C76 chip to the adapter
   - **Pin 1 of chip → Pin 1 of adapter**
   - All 8 pins must be soldered cleanly

### Step 3: Insert Adapter into CH341A
1. Open the ZIF socket lever on the CH341A
2. Insert the adapter board
   - Pin 1 of adapter → Pin 1 marking on ZIF socket
3. Close the ZIF lever
4. Connect USB cable to computer

---

## Pin Alignment Reference

**Critical:** Pin 1 must be correctly aligned throughout the chain.

### SOIC8 Chip Pin Numbering
```
Top view of S93C76 chip:

    ●─┐ ← Pin 1 (dot marking)
  1 │ │ 8
  2 │ │ 7
  3 │ │ 6
  4 │ │ 5
    └─┘

Pin 1 = CS (Chip Select)
Pin 8 = VCC (+5V)
```

### Test Clip Connection
```
Red wire on clip = Pin 1

Looking at clip from above:

    Red ─→ [1 2 3 4 5 6 7 8] ← Clip pins
           └────────────────┘
```

### CH341A ZIF Socket (16-pin) with 8-pin Adapter

The CH341A has a **16-pin ZIF socket** but SOIC8 adapters only use **8 pins**.

**Important:** The 8-pin adapter goes on the **LEFT side** of the socket (when Pin 1 notch is at top).

```
Top view of CH341A ZIF socket (16 pins total):

Pin 1 notch ─→  ┌─┐
                │ │  ← Lever (lift to open)
                │ │
     ┌──────────┴─┴──────────┐
  1  │ ○                    ○ │ 16
  2  │ ○                    ○ │ 15
  3  │ ○                    ○ │ 14
  4  │ ○                    ○ │ 13
  5  │ ○                    ○ │ 12
  6  │ ○                    ○ │ 11
  7  │ ○                    ○ │ 10
  8  │ ○                    ○ │ 9
     └────────────────────────┘

     ↑ Use these 8 holes
     (Pins 1-8 on LEFT side)
```

**How to insert 8-pin adapter:**
```
Step 1: Lift the lever to open the ZIF socket

Step 2: Insert adapter on LEFT side, aligning Pin 1

Pin 1 notch ─→  ┌─┐
                │ │
     ┌──────────┴─┴──────────┐
  1  │ ●                    ○ │  ← Adapter pins in
  2  │ ●                    ○ │     these 8 holes
  3  │ ●                    ○ │     (pins 1-8)
  4  │ ●                    ○ │
  5  │ ●                    ○ │  ← Empty holes
  6  │ ●                    ○ │     on right side
  7  │ ●                    ○ │     (pins 9-16)
  8  │ ●                    ○ │
     └────────────────────────┘
     ● = Adapter board pins
     ○ = Empty holes

Step 3: Close the lever to clamp the adapter
```

**Key Points:**
- **Pin 1 of adapter → Pin 1 of ZIF socket** (top-left when notch is at top)
- Adapter sits on **LEFT side** (pins 1-8)
- **Right side pins (9-16) stay empty**
- Notch/mark on ZIF socket shows Pin 1 location

---

## Common Connection Mistakes

❌ **Wrong Pin 1 alignment**
- Double-check red wire position
- Verify chip Pin 1 dot/notch
- Confirm ZIF socket Pin 1 marking

❌ **Poor clip contact**
- Clip not fully seated on chip
- Dirty chip pins (clean with isopropyl alcohol)
- Bent pins on test clip

❌ **Cluster still powered**
- ALWAYS disconnect cluster power before connecting programmer
- Residual power can damage chip or programmer

---

## Testing Your Connection

Before attempting to read the EEPROM:

1. **Visual inspection:**
   - All clip pins touching chip legs
   - Red wire at Pin 1 position
   - No bent pins or poor contacts

2. **Software detection:**
   - Open AsProgrammer
   - Select "93C76" chip
   - Click "Detect" or "Read IC"
   - If it reads data (not all 0xFF or 0x00), connection is good

3. **Verify read:**
   - Read the chip twice
   - Compare both files - they should be identical
   - If different, connection is unreliable

---

## Software Options

### Option 1: AsProgrammer (Recommended for Windows)
- **Included in this repo:** `tools/AsProgrammer/AsProgrammer.exe`
- Also available on [GitHub](https://github.com/nofeletru/UsbAsp-flash-dump)
- Free and open source
- Supports wide range of EEPROM chips including 93C76
- Simple interface for read/write/verify operations

**Running AsProgrammer:**
1. Navigate to `tools/AsProgrammer/`
2. Run `AsProgrammer.exe`
3. No installation needed - it's portable

**For 93C76 chip in AsProgrammer:**
1. Select chip: Look for "93C76" or "SII 93C76" in chip database
2. Choose organization: Usually 8-bit (x8) mode for automotive applications
3. Verify voltage: 5V setting

### Option 2: CH341A Programmer Software
- Usually included on CD with hardware or downloadable from manufacturer
- Windows-based GUI application
- Chip auto-detection feature

### Option 3: Flashrom (Linux/Advanced Users)
```bash
# Install flashrom
sudo apt-get install flashrom

# Read EEPROM
flashrom -p ch341a_spi -r cluster_backup.bin

# Write EEPROM
flashrom -p ch341a_spi -w cluster_backup.bin
```

---

## Subaru Cluster EEPROM Details

### Cluster Information
**Vehicle:** 2013 Subaru WRX
**Cluster Type:** Factory instrument cluster
**Purpose:** Backup cluster purchased from eBay

### Main Microcontroller (MCU)
**Chip Model:** MB90428GAV
**Manufacturer:** Fujitsu
**Family:** F2MC-16LX series
**Type:** 16-bit microcontroller
**Common Use:** Automotive instrument clusters, body control modules
**Features:** Built-in CAN controller, A/D converter, timer units

### EEPROM Chip Details
**Chip Model:** S93C76 (Seiko/SII 93C76)
**Package Type:** SOIC8 (surface mount)
**Capacity:** 8Kbit (1024 bytes / 1KB)
**Interface:** Microwire/SPI (3-wire serial)
**Voltage:** 5V (4.5V - 5.5V)
**Organization:** 1024 x 8 bits or 512 x 16 bits
**Location on PCB:** _Located near MB90428GAV MCU on main cluster PCB_

**Pin Configuration (SOIC8):**
```
    Pin 1: CS  (Chip Select)
    Pin 2: SK  (Serial Clock)
    Pin 3: DI  (Data In)
    Pin 4: DO  (Data Out)
    Pin 5: GND (Ground)
    Pin 6: ORG (Organization Select - typically tied to VCC or GND)
    Pin 7: NC  (No Connect)
    Pin 8: VCC (Power Supply +5V)
```

### Data Stored in Cluster EEPROM
The EEPROM typically contains:
- **Odometer/mileage data**
- **VIN (Vehicle Identification Number)**
- Calibration data
- Security/immobilizer information (if applicable)
- Configuration settings

---

## Safety Warnings

⚠️ **IMPORTANT PRECAUTIONS:**

1. **Power Off:** Ensure the cluster is completely disconnected from vehicle power before attempting EEPROM access
2. **Voltage Levels:** Most automotive EEPROMs are 5V - verify chip specifications before connecting
3. **Static Protection:** Use ESD protection when handling the cluster PCB
4. **Backup First:** ALWAYS read and backup the original EEPROM data before any modifications
5. **Legal Notice:** Modifying odometer data may be illegal in your jurisdiction - this guide is for backup and restoration purposes only

---

## Procedure

### Step 1: Cluster Disassembly
1. Remove instrument cluster from vehicle (if not already removed)
2. Remove cluster housing/cover to access PCB
3. Locate the EEPROM chip on the PCB
   - Look for 8-pin IC chips (SOIC8 or DIP8)
   - Common locations: near the main processor or display connector
   - Check chip markings against datasheet

### Step 2: EEPROM Connection

#### Method A: Using SOIC8 Test Clip (In-Circuit Programming)
1. Identify pin 1 on the EEPROM chip (usually marked with dot or notch)
2. Align the red wire on the test clip to pin 1
3. Carefully clamp the clip onto the EEPROM chip
4. Connect the clip to the CH341A programmer's ZIF socket or header pins

**SOIC8 Clip Pinout:**
```
Red wire = Pin 1

    Pin 1 ●─┐
    Pin 2   │
    Pin 3   ├─ SOIC8 Chip
    Pin 4   │
    Pin 5   │
    Pin 6   │
    Pin 7   │
    Pin 8  ─┘
```

#### Method B: Desoldering (More Reliable)
1. Use hot air station or soldering iron to carefully remove EEPROM
2. Insert chip into appropriate adapter board
3. Insert adapter into CH341A ZIF socket
4. **Note:** Only do this if comfortable with SMD soldering

### Step 3: Reading the EEPROM

#### Using AsProgrammer:
1. Connect CH341A to computer via USB
2. Launch AsProgrammer
3. Select your EEPROM chip model from the database
4. Click "Read" button
5. Save the file with a descriptive name: `cluster_backup_YYYYMMDD.bin`
6. **Verify:** Read again and compare files to ensure accuracy

#### Using Command Line (Linux):
```bash
# Read EEPROM contents
flashrom -p ch341a_spi -c "CHIP_MODEL" -r cluster_backup.bin

# Verify the read
flashrom -p ch341a_spi -c "CHIP_MODEL" -v cluster_backup.bin
```

### Step 4: Writing to EEPROM (If Needed)

⚠️ **Warning:** Writing incorrect data can brick your cluster. Only proceed if you have a verified backup.

#### Using AsProgrammer:
1. Load the backup file you want to write
2. Click "Write" button
3. Wait for write operation to complete
4. Click "Verify" to confirm write was successful

#### Using Command Line (Linux):
```bash
# Write to EEPROM
flashrom -p ch341a_spi -c "CHIP_MODEL" -w cluster_backup.bin

# Verify write
flashrom -p ch341a_spi -c "CHIP_MODEL" -v cluster_backup.bin
```

### Step 5: Testing
1. Disconnect CH341A programmer
2. Reinstall EEPROM (if removed) or remove test clip
3. Reinstall cluster in vehicle
4. Power on and verify:
   - Odometer reading matches expectation
   - All gauges function properly
   - No warning lights related to cluster communication

---

## Troubleshooting

### CH341A Not Detected
- Check USB cable connection
- Install CH341 drivers (Windows)
- Try different USB port
- Check device manager for unknown devices

### Cannot Read EEPROM / Read Errors
- Verify correct chip model selected in software
- Check test clip connection (ensure all pins are making contact)
- Try lowering SPI clock speed in software settings
- Ensure chip is not write-protected (check WP pin)
- Verify cluster is completely powered off

### Read Data Appears All 0xFF or 0x00
- Poor connection - reseat test clip
- Wrong chip selected in software
- Chip may be damaged
- Voltage level mismatch

---

## Common Subaru EEPROM Chips

Subaru clusters commonly use these EEPROM chips:
- **24C16** (2KB, I2C interface)
- **24C08** (1KB, I2C interface)
- **93C56** (2KB, Microwire interface)
- **93C66** (4KB, Microwire interface)
- **93C76** (1KB, Microwire interface) ← **Your cluster uses this chip**

> **Note:** The 93Cxx series uses Microwire/SPI interface, while 24Cxx uses I2C. Make sure your programmer software is configured for the correct protocol.

---

## Important Notes for 93C76

### Organization Mode
The 93C76 can operate in two modes:
- **x8 mode** (1024 x 8 bits) - Most common for automotive clusters
- **x16 mode** (512 x 16 bits)

The ORG pin (pin 6) determines the mode:
- ORG tied to GND = x16 mode
- ORG tied to VCC = x8 mode

**Check your cluster PCB to see how the ORG pin is connected.** Most Subaru clusters use x8 mode.

### Reading 93C76 with CH341A
The CH341A supports Microwire/SPI EEPROMs like the 93C76. When using the test clip:
1. Ensure pin 1 (CS) aligns with the red wire on the clip
2. The CH341A will provide 5V power to the chip
3. Select "93C76" in your programmer software
4. Choose x8 or x16 organization based on your cluster's configuration

### File Size
When you read the 93C76, the backup file should be:
- **1024 bytes (1KB)** in x8 mode
- **1024 bytes (1KB)** in x16 mode (same size, different organization)

If your file is significantly different, double-check chip selection and connection.

---

## Next Steps

- [ ] Identify EEPROM chip on backup cluster PCB
- [ ] Document chip model and location (add photos)
- [ ] Read and backup original EEPROM data
- [ ] Test cluster functionality after EEPROM read
- [ ] Document any findings about data structure

---

## References

- [CH341A Programmer GitHub](https://github.com/boseji/CH341-Store)
- [AsProgrammer Documentation](https://github.com/nofeletru/UsbAsp-flash-dump)
- [Flashrom Documentation](https://www.flashrom.org/)

---

## Legal Disclaimer

This guide is provided for educational and backup purposes only. Modifying odometer readings is illegal in most jurisdictions. The author assumes no responsibility for misuse of this information or any damage to equipment.
