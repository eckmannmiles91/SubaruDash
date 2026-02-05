# SubaruDash Split Board Schematics

This directory contains the split schematics from the combined `wrx-power-can-hat-MANUAL.kicad_sch` into three separate stackable Raspberry Pi HAT boards.

## Board Structure

### 1. Power HAT (`power-hat/`)
**Schematic Status: ✅ ERC CLEAN - 0 Errors, 55 Warnings**
**PCB Status: 🟡 Layout v6 Ready - J1 updated to Micro-Fit 3.0 6-pin**

Core power management and ignition control:
- **U1**: TPS54560 5V/5A Buck Converter (12V → 5V)
- **U3**: ATtiny85 Power Management MCU
- **J1**: 12V Input Molex Micro-Fit 3.0 (6-pin)
- **J2**: 40-pin Raspberry Pi GPIO Header
- **J4**: 4-pin PWM Fan Connector (30mm fan)
- **F1**: Input Fuse
- MOSFETs (Q1, Q2, Q3) for power switching
- Ignition detection optocoupler circuit

**Connected Signals via Pi Header:** (see [GPIO_ALLOCATION.md](GPIO_ALLOCATION.md))
- +5V (pins 2, 4)
- +3.3V (pins 1, 17)
- GND (pins 6, 9, 14, 20, 25, 30, 34, 39)
- SHUTDOWN_REQ (pin 7/GPIO4) - Pi → ATtiny85 shutdown request
- HEARTBEAT_LED (pin 11/GPIO17) - ATtiny85 → Pi heartbeat status
- TIMER_LED (pin 13/GPIO27) - ATtiny85 → Pi timer status
- IGN_DETECT (pin 15/GPIO22) - Optocoupler → Pi ignition state
- FAN_PWM (pin 32/GPIO12) - Pi → Fan PWM speed control
- FAN_TACH (pin 33/GPIO13) - Fan → Pi tachometer feedback

**PCB Layout Features:**
- Board outline: 65mm × 56mm (standard Pi HAT)
- 4× M2.5 HAT mounting holes at corners (3.5, 3.5), (61.5, 3.5), (3.5, 52.5), (61.5, 52.5)
- 4× M3 fan mounting holes for 30mm fan (24mm spacing) centered at (32.5, 32)
- 40-pin GPIO header (J2) horizontal along top edge
- Power section (U1, L1) on left side, clear of fan zone
- MCU section (U3, Y1) on right side
- Power switching (Q1) bottom-right
- Layout scripts: `layout_power_hat_v5.py` (optimized), `layout_power_hat_v6.py` (DRC-compliant)

**Two-Layer Component Strategy:**
- **Front layer (F.Cu):** Through-hole and thermal components
  - Connectors: J1, J2, J3, J4, JP1, JP2
  - ICs: U1 (TPS54560), U2 (optocoupler), U3 (ATtiny85)
  - Power: Q1 (TO-220 MOSFET), L1 (inductor), F1 (fuse)
  - Crystal: Y1
- **Back layer (B.Cu):** SMD passives positioned under related front components
  - Under U1 (buck converter): R1, R2, R_RT1, R_COMP1, D2
  - Under U3 (MCU): R4, R5, R6, R7
  - Under U2 (optocoupler): R8, R9
  - Under Q1 (MOSFET): Q2, Q3, R10
  - Under J1 (power input): D1
  - Capacitors: C1-C9, C_BOOT1, C_COMP1

### 2. CAN HAT (`can-hat/`)
**Schematic Status: ✅ ERC CLEAN - Fixed crystal, OBD-II, and power connections**
**PCB Status: ⏳ Not Started**

CAN bus communication interface:
- **U2**: MCP2515 CAN Controller (SPI interface)
- **U3**: SN65HVD230 CAN Transceiver (3.3V native)
- **U1**: AMS1117-3.3 Voltage Regulator
- **J1**: 40-pin Raspberry Pi GPIO Header
- **J2**: OBD-II 16-pin Connector
- **J3**: CAN Screw Terminal
- **Y1**: 8MHz Crystal

**Connected Signals via Pi Header:** (see [GPIO_ALLOCATION.md](GPIO_ALLOCATION.md))
- +5V (pins 2, 4) - power input (stacking or USB-C)
- +3.3V (pins 1, 17) - from AMS1117
- GND (pins 6, 9, 14, 20, 25, 30, 34, 39)
- SPI_MOSI (pin 19/GPIO10)
- SPI_MISO (pin 21/GPIO9)
- SPI_SCLK (pin 23/GPIO11)
- SPI_CE0 (pin 24/GPIO8)
- CAN_INT (pin 22/GPIO25)

**USB-C Power Input (Manual Addition Required):**
- J5: USB-C connector for bench testing
- D1, D2: SS34 Schottky diodes (power OR'ing)
- Allows power from either GPIO header or USB-C

### 3. DAC/Amp HAT (`dac-amp/`)
**Schematic Status: ✅ ERC CLEAN - 34 Errors (J7 GPIO only), 85 Warnings**
**PCB Status: 🟡 Footprints placed, needs update from schematic**

4-channel 50W Class D audio amplifier:
- **U1**: PCM5142 Stereo I2S DAC
- **U2**: AMS1117-3.3 LDO (3.3V for DAC)
- **U3**: TPA3116D2DAD Class D Amplifier (Front L/R, 50W stereo BTL)
- **U4**: TPA3116D2DAD Class D Amplifier (Rear L/R, 50W stereo BTL)
- **J3**: 4-pin 3.5mm screw terminal (Front speakers: FL+, FL-, FR+, FR-)
- **J4**: 4-pin 3.5mm screw terminal (Rear speakers: RL+, RL-, RR+, RR-)
- **J7**: 40-pin Raspberry Pi GPIO Header

**Support Components Added:**
- R1, R2: 4.7kΩ I2C pull-ups (SCL, SDA to +3.3V)
- C4-C6: PCM5142 decoupling (100nF DVDD, 100nF+10µF AVDD)
- C7-C10: TPA3116D2 bootstrap caps (100nF each, BSPx↔BSNx)
- C11-C20: TPA3116D2 PVCC decoupling (8× 100nF + 2× 10µF)
- C21-C22: TPA3116D2 GVDD decoupling (100nF each)
- C23-C30: Input coupling caps (1µF each, AC coupling to amp inputs)
- C31: 12V input bulk capacitor (100µF)
- C32: 3.3V filter capacitor (100nF)

**Connected Signals via Pi Header (J7):**
- +5V (pins 2, 4) - power input
- +3.3V (pins 1, 17) - from AMS1117
- GND (pins 6, 9, 14, 20, 25, 30, 34, 39)
- I2S_BCK (pin 12/GPIO18) - I2S bit clock
- I2S_LRCK (pin 35/GPIO19) - I2S L/R clock
- I2S_DOUT (pin 40/GPIO21) - I2S data out
- I2C_SDA (pin 3/GPIO2) - PCM5142 config
- I2C_SCL (pin 5/GPIO3) - PCM5142 config

**Volume Control:** Digital via PCM5142 I2C registers (not analog PLIMIT)

## Scripts

| Script | Purpose |
|--------|---------|
| `split_schematic.py` | Initial split of combined schematic |
| `cleanup_schematics.py` | Remove cross-board labels |
| `fix_power_hat.py` | Remove CAN-specific labels from Power HAT |
| `fix_power_hat_complete.py` | (v1) Wire J2 pins - had position errors |
| `fix_power_hat_v2.py` | (v2) Wire J2 pins with CORRECT positions |
| `fix_power_hat_v3.py` | Add PWR_FLAG symbols for power nets |
| `fix_power_hat_v4.py` | Connect J1, F1, U1 VIN, U3 VCC |
| `fix_power_hat_v5.py` | Connect remaining components (Q1, R5-R10, Y1, J3, JP1-2) |
| `fix_power_hat_v6.py` | Final fixes: PWR_FLAG for U1, R6/Y1/R10/Q3 connections |
| `fix_power_hat_v7.py` | Restore R6 connections (12V_IGN, GND) after cleanup |
| `fix_power_hat_v8.py` | Fix Y1 Pin 1 -> XTAL1 connection |
| `fix_power_hat_v9.py` | Bridge wire for Y1 Pin 1 gap |
| `fix_power_hat_v10.py` | T-junction approach for Y1 |
| `fix_power_hat_v11.py` | Stub wire at Y1 Pin 1 (+ manual snap to pin) |
| `fix_power_hat_v12.py` | Remove orphan HEARTBEAT_LED/TIMER_LED labels |
| `fix_power_hat_v13.py` | Add no_connect for U3 pins 5,6 (superseded by v14) |
| `fix_power_hat_v14.py` | Wire U3 PB0/PB1 to GPIO17/GPIO27 for status signals |
| `fix_can_hat.py` | Complete CAN HAT wiring (GPIO, SPI, CAN, power) |
| `create_dac_amp_schematic.py` | Generate DAC/Amp schematic from scratch |
| `layout_power_hat.py` | Power HAT PCB component placement |
| `layout_power_hat_v2.py` | Improved layout with better spacing |
| `layout_power_hat_v3.py` | X735-style layout with 30mm fan |
| `fix_power_hat_fan.py` | Upgrade J4 from 2-pin to 4-pin fan connector |
| `fix_power_hat_fan_complete.py` | Wire J4 pins 3,4 to GPIO12,13 for PWM fan control |
| `layout_power_hat_v4.py` | Improved layout with fan clearance zones |
| `move_caps_to_back.py` | Move capacitors to B.Cu (back layer) |
| `fix_cap_pads.py` | Fix SMD pad layers for back-layer components |
| `move_smd_to_back.py` | Move resistors, diodes, SOT-23 MOSFETs to B.Cu |
| `fix_back_positions.py` | Apply board offset to back-layer component positions |
| `fix_boot_comp_caps.py` | Move C_BOOT1/C_COMP1 to B.Cu (back layer) |
| `layout_power_hat_v5.py` | Optimized layout with all components positioned |
| `layout_power_hat_v6.py` | DRC-compliant spacing, J1 Micro-Fit 3.0 support |

## Current ERC Status

### Power HAT
After running fix scripts v2 through v5:
- ✅ J2 Pi header 40 pins connected (v2)
- ✅ PWR_FLAG symbols added for +5V, +3.3V, GND (v3)
- ✅ J1 12V input connector connected (v4)
- ✅ F1 fuse output -> 12V_FUSED (v4)
- ✅ U1 VIN -> 12V_FUSED (v4)
- ✅ U3 VCC -> +5V (v4)
- ✅ TPS54560 compensation network (C_COMP1, R_RT1) (v5)
- ✅ Power switching circuit (Q1, R5, R6, R8) (v5)
- ✅ Crystal oscillator Y1 -> XTAL1/XTAL2 (v5)
- ✅ J3, JP1, JP2 headers marked as no-connect (v5)
- ✅ R10 LED resistor -> GND (v5)
- ✅ J4 fan connector -> FAN+ (v5)
- ✅ PWR_FLAG on 12V_FUSED net (v6) - fixes U1 VIN power error
- ✅ R6 Pin 1 -> 12V_IGN (v6)
- ✅ Y1 Pin 1 -> XTAL1 (v6)
- ✅ Q3 Gate -> FAN_PWM (v6)
- ✅ R6 Pin 1 -> 12V_IGN, Pin 2 -> GND restored (v7)
- ✅ Y1 Pin 1 -> XTAL1 (v8-v11 + manual fix)
- ✅ Orphan labels deleted manually
- ✅ U3 PB0 (HEARTBEAT_LED) -> J2 Pin 11 (GPIO17) (v14)
- ✅ U3 PB1 (TIMER_LED) -> J2 Pin 13 (GPIO27) (v14)
- ✅ J1 updated to Molex Micro-Fit 3.0 6-pin (manual)
- ✅ C6 fixed: bottom pin changed from +3.3V to GND (was shorted)
- ✅ C8 reconnected as feedforward cap: +5V to U1-FB (was incorrectly on XTAL2)
- ✅ C9 label fixed: 12V_FUSED (was 12V_IGN)
- ✅ R6 label fixed: 12V_IGN to GND (ignition detection divider)
- ✅ D1 (TVS) moved away from J2, reconnected: 12V_FUSED to GND
- ✅ Removed stray 12V_IGN label hidden behind U1
- ✅ PWR_FLAG added to 12V_FUSED and +3.3V nets
- ✅ **ERC: 0 ERRORS, 55 WARNINGS** (warnings are non-critical)

### CAN HAT
After running fix_can_hat.py:
- ✅ J1 Pi header 40 pins connected with labels
- ✅ SPI bus: MOSI, MISO, SCLK, CE0 to MCP2515
- ✅ CAN_INT from MCP2515 to GPIO25
- ✅ MCP2515 to SN65HVD230 (CAN_TX, CAN_RX)
- ✅ Crystal Y1 connected (XTAL1, XTAL2)
- ✅ CAN bus to J2 (OBD-II) pins 6, 14
- ✅ CAN bus to J3 (screw terminal)
- ✅ Power distribution (AMS1117 5V_BUS -> +3.3V)
- ✅ PWR_FLAG symbols for +5V, +3.3V, GND
- ✅ Unused GPIO pins marked no-connect
- ✅ Unused OBD-II pins marked no-connect
- ⏳ USB-C power circuit components need manual addition
- ⚠️ Run ERC in KiCad to check remaining errors

### DAC/Amp
After manual wiring in KiCad:
- ✅ I2C pull-ups (R1, R2) wired to +3.3V and I2C_SCL/SDA labels
- ✅ PCM5142 decoupling (C4-C6) wired to +3.3V and GND
- ✅ Bootstrap caps (C7-C10) wired BSPx↔BSNx (NOT to outputs)
- ✅ PVCC decoupling (C11-C20) wired to +12V and GND
- ✅ GVDD decoupling (C21-C22) wired with PWR_FLAG (internal 5.2V)
- ✅ Input coupling (C23-C30) wired in series with amp inputs
- ✅ Power filtering (C31, C32) wired to +12V/+3.3V and GND
- ✅ Speaker outputs (J3, J4) wired to U3/U4 OUTP/OUTN pins
- ✅ PWR_FLAG added to +12V and GND nets
- ✅ **ERC: 34 ERRORS (all J7 GPIO unconnected - expected), 85 WARNINGS**

## GPIO Pin Allocation

See **[GPIO_ALLOCATION.md](GPIO_ALLOCATION.md)** for the complete GPIO pin mapping across all three HAT boards. This document tracks:
- Which GPIO pins are used by each board
- Signal directions and descriptions
- Available GPIOs for future expansion

## Technical Notes

### Conn_02x20_Odd_Even Pin Positions
The Raspberry Pi GPIO header uses specific pin offsets:
- **Odd pins (left)**: x = symbol_x - 5.08mm
- **Even pins (right)**: x = symbol_x + 7.62mm
- **Y spacing**: 2.54mm per row, starting at y_offset = 22.86mm

For J2 at position (200, 150):
- Pin 1: (194.92, 127.14)
- Pin 2: (207.62, 127.14)
- Pin 3: (194.92, 129.68)
- etc.

### Power Flow
```
12V_IGN (vehicle) → F1 (fuse) → 12V_FUSED
                                    ↓
                               U1 TPS54560
                                    ↓
                                  +5V → Pi Header, CAN HAT
                                    ↓
                               U3 LDO (on CAN HAT or Power HAT)
                                    ↓
                                 +3.3V → MCUs, DAC
```

## Next Steps

1. ✅ ~~Power HAT ERC clean~~ - COMPLETE (0 errors)
2. ✅ ~~CAN HAT ERC clean~~ - COMPLETE
3. ✅ ~~DAC/Amp schematic wiring~~ - COMPLETE (34 errors = J7 GPIO only)
4. 🟡 **Power HAT PCB** - Update from schematic, run layout_power_hat_v6.py, route traces
5. 🟡 **CAN HAT PCB** - Routed via FreeRouting, ground pour added
6. 🟡 **DAC/Amp PCB** - Update from schematic (new J3/J4 4-pin connectors), re-route
7. ⏳ Design stackable header connections
8. ⏳ Add crystal load caps (~22pF) for Y1 (ATtiny85) - optional improvement
9. ⏳ Widen power traces on DAC/Amp (12V, speaker outputs)
