# DAC/Amp HAT v2.0 - Realistic Design Plan

## Overview

Improved revision focusing on changes that **actually fit** on the 65×56mm HAT form factor.

## v1.0 Baseline (Current)

| Spec | Value |
|------|-------|
| DAC | PCM5142 (I2S, 32-bit) |
| Amps | 2× TPA3116D2DAD (50W stereo BTL each) |
| Layers | 2 |
| Power traces | +12V @ 1.0mm, speakers @ 0.75mm |
| Thermal vias | 6-8 per amp |
| Output filtering | None |
| Ground topology | Single pour |
| Protection | None |

---

## v2.0 Realistic Targets

| Spec | Target | Fits? |
|------|--------|-------|
| Layers | **4-layer** (GND + 12V planes) | ✅ |
| Thermal vias | **16 per amp** | ✅ |
| Power traces | **1.5mm** (12V), **1.0mm** (speakers) | ✅ |
| Input protection | **TVS + polyfuse** | ✅ |
| Power filtering | **Ferrite beads on 3.3V** | ✅ |
| Bulk cap upgrade | **470µF** (vs 100µF) | ✅ |
| Mute control | **Software via PCM5142** | ✅ |
| Output LC filters | ❌ **Skipped** (no space) | - |
| Hardware mute relay | ❌ **Skipped** (no space) | - |

---

## What We're Adding (Fits on HAT)

### 1. 4-Layer PCB Stackup

| Layer | Purpose |
|-------|---------|
| F.Cu (Top) | Signal, components |
| In1.Cu | **GND plane** (solid) |
| In2.Cu | **+12V plane** (for amps) |
| B.Cu (Bottom) | Signal, components |

**Benefits:**
- Much easier routing (signals only on outer layers)
- Lower impedance power delivery
- Better thermal spreading via planes
- Improved EMI shielding
- Cost: ~$20 more for 5 boards

### 2. Input Protection Circuit

```
J2 +12V ──┬── F2 (polyfuse) ── D1 (TVS) ──┬── +12V_PROTECTED
          │                               │
          └───────────────────────────────┴── GND
```

| Ref | Value | Package | MPN |
|-----|-------|---------|-----|
| F2 | 5A polyfuse | 1812 | MF-MSMF500/24X-2 |
| D1 | TVS 15V | SMB | SMBJ15CA |

**Footprint:** ~25mm² total - **fits easily**

### 3. Power Rail Filtering

```
+3.3V_RAW (from AMS1117) ── FB1 ── +3.3V_CLEAN (to DAC analog)
```

| Ref | Value | Package | MPN |
|-----|-------|---------|-----|
| FB1 | 600Ω@100MHz | 0805 | BLM21PG601SN1D |
| FB2 | 600Ω@100MHz | 0805 | BLM21PG601SN1D |

**Footprint:** ~8mm² total - **fits easily**

### 4. Bulk Capacitor Upgrade

| Current | Upgraded |
|---------|----------|
| C31: 100µF 8mm dia | C31: 470µF 10mm dia |

**Note:** May need to verify 10mm cap fits in current location, or use 8mm 220µF

### 5. More Thermal Vias

```
Current: 6-8 vias per amp
Target:  16 vias per amp (4×4 grid)

  ┌───────────────┐
  │ o  o  o  o    │
  │ o  o  o  o    │  Thermal pad
  │ o  o  o  o    │  ~3.7 × 3.8mm
  │ o  o  o  o    │
  └───────────────┘
```

**Footprint:** Zero additional space (vias go under existing thermal pads)

### 6. Software Mute (No Hardware)

The PCM5142 supports **soft mute** via I2C register:
- Register 0x03, bit 4 = mute
- Gradual volume ramp prevents pop
- Controlled by Raspberry Pi on shutdown

**No additional components needed.**

---

## What We're NOT Adding (Won't Fit)

### ❌ Output LC Filters

| Component | Size | Problem |
|-----------|------|---------|
| 8× Inductors (10µH 5A) | 12mm dia or 12×12mm SMD | Would need ~800mm² |
| 8× Filter caps | Small (0805) | Caps fit, inductors don't |

**Alternative:** Add external filter board between amp and speakers if EMI is an issue.

### ❌ Hardware Mute Relays

| Component | Size | Problem |
|-----------|------|---------|
| 2× DPDT Relay (G5V-2) | 20×10mm each | Would need ~400mm² |
| Driver circuit | ~50mm² | Additional space |

**Alternative:** Software mute via PCM5142 is adequate for car use.

---

## Revised BOM Changes

### New Components (6 total)

| Ref | Description | Package | MPN | Qty |
|-----|-------------|---------|-----|-----|
| F2 | 5A polyfuse | 1812 | MF-MSMF500/24X-2 | 1 |
| D1 | TVS 15V bidir | SMB | SMBJ15CA | 1 |
| FB1 | Ferrite 600Ω | 0805 | BLM21PG601SN1D | 1 |
| FB2 | Ferrite 600Ω | 0805 | BLM21PG601SN1D | 1 |
| C31 | 470µF 25V | Radial 10mm | UVR1E471MED1TD | 1 |

**Total new footprint:** ~40mm² (easily fits)

### Removed/Changed

| Ref | Change |
|-----|--------|
| C31 | Upgraded from 100µF to 470µF |

---

## PCB Layout Changes

### 1. Layer Stackup (4-Layer)

Standard 1.6mm 4-layer:
```
F.Cu    ─── 0.035mm (1oz copper)
Prepreg ─── 0.2mm
In1.Cu  ─── 0.035mm (1oz, GND plane)
Core    ─── 1.0mm
In2.Cu  ─── 0.035mm (1oz, +12V plane)
Prepreg ─── 0.2mm
B.Cu    ─── 0.035mm (1oz copper)
```

### 2. Trace Width Targets

| Net | v1.0 | v2.0 |
|-----|------|------|
| +12V (to amps) | 1.0mm | **Via to +12V plane** |
| Speaker outputs | 0.75mm | **1.0mm** |
| Audio signals | 0.25mm | 0.25mm |
| I2S/I2C | 0.25mm | 0.25mm |

**Note:** With internal +12V plane, surface traces only need to connect to vias.

### 3. Ground Plane Strategy

With 4-layer board, GND plane (In1.Cu) is solid under entire board.
- Digital and analog share plane (acceptable for this design)
- Plane provides low-impedance return path
- No need for split plane complexity

### 4. Thermal Via Upgrade

| Amp | Current | Target |
|-----|---------|--------|
| U3 | 6 vias | 16 vias (4×4) |
| U4 | 8 vias | 16 vias (4×4) |

Via spec:
- Drill: 0.3mm
- Pad: 0.6mm
- Spacing: 0.9mm grid
- All on GND net

### 5. Protection Component Placement

Place near J2 (12V input):
```
J2 ──[F2]──[D1]── to +12V distribution
```

Place FB1/FB2 between AMS1117 output and DAC:
```
U2 out ──[FB1]── U1 AVDD
U2 out ──[FB2]── U1 DVDD
```

---

## Manufacturing Specs

| Spec | v1.0 | v2.0 |
|------|------|------|
| Layers | 2 | **4** |
| Copper weight | 1oz | **2oz outer, 1oz inner** |
| Board thickness | 1.6mm | 1.6mm |
| Min trace/space | 4/4mil | 6/6mil (easier with planes) |
| Min hole | 0.3mm | 0.3mm |
| Surface finish | ENIG | ENIG |
| Via process | Tenting | Tenting |

**Estimated cost (5 pcs PCBA):**
- v1.0: ~$70-100
- v2.0: ~$90-120 (+$20-30 for 4-layer)

---

## Implementation Checklist

### Phase 1: Schematic Updates
- [ ] Add F2 (polyfuse) in series with +12V input
- [ ] Add D1 (TVS) from +12V to GND
- [ ] Add FB1 between AMS1117 and DAC AVDD
- [ ] Add FB2 between AMS1117 and DAC DVDD
- [ ] Change C31 value to 470µF
- [ ] Run ERC

### Phase 2: PCB Layout
- [ ] Change board to 4-layer stackup
- [ ] Define In1.Cu as GND plane (solid fill)
- [ ] Define In2.Cu as +12V plane (connected to amp PVCC)
- [ ] Place F2 and D1 near J2
- [ ] Place FB1 and FB2 near U2/U1
- [ ] Increase thermal vias to 16 per amp
- [ ] Verify C31 footprint fits 10mm cap (or use 8mm 220µF)
- [ ] Route remaining signals
- [ ] Run DRC

### Phase 3: Manufacturing
- [ ] Generate 4-layer Gerbers
- [ ] Update BOM
- [ ] Generate placement file
- [ ] Verify in PCBWay viewer
- [ ] Order prototypes

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| 4-layer routing issues | Low | Inner planes simplify routing |
| 470µF cap doesn't fit | Medium | Fall back to 220µF 8mm or parallel 100µF |
| Cost increase | Certain | ~$20-30 more, worth it |
| EMI without output filters | Medium | Test v1.0 first, add external if needed |

---

## Testing Plan

### v1.0 Prototype Testing
1. Basic power-up test (no smoke)
2. I2S audio playback test
3. Volume control via I2C
4. Thermal monitoring at various power levels
5. Listen for noise/interference
6. Measure output with oscilloscope

### v2.0 Improvements to Verify
1. Thermal performance (should run cooler)
2. Power supply noise (should be cleaner)
3. Protection circuit (verify TVS clamps transients)

---

## Summary

**v2.0 Realistic Scope:**

| Feature | Status |
|---------|--------|
| 4-layer board | ✅ Adding |
| TVS protection | ✅ Adding |
| Polyfuse protection | ✅ Adding |
| Ferrite filtering | ✅ Adding |
| More thermal vias | ✅ Adding |
| Larger bulk cap | ✅ Adding |
| Software mute | ✅ Via PCM5142 |
| Output LC filters | ❌ Won't fit |
| Hardware mute relay | ❌ Won't fit |

**Total new components:** 5 (plus upgraded C31)
**Additional board space needed:** ~40mm² (fits easily)
**Cost increase:** ~$20-30 per 5 boards

This is a practical, achievable improvement that makes the board more robust without requiring a form factor change.
