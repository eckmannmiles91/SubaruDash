# Power HAT Component Recommendations

**Date:** 2026-02-06
**Status:** Pending implementation

## Summary

Analysis against TPS54560 datasheet identified marginal input/output capacitance and undersized catch diode for full 5A operation.

## Required Changes

### 1. Additional Input Capacitors (Critical)

**Issue:** Only C9 (22uF) on input. TI recommends >=30uF for 5A operation.

| Ref | Value | Footprint | Layer | Position (mm) | Net |
|-----|-------|-----------|-------|---------------|-----|
| C12 | 10uF 25V | 0805 | B.Cu | (103.5, 62.5) | 12V_FUSED, GND |
| C13 | 10uF 25V | 0805 | B.Cu | (103.5, 66.0) | 12V_FUSED, GND |

**Placement:** Right of C9, below D1 on back layer

### 2. Additional Output Capacitors (Critical)

**Issue:** Only C2 (10uF) on output. Need >=50uF for good transient response.

| Ref | Value | Footprint | Layer | Position (mm) | Net |
|-----|-------|-----------|-------|---------------|-----|
| C14 | 22uF 10V | 1206 | B.Cu | (99.78, 98.0) | +5V, GND |
| C15 | 22uF 10V | 1206 | B.Cu | (99.78, 94.0) | +5V, GND |

**Placement:** Below R_RT1, between L1 output and U2

### 3. Upgrade Catch Diode (Recommended)

**Issue:** D2 = SS34 (3A rated). At 5A output, this is stressed.

| Ref | Current | Replace With | Footprint |
|-----|---------|--------------|-----------|
| D2 | SS34 | SS54 or STPS5L40 | SMA (same) |

**Action:** Change value in schematic only - same footprint

## Current Components (Verified OK)

| Component | Value | Purpose | Status |
|-----------|-------|---------|--------|
| C_BOOT1 | 100nF | Bootstrap cap | OK |
| R_RT1 | 100k | Sets 400kHz switching | OK |
| R1 | 10k 1% | Feedback bottom | OK |
| R3 | 51k 1% | Feedback top (5V out) | OK |
| R_COMP1 | 10k | Compensation resistor | OK |
| C_COMP1 | 2.2nF | Compensation cap | OK |
| C8 | 47pF | Compensation pole | OK |
| L1 | 33uH | Output inductor | OK |
| C3, C4 | 22pF | ATtiny85 crystal load | OK |
| C1 | 100nF | ATtiny85 decoupling | OK |

## Implementation Steps

1. Open `power-hat.kicad_sch` in KiCad
2. Add C12, C13, C14, C15 capacitor symbols
3. Wire C12, C13 to 12V_FUSED and GND
4. Wire C14, C15 to +5V and GND
5. Change D2 value from SS34 to SS54
6. Update PCB from schematic
7. Place new caps at positions listed above (all on B.Cu)
8. Route short traces to power nets
9. Run DRC
10. Regenerate gerbers

## References

- [TPS54560 Datasheet](https://www.ti.com/lit/ds/symlink/tps54560.pdf)
- [TPS54560EVM-515 User Guide](https://www.ti.com/tool/TPS54560EVM-515)
