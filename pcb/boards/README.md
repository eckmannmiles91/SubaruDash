# SubaruDash Split Board Schematics

This directory contains the split schematics from the combined `wrx-power-can-hat-MANUAL.kicad_sch` into three separate stackable Raspberry Pi HAT boards.

## Board Structure

### 1. Power HAT (`power-hat/`)
**Status: ✅ ERC CLEAN - 0 Errors, 73 Warnings**

Core power management and ignition control:
- **U1**: TPS54560 5V/5A Buck Converter (12V → 5V)
- **U3**: ATtiny85 Power Management MCU
- **J1**: 12V Input Screw Terminal
- **J2**: 40-pin Raspberry Pi GPIO Header
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

### 2. CAN HAT (`can-hat/`)
**Status: Major Wiring Complete (fix_can_hat.py) - Needs USB-C Components**

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

### 3. DAC/Amp Module (`dac-amp/`)
**Status: Schematic Generated - Needs Wiring**

4-channel 50W Class D audio amplifier:
- **U1**: PCM5142 Stereo I2S DAC
- **U2**: TPA3116D2 Class D Amplifier (Front L/R)
- **U3**: TPA3116D2 Class D Amplifier (Rear L/R)
- **U4**: AMS1117-3.3 LDO (3.3V for DAC)
- Speaker output connectors (4x 2-pin)

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
- ✅ **ERC: 0 ERRORS** (warnings are non-critical)

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
- Components placed with labels
- Needs I2S, power, and speaker wiring

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

1. ✅ ~~Power HAT ERC clean~~ - COMPLETE
2. Run ERC on CAN HAT, fix remaining errors
3. Wire DAC/Amp schematic
4. Create PCB layouts for each board
5. Design stackable header connections
