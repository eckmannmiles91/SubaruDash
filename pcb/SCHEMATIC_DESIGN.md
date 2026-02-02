# WRX Power & CAN HAT - Schematic Design Guide

Detailed schematic sections with component values, part numbers, and design notes for KiCad implementation.

---

## KiCad Project Setup

### 1. Create New Project
```
File → New Project
Name: wrx-power-can-hat
Location: C:\Users\eckma\projects\SubaruDash\pcb\
```

### 2. Project Structure
```
pcb/
├── wrx-power-can-hat.kicad_pro        # KiCad project file
├── wrx-power-can-hat.kicad_sch        # Schematic file
├── wrx-power-can-hat.kicad_pcb        # PCB layout file
├── library/                            # Custom symbols/footprints
├── gerbers/                            # Manufacturing files
└── bom/                                # Bill of materials
```

### 3. Symbol Libraries Needed
Add these symbol libraries in KiCad:
- **Device** - Resistors, capacitors, diodes, LEDs
- **Power** - Power symbols (GND, +5V, +12V, +3.3V)
- **Connector** - Headers, screw terminals
- **Interface_CAN_LIN** - MCP2515, SN65HVD230
- **Regulator_Switching** - LM2596
- **Timer** - NE555 or ATtiny85
- **Transistor_FET** - MOSFETs
- **Isolator** - Optoisolators

---

## Circuit Section 1: Power Input & Protection

### Schematic (ASCII Representation)
```
12V_IN ───[F1 5A]───┬───[D1 TVS]───┬───[D2 Schottky]───┬─── 12V_PROTECTED
                     │              │                    │
                     │              │                    │
                  [LED1]         [C1 100µF]          [Q1 P-FET]
                     │              │                    │ (Controlled)
                    [R1]           GND                   │
                     │                                   ↓
                    GND                              To Buck Converter
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **F1** | 5A | 0154005.DR | 1206 SMD | Automotive fuse | WK5505CT-ND | Resettable polyfuse |
| **D1** | SMBJ18A | SMBJ18A | DO-214AA | 18V TVS diode | SMBJ18ALFCT-ND | Overvoltage clamp |
| **D2** | SS34 | SS34 | DO-214AC | 40V 3A Schottky | SS34FDICT-ND | Reverse polarity |
| **Q1** | IRF9540 | IRF9540NPBF | TO-220 | -100V -23A P-FET | IRF9540NPBF-ND | High-side switch |
| **R1** | 1kΩ | RC0805FR-071KL | 0805 | 1/8W | 311-1.00KCRCT-ND | LED current limit |
| **R2** | 10kΩ | RC0805FR-0710KL | 0805 | 1/8W | 311-10.0KCRCT-ND | Gate pull-up |
| **R3** | 100Ω | RC0805FR-07100RL | 0805 | 1/8W | 311-100CRCT-ND | Gate resistor |
| **C1** | 100µF | EEE-FK1E101P | Radial | 25V electrolytic | P122094-ND | Input filter |
| **LED1** | Green | LTST-C150GKT | 0805 | Green LED | 160-1427-1-ND | Power indicator |

### Power Input Connector
| Ref | Part Number | Package | Specs | Digi-Key |
|-----|-------------|---------|-------|----------|
| **J1** | ED555/2DS | 5mm pitch | 2-position screw terminal | ED2635-ND |

### Net Labels
- `12V_IN` - Raw 12V from car
- `12V_PROTECTED` - Protected 12V after polyfuse and TVS
- `12V_SWITCHED` - 12V after P-FET (controlled by timer)
- `GND` - Common ground

---

## Circuit Section 2: Buck Converter (12V → 5V)

### Schematic
```
12V_SWITCHED ───┬───[L1 33µH]───┬───[D3 Schottky]───┬─── 5V_OUT
                │               │                    │
             [U1 LM2596]        │                 [C3 220µF]
                │            [C2 100µF]              │
                │               │                    │
               GND             GND                  GND

U1 Pinout:
  Pin 1: VIN  (12V_SWITCHED)
  Pin 2: OUT  (to L1)
  Pin 3: GND
  Pin 4: FB   (feedback - voltage divider)
  Pin 5: ON/OFF (tied to VIN)
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **U1** | LM2596S-5.0 | LM2596S-5.0/NOPB | TO-263-5 | 5V 3A buck | LM2596S-5.0/NOPBCT-ND | Fixed 5V output |
| **L1** | 33µH | SRR1260-330M | 12x12mm | 33µH 5A | SRR1260-330MCT-ND | High current inductor |
| **D3** | SS54 | SS54 | DO-214AC | 40V 5A Schottky | SS54-E3/61TGICT-ND | Freewheeling diode |
| **C2** | 100µF | EEE-FK1E101P | Radial | 25V electrolytic | P122094-ND | Input cap |
| **C3** | 220µF | EEE-FK1E221P | Radial | 25V electrolytic | P122106-ND | Output cap |
| **C4** | 100nF | C0805C104K5RACTU | 0805 | Ceramic bypass | 399-1170-1-ND | Bypass cap |

### Feedback Network (if using adjustable version)
For LM2596-ADJ (if you want adjustable voltage later):
- **R4** = 1kΩ (top of divider, FB to OUT)
- **R5** = 3.3kΩ (bottom of divider, FB to GND)
- Vout = 1.23V × (1 + R4/R5) = 5.0V

**For simplicity, use LM2596S-5.0 (fixed 5V output)** - no feedback network needed!

---

## Circuit Section 3: Ignition Detection (Optoisolator)

### Schematic
```
12V_IGN ───[R6 1kΩ]───[U2 LTV-817 Pin 1]
                          Pin 2 ───GND

                      [U2 Pin 4]───[R7 10kΩ]───3.3V
                          │
                      [U2 Pin 3]───GND
                          │
                          └──────── IGNITION_DETECT (GPIO 26)
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **U2** | LTV-817S | LTV-817S | SOP-4 | Optoisolator | 160-1367-5-ND | SMD version of PC817 |
| **R6** | 1kΩ | RC0805FR-071KL | 0805 | 1/8W | 311-1.00KCRCT-ND | LED current limit |
| **R7** | 10kΩ | RC0805FR-0710KL | 0805 | 1/8W | 311-10.0KCRCT-ND | Pull-up resistor |
| **C5** | 100nF | C0805C104K5RACTU | 0805 | Ceramic | 399-1170-1-ND | Noise filter |
| **D4** | 1N4148 | 1N4148W-7-F | SOD-123 | Small signal | 1N4148W-FDICT-ND | Reverse protection |

### Input Connector
| Ref | Part Number | Package | Digi-Key |
|-----|-------------|---------|----------|
| **J2** | ED555/2DS | 5mm pitch 2-pos | ED2635-ND |

### Operation
- Ignition ON (12V) → LED on → Transistor on → GPIO 26 = LOW
- Ignition OFF (0V) → LED off → Transistor off → GPIO 26 = HIGH (pulled up)

---

## Circuit Section 4: Timer Circuit (ATtiny85)

### Schematic
```
                        ┌─────────┐
    3.3V ───[C6]───────┤VCC   PB0├──── TIMER_OUTPUT (to Q1 gate driver)
                        │         │
 IGNITION_DETECT ───────┤PB1   PB1├──── Not used
                        │         │
  SHUTDOWN_SIG ─────────┤PB2   PB2├──── Not used
                        │         │
          12V_SENSE ────┤PB3   PB3├──── Not used (ADC input for voltage)
                        │         │
           LED_TIMER ───┤PB4   GND├──── GND
                        └─────────┘
                        ATtiny85-20SU
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **U3** | ATtiny85 | ATTINY85-20SU | SOIC-8 | 8-bit micro | ATTINY85-20SU-ND | Programmable timer |
| **C6** | 100nF | C0805C104K5RACTU | 0805 | Bypass cap | 399-1170-1-ND | Power decoupling |
| **R8** | 10kΩ | RC0805FR-0710KL | 0805 | Reset pull-up | 311-10.0KCRCT-ND | Reset pin |
| **R9** | 470Ω | RC0805FR-07470RL | 0805 | LED resistor | 311-470CRCT-ND | Timer LED |
| **LED2** | Red | LTST-C150CKT | 0805 | Red LED | 160-1405-1-ND | Timer active |

### Programming Header (ISP)
| Ref | Part Number | Package | Digi-Key |
|-----|-------------|---------|----------|
| **J3** | 3220-06-0100-00 | 2x3 0.1" header | 609-3234-ND |

**ISP Pinout:**
```
MISO  [ 1  2 ] VCC
SCK   [ 3  4 ] MOSI
RST   [ 5  6 ] GND
```

### ATtiny85 Firmware Logic (Pseudocode)
```c
// Main logic
void loop() {
  if (ignition_on) {
    timer_active = false;
    power_mosfet_on();  // Keep power enabled
  }
  else {  // Ignition OFF
    if (!timer_active) {
      start_45s_timer();
      timer_active = true;
    }

    if (shutdown_signal_received || timer_expired) {
      power_mosfet_off();  // Cut power
      timer_active = false;
    }
  }
}
```

---

## Circuit Section 5: P-FET Gate Driver (Power Control)

### Schematic
```
TIMER_OUTPUT ───[R10]───┬───[Q2 N-FET Gate]
                        │
                     [R11 10kΩ]
                        │
                       GND

Q2 Drain ────── Q1 Gate (P-FET from Section 1)
Q2 Source ───── GND

Q1 Source ───── 12V_PROTECTED
Q1 Drain ────── 12V_SWITCHED (to buck converter)
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **Q2** | 2N7002 | 2N7002 | SOT-23 | N-channel FET | 2N7002NCT-ND | Gate driver |
| **R10** | 470Ω | RC0805FR-07470RL | 0805 | Gate resistor | 311-470CRCT-ND | Limits gate current |
| **R11** | 10kΩ | RC0805FR-0710KL | 0805 | Pull-down | 311-10.0KCRCT-ND | Ensure FET off |

### Operation
- TIMER_OUTPUT HIGH → Q2 on → Q1 gate pulled to GND → Q1 on → 12V flows
- TIMER_OUTPUT LOW → Q2 off → Q1 gate pulled high → Q1 off → 12V cut

---

## Circuit Section 6: CAN Bus Interface

### Schematic
```
                       ┌──────────────┐
    3.3V ─────[C7]────┤VDD        TXD├─── To U5 Pin 1 (TXD)
                      │              │
  GPIO 10 (MOSI) ─────┤SI        RXD├─── To U5 Pin 4 (RXD)
  GPIO 9  (MISO) ─────┤SO           │
  GPIO 11 (SCK)  ─────┤SCK      TXCAN├─── Not used
  GPIO 8  (CS)   ─────┤CS       RXCAN├─── Not used
  GPIO 25 (INT)  ─────┤INT       VSS├─── GND
                      │              │
           [XTAL 8MHz]┤OSC1     OSC2├─── [XTAL]
                      └──────────────┘
                      U4: MCP2515-I/SO

                       ┌──────────────┐
        TXD ───────────┤TXD      CANH├─── To J4 (CANH screw terminal)
        RXD ───────────┤RXD      CANL├─── To J5 (CANL screw terminal)
                       │              │
       3.3V ───[C8]────┤VDD       GND├─── GND
                       └──────────────┘
                       U5: SN65HVD230DR

   CANH ───┬─── J4 (screw terminal)
           │
        [JP1 120Ω]  ← Jumper-selectable termination resistor
           │
   CANL ───┴─── J5 (screw terminal)
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **U4** | MCP2515 | MCP2515-I/SO | SOIC-18 | CAN controller | MCP2515-I/SO-ND | 3.3V compatible |
| **U5** | SN65HVD230 | SN65HVD230DR | SOIC-8 | 3.3V transceiver | 296-42876-1-ND | No level shifter! |
| **Y1** | 8MHz | ABM3-8.000MHZ-B2-T | 5x3.2mm | Crystal | 535-9122-1-ND | MCP2515 clock |
| **C7** | 100nF | C0805C104K5RACTU | 0805 | Bypass cap | 399-1170-1-ND | MCP2515 VDD |
| **C8** | 100nF | C0805C104K5RACTU | 0805 | Bypass cap | 399-1170-1-ND | SN65HVD230 VDD |
| **C9** | 22pF | C0805C220J5GACTU | 0805 | Load cap | 399-1118-1-ND | Crystal load |
| **C10** | 22pF | C0805C220J5GACTU | 0805 | Load cap | 399-1118-1-ND | Crystal load |
| **R12** | 10kΩ | RC0805FR-0710KL | 0805 | INT pull-up | 311-10.0KCRCT-ND | Optional |
| **R13** | 120Ω | RC0805FR-07120RL | 0805 | Termination | 311-120CRCT-ND | Via JP1 jumper |

### CAN Connectors
| Ref | Part Number | Package | Digi-Key |
|-----|-------------|---------|----------|
| **J4** | ED555/2DS | 5mm pitch 2-pos | ED2635-ND |
| **JP1** | Header 2-pin | 0.1" pitch | S1011EC-02-ND |

### Protection (CAN Lines)
| Ref | Value | Part Number | Package | Digi-Key |
|-----|-------|-------------|---------|----------|
| **D5, D6** | TPD2E001 | TPD2E001DRLR | SOT-553 | 296-18472-1-ND |

**ESD Protection:**
- D5: CANH to GND (bidirectional TVS)
- D6: CANL to GND (bidirectional TVS)

---

## Circuit Section 7: Fan Control

### Schematic
```
GPIO 17 (PWM) ───[R14]───┬───[Q3 Gate]
                         │
                      [R15 10kΩ]
                         │
                        GND

Q3 Drain ────── Fan Negative (J6 Pin 2)
Q3 Source ───── GND

Fan Positive (J6 Pin 1) ────[JP2]──── Select: 5V or 12V_SWITCHED
                                        ↑
                                     Jumper

[D7 Flyback] ──── Across fan motor (cathode to +, anode to -)
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **Q3** | 2N7002 | 2N7002 | SOT-23 | N-channel FET | 2N7002NCT-ND | PWM switch |
| **R14** | 470Ω | RC0805FR-07470RL | 0805 | Gate resistor | 311-470CRCT-ND | Limits current |
| **R15** | 10kΩ | RC0805FR-0710KL | 0805 | Pull-down | 311-10.0KCRCT-ND | Ensure off |
| **D7** | 1N4148 | 1N4148W-7-F | SOD-123 | Flyback diode | 1N4148W-FDICT-ND | Motor protection |

### Fan Connector
| Ref | Part Number | Package | Digi-Key |
|-----|-------------|---------|----------|
| **J6** | B2B-XH-A | JST-XH 2-pin | 455-2249-ND |
| **JP2** | Header 3-pin | 0.1" pitch | S1011EC-03-ND |

**JP2 Jumper Configuration:**
```
Pin 1: 5V_OUT
Pin 2: Fan Positive (center)
Pin 3: 12V_SWITCHED

Install jumper on pins 1-2 for 5V fan
Install jumper on pins 2-3 for 12V fan
```

---

## Circuit Section 8: Status LEDs

### Schematic
```
5V_OUT ────[R16]────[LED3 Green]────GND    (Power indicator)

IGNITION_DETECT ────[R17]────[LED4 Yellow]────GND   (Ignition ON)

CAN_RX ────[R18]────[LED5 Blue]────GND     (CAN activity)

TIMER_OUTPUT ────[R19]────[LED6 Red]────GND    (Timer/Shutdown active)
```

### Components

| Ref | Value | Part Number | Package | Digi-Key | Notes |
|-----|-------|-------------|---------|----------|-------|
| **LED3** | Green | LTST-C150GKT | 0805 | 160-1427-1-ND | Power ON |
| **LED4** | Yellow | LTST-C150YKT | 0805 | 160-1415-1-ND | Ignition ON |
| **LED5** | Blue | LTST-C150TBKT | 0805 | 160-1579-1-ND | CAN activity |
| **LED6** | Red | LTST-C150CKT | 0805 | 160-1405-1-ND | Timer active |
| **R16-R19** | 1kΩ | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | Current limit |

**LED Placement:** Position LEDs near board edge for visibility

---

## Circuit Section 9: 3.3V Regulator

While the Raspberry Pi provides 3.3V, add a backup regulator for reliability:

### Schematic
```
5V_OUT ───[C11]───[U6 AMS1117-3.3]───[C12]───3.3V_OUT
                        │
                       GND
```

### Components

| Ref | Value | Part Number | Package | Digi-Key | Notes |
|-----|-------|-------------|---------|----------|-------|
| **U6** | AMS1117-3.3 | AMS1117-3.3 | SOT-223 | 1034-1014-1-ND | LDO regulator |
| **C11** | 10µF | GRM21BR61C106KE15L | 0805 | 490-3886-1-ND | Input cap |
| **C12** | 22µF | GRM21BR61A226ME44L | 0805 | 490-10749-1-ND | Output cap |

**Note:** Pi provides 3.3V on pin 1, but this backup ensures clean 3.3V for CAN/ATtiny85.

---

## Circuit Section 10: Raspberry Pi GPIO Header

### Schematic
```
                    Raspberry Pi GPIO Header (40-pin)
                    ================================
    3.3V ────── Pin 1       Pin 2 ────── 5V (from buck converter)
             ── Pin 3       Pin 4 ────── 5V
             ── Pin 5       Pin 6 ────── GND
             ── Pin 7       Pin 8 ──
             ── Pin 9       Pin 10 ──
  FAN_PWM ── Pin 11 (GPIO 17)  Pin 12 ────── SHUTDOWN_SIG (GPIO 18)
             ── Pin 13      Pin 14 ────── GND
             ── Pin 15      Pin 16 ──
             ── Pin 17      Pin 18 ──
   MOSI   ── Pin 19 (GPIO 10)  Pin 20 ────── GND
   MISO   ── Pin 21 (GPIO 9)   Pin 22 ────── INT (GPIO 25)
   SCK    ── Pin 23 (GPIO 11)  Pin 24 ────── CS (GPIO 8)
             ── Pin 25      Pin 26 ──
             ── ...
   IGN_DET── Pin 37 (GPIO 26)  Pin 38 ──
             ── Pin 39      Pin 40 ──
```

### Component
| Ref | Part Number | Package | Digi-Key | Notes |
|-----|-------------|---------|----------|-------|
| **J7** | SSW-120-02-T-D | 2x20 female | SAM1206-20-ND | Tall stacking header |

**Critical Connections:**
- Pin 2, 4: 5V from buck converter
- Pin 6, 9, 14, 20, 25, 30, 34, 39: GND
- Pin 11 (GPIO 17): Fan PWM output
- Pin 12 (GPIO 18): Safe shutdown signal (input to HAT)
- Pin 19, 21, 23, 24 (GPIO 10, 9, 11, 8): SPI to MCP2515
- Pin 22 (GPIO 25): INT from MCP2515
- Pin 37 (GPIO 26): Ignition detect input

---

## Power Distribution (Power Flags)

### Global Power Nets
```
+12V_IN         ← Raw 12V input
+12V_PROTECTED  ← After protection circuit
+12V_SWITCHED   ← After P-FET (controlled)
+5V             ← Buck converter output
+3.3V           ← LDO output
GND             ← Common ground
```

**In KiCad:** Use power port symbols for all power nets.

---

## Complete Bill of Materials (BOM)

### Summary by Category

**Power:**
- 1x LM2596S-5.0 Buck converter
- 1x IRF9540 P-channel MOSFET
- 1x AMS1117-3.3 LDO regulator
- Inductors, diodes, capacitors

**Control:**
- 1x ATtiny85-20SU Microcontroller
- 2x 2N7002 N-channel MOSFETs

**CAN:**
- 1x MCP2515-I/SO CAN controller
- 1x SN65HVD230DR CAN transceiver
- 1x 8MHz crystal

**Protection:**
- 1x SMBJ18A TVS diode
- 2x SS34/SS54 Schottky diodes
- 2x TPD2E001 ESD protection (CAN)
- 1x 5A Polyfuse

**Isolation:**
- 1x LTV-817S Optoisolator

**Passives:**
- ~20x Resistors (0805)
- ~15x Capacitors (0805, radial)
- 4x LEDs (0805)

**Connectors:**
- 1x 40-pin stacking header
- 3x Screw terminals (2-position, 5mm)
- 1x JST-XH 2-pin (fan)
- 1x ISP header (2x3)
- 2x Jumpers (2-pin, 3-pin)

**Total Estimated Cost:** $25-35 per board (single quantity)

---

## Design Verification Checklist

Before finalizing schematic:

### Electrical Rules Check (ERC)
- [ ] All power pins connected
- [ ] No unconnected nets
- [ ] All components have values
- [ ] Net names are consistent

### Power Distribution
- [ ] All ICs have bypass capacitors (100nF ceramic)
- [ ] Buck converter has input/output bulk caps
- [ ] 3.3V regulator has proper caps
- [ ] Ground connections verified

### GPIO Assignments
- [ ] No conflicting Pi GPIO usage
- [ ] SPI pins correct (MOSI, MISO, SCK, CS)
- [ ] PWM pin correct for fan control
- [ ] Shutdown and ignition pins defined

### Protection
- [ ] TVS diode on 12V input
- [ ] Reverse polarity protection
- [ ] ESD protection on CAN lines
- [ ] Flyback diode on fan

### Mechanical
- [ ] 40-pin header positioned correctly
- [ ] Screw terminals on accessible edge
- [ ] LEDs visible on board edge
- [ ] Mounting holes at HAT locations

---

## Next Steps

1. **Create KiCad project** (File → New Project)
2. **Add symbol libraries** (Preferences → Manage Symbol Libraries)
3. **Draw schematics** section by section using this guide
4. **Assign footprints** to all components
5. **Run ERC** (Inspect → Electrical Rules Checker)
6. **Generate netlist** for PCB layout
7. **Move to PCB layout phase**

---

## ATtiny85 Firmware Notes

### Pin Assignments
```
PB0 (Pin 5):  TIMER_OUTPUT - to gate driver
PB1 (Pin 6):  IGNITION_DETECT - input from optoisolator
PB2 (Pin 7):  SHUTDOWN_SIG - input from Pi GPIO 18
PB3 (Pin 2):  12V_SENSE - ADC input (optional voltage monitoring)
PB4 (Pin 3):  LED_TIMER - timer status LED
```

### Arduino Programming
1. Install ATtinyCore in Arduino IDE
2. Programmer: USBasp or Arduino as ISP
3. Board: ATtiny25/45/85
4. Chip: ATtiny85
5. Clock: 1MHz (internal)
6. Upload firmware via ISP header (J3)

**I can write the complete Arduino firmware once schematic is done!**

---

This guide provides all component values and circuit details needed to create the KiCad schematic. Ready to start drawing in KiCad?
