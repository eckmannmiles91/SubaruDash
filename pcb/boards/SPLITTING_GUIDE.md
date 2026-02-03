# Schematic Splitting Guide

Step-by-step instructions to split the combined schematic into 3 boards.

---

## Preparation

1. **Backup** the original schematic:
   ```
   Copy: wrx-power-can-hat-MANUAL.kicad_sch
   To:   wrx-power-can-hat-MANUAL-BACKUP-PRESPLIT.kicad_sch
   ```

2. **Open** each new project in KiCad:
   - `boards/can-hat/can-hat.kicad_pro`
   - `boards/power-hat/power-hat.kicad_pro`
   - `boards/dac-amp/dac-amp.kicad_pro`

---

## Method: Copy Components in KiCad

### Step 1: Open Original Schematic
1. Open `wrx-power-can-hat-MANUAL.kicad_sch` in Eeschema

### Step 2: Create CAN HAT Schematic

1. Open `boards/can-hat/can-hat.kicad_pro` in a new KiCad window
2. Open its schematic editor (Eeschema)

3. **From original schematic, SELECT and COPY (Ctrl+C):**

   **ICs:**
   - U4 (MCP2515)
   - U5 (SN65HVD230)
   - U6 (AMS1117-3.3)

   **Passive Components:**
   - Y1 (16MHz crystal)
   - C3, C4 (LDO caps)
   - C11, C12 (crystal load caps)
   - C13, C14, C15, C16, C17 (decoupling)
   - L2, L3 (ferrite beads)
   - R11, R12, R13 (LED resistors)
   - R14, R15, R16, R17 (misc)
   - R18 (120Ω termination)

   **Connectors:**
   - J2 (Pi header - you'll need to add a new one)
   - J3 (OBD-II connector)
   - J4 (CAN termination)

   **Indicators:**
   - LED1, LED2, LED3

4. **Paste (Ctrl+V)** into CAN HAT schematic
5. **Wire** the components together
6. **Add power symbols** (+5V, +3.3V, GND)
7. **Save**

### Step 3: Create Power HAT Schematic

1. Open `boards/power-hat/power-hat.kicad_pro`
2. Open its schematic editor

3. **From original schematic, SELECT and COPY:**

   **ICs:**
   - U1 (TPS54560BDDA)
   - U2 (LTV-817S optocoupler)
   - U3 (ATtiny85)

   **Power Components:**
   - L1 (22µH inductor)
   - D1 (SS34 catch diode)
   - D2 (SMBJ18A TVS)
   - F1 (fuse holder)

   **MOSFETs:**
   - Q1 (IRLB8721PBF)
   - Q2, Q3 (2N7002)

   **Capacitors:**
   - C1, C_BOOT1 (bootstrap)
   - C2 (output bulk)
   - C5 (soft-start)
   - C6, C7, C_COMP1 (compensation)
   - C8 (feedforward)
   - C10, C20 (input bulk)

   **Resistors:**
   - R1, R6 (voltage dividers)
   - R4, R5 (feedback - 1%)
   - R8, R9 (misc)
   - R10, R_COMP1 (compensation)
   - R_RT1 (timing)
   - R19, R20, R21 (gate drive)

   **Connectors:**
   - J1 (Molex vehicle harness)
   - J2 (Pi header - add new one)
   - J5 (ISP header)
   - J6 (FAN)
   - JP1, JP2 (jumpers)

4. **Paste** into Power HAT schematic
5. **Wire** the components
6. **Add power symbols**
7. **Save**

### Step 4: Create DAC/Amp Schematic (New Design)

This board needs new components not in the original schematic.

1. Open `boards/dac-amp/dac-amp.kicad_pro`
2. Open its schematic editor

3. **Add NEW symbols:**

   **ICs:**
   - PCM5142RGZR (Quad I2S DAC) - from `Audio_Module:PCM5142`
   - 2× TPA3116D2 (Class D Amp) - from `Amplifier_Audio:TPA3116D2`

   **Connectors:**
   - 6-pin JST for I2S input (BCK, LRCK, DIN, GND, GND, 3.3V)
   - 2-pin for 12V power input
   - ISO 10487-B or screw terminals for speaker outputs

   **Passive Components:**
   - Decoupling capacitors for DAC
   - LC output filters for Class D amps
   - Input capacitors for amps

4. **Wire** the I2S signals from input connector to PCM5142
5. **Wire** DAC outputs to TPA3116D2 inputs
6. **Wire** amp outputs to speaker connector
7. **Add power regulation** (12V → 5V → 3.3V)
8. **Save**

---

## Quick Reference: Component Allocation

### CAN HAT Components
```
U4, U5, U6
Y1
C3, C4, C11, C12, C13, C14, C15, C16, C17
L2, L3
R11, R12, R13, R14, R15, R16, R17, R18
J3, J4
LED1, LED2, LED3
+ New J2 (Pi header)
```

### Power HAT Components
```
U1, U2, U3
Q1, Q2, Q3
F1, D1, D2, L1
C1, C2, C5, C6, C7, C8, C10, C20, C_BOOT1, C_COMP1
R1, R4, R5, R6, R8, R9, R10, R19, R20, R21, R_COMP1, R_RT1
J1, J5, J6, JP1, JP2
+ New J2 (Pi header)
```

### DAC/Amp Components (All New)
```
PCM5142 (Quad DAC)
2× TPA3116D2 (Class D Amps)
I2S input connector
12V power connector
Speaker output connector
Supporting passives
```

---

## After Splitting

1. **Run ERC** on each schematic
2. **Assign footprints** to any new components
3. **Update PCB** from schematic for each board
4. **Layout** each board separately

---

## Tips

- Use **hierarchical sheets** in KiCad if you want to keep sections organized
- Copy the **entire wire connections** along with components when possible
- Each board needs its **own Pi header (J2)** - they don't share
- Use **global labels** for signals that go to the Pi header
- The Power HAT provides 5V to Pi, CAN HAT uses Pi's 5V/3.3V

---

## Testing Order

1. **CAN HAT** - Simplest, test CAN communication first
2. **Power HAT** - Test power delivery and shutdown
3. **DAC/Amp** - Test audio output last (can use off-the-shelf initially)
