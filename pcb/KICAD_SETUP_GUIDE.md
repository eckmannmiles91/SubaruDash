# KiCad Project Setup Guide - WRX Power & CAN HAT

Step-by-step instructions for creating the schematic and PCB layout in KiCad.

---

## Prerequisites

### Install KiCad 8.x (Latest Stable)

Download from: https://www.kicad.org/download/

**Recommended version:** KiCad 8.0 or later (has improved Pi HAT templates and better library management)

### Verify Installation

After installing, verify KiCad can launch:
1. Open KiCad
2. You should see the KiCad Project Manager window

---

## Part 1: Create New Project

### Step 1: Create Project

1. Open KiCad
2. Click **File → New Project**
3. Navigate to: `C:\Users\eckma\projects\SubaruDash\pcb\kicad\`
4. Name the project: `wrx-power-can-hat`
5. Click **Save**

This creates:
- `wrx-power-can-hat.kicad_pro` - Project file
- `wrx-power-can-hat.kicad_sch` - Schematic file (empty)
- `wrx-power-can-hat.kicad_pcb` - PCB file (empty)

### Step 2: Configure Symbol Libraries

KiCad needs access to component symbol libraries.

1. In KiCad Project Manager, click **Preferences → Manage Symbol Libraries**
2. Verify these libraries are in the **Global Libraries** tab:
   - ✓ Device (resistors, capacitors, LEDs)
   - ✓ power (power symbols: GND, +5V, +12V, +3.3V)
   - ✓ Connector (headers, screw terminals)
   - ✓ Interface_CAN_LIN (MCP2515, CAN transceivers)
   - ✓ Regulator_Switching (LM2596)
   - ✓ MCU_Microchip_ATtiny (ATtiny85)
   - ✓ Transistor_FET (MOSFETs)
   - ✓ Isolator (Optoisolators)

If any are missing, they should be in the default KiCad installation.

### Step 3: Configure Footprint Libraries

1. Click **Preferences → Manage Footprint Libraries**
2. Verify these are available in **Global Libraries**:
   - ✓ Resistor_SMD (0805 resistors)
   - ✓ Capacitor_SMD (0805 capacitors)
   - ✓ LED_SMD (0805 LEDs)
   - ✓ Package_SO (SOIC packages)
   - ✓ Package_TO_SOT_SMD (SOT-23 for MOSFETs)
   - ✓ Package_DIP (DIP-8 socket for ATtiny85)
   - ✓ Connector_PinHeader_2.54mm (GPIO headers)
   - ✓ TerminalBlock_Phoenix (screw terminals)

### Step 4: PCB Design Rules Setup

We'll use **JLCPCB** design rules (cheap, fast, good quality):

1. Open the schematic: Double-click `wrx-power-can-hat.kicad_sch`
2. Later when we get to PCB layout, we'll configure:
   - **Trace width:** 0.25mm (signal), 0.5mm (power), 1.0mm (12V)
   - **Clearance:** 0.2mm minimum
   - **Via size:** 0.8mm drill, 0.4mm hole
   - **Board size:** 85mm x 56mm (Pi HAT standard)

---

## Part 2: Create Schematic - Section by Section

We'll create the schematic in 10 sections, matching SCHEMATIC_DESIGN.md.

### Section 1: Power Input & Protection

Open the schematic editor and start adding components.

#### Add Components

1. Press **A** (Add Symbol) or click the "Add symbol" toolbar button
2. Search for and place these components:

**Power symbols:**
- Type `GND` → select "power:GND" → place 4-5 instances (we'll use many)
- Type `+12V` → select "power:+12V" → place 2 instances
- Type `+5V` → select "power:+5V" → place 1 instance

**Fuse:**
- Type `Fuse` → select "Device:Fuse" → place as **F1**
- Right-click → Properties → Value: "5A PTC"
- Footprint: "Fuse:Fuse_1206_3216Metric"

**Diodes:**
- Type `D_TVS` → select "Device:D_TVS" → place as **D1**
  - Value: "SMBJ18A"
  - Footprint: "Diode_SMD:D_SMB"
- Type `D_Schottky` → select "Device:D_Schottky" → place as **D2**
  - Value: "SS34"
  - Footprint: "Diode_SMD:D_SMA"

**P-FET:**
- Type `MOSFET` → select "Transistor_FET:IRF9540N" → place as **Q1**
  - Footprint: "Package_TO_SOT_THT:TO-220-3_Vertical"

**Resistors:**
- Type `R` → select "Device:R" → place 3 instances
  - **R1:** 1kΩ (LED current limit)
  - **R2:** 10kΩ (gate pull-up)
  - **R3:** 100Ω (gate resistor)
  - Footprint: "Resistor_SMD:R_0805_2012Metric"

**Capacitor:**
- Type `CP` → select "Device:CP" → place as **C1**
  - Value: "100µF 25V"
  - Footprint: "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm"

**LED:**
- Type `LED` → select "Device:LED" → place as **LED1**
  - Value: "Green"
  - Footprint: "LED_SMD:LED_0805_2012Metric"

**Screw Terminal:**
- Type `Screw_Terminal` → select "Connector:Screw_Terminal_01x02" → place as **J1**
  - Value: "12V_IN"
  - Footprint: "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal"

#### Wire Components

1. Press **W** (begin wire) to connect components
2. Follow the schematic from SCHEMATIC_DESIGN.md Section 1
3. Add **net labels** (press **L**):
   - `12V_IN` - Input from screw terminal
   - `12V_PROTECTED` - After polyfuse and TVS
   - `12V_SWITCHED` - After P-FET (Q1)

**Tip:** Use hierarchical labels for signals that go between schematic pages (we'll create multiple pages for organization).

---

### Section 2: Buck Converter (12V → 5V)

#### Add Components

**Buck Regulator IC:**
- Type `LM2596` → select "Regulator_Switching:LM2596S-5.0" → place as **U1**
  - Footprint: "Package_TO_SOT_SMD:TO-263-5_TabPin3"

**Inductor:**
- Type `L` → select "Device:L" → place as **L1**
  - Value: "33µH"
  - Footprint: "Inductor_SMD:L_12x12mm_H8mm" (large power inductor)

**Diodes:**
- Type `D_Schottky` → place as **D3**
  - Value: "SS54"
  - Footprint: "Diode_SMD:D_SMA"

**Capacitors:**
- Type `CP` → place as **C2**
  - Value: "100µF 25V"
  - Footprint: "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm"
- Type `CP` → place as **C3**
  - Value: "220µF 16V"
  - Footprint: "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm"

**Resistors (feedback divider):**
- Type `R` → place **R4** and **R5**
  - R4: 1.5kΩ
  - R5: 1kΩ
  - Footprint: "Resistor_SMD:R_0805_2012Metric"

#### Wire and Label

Follow schematic Section 2, add net labels:
- `12V_SWITCHED` (input from Q1)
- `5V_OUT` (output to Pi)

---

### Section 3: Ignition Detection (Optoisolator)

#### Add Components

**Optoisolator:**
- Type `LTV-817` → select "Isolator:LTV-817S" → place as **U2**
  - Footprint: "Package_SO:SOP-4_4.4x2.6mm_P1.27mm"

**Resistors:**
- Type `R` → place as **R6** and **R7**
  - R6: 1kΩ (input current limit)
  - R7: 10kΩ (output pull-up)
  - Footprint: "Resistor_SMD:R_0805_2012Metric"

**Capacitor:**
- Type `C` → place as **C4**
  - Value: "100nF"
  - Footprint: "Capacitor_SMD:C_0805_2012Metric"

#### Wire and Label

Add net labels:
- `12V_IGN` (ignition input from car)
- `IGNITION_DETECT` (output to ATtiny85)
- Connect to GPIO 26 (we'll add Pi header later)

---

### Section 4: Timer Circuit (ATtiny85)

#### Add Components

**Microcontroller:**
- Type `ATtiny85` → select "MCU_Microchip_ATtiny:ATtiny85-20PU" → place as **U3**
  - Footprint: "Package_DIP:DIP-8_W7.62mm_Socket" (note: socket!)

**Socket (add to BOM manually):**
- We'll place a socket footprint for the ATtiny85

**Capacitor:**
- Type `C` → place as **C6**
  - Value: "100nF"
  - Footprint: "Capacitor_SMD:C_0805_2012Metric"

**Resistors:**
- R8: 10kΩ (reset pull-up)
- R9: 470Ω (timer LED)
- R14: 470Ω (heartbeat LED)

**LEDs:**
- LED2: Red (timer status)
- LED3: Yellow (heartbeat)
- Footprint: "LED_SMD:LED_0805_2012Metric"

**Programming Header (ISP):**
- Type `Conn_02x03` → select "Connector_Generic:Conn_02x03_Odd_Even" → place as **J3**
  - Value: "ISP"
  - Footprint: "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical"

#### Wire ATtiny85 Pins

Following the corrected pinout from SCHEMATIC_DESIGN.md:
- Pin 1 (RESET): Connect R8 (10kΩ) to VCC, also to J3 pin 5 (ISP RESET)
- Pin 2 (PB3): Timer LED (LED2) via R9
- Pin 3 (PB4): Heartbeat LED (LED3) via R14
- Pin 4 (GND): Ground
- Pin 5 (PB0): IGNITION_DETECT (from PC817)
- Pin 6 (PB1): SHUTDOWN_SIG (from Pi GPIO - TBD)
- Pin 7 (PB2): POWER_CTRL (to Q2 gate driver)
- Pin 8 (VCC): 3.3V via C6

**ISP Header Connections:**
```
MISO [ 1  2 ] VCC    → Pin 6 (PB1) and Pin 8
SCK  [ 3  4 ] MOSI   → Pin 7 (PB2) and Pin 5 (PB0)
RST  [ 5  6 ] GND    → Pin 1 (RESET) and Pin 4
```

---

### Section 5: P-FET Gate Driver

#### Add Components

**N-FET:**
- Type `2N7002` → select "Transistor_FET:2N7002" → place as **Q2**
  - Footprint: "Package_TO_SOT_SMD:SOT-23"

**Resistors:**
- R10: 470Ω (gate resistor)
- R11: 10kΩ (pull-down)

#### Wire

- POWER_CTRL (from ATtiny85 PB2) → R10 → Q2 gate
- Q2 drain → Q1 gate (P-FET from Section 1)
- Q2 source → GND
- R11 from Q2 gate to GND

---

### Section 6: CAN Bus Interface

#### Add Components

**CAN Controller:**
- Type `MCP2515` → select "Interface_CAN_LIN:MCP2515-I_SO" → place as **U4**
  - Footprint: "Package_SO:SOIC-18W_7.5x11.6mm_P1.27mm"

**CAN Transceiver:**
- Type `SN65HVD230` → select "Interface_CAN_LIN:SN65HVD230" → place as **U5**
  - Footprint: "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"

**Crystal:**
- Type `Crystal` → select "Device:Crystal" → place as **Y1**
  - Value: "8MHz"
  - Footprint: "Crystal:Crystal_SMD_5032-2Pin_5.0x3.2mm"

**Capacitors:**
- C7, C8: 100nF (bypass)
- C9, C10: 22pF (crystal load caps)

**Resistors:**
- R12: 10kΩ (INT pull-up, optional)
- R13: 120Ω (termination resistor)

**Screw Terminals:**
- Type `Screw_Terminal_01x02` → place 2 instances as **J4** and **J5**
  - J4: CANH
  - J5: CANL
  - Or use a single 3-position terminal (CANH, CANL, GND)

**Jumper for Termination:**
- Type `Jumper_NO` → place as **JP1**
  - Connects R13 (120Ω) between CANH and CANL when closed

#### Wire MCP2515

- VDD → 3.3V
- VSS → GND
- SI → Pi GPIO 10 (MOSI)
- SO → Pi GPIO 9 (MISO)
- SCK → Pi GPIO 11
- CS → Pi GPIO 8
- INT → Pi GPIO 25
- OSC1, OSC2 → Crystal Y1 with C9, C10 to ground
- TXD → U5 pin 1
- RXD → U5 pin 4

#### Wire SN65HVD230

- VDD → 3.3V (via C8)
- GND → GND
- TXD → U4 TXD
- RXD → U4 RXD
- CANH → J4 (screw terminal) and one side of JP1
- CANL → J5 (screw terminal) and other side of JP1

---

### Section 7: Fan Control

#### Add Components

**N-FET:**
- Type `2N7002` → place as **Q3**
  - Footprint: "Package_TO_SOT_SMD:SOT-23"

**Diode (flyback):**
- Type `D` → place as **D7**
  - Value: "1N4148"
  - Footprint: "Diode_SMD:D_SOD-323"

**Resistor:**
- R15: 1kΩ (gate resistor)

**Voltage Select Jumper:**
- Type `Jumper` → place as **JP2**
  - 3-position: 5V, 12V select

**Fan Connector:**
- Type `Conn_01x02` → place as **J6**
  - Value: "FAN"
  - Footprint: "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical"

#### Wire

- Pi GPIO 17 (PWM) → R15 → Q3 gate
- Q3 drain → Fan connector pin 1 (via JP2 for voltage select)
- Q3 source → GND
- D7 across fan connector (flyback protection)

---

### Section 8: Status LEDs

Add power indicator LEDs:

- **LED4:** Power LED (green) - on 5V rail with 1kΩ resistor (R16)
- **LED5:** CAN activity LED (blue) - connected to MCP2515 CLKOUT or custom signal
- **LED1:** Already placed in Section 1 (12V input indicator)

All LEDs: 0805 footprint with 470Ω or 1kΩ current-limiting resistors.

---

### Section 9: 3.3V Regulator (Backup)

#### Add Components

**LDO Regulator:**
- Type `AMS1117` → select "Regulator_Linear:AMS1117-3.3" → place as **U6**
  - Footprint: "Package_TO_SOT_SMD:SOT-223-3_TabPin2"

**Capacitors:**
- C11: 10µF (input)
- C12: 10µF (output)
- Footprint: "Capacitor_SMD:C_0805_2012Metric"

#### Wire

- Input: 5V_OUT
- Output: 3.3V (backup, Pi also provides 3.3V on pin 1)
- GND: Common ground

This ensures ATtiny85, MCP2515, and SN65HVD230 have clean 3.3V even if Pi 3.3V is noisy.

---

### Section 10: Raspberry Pi 40-Pin GPIO Header

#### Add Component

**Stacking Header:**
- Type `Raspberry_Pi` → search for "Conn_02x20_Odd_Even" → place as **J2**
  - Value: "Pi_GPIO"
  - Footprint: "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" (for stacking header)

**Alternative:** Search KiCad library for "Raspberry_Pi_2_3" connector symbol (has all pins pre-labeled).

#### Connect Pi GPIO Signals

Map these signals to the Pi header:

| Pi Pin | GPIO | Signal | Connects To |
|--------|------|--------|-------------|
| 1 | 3.3V | 3.3V_PI | (optional use) |
| 2 | 5V | 5V | From buck converter output |
| 4 | 5V | 5V | (parallel) |
| 6 | GND | GND | Common ground |
| 8 | GPIO 14 | UART TX | (reserved, not used) |
| 10 | GPIO 15 | UART RX | (reserved, not used) |
| 12 | GPIO 18 | X735_SHUTDOWN | (if using X735-compatible shutdown) |
| 19 | GPIO 10 | SPI_MOSI | To MCP2515 SI |
| 21 | GPIO 9 | SPI_MISO | To MCP2515 SO |
| 22 | GPIO 25 | CAN_INT | To MCP2515 INT |
| 23 | GPIO 11 | SPI_SCLK | To MCP2515 SCK |
| 24 | GPIO 8 | SPI_CE0 | To MCP2515 CS |
| 37 | GPIO 26 | IGN_DETECT | To PC817 output |

**Note:** Some pins reserved for future use (I2C, UART, etc.).

---

## Part 3: Schematic Organization Best Practices

### Use Hierarchical Sheets (Optional)

For complex designs, split schematic into multiple pages:

1. **Page 1:** Power (Sections 1-2)
2. **Page 2:** Control (Sections 3-5)
3. **Page 3:** CAN Interface (Section 6)
4. **Page 4:** Peripherals (Sections 7-8, GPIO header)

To create hierarchical sheets:
- Click **Place → Hierarchical Sheet**
- Draw rectangle, name it (e.g., "Power")
- Add hierarchical pins for connections between sheets

### Net Labels and Power Symbols

Use consistent naming:
- **Power rails:** `+12V`, `+5V`, `+3.3V`, `GND`
- **Signals:** `IGNITION_DETECT`, `POWER_CTRL`, `CAN_INT`, etc.

### Run Electrical Rules Check (ERC)

Before moving to PCB layout:

1. Click **Inspect → Electrical Rules Checker**
2. Fix all errors (missing connections, floating pins, etc.)
3. Warnings are usually okay (unused pins, etc.)

---

## Part 4: Assign Footprints

Each component needs a physical footprint (PCB layout).

### Method 1: Assign During Placement

When placing components, assign footprints immediately in the Properties dialog.

### Method 2: Assign in Footprint Editor

1. Click **Tools → Assign Footprints**
2. This opens a table showing Symbol → Footprint mapping
3. For each component, select the correct footprint from the list
4. Click **Apply**, **Save Schematic**, and **Continue**

**Common Footprints:**
- **0805 SMD:** Resistors, capacitors, LEDs
- **SOIC, SOT-23:** ICs, transistors
- **DIP-8:** ATtiny85 with socket
- **TO-220:** P-FET (Q1)
- **Screw terminals:** Phoenix 5mm pitch
- **Pi GPIO:** 2x20 female header (stacking)

---

## Part 5: Generate Netlist and Move to PCB Layout

### Generate Netlist

1. Click **Tools → Generate Netlist File**
2. Click **Generate Netlist**
3. Save as `wrx-power-can-hat.net`

### Open PCB Editor

1. In KiCad Project Manager, double-click `wrx-power-can-hat.kicad_pcb`
2. In PCB Editor, click **Tools → Update PCB from Schematic (F8)**
3. Click **Update PCB**
4. All components will appear in a cluster - you'll place them on the board

---

## Part 6: PCB Layout (Overview)

Detailed PCB layout guide will be in a separate document, but here's the overview:

### Board Outline

1. Select **Edge.Cuts** layer
2. Draw rectangle: **85mm x 56mm** (Raspberry Pi HAT standard)
3. Add **4 mounting holes** at Pi HAT locations:
   - (3.5, 3.5)
   - (61.5, 3.5)
   - (3.5, 52.5)
   - (61.5, 52.5)
   - Hole size: 2.75mm

### Component Placement Strategy

**Top layer (component side):**
- 40-pin GPIO header at edge (aligns with Pi)
- ATtiny85 in center (easy access to remove/reprogram)
- Buck converter and power components near 12V input
- CAN components near screw terminals
- LEDs visible from top

**Bottom layer:**
- Minimize components if possible (or use 2-layer design with SMD on both sides)

### Routing Tips

- **Power traces:** Wide (1mm for 12V, 0.5mm for 5V, 0.25mm for signals)
- **Ground plane:** Pour copper on both layers for GND
- **Keep CAN traces short** and differential if possible
- **Separate analog and digital grounds** (star ground at power input)

### Design Rule Check (DRC)

Before ordering:
1. Click **Inspect → Design Rules Checker**
2. Fix all errors
3. Verify: trace widths, clearances, hole sizes

---

## Part 7: Generate Gerber Files for Manufacturing

### Configure Output

1. Click **File → Plot**
2. Select layers to plot:
   - ✓ F.Cu (front copper)
   - ✓ B.Cu (back copper)
   - ✓ F.SilkS (front silkscreen)
   - ✓ B.SilkS (back silkscreen)
   - ✓ F.Mask (front soldermask)
   - ✓ B.Mask (back soldermask)
   - ✓ Edge.Cuts (board outline)
3. Output directory: `gerbers/`
4. Click **Plot**

### Generate Drill Files

1. Click **Generate Drill Files**
2. Use default settings (Excellon format)
3. Click **Generate Drill File**

### Zip for JLCPCB

1. Compress all Gerber files + drill file into `wrx-power-can-hat-gerbers.zip`
2. Upload to JLCPCB.com
3. Select options:
   - **PCB Qty:** 5 (minimum order)
   - **PCB Thickness:** 1.6mm
   - **PCB Color:** Green (or your preference)
   - **Surface Finish:** HASL (or ENIG for better quality)
   - **Remove Order Number:** Yes (costs $1.50 extra)

---

## Part 8: Bill of Materials (BOM) Export

### Generate BOM from KiCad

1. In Schematic Editor, click **Tools → Generate BOM**
2. Use the built-in BOM plugin or install "KiBoM" for better formatting
3. Export to CSV

### Create Digi-Key Cart

1. Open the generated CSV
2. Use Digi-Key's BOM upload tool: https://www.digikey.com/en/resources/online-conversion-calculators/bom-tool
3. Upload CSV and review parts
4. Add to cart

**Recommended:** Order 2-3x quantity for spares (resistors, capacitors, LEDs are cheap).

---

## Next Steps

1. **Complete schematic** following sections 1-10 above
2. **Run ERC** and fix errors
3. **Assign footprints** to all components
4. **Generate netlist** and update PCB
5. **Layout PCB** (detailed guide coming next)
6. **Run DRC** and verify design
7. **Generate Gerbers** and order from JLCPCB
8. **Order components** from Digi-Key
9. **Assemble and test!**

---

## Helpful Resources

- [KiCad Documentation](https://docs.kicad.org/)
- [KiCad Tutorial (Getting Started)](https://docs.kicad.org/8.0/en/getting_started_in_kicad/getting_started_in_kicad.html)
- [Raspberry Pi HAT Design Guide](https://github.com/raspberrypi/hats)
- [JLCPCB Capabilities](https://jlcpcb.com/capabilities/Capabilities)
- [Digi-Key Reference Designs](https://www.digikey.com/en/resources/design-tools/reference-designs)

---

## Troubleshooting

**"Can't find library"**
- Go to **Preferences → Manage Symbol/Footprint Libraries**
- Verify default libraries are enabled

**"Footprint not found"**
- Check that the footprint library exists
- Try alternative footprints (e.g., generic 0805 instead of manufacturer-specific)

**ERC errors:**
- **Power pin not driven:** Add power symbols (+5V, GND, etc.)
- **Pin not connected:** Connect all IC pins (even unused ones to VCC or GND)

**DRC errors:**
- **Clearance violations:** Increase spacing or make traces narrower
- **Unconnected nets:** Route all traces or add copper pours for ground

---

Ready to start? Open KiCad and begin with Section 1!
