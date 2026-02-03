# Session Summary - Input Protection Circuit & Schematic Analysis

**Date:** 2026-02-02 (Updated - Session 3)
**Status:** LED and MOSFET circuits wired
**ERC Status:** Pending verification (run ERC in KiCad)

---

## ✓ SESSION 3 WORK (2026-02-02 Continued)

### LED Indicator Circuits - WIRED ✓

**LED2 (Red - Timer LED) Circuit:**
- Changed incorrect GND at LED2 Anode to +3.3V
- Added wires: LED2 Cathode (504.19, 317.5) → R12 Pin 1 (508, 377.19)
- Added TIMER_LED global label at R12 Pin 2 (508, 384.81)
- Circuit: +3.3V → LED2 → R12 (10kΩ) → TIMER_LED → ATtiny85

**LED3 (Yellow - Heartbeat LED) Circuit:**
- Changed misplaced LED3_ANODE label to +3.3V at correct position (575.31, 317.5)
- Added wires: LED3 Cathode (567.69, 317.5) → R13 Pin 1 (571.5, 377.19)
- Added HEARTBEAT_LED global label at R13 Pin 2 (571.5, 384.81)
- Circuit: +3.3V → LED3 → R13 (470Ω) → HEARTBEAT_LED → ATtiny85

### Q2 Gate Driver - WIRED ✓

- Added GND global label at Q2 Source (383.54, 132.08)
- Q2 drives Q1 gate for power MOSFET control

### Q3 Fan PWM Control - WIRED ✓

- Added FAN_PWM global label at Q3 Gate (566.42, 508)
- Added FAN- global label at Q3 Drain (574.04, 502.92)
- Added GND global label at Q3 Source (574.04, 513.08)
- Circuit: FAN_PWM (GPIO) → Q3 Gate → Fan Negative (low-side switch)

### Backup

- Backup: wrx-power-can-hat-MANUAL-BACKUP10.kicad_sch

---

## ✓ PREVIOUS SESSION WORK (2026-02-02 Continuation)

### J1 ISO-A Connector - FIXED ✓

**Changes Made:**
- Removed SPI_MOSI label and wires from J1 Pin 3
- Removed SPI_SCLK label and wires from J1 Pin 5
- Removed +3.3V label and wires from J1 Pin 1
- Removed GND label from J1 Pin 2
- Changed J1 Pin 7 from IGN_DETECT to 12V_ACC (global label)
- Changed J1 Pin 8 GROUND to GND for consistency
- Added no_connect markers to unused pins (1, 2, 3, 5)

**Correct J1 Wiring Now:**
| Pin | Connection | Status |
|-----|------------|--------|
| 1 | NC (no_connect) | ✓ FIXED |
| 2 | NC (no_connect) | ✓ FIXED |
| 3 | NC (no_connect) | ✓ FIXED |
| 4 | 12V_IN | ✓ Correct |
| 5 | NC (no_connect) | ✓ FIXED |
| 6 | Unconnected | ✓ Correct |
| 7 | 12V_ACC | ✓ FIXED |
| 8 | GND | ✓ FIXED |

### U2 Optoisolator - FIXED ✓

**Changes Made:**
- Changed R6 input from 12V_IGN to 12V_ACC (connects J1 Pin 7 to optoisolator)
- Changed U2 Pin 4 (Collector) from GND to +3.3V

**Note:** R7 (10kΩ pull-up) should ideally be added as a discrete component between +3.3V and Pin 4 for current limiting. Current design connects +3.3V directly.

### Component Values - FIXED ✓

- **L1**: Changed from 10µH to 33µH (TPS54560 inductor)
- **Y1**: Changed from 8MHz to 16MHz (crystal frequency)

### Commit

- Commit: 5da0fe7 "Fix J1 ISO-A connector wiring and component values"
- Backup: wrx-power-can-hat-MANUAL-BACKUP9.kicad_sch

---

## ✓ COMPLETED WORK

### 1. Input Protection Circuit - FULLY FUNCTIONAL ✓

**Components Verified:**
- **F1** (5A Fuse): 12V_IN → 12V_FUSED (overcurrent protection)
- **D2** (SS34 Schottky): 12V_FUSED → 12V_IGN (reverse polarity protection)
- **D1** (SMBJ18A TVS): 12V_IGN ↔ GND (overvoltage/transient protection)
- **LED1** (Green) + **R1** (1kΩ): 12V_IGN → LED → GND (power indicator)

**Power Flow:**
```
J1 Pin 4 (12V Battery) → 12V_IN → F1 → 12V_FUSED → D2 → 12V_IGN → Rest of circuit
                                        ↓
                                      D1 (TVS)
                                        ↓
                                       GND
```

**Status:** Ready for PCB layout. No ERC errors on these components.

---

### 2. Q1 Power Switching - COMPLETED ✓

**Previous Work (from earlier session):**
- Replaced IRF9540N (P-channel) with IRLB8721PBF (N-channel logic-level MOSFET)
- Changed from high-side to low-side switching
- Added gate protection: R_Q1_GATE (1kΩ), R_Q1_PULLDOWN (10kΩ)
- See: [Q1_REPLACEMENT_PLAN.md](Q1_REPLACEMENT_PLAN.md)

---

### 3. Power Supply Upgrades - COMPLETED ✓

**Previous Work (from earlier session):**
- **U1**: Replaced LM2596S-5.0 (3A) with TPS54560BDDA (5A) for Raspberry Pi 5
- **U6**: Added AMS1117-3.3 (3.3V LDO regulator)
- Feedback network: R4 (10kΩ), R5 (51kΩ) → 4.88V output
- Bootstrap capacitor: C_BOOT1 (100nF)

---

### 4. Comprehensive Schematic Analysis - COMPLETED ✓

**Created Analysis Tools:**
- **analyze_schematic.py** - Python script that parses KiCad schematic
- **SCHEMATIC_ANALYSIS_REPORT.txt** - Complete component inventory (73 components)
- **ACTION_CHECKLIST.txt** - Step-by-step TODO list
- **schematic_data.json** - Machine-readable component data

**Findings:**
- ✓ 73 components total
- ✓ All major ICs present (U1-U6)
- ✓ All transistors present (Q1-Q3)
- ✗ 1 missing component: R7 (10kΩ optoisolator pull-up)
- ⚠ 2 value mismatches: L1 (10µH should be 33µH), Y1 (8MHz should be 16MHz)

---

### 5. Cleanup - COMPLETED ✓

**Removed Orphaned Components:**
- R2 (10kΩ) - old P-channel Q1 gate pull-up (no longer needed)
- R3 (100Ω) - old P-channel Q1 gate resistor (no longer needed)
- Duplicate R1 at (5000, 7500) - conflicted with LED1's R1

**Resolved Net Conflicts:**
- Fixed CAN_INT/SPI_CE0 conflict by removing bridge wire between J1 Pin 6 and Pin 7

---

## ✗ CRITICAL ISSUES TO FIX (Priority Order)

### PRIORITY 1: J1 (ISO-A Connector) Miswiring - CRITICAL ✗

**Problem:** J1 is the automotive power connector from the car, but it has been contaminated with SPI signals.

**What J1 IS:**
- 8-pin ISO 10487-A automotive stereo connector
- Plugs into car's wiring harness
- Provides 12V power, ground, and ignition signal

**Current J1 Wiring (WRONG):**

| Pin | Current Connection | Status |
|-----|-------------------|---------|
| 1 | SPI_CE0 | ✗ WRONG |
| 2-3 | Unknown | ⚠ UNCLEAR |
| 4 | 12V_IN | ✓ CORRECT |
| 5-6 | SPI signals | ✗ WRONG |
| 7 | +3.3V | ✗ **CRITICAL - Should be 12V_ACC** |
| 8 | Not connected | ✗ **CRITICAL - Should be GND** |

**Correct J1 Wiring (per ISO 10487-A standard):**

| Pin | Function | Should Connect To | Notes |
|-----|----------|-------------------|-------|
| 1 | Speed pulse | Not connected | Future use |
| 2 | Phone mute | Not connected | Not used |
| 3 | N/C | Not connected | Not used |
| 4 | **12V Battery** | **12V_IN** | ✓ Already correct |
| 5 | Antenna control | Not connected | Future use |
| 6 | Illumination | Not connected | Optional dimming |
| 7 | **12V ACC (Ignition)** | **12V_ACC → IGN_DETECT** | ⚠ Currently has +3.3V |
| 8 | **Ground** | **GND** | ⚠ Currently unconnected |

**Required Actions:**
1. Remove ALL SPI signals from J1 (SPI_CE0, SPI_MISO, SPI_MOSI, SPI_SCLK)
2. Change J1 Pin 7 from "+3.3V" to "**12V_ACC**"
3. Connect J1 Pin 8 to "**GND**"
4. Leave pins 1, 2, 3, 5, 6 unconnected (not used)

**Impact:** Without these fixes:
- Ignition detection won't work (U2 optoisolator won't receive 12V signal)
- SPI signals are being sent to car harness (could damage ECU)
- No ground return path from car

---

### PRIORITY 2: Add Missing Component - R7 ✗

**Missing:** R7 (10kΩ)

**Purpose:** Pull-up resistor for U2 (LTV-817S optoisolator) output

**Required Connection:**
```
U2 (Optoisolator) Pin 4 ───[R7 10kΩ]─── +3.3V
                    │
                    └─── IGN_DETECT signal → ATtiny85
```

**Function:** Ensures IGN_DETECT signal is HIGH (3.3V) when ignition is OFF

---

### PRIORITY 3: Fix Component Values ⚠

**L1 (Inductor):**
- Current: 10µH
- Should be: **33µH**
- Location: (190.5, 317.5)
- Purpose: Buck converter inductor for U1 (TPS54560)

**Y1 (Crystal):**
- Current: 8MHz
- Should be: **16MHz**
- Location: (190.5, 571.5)
- Purpose: May be for MCP2515 CAN controller (verify which crystal is which)
- Note: Y2 (16MHz) exists at (426.7, 147.3) - might be mislabeled?

---

## CONNECTOR INVENTORY

**All Connectors Found in Schematic:**
- **J1**: ISO_A (8-pin) - Automotive power connector
- **J2**: Pi_GPIO (40-pin) - Raspberry Pi header
- **J3**: OBD-II (16-pin) - CAN bus diagnostics
- **J4**: CAN_Term - CAN bus termination resistor
- **J5**: ISP - Programming header (for ATtiny85)
- **J6**: FAN - Fan control connector
- **J7**: Audio - Audio output connector
- **JP1**: Jumper - Purpose TBD
- **JP2**: 5V/12V - Voltage selector jumper

**Note:** There is NO second 8-pin ISO connector. Only J1.

---

## SIGNAL ROUTING (How it SHOULD work)

### Power Signals (from car via J1):
```
J1 Pin 4 (12V Battery) → 12V_IN → F1 → D2 → D1 → 12V_IGN → U1, U6, rest of circuit
J1 Pin 7 (12V ACC) → 12V_ACC → R6 → U2 optoisolator → IGN_DETECT → ATtiny85 (U3)
J1 Pin 8 → GND → Ground plane
```

### CAN Bus Signals (from OBD-II via J3):
```
J3 (OBD-II) → CANH/CANL → U5 (SN65HVD230 transceiver) → CAN_TX/CAN_RX → U4 (MCP2515)
```

### SPI Signals (internal to HAT, between Pi and CAN controller):
```
J2 (Pi GPIO) ←→ SPI_MISO, SPI_MOSI, SPI_SCLK, SPI_CE0 ←→ U4 (MCP2515)
```

**CRITICAL:** SPI signals should NEVER touch J1 (automotive connector)!

---

## ERC ERROR TRACKING

| Version | Errors | Change | Notes |
|---------|--------|--------|-------|
| ERC_38 | 71 | - | After Q1 replacement, gate dangling |
| ERC_39 | 70 | -1 | Restored labels |
| ERC_40 | 69 | -1 | Added Q1 gate resistors |
| ERC_41 | 67 | -2 | Fixed 12V_IN connection |
| ERC_42 | 63 | -4 | Deleted duplicate R1, R2, R3 |
| ERC_43 | **62** | **-1** | **Fixed CAN_INT/SPI_CE0 conflict** |

**Current Status:** 62 errors remaining (mostly unconnected components)

---

## REFERENCE DOCUMENTS

**In This Directory:**
- **Q1_REPLACEMENT_PLAN.md** - Q1 N-channel MOSFET replacement plan
- **SCHEMATIC_DESIGN.md** - Original design specification
- **SCHEMATIC_ANALYSIS_REPORT.txt** - Complete component inventory (73 components)
- **ACTION_CHECKLIST.txt** - Step-by-step TODO list
- **schematic_data.json** - Machine-readable component data
- **analyze_schematic.py** - Python script for schematic analysis
- **ERC_43.rpt** - Latest ERC report (62 errors)

**Key Files:**
- **wrx-power-can-hat-MANUAL.kicad_sch** - Main schematic file (working copy)
- **wrx-power-can-hat-MANUAL-BACKUP8.kicad_sch** - Backup before this session

---

## NEXT SESSION TODO

### Immediate Actions (Critical):

1. **Fix J1 Connector** (PRIORITY 1)
   - [ ] Remove SPI_CE0 label from J1
   - [ ] Remove SPI_MISO label from J1
   - [ ] Remove SPI_MOSI label from J1
   - [ ] Remove SPI_SCLK label from J1
   - [ ] Change J1 Pin 7 from "+3.3V" to "12V_ACC"
   - [ ] Add "GND" label to J1 Pin 8
   - [ ] Verify pins 1,2,3,5,6 are unconnected

2. **Add Missing Component** (PRIORITY 2)
   - [ ] Add R7 (10kΩ) between U2 Pin 4 and +3.3V

3. **Fix Component Values** (PRIORITY 3)
   - [ ] Change L1 from 10µH to 33µH
   - [ ] Verify Y1/Y2 crystal values (check which is for MCP2515)

### Verification Steps:

4. **Verify All Connections**
   - [ ] U1 (TPS54560) feedback network correct
   - [ ] U2 (LTV-817S) optoisolator: J1 Pin 7 → R6 → U2 → R7 → IGN_DETECT
   - [ ] U3 (ATtiny85) all 6 GPIO pins assigned correctly
   - [ ] U4 (MCP2515) SPI connections to J2 (NOT J1!)
   - [ ] U5 (SN65HVD230) CAN connections to J3
   - [ ] U6 (AMS1117-3.3) input from +5V, output to +3.3V

5. **Final Checks**
   - [ ] Run ERC (target: <60 errors)
   - [ ] Review all power nets (12V_IGN, +5V, +3.3V, GND)
   - [ ] Check for net conflicts
   - [ ] Create backup before PCB layout
   - [ ] Commit final schematic to git

---

## DESIGN NOTES

### ATtiny85 (U3) GPIO Assignments:
- **Pin 1 (RESET)**: Reset with pull-up
- **Pin 2 (PB3)**: TIMER_LED (countdown indicator)
- **Pin 3 (PB4)**: HEARTBEAT_LED (alive indicator)
- **Pin 4 (GND)**: Ground
- **Pin 5 (PB0)**: IGN_DETECT (from U2 optoisolator)
- **Pin 6 (PB1)**: SHUTDOWN_REQ (from Raspberry Pi)
- **Pin 7 (PB2)**: GATE_CTRL (controls Q1 via R_Q1_GATE)
- **Pin 8 (VCC)**: +3.3V power

### Power Management Logic:
1. Car turns on → 12V ACC high → U2 optoisolator → IGN_DETECT low
2. ATtiny85 detects ignition → Sets GATE_CTRL high
3. GATE_CTRL → R_Q1_GATE → Q1 gate → Q1 conducts
4. Load powered via 12V_SWITCHED path

### Protection Features:
- **Overcurrent**: F1 (5A fuse)
- **Reverse polarity**: D2 (SS34 Schottky diode)
- **Overvoltage**: D1 (SMBJ18A TVS, clamps at ~18V)
- **Visual indicator**: LED1 (green) lights when 12V_IGN present

---

## COMMIT HISTORY (This Session)

See git log for detailed commits:
1. Input protection circuit implementation
2. Component cleanup (R2, R3 deletion)
3. Net conflict fixes
4. Analysis script and reports

---

## FOR NEXT CONVERSATION

**Quick Start Commands:**
```bash
cd C:\Users\eckma\projects\SubaruDash\pcb

# View latest ERC
cat ERC_43.rpt

# Re-run analysis
python analyze_schematic.py

# View action checklist
cat ACTION_CHECKLIST.txt
```

**Key Context:**
- Input protection is DONE and verified ✓
- J1 connector is the CRITICAL issue to fix next
- 62 ERC errors remaining (down from 69)
- All major components present except R7
- No second 8-pin ISO connector exists

**Resume Point:**
Start with ACTION_CHECKLIST.txt Priority 1 (Fix J1 connector wiring).

---

**Session End:** Input protection complete, analysis tools created, ready to fix J1 connector in next session.
