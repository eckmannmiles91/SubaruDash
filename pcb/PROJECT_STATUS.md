# WRX Power & CAN HAT - Project Status

Current progress and next steps for the custom PCB design.

---

## ✅ Completed

### Design Documentation
- [x] Feature specification (CUSTOM_PCB_DESIGN.md)
- [x] Complete schematic design with all 10 circuit sections (SCHEMATIC_DESIGN.md)
- [x] Bill of Materials with Digi-Key part numbers
- [x] ATtiny85 firmware written and documented (firmware/timer_controller.ino)
- [x] ATtiny85 programming guide (firmware/README.md)
- [x] KiCad setup and schematic creation guide (KICAD_SETUP_GUIDE.md)
- [x] Component quick reference for KiCad (kicad/COMPONENT_REFERENCE.md)

### Design Decisions
- [x] DIP-8 package chosen for ATtiny85 (easy reprogramming via socket)
- [x] 3.3V-native CAN transceiver (SN65HVD230) eliminates level shifters
- [x] Fixed 45-second shutdown delay timer
- [x] Single CAN bus interface
- [x] **ISO 10487-A connector** for power input (universal car harness compatibility)
- [x] **Female OBD-II connector** for CAN bus (plug-and-play with Y-splitter)
- [x] **4-channel audio** with PCM5142 quad I2S DAC
- [x] **Separate amp module** design (2× TPA3116D2 for 4× 50W speakers)
- [x] **ISO 10487-B connector** on amp module (universal speaker harness)
- [x] PWM fan control
- [x] Status LEDs for debugging

### Firmware
- [x] ATtiny85 state machine implemented
- [x] 45-second timer logic with edge case handling
- [x] Ignition detection with debouncing
- [x] Power control output for P-FET gate driver
- [x] Status LEDs (timer, heartbeat)
- [x] Ready to flash and test

---

## 🚧 In Progress

### KiCad Schematic Design
- [ ] Install KiCad 8.x
- [ ] Create new project: wrx-power-can-hat
- [ ] Configure symbol and footprint libraries
- [ ] Place and wire components (Sections 1-11)
  - [ ] Section 1: Power Input & Protection (with ISO A connector)
  - [ ] Section 2: Buck Converter (12V → 5V)
  - [ ] Section 3: Ignition Detection (Optoisolator)
  - [ ] Section 4: Timer Circuit (ATtiny85)
  - [ ] Section 5: P-FET Gate Driver
  - [ ] Section 6: CAN Bus Interface (with OBD-II connector)
  - [ ] Section 7: Fan Control
  - [ ] Section 8: Status LEDs
  - [ ] Section 9: 3.3V Regulator (Backup)
  - [ ] Section 10: Raspberry Pi GPIO Header
  - [ ] Section 11: 4-Channel I2S DAC (PCM5142)
- [ ] Run Electrical Rules Check (ERC)
- [ ] Assign footprints to all components
- [ ] Generate netlist

---

## 📋 Next Steps

### PCB Layout (After Schematic Complete)
1. [ ] Open PCB editor
2. [ ] Update PCB from schematic (import components)
3. [ ] Draw board outline (85mm x 56mm HAT size)
4. [ ] Add mounting holes at Pi HAT locations
5. [ ] Place components strategically:
   - [ ] 40-pin GPIO header at board edge
   - [ ] ATtiny85 accessible for reprogramming
   - [ ] Power components near 12V input
   - [ ] CAN components near screw terminals
6. [ ] Route power traces (wide: 1mm for 12V, 0.5mm for 5V)
7. [ ] Route signal traces (0.25mm)
8. [ ] Add ground plane (copper pour)
9. [ ] Add silkscreen labels
10. [ ] Run Design Rules Check (DRC)
11. [ ] Generate 3D view and verify

### Manufacturing Files
1. [ ] Generate Gerber files
2. [ ] Generate drill files
3. [ ] Create assembly drawing (component placement diagram)
4. [ ] Export BOM to CSV
5. [ ] Zip Gerbers for JLCPCB

### Order Components
1. [ ] Upload BOM to Digi-Key
2. [ ] Review and order (2-3x quantity for spares)
3. [ ] Order 3x ATtiny85-20PU chips
4. [ ] Order DIP-8 socket

### Order PCB
1. [ ] Upload Gerbers to JLCPCB
2. [ ] Select options:
   - Qty: 5
   - Thickness: 1.6mm
   - Color: Green (or preference)
   - Surface finish: HASL or ENIG
3. [ ] Place order

### Assembly & Testing
1. [ ] Solder SMD components (0805s, ICs)
2. [ ] Solder through-hole components (screw terminals, headers, socket)
3. [ ] Flash ATtiny85 with firmware using Arduino Mega ISP
4. [ ] Insert ATtiny85 into socket
5. [ ] Bench test without Pi:
   - [ ] Apply 12V, verify 5V output
   - [ ] Test ignition detection (button + LED)
   - [ ] Test timer circuit (45s countdown)
   - [ ] Verify power cutoff after timer
6. [ ] Test with Raspberry Pi:
   - [ ] Mount HAT on Pi
   - [ ] Apply 12V ACC power
   - [ ] Verify Pi boots
   - [ ] Test CAN interface (MCP2515)
   - [ ] Test shutdown sequence
7. [ ] Car installation test:
   - [ ] Connect to OBD-II splitter
   - [ ] Test ignition ON → Pi boots
   - [ ] Test ignition OFF → 45s delay → shutdown
   - [ ] Monitor for issues overnight

---

## 🎯 Current Milestone

**Milestone 1: Complete KiCad Schematic** (Target: This week)

Your immediate next action:
1. Open [KICAD_SETUP_GUIDE.md](KICAD_SETUP_GUIDE.md)
2. Install KiCad 8.x if not already installed
3. Create the project following Part 1 of the guide
4. Start placing components from Section 1 (use [COMPONENT_REFERENCE.md](kicad/COMPONENT_REFERENCE.md))

---

## 📊 Project Timeline Estimate

| Phase | Duration | Status |
|-------|----------|--------|
| Design Documentation | 3-5 days | ✅ Complete |
| Firmware Development | 1-2 days | ✅ Complete |
| KiCad Schematic | 4-6 hours | 🚧 In Progress |
| PCB Layout | 6-8 hours | ⏸️ Pending |
| Generate Manufacturing Files | 1 hour | ⏸️ Pending |
| Order Components (Digi-Key) | 3-5 days shipping | ⏸️ Pending |
| Order PCB (JLCPCB) | 5-7 days production + shipping | ⏸️ Pending |
| Assembly (SMD + THT) | 2-3 hours | ⏸️ Pending |
| Bench Testing | 2-3 hours | ⏸️ Pending |
| Car Installation & Testing | 1-2 hours | ⏸️ Pending |
| **Total Project Time** | **~3-4 weeks** | |

**Note:** Schematic and PCB layout are the most time-consuming steps, but only need to be done once.

---

## 💰 Cost Breakdown

| Item | Estimated Cost | Status |
|------|---------------|--------|
| PCB Fabrication (5 boards) | $10-20 | ⏸️ Not ordered |
| Components (Digi-Key BOM) | $30-40 | ⏸️ Not ordered |
| Shipping (Digi-Key) | $5-8 | ⏸️ Not ordered |
| Shipping (JLCPCB) | $15-25 | ⏸️ Not ordered |
| **Total per board** | **$12-18** | |
| **Total project cost** | **$60-95** | |

**Savings:** Custom HAT (~$15/board) vs buying individual modules:
- X735 V3.0: ~$25
- DROK timer relay: ~$12
- MCP2515 + level shifter: ~$15
- PC817 module: ~$5
- **Total if buying modules:** ~$57

**Your custom HAT gives you:**
- Everything integrated on one board
- Cleaner installation (no jumper wire mess)
- Professional appearance
- Easy to replicate (order more boards anytime)

---

## 📁 Project Structure

```
SubaruDash/pcb/
├── CUSTOM_PCB_DESIGN.md          # High-level feature spec
├── SCHEMATIC_DESIGN.md            # Detailed circuit design (all 10 sections)
├── KICAD_SETUP_GUIDE.md           # Step-by-step KiCad instructions
├── PROJECT_STATUS.md              # This file (current status)
│
├── firmware/
│   ├── timer_controller.ino      # ATtiny85 firmware
│   └── README.md                 # Programming instructions
│
├── kicad/
│   ├── wrx-power-can-hat.kicad_pro    # KiCad project (not created yet)
│   ├── wrx-power-can-hat.kicad_sch    # Schematic file (not created yet)
│   ├── wrx-power-can-hat.kicad_pcb    # PCB layout (not created yet)
│   ├── COMPONENT_REFERENCE.md         # Quick component lookup
│   ├── library/                       # Custom symbols/footprints (if needed)
│   ├── gerbers/                       # Manufacturing files (after PCB done)
│   ├── bom/                           # Bill of materials exports
│   └── datasheets/                    # Component datasheets (optional)
```

---

## 🛠️ Tools Required

### Software
- [x] KiCad 8.x (download: https://www.kicad.org/download/)
- [x] Arduino IDE (for ATtiny85 programming)
- [ ] Web browser (JLCPCB, Digi-Key)

### Hardware (for assembly)
- [ ] Soldering iron (temperature controlled, 300-350°C)
- [ ] Solder (60/40 or 63/37 leaded, 0.6mm diameter)
- [ ] Flux pen (helps with SMD soldering)
- [ ] Tweezers (for placing SMD components)
- [ ] Multimeter (for continuity and voltage testing)
- [ ] Arduino Mega (for ATtiny85 ISP programming)

### Optional but Helpful
- [ ] Magnifying glass or microscope (for SMD inspection)
- [ ] Solder wick (for fixing mistakes)
- [ ] Isopropyl alcohol (for cleaning flux residue)
- [ ] Hot air station (if you mess up and need to rework)

---

## 🚨 Critical Reminders

1. **ATtiny85 Socket:** Make sure to use DIP-8 socket on PCB - allows easy reprogramming
2. **Pin Assignments:** ATtiny85 pin diagram in SCHEMATIC_DESIGN.md Section 4 is correct and matches firmware
3. **Power Trace Width:** Use wide traces for power (1mm for 12V, 0.5mm for 5V) to handle current
4. **CAN Termination:** JP1 jumper allows 120Ω termination - only close if this is the last device on CAN bus
5. **GPIO Voltage:** Pi GPIO is 3.3V - do NOT connect 5V signals directly!
6. **Firmware Timing:** ATtiny85 uses internal 8MHz oscillator - set fuses correctly when programming

---

## 📞 Getting Help

If you run into issues:

1. **KiCad Schematic Problems:**
   - Refer to [KICAD_SETUP_GUIDE.md](KICAD_SETUP_GUIDE.md)
   - Check [KiCad forums](https://forum.kicad.info/)
   - Search for similar HAT designs on GitHub

2. **Firmware Issues:**
   - Refer to [firmware/README.md](firmware/README.md)
   - Verify wiring between Arduino Mega and ATtiny85
   - Check ATtiny85 fuse settings

3. **PCB Manufacturing:**
   - JLCPCB has built-in DRC (design rule check) when you upload Gerbers
   - If DRC fails, they'll tell you what needs fixing

4. **Component Sourcing:**
   - If Digi-Key part is out of stock, search for the value/package (e.g., "1kΩ 0805")
   - Most 0805 resistors/capacitors are interchangeable

---

## ✨ Next Action

**Open KiCad and start creating the schematic!**

👉 Follow [KICAD_SETUP_GUIDE.md](KICAD_SETUP_GUIDE.md) Part 1 to get started.

Once you complete the schematic and run ERC successfully, come back for PCB layout instructions.

Good luck! 🚀
