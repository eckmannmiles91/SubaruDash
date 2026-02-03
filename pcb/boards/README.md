# SubaruDash Split Board Schematics

This directory contains the split schematics from the combined `wrx-power-can-hat-MANUAL.kicad_sch` into three separate stackable Raspberry Pi HAT boards.

## Board Structure

### 1. Power HAT (`power-hat/`)
**Status: In Progress - J2 Pi Header Connected**

Core power management and ignition control:
- **U1**: TPS54560 5V/5A Buck Converter (12V → 5V)
- **U3**: ATtiny85 Power Management MCU
- **J1**: 12V Input Screw Terminal
- **J2**: 40-pin Raspberry Pi GPIO Header
- **F1**: Input Fuse
- MOSFETs (Q1, Q2, Q3) for power switching
- Ignition detection optocoupler circuit

**Connected Signals via Pi Header:**
- +5V (pins 2, 4)
- +3.3V (pins 1, 17)
- GND (pins 6, 9, 14, 20, 25, 30, 34, 39)
- SHUTDOWN_REQ (pin 15/GPIO22) - ATtiny85 → Pi shutdown signal

### 2. CAN HAT (`can-hat/`)
**Status: Template Created - Needs Wiring**

CAN bus communication interface:
- **U5**: MCP2515 CAN Controller (SPI interface)
- **U6**: MCP2551 CAN Transceiver
- SPI connection to Raspberry Pi
- CAN bus termination and protection

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
| `create_dac_amp_schematic.py` | Generate DAC/Amp schematic from scratch |

## Current ERC Status

### Power HAT
After running fix scripts v2 and v3:
- ✅ J2 Pi header pins connected (was 40 errors)
- ✅ PWR_FLAG symbols added for +5V, +3.3V, GND
- ⚠️ Remaining: J1, F1, U1, U3 need manual wiring
- ⚠️ Various resistors/capacitors need reconnection

### CAN HAT
- Needs wiring of J2 Pi header
- Needs SPI and CAN signal connections

### DAC/Amp
- Components placed with labels
- Needs I2S, power, and speaker wiring

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

1. Open `power-hat.kicad_sch` in KiCad and run ERC
2. Manually wire remaining disconnected components
3. Repeat for CAN HAT and DAC/Amp
4. Create PCB layouts for each board
5. Design stackable header connections
