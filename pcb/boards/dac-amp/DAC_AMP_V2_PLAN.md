# DAC/Amp HAT v2.0 - Design Plan

## Overview

Improved revision of the 4-channel Class D amplifier HAT with better audio quality, EMI compliance, and thermal management.

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

## v2.0 Target Specifications

| Spec | Target |
|------|--------|
| DAC | PCM5142 or PCM5242 |
| Amps | 2× TPA3116D2DAD (keep for compatibility) |
| Layers | **4-layer** (F.Cu, GND, +12V, B.Cu) |
| Power traces | +12V @ 2.0mm, speakers @ 1.5mm |
| Thermal vias | **16+ per amp** |
| Output filtering | **LC filter per channel** |
| Ground topology | **Split analog/digital** |
| Protection | **TVS + polyfuse + mute relay** |

---

## Schematic Changes

### 1. Output LC Filters (Per Channel - 8 Total)

```
Amp Output ──┬── L (10µH) ──┬── Speaker Terminal
             │              │
             └── C (680nF) ─┴── GND
```

**Components to add:**
| Ref | Value | Package | Purpose |
|-----|-------|---------|---------|
| L1-L8 | 10µH | 1210 or through-hole | Output filter inductor |
| C33-C40 | 680nF | 0805 (100V rated) | Output filter capacitor |

**Inductor spec:**
- Current rating: >5A
- DCR: <50mΩ
- Shielded preferred (reduces EMI radiation)
- Example: Bourns SRR1210A-100M

### 2. Input Protection

```
J2 +12V ──┬── F1 (polyfuse 5A) ──┬── TVS ──┬── +12V_FUSED
          │                      │         │
          └──────────────────────┴─────────┴── GND
```

**Components to add:**
| Ref | Value | Package | Purpose |
|-----|-------|---------|---------|
| F2 | 5A polyfuse | 1812 | Resettable overcurrent protection |
| D1 | SMBJ15A | SMB | TVS for transient suppression |

### 3. Mute Relay Circuit

```
+12V ────┬── D2 (flyback) ──┬── Relay Coil ── Q1 (MOSFET) ── GND
         │                  │                      │
         └──────────────────┘                GPIO_MUTE

Relay contacts in series with speaker outputs (normally open)
```

**Components to add:**
| Ref | Value | Package | Purpose |
|-----|-------|---------|---------|
| K1 | G5V-2 (DPDT) | Through-hole | Mute relay (front channels) |
| K2 | G5V-2 (DPDT) | Through-hole | Mute relay (rear channels) |
| Q5 | 2N7002 | SOT-23 | Relay driver MOSFET |
| D2 | 1N4148 | SOD-123 | Flyback diode |
| R3 | 10k | 0805 | Gate pull-down |

**GPIO Assignment:** GPIO24 (pin 18) for mute control

### 4. Soft-Start Circuit

```
+12V_FUSED ── R (10Ω 5W) ──┬── C (1000µF) ──┬── +12V_SOFT
                           │               │
                           └── Relay bypass┘
```

Delays full power to amps, prevents speaker pop.

### 5. Bulk Capacitance Upgrade

| Current | Upgraded |
|---------|----------|
| C31: 100µF | C31: 470µF (or 1000µF) |

Add parallel caps for lower ESR:
| Ref | Value | Package |
|-----|-------|---------|
| C41 | 100µF | 0805 (MLCC, optional parallel) |
| C42 | 100µF | 0805 (MLCC, optional parallel) |

### 6. Ferrite Beads on Power Rails

```
+3.3V_RAW ── FB1 ── +3.3V_ANALOG (to DAC)
+3.3V_RAW ── FB2 ── +3.3V_DIGITAL (to DAC digital)
```

| Ref | Value | Package |
|-----|-------|---------|
| FB1 | 600Ω@100MHz | 0805 |
| FB2 | 600Ω@100MHz | 0805 |

---

## PCB Layout Changes

### 1. 4-Layer Stackup

| Layer | Purpose |
|-------|---------|
| F.Cu (Top) | Signal, components |
| In1.Cu | **GND plane** |
| In2.Cu | **+12V plane** |
| B.Cu (Bottom) | Signal, components |

**Benefits:**
- Lower power impedance
- Better heat spreading
- Improved EMI shielding
- Cleaner routing

### 2. Ground Plane Split

```
┌─────────────────────────────────────┐
│  DIGITAL GND        │  ANALOG GND   │
│  (DAC digital,      │  (DAC analog, │
│   Pi GPIO)          │   amp inputs) │
│                     │               │
│         ← Single point bridge →     │
└─────────────────────────────────────┘
```

- Bridge at power input (star ground)
- Keeps digital switching noise away from analog

### 3. Thermal Via Array

```
  ┌─────────────────┐
  │ o o o o o o o o │
  │ o o o o o o o o │  ← 16 vias minimum
  │ o o o o o o o o │     (4×4 or 4×5 grid)
  │ o o o o o o o o │
  └─────────────────┘
```

- Via size: 0.4mm drill, 0.8mm pad
- Spacing: 1.0mm grid
- All connected to GND plane

### 4. Component Placement Zones

```
┌────────────────────────────────────────────────┐
│ [Power Input]  [Bulk Caps]  [Protection]       │
│                                                │
│ [DAC Section]          [Amp U3]    [Amp U4]   │
│  - PCM5142              - TPA3116   - TPA3116 │
│  - 3.3V LDO             - Bootstrap - Bootstrap│
│  - Decoupling           - PVCC caps - PVCC caps│
│                                                │
│ [Output Filters]       [Mute Relays]          │
│                                                │
│ [Speaker Terminals J3]  [Speaker Terminals J4]│
└────────────────────────────────────────────────┘
```

### 5. Trace Width Targets

| Net | v1.0 | v2.0 Target |
|-----|------|-------------|
| +12V main | 1.0mm | 2.0mm |
| Speaker outputs | 0.75mm | 1.5mm |
| GND return | Pour | Plane (4-layer) |
| Audio signals | 0.25mm | 0.3mm (with guard traces) |
| I2S/I2C | 0.25mm | 0.25mm (matched length) |

---

## New BOM (Additional Components)

### Output Filters (8 channels)

| Ref | Description | MPN | Qty |
|-----|-------------|-----|-----|
| L1-L8 | 10µH 5A shielded | SRR1210A-100M | 8 |
| C33-C40 | 680nF 100V X7R | GRM31CR72A684KA88L | 8 |

### Protection

| Ref | Description | MPN | Qty |
|-----|-------------|-----|-----|
| F2 | 5A polyfuse | MF-MSMF500 | 1 |
| D1 | TVS 15V bidirectional | SMBJ15CA | 1 |

### Mute Circuit

| Ref | Description | MPN | Qty |
|-----|-------------|-----|-----|
| K1, K2 | DPDT relay 12V | G5V-2-DC12 | 2 |
| Q5 | N-FET SOT-23 | 2N7002 | 1 |
| D2 | Flyback diode | 1N4148WS | 1 |
| R3 | 10k 0805 | RC0805FR-0710KL | 1 |

### Ferrites

| Ref | Description | MPN | Qty |
|-----|-------------|-----|-----|
| FB1, FB2 | 600Ω@100MHz | BLM21PG601SN1D | 2 |

### Bulk Caps

| Ref | Description | MPN | Qty |
|-----|-------------|-----|-----|
| C31 | 470µF 25V | UVR1E471MED | 1 |

---

## GPIO Allocation Update

| GPIO | Pin | Function | v1.0 | v2.0 |
|------|-----|----------|------|------|
| GPIO2 | 3 | I2C_SDA | DAC config | DAC config |
| GPIO3 | 5 | I2C_SCL | DAC config | DAC config |
| GPIO18 | 12 | I2S_BCK | I2S clock | I2S clock |
| GPIO19 | 35 | I2S_LRCK | I2S L/R | I2S L/R |
| GPIO21 | 40 | I2S_DOUT | I2S data | I2S data |
| GPIO24 | 18 | MUTE | - | **Mute relay control** |
| GPIO23 | 16 | FAULT | - | **Amp fault status** |

---

## Manufacturing Changes

| Spec | v1.0 | v2.0 |
|------|------|------|
| Layers | 2 | **4** |
| Copper weight | 1-2oz | **2oz all layers** |
| Board thickness | 1.6mm | 1.6mm |
| Min trace | 4/4mil | 6/6mil |
| Surface finish | ENIG | ENIG |
| Estimated cost (5 pcs) | ~$45 | ~$80-100 |

---

## Implementation Phases

### Phase 1: Schematic Updates
1. [ ] Add output LC filter network (L1-L8, C33-C40)
2. [ ] Add TVS and polyfuse to 12V input
3. [ ] Add mute relay circuit
4. [ ] Add ferrite beads to 3.3V rails
5. [ ] Upgrade bulk capacitor value
6. [ ] Add FAULT and MUTE GPIO connections
7. [ ] Run ERC

### Phase 2: PCB Layout
1. [ ] Create 4-layer board stackup
2. [ ] Define ground plane split regions
3. [ ] Place new components
4. [ ] Increase thermal via count (16+ per amp)
5. [ ] Widen power traces
6. [ ] Route with guard traces on audio signals
7. [ ] Add via stitching around board edges
8. [ ] Run DRC

### Phase 3: Manufacturing Files
1. [ ] Generate Gerbers (4-layer)
2. [ ] Update BOM with new components
3. [ ] Generate placement file
4. [ ] Review in PCBWay viewer
5. [ ] Order prototypes

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| 4-layer routing complexity | Use inner planes for power, simplifies routing |
| Relay adds pop when muting | Add RC delay to relay drive |
| LC filter resonance | Calculate corner frequency, verify no ringing |
| Cost increase | Worth it for production quality |
| Board space for relays | May need to move to larger form factor or vertical mount |

---

## Timeline

| Phase | Estimated Effort |
|-------|------------------|
| Schematic updates | 2-3 hours |
| PCB layout | 4-6 hours |
| Review and DRC | 1-2 hours |
| Order and receive | 1-2 weeks |
| Test v2.0 | 2-3 hours |

---

## Notes

- Test v1.0 first to validate basic functionality
- v2.0 changes can be incremental (do output filters first, then 4-layer)
- Consider making output filters a daughter board if space is tight
- Mute relay is optional but highly recommended for car install

---

## References

- TPA3116D2 Datasheet: Output filter design guidelines
- PCM5142 Datasheet: Layout recommendations
- TI Application Note SLOA119: Class D output filter design
- IPC-2221: PCB trace current capacity
