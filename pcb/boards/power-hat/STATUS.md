# Power HAT PCB Status

## Current State: DRC CLEAN - Ready for Manufacturing

**Date:** 2026-02-04
**DRC Report:** DRC_20.rpt - 120 warnings, 0 errors

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
| DRC_18 | 126 | 6 | Edge clearance + track crossing after trace widening attempt |
| DRC_19 | 121 | 1 | Fixed edge clearance, 1 track crossing remaining |
| DRC_20 | 120 | 0 | Fixed track crossing - CLEAN |

## Remaining Warnings (Acceptable)

All 120 remaining violations are warnings:
- **Library footprint mismatches (20):** Local footprints differ from library - OK
- **Non-mirrored text on back layer (81):** Cosmetic only
- **Silk overlap (14):** Reference designators overlap - cosmetic
- **Silk over copper (5):** Silkscreen clipped by pads - normal

## Power Trace Analysis

**Power nets:** 0.6mm (24 mil) - 165 segments
**Signal nets:** 0.2mm (8 mil) - 227 segments

| Net | Current | Trace Width | 1oz Copper | 2oz Copper |
|-----|---------|-------------|------------|------------|
| GND | Return | 0.6mm | ~2A | ~4A |
| +5V | 3-5A | 0.6mm | ~2A | ~4A |
| 12V_FUSED | 5A | 0.6mm | ~2A | ~4A |
| U1_SW | 5A pulsed | 0.6mm | ~2A | ~4A |

**Recommendation:** Order with 2oz copper for full 5A headroom. 1oz is adequate for typical Pi loads (2-3A).

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

1. ~~Widen power traces~~ ✓ Already 0.6mm on power nets
2. ~~Run final DRC~~ ✓ DRC_20 clean
3. Generate Gerbers
4. Order prototype (recommend 2oz copper for full 5A capacity)
