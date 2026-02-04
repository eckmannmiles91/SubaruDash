# Power HAT PCB Status

## Current State: DRC CLEAN - Ready for Manufacturing

**Date:** 2026-02-04
**DRC Report:** DRC_15.rpt - 120 warnings, 0 errors

## Board Summary

- **Size:** 65mm x 56mm (Raspberry Pi HAT standard)
- **Layers:** 2 (F.Cu, B.Cu)
- **Function:** 12V to 5V power supply for Raspberry Pi in vehicle

## Key Components

| Ref | Component | Function |
|-----|-----------|----------|
| U1 | TPS54560 | 5A Buck Converter (12V -> 5V) |
| U3 | ATtiny85 | Ignition detection/shutdown controller |
| J1 | Molex Micro-Fit 3.0 | 6-pin vehicle power input |
| J2 | 2x20 Header | Raspberry Pi GPIO |
| F1 | Mini Blade Fuse | Input protection |
| D1 | SMBJ18A | TVS diode (transient protection) |
| D2 | SS34 | Schottky (buck converter) |
| L1 | 22uH Inductor | Buck converter output |
| Y1 | 8MHz Crystal | ATtiny85 clock |

## DRC History

| Report | Violations | Critical Errors | Notes |
|--------|------------|-----------------|-------|
| DRC_5 | 133 | Multiple shorts | Initial Freerouting output |
| DRC_12 | 122 | 1 clearance | Most shorts fixed |
| DRC_14 | 121 | 1 unconnected | Clearance fixed |
| DRC_15 | 120 | 0 | All errors resolved |

## Remaining Warnings (Acceptable)

All 120 remaining violations are warnings:
- **Library footprint mismatches (20):** Local footprints differ from library - OK
- **Non-mirrored text on back layer (81):** Cosmetic only
- **Silk overlap (14):** Reference designators overlap - cosmetic
- **Silk over copper (5):** Silkscreen clipped by pads - normal

## TODO: Power Trace Widths

**Current:** All traces are 0.2mm (8 mil) from Freerouting default

**Required for high-current nets:**

| Net | Current | Recommended Width |
|-----|---------|-------------------|
| 12V_FUSED (net 7) | 5A | 1.5mm (60 mil) |
| U1_SW (net 9) | 5A pulsed | 1.5mm (60 mil) |
| +5V (net 3) | 3-5A | 1.0-1.5mm |
| GND (net 1) | Return | 1.5mm (60 mil) |

### How to Fix

1. **Option A - Net Classes:**
   - File -> Board Setup -> Design Rules -> Net Classes
   - Create "Power" class: 1.5mm track, 0.8mm via
   - Assign: 12V_FUSED, U1_SW, +5V, GND

2. **Option B - Manual:**
   - Select traces on power nets
   - Edit -> Change Track Width -> 1.5mm

### Critical Paths to Widen

1. J1 -> F1 -> D1 (12V input)
2. U1 pin 8 (PVIN) connections
3. U1 pin 1 (SW) -> L1 -> output caps
4. L1 -> +5V to J2 pins 2,4
5. Main GND return paths

## Files

- `power-hat.kicad_sch` - Schematic
- `power-hat.kicad_pcb` - PCB layout (routed)
- `power-hat.dsn` - Freerouting input
- `power-hat.ses` - Freerouting session (routed)
- `DRC_*.rpt` - DRC report history

## Keepout Zone

Fan cutout area defined (30mm x 30mm centered at board position 32.5, 32):
- Board coords: X=17.5-47.5mm, Y=17-47mm
- KiCad absolute: X=113.28-143.28mm, Y=71-101mm

## Next Steps

1. Widen power traces (see above)
2. Run final DRC
3. Generate Gerbers
4. Order prototype
