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

### Power Input Connector (ISO 10487-A Standard)
| Ref | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------------|---------|-------|----------|-------|
| **J1** | Molex 171822-0008 | 8-pin ISO | ISO 10487-A Power | WM18753-ND | Universal car harness |

**J1 Pinout (ISO 10487-A):**
```
Pin 1: Speed/CAN    - Not connected (future use)
Pin 2: Phone mute   - Not connected
Pin 3: N/C          - Not connected
Pin 4: 12V Battery  → 12V_IN (to F1 fuse)
Pin 5: Antenna      - Not connected (future use)
Pin 6: Illumination - Not connected (optional dimming)
Pin 7: 12V ACC      → IGNITION_DETECT (to PC817 input)
Pin 8: Ground       → GND
```

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
ATtiny85-20PU DIP-8 Pinout:

                         ┌────────┐
    RESET ─────[R8]─────┤1 RST  8├──── VCC (3.3V via C6)
                         │        │
   TIMER_LED ───[R9]────┤2 PB3  7├──── POWER_CTRL (to Q2 gate driver)
                         │        │
 HEARTBEAT_LED ─────────┤3 PB4  6├──── SHUTDOWN_SIG (from Pi GPIO)
                         │        │
           GND ─────────┤4 GND  5├──── IGNITION_IN (from PC817 output)
                         └────────┘

Pin Assignments:
- Pin 1 (PB5/RESET): Reset with 10kΩ pull-up to VCC
- Pin 2 (PB3): Timer status LED (blinks during countdown)
- Pin 3 (PB4): Heartbeat LED (blinks every 2s)
- Pin 4: Ground
- Pin 5 (PB0): Ignition detect input (LOW = ON, HIGH = OFF)
- Pin 6 (PB1): Shutdown signal from Pi (HIGH = shutdown)
- Pin 7 (PB2): Power control output (HIGH = power ON)
- Pin 8 (VCC): 3.3V power (decoupled with C6)
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **U3** | ATtiny85 | ATTINY85-20PU | DIP-8 | 8-bit micro | ATTINY85-20PU-ND | Programmable timer (3x) |
| **U3 Socket** | DIP-8 | 4808-3000-CP | DIP-8 | IC socket | AE10012-ND | Easy reprogramming |
| **C6** | 100nF | C0805C104K5RACTU | 0805 | Bypass cap | 399-1170-1-ND | Power decoupling |
| **R8** | 10kΩ | RC0805FR-0710KL | 0805 | Reset pull-up | 311-10.0KCRCT-ND | Reset pin |
| **R9** | 470Ω | RC0805FR-07470RL | 0805 | LED resistor | 311-470CRCT-ND | Timer LED |
| **R14** | 470Ω | RC0805FR-07470RL | 0805 | LED resistor | 311-470CRCT-ND | Heartbeat LED |
| **LED2** | Red | LTST-C150CKT | 0805 | Red LED | 160-1405-1-ND | Timer active |
| **LED3** | Yellow | LTST-C150YKT | 0805 | Yellow LED | 160-1130-1-ND | Heartbeat (2s) |

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
POWER_CTRL ───[R10]───┬───[Q2 N-FET Gate]
(ATtiny85 PB2)        │
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
- POWER_CTRL HIGH (ATtiny85 PB2) → Q2 on → Q1 gate pulled to GND → Q1 on → 12V flows
- POWER_CTRL LOW (ATtiny85 PB2) → Q2 off → Q1 gate pulled high → Q1 off → 12V cut

**State Machine:**
- Ignition ON → POWER_CTRL = HIGH → Power flows to Pi
- Ignition OFF → Start 45s timer, POWER_CTRL = HIGH → Power still on
- Timer expires OR Pi signals shutdown → POWER_CTRL = LOW → Power cut

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
        TXD ───────────┤TXD      CANH├─── To J4 OBD-II Pin 6
        RXD ───────────┤RXD      CANL├─── To J4 OBD-II Pin 14
                       │              │
       3.3V ───[C8]────┤VDD       GND├─── GND
                       └──────────────┘
                       U5: SN65HVD230DR

   CANH ───┬─── J4 Pin 6 (OBD-II Female)
           │
           └─── J5 Pin 1 (Screw terminal - optional)
           │
        [JP1 120Ω]  ← Jumper-selectable termination resistor
           │
   CANL ───┬─── J4 Pin 14 (OBD-II Female)
           │
           └─── J5 Pin 2 (Screw terminal - optional)

           J4 Pin 4 (GND) ──→ Common GND (optional chassis ground)

User Options:
  - Option A: Plug OBD-II Y-splitter into J4 (most users)
  - Option B: Wire directly to J5 screw terminals (custom setups)
  - Both connected in parallel - use either or both
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

### CAN Connectors (Dual Option - Maximum Flexibility)

| Ref | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------------|---------|-------|----------|-------|
| **J4** | TE 1-1718644-1 | 16-pin OBD-II | J1962 Female | A115904-ND | Right-angle PCB mount |
| **J5** | ED555/2DS | 5mm pitch 2-pos | Screw terminal | ED2635-ND | Optional backup |

**J4 Pinout (OBD-II J1962):**
```
Pin 6:  CANH (CAN High)  → To SN65HVD230 CANH (also J5 Pin 1)
Pin 14: CANL (CAN Low)   → To SN65HVD230 CANL (also J5 Pin 2)
Pin 4:  Chassis Ground   → GND (optional)
Pin 16: +12V Battery     → Not connected (already have via ISO A)
All other pins: Not connected
```

**J5 Pinout (Screw Terminal - wired in parallel with J4):**
```
Pin 1: CANH (CAN High)  → Parallel with J4 Pin 6
Pin 2: CANL (CAN Low)   → Parallel with J4 Pin 14
```

**User Options:**
- **Option A (Most Users):** Plug OBD-II Y-splitter into J4
  - Car OBD-II port → Splitter → J4 (plug and play!)
- **Option B (Advanced/Custom):** Wire to J5 screw terminals
  - Direct wire from CAN source (OBD-II extension, Seicane harness, etc.)
- **Option C:** Use OBD-II extension cable plugged into J4
  - Relocate OBD-II port closer to head unit location
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
- Pin 3, 5: I2C (GPIO 2 SDA, GPIO 3 SCL) to PCM5142
- Pin 6, 9, 14, 20, 25, 30, 34, 39: GND
- Pin 11 (GPIO 17): Fan PWM output
- Pin 12 (GPIO 18): I2S_SCLK to PCM5142
- Pin 19, 21, 23, 24 (GPIO 10, 9, 11, 8): SPI to MCP2515
- Pin 22 (GPIO 25): INT from MCP2515
- Pin 35 (GPIO 19): I2S_FS to PCM5142
- Pin 37 (GPIO 26): Ignition detect input
- Pin 40 (GPIO 21): I2S_DOUT to PCM5142

---

## Circuit Section 11: 4-Channel I2S DAC (Audio Output)

### Schematic
```
Raspberry Pi I2S:
  GPIO 18 (I2S_SCLK)  ───→ PCM5142 BCK (Bit Clock)
  GPIO 19 (I2S_FS)    ───→ PCM5142 LRCK (Frame Sync)
  GPIO 21 (I2S_DOUT)  ───→ PCM5142 DIN (Data In)
  GPIO 2  (I2C_SDA)   ───→ PCM5142 SDA (Configuration)
  GPIO 3  (I2C_SCL)   ───→ PCM5142 SCL (Configuration)

                         ┌──────────────┐
    3.3V ───[C13]───────┤VDD           │
    3.3V ───[C14]───────┤DVDD          │
                         │              │
    I2S_SCLK ───────────┤BCK      OUTL1├───[C15 2.2µF]───[R16 1kΩ]─→ J7 Pin 1 (FL)
    I2S_FS   ───────────┤LRCK     OUTR1├───[C16 2.2µF]───[R17 1kΩ]─→ J7 Pin 2 (FR)
    I2S_DOUT ───────────┤DIN      OUTL2├───[C17 2.2µF]───[R18 1kΩ]─→ J7 Pin 3 (RL)
                         │         OUTR2├───[C18 2.2µF]───[R19 1kΩ]─→ J7 Pin 4 (RR)
    I2C_SDA  ───────────┤SDA           │
    I2C_SCL  ───────────┤SCL       AGND├─→ GND
                         │         DGND├─→ GND
                         └──────────────┘
                         U7: PCM5142RGZR

J7 (6-pin audio output to amp module):
  Pin 1: Front Left (FL)   ──→ To amp module
  Pin 2: Front Right (FR)  ──→ To amp module
  Pin 3: Rear Left (RL)    ──→ To amp module
  Pin 4: Rear Right (RR)   ──→ To amp module
  Pin 5: GND               ──→ To amp module
  Pin 6: GND               ──→ To amp module
```

### Components

| Ref | Value | Part Number | Package | Specs | Digi-Key | Notes |
|-----|-------|-------------|---------|-------|----------|-------|
| **U7** | PCM5142 | PCM5142RGZR | VQFN-48 | Quad I2S DAC | 296-38727-1-ND | 32-bit, 4-channel |
| **C13** | 1µF | C0805C105K5RACTU | 0805 | VDD decoupling | 399-1284-1-ND | Ceramic |
| **C14** | 1µF | C0805C105K5RACTU | 0805 | DVDD decoupling | 399-1284-1-ND | Ceramic |
| **C15** | 2.2µF | GRM21BR61E225KA12L | 0805 | DC blocking | 490-3897-1-ND | Front Left |
| **C16** | 2.2µF | GRM21BR61E225KA12L | 0805 | DC blocking | 490-3897-1-ND | Front Right |
| **C17** | 2.2µF | GRM21BR61E225KA12L | 0805 | DC blocking | 490-3897-1-ND | Rear Left |
| **C18** | 2.2µF | GRM21BR61E225KA12L | 0805 | DC blocking | 490-3897-1-ND | Rear Right |
| **R16** | 1kΩ | RC0805FR-071KL | 0805 | Series resistor | 311-1.00KCRCT-ND | FL output |
| **R17** | 1kΩ | RC0805FR-071KL | 0805 | Series resistor | 311-1.00KCRCT-ND | FR output |
| **R18** | 1kΩ | RC0805FR-071KL | 0805 | Series resistor | 311-1.00KCRCT-ND | RL output |
| **R19** | 1kΩ | RC0805FR-071KL | 0805 | Series resistor | 311-1.00KCRCT-ND | RR output |
| **J7** | Audio Out | JST B6B-XH-A | 6-pin JST-XH | To amp module | 455-2249-ND | Line level output |

**Output Signal:** Clean 2V RMS line-level stereo on 4 channels (FL, FR, RL, RR)

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
- 3x ATtiny85-20PU Microcontroller (DIP-8, order extras for firmware iteration)
- 1x DIP-8 IC socket (for easy reprogramming)
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

**Audio:**
- 1x PCM5142 Quad I2S DAC (4-channel output)

**Passives:**
- ~24x Resistors (0805)
- ~18x Capacitors (0805, radial)
- 4x LEDs (0805)

**Connectors:**
- 1x 40-pin stacking header (GPIO)
- 1x ISO 10487-A 8-pin (power input from car)
- 1x OBD-II J1962 16-pin female (CAN bus plug-and-play)
- 1x JST-XH 6-pin (audio output to amp module)
- 1x JST-XH 2-pin (fan)
- 1x ISP header 2x3 (ATtiny85 programming)
- 2x Jumpers (CAN termination, fan voltage select)

**Total Estimated Cost:** $40-48 per board (single quantity)

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
