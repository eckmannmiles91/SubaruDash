# Manual Component Replacement Guide

Follow these steps to replace U3, U4, and U5 with the correct components in KiCad.

## Component Replacements Needed:

1. **U3**: SN65HVD230 → ATtiny85-20PU (microcontroller)
2. **U4**: LTV-817S → MCP2515 (CAN controller)
3. **U5**: PCM5142 → SN65HVD230 (CAN transceiver)

---

## Step-by-Step Instructions

### Step 1: Replace U3 (SN65HVD230 → ATtiny85)

1. **Find U3** in the schematic (it's the SN65HVD230 component)
2. **Click on U3** to select it
3. Press **E** (or right-click → Properties) to edit
4. In the Properties dialog:
   - Click on the **Symbol** field where it says "SN65HVD230"
   - Click the **📚 library icon** to browse for a new symbol
5. In the symbol browser:
   - Search for: **ATtiny85**
   - Select: **MCU_Microchip_ATtiny:ATtiny85-20PU**
   - Click **OK**
6. The footprint should auto-update to **Package_DIP:DIP-8_W7.62mm**
7. Click **OK** to close Properties
8. Press **Ctrl+S** to save

**Result:** U3 is now an ATtiny85 microcontroller (8 pins)

---

### Step 2: Replace U4 (LTV-817S → MCP2515)

1. **Find U4** in the schematic (it's the LTV-817S optoisolator)
2. **Click on U4** to select it
3. Press **E** to edit properties
4. In the Properties dialog:
   - Click on the **Symbol** field
   - Click the **📚 library icon**
5. In the symbol browser:
   - Search for: **MCP2515**
   - Select: **Interface_CAN_LIN:MCP2515-I/SO** (or MCP2515-I/ST)
   - Click **OK**
6. The footprint should auto-update to a SOIC-18 or TSSOP-20 package
7. Click **OK** to close Properties
8. Press **Ctrl+S** to save

**Result:** U4 is now an MCP2515 CAN controller (18 pins)

---

### Step 3: Replace U5 (PCM5142 → SN65HVD230)

1. **Find U5** in the schematic (it's the PCM5142 audio DAC)
2. **Click on U5** to select it
3. Press **E** to edit properties
4. In the Properties dialog:
   - Click on the **Symbol** field
   - Click the **📚 library icon**
5. In the symbol browser:
   - Search for: **SN65HVD230**
   - Select: **Interface_CAN_LIN:SN65HVD230**
   - Click **OK**
6. The footprint should auto-update to **Package_SO:SOIC-8_3.9x4.9mm_P1.27mm**
7. Click **OK** to close Properties
8. Press **Ctrl+S** to save

**Result:** U5 is now an SN65HVD230 CAN transceiver (8 pins)

---

## After Replacing All Components

1. **Save the schematic**: Press **Ctrl+S**
2. **Save As**: File → Save As → Name it **wrx-power-can-hat-MANUAL.kicad_sch**
3. **Run ERC**: Inspect → Electrical Rules Checker → Run ERC
4. **Save ERC report**: Save as **ERC_9.rpt**
5. **Close KiCad**

Then we'll use the ERC report to add the correct pin connections!

---

## Tips

- If you can't find a component in the library, you may need to:
  - Install additional libraries
  - Or choose a similar component (e.g., ATtiny84 instead of ATtiny85)

- The component should snap to the same location as the old one

- Don't worry about wiring yet - we'll fix all connections after replacement

---

**Ready?** Start with U3 and work through each one. Let me know when you're done or if you get stuck!
