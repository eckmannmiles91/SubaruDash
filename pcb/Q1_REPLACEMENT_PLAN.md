# Q1 Replacement Plan: P-Channel to N-Channel MOSFET

## Issue Discovered
- Q1 (IRF9540N P-Channel) gate is unconnected in schematic
- ATtiny85 outputs 3.3V, but Q1 needs 12V gate drive for proper operation
- P-channel high-side switching incompatible with 3.3V logic

## Solution: Replace with N-Channel Low-Side Switch

### Component Selection
**Primary Choice: IRLB8721PBF**
- Type: N-Channel Logic-Level MOSFET
- Ratings: 30V, 62A
- RDS(on): 3.7mΩ @ 3.3V Vgs
- Package: TO-220
- Gate Threshold: 1-2V (fully on at 3.3V)

**Alternative: IRL540N**
- Type: N-Channel Logic-Level MOSFET
- Ratings: 100V, 28A
- Package: TO-220

### Circuit Configuration Change

**OLD (P-Channel High-Side):**
```
12V_FUSED → [Q1 S-D] → 12V_SWITCHED → Load → GND
```

**NEW (N-Channel Low-Side):**
```
12V_FUSED → Load → 12V_SWITCHED → [Q1 D-S] → GND
                                        ↑
                                    GATE_CTRL (via resistors)
```

### Implementation Steps

#### 1. Replace Q1 Component
- Delete current Q1 (IRF9540N)
- Add: Transistor_FET:IRLB8721 or IRL540N
- Reference: Q1
- Value: "IRLB8721" or "IRL540N"

#### 2. Q1 Pin Connections
- **Pin 1 (Gate)**: Connect to "Q1_GATE" label
- **Pin 2 (Drain)**: Connect to "12V_SWITCHED" label
- **Pin 3 (Source)**: Connect to GND power symbol

#### 3. Add Gate Drive Resistors

**R_Q1_GATE (1kΩ):**
- Purpose: Limit gate drive current
- Connection: GATE_CTRL → Q1_GATE
- Reference: Use next available R number (R20 or similar)

**R_Q1_PULLDOWN (10kΩ):**
- Purpose: Ensure MOSFET stays OFF when ATtiny85 not driving
- Connection: Q1_GATE → GND
- Reference: Use next available R number (R21 or similar)

### Gate Drive Circuit Schematic
```
ATtiny85 GATE_CTRL → [R_Q1_GATE: 1kΩ] → Q1_GATE → Q1 Pin 1
                                            ↓
                                    [R_Q1_PULLDOWN: 10kΩ]
                                            ↓
                                           GND
```

### Load Connection Update
The load (Raspberry Pi or accessories) connects:
- **Positive (+)**: 12V_FUSED (direct from input)
- **Ground (-)**: 12V_SWITCHED (switched by Q1)

When GATE_CTRL is HIGH (3.3V):
- Q1 conducts (ON)
- 12V_SWITCHED connects to GND
- Load is powered

When GATE_CTRL is LOW (0V):
- Q1 blocks (OFF)
- 12V_SWITCHED is floating
- Load is unpowered

### Expected Results
- ATtiny85 can now control Q1 with 3.3V logic ✓
- Clean on/off switching of 12V accessories ✓
- Proper gate protection with resistors ✓
- Compatible with automotive environment ✓

### Next Session TODO
1. Delete Q1 (IRF9540N P-channel)
2. Add Q1 (IRLB8721 or IRL540N N-channel)
3. Wire Q1 pins (Gate to Q1_GATE, Drain to 12V_SWITCHED, Source to GND)
4. Add R_Q1_GATE (1kΩ) between GATE_CTRL and Q1_GATE
5. Add R_Q1_PULLDOWN (10kΩ) between Q1_GATE and GND
6. Run ERC to verify
7. Test circuit logic
8. Commit changes

## Current Status: Plan Complete, Ready for Implementation
