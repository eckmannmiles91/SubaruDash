# WRX Power & CAN HAT - Installation Guide

Step-by-step installation instructions for the custom Pi HAT and amp module.

---

## What You'll Need

### Hardware
- WRX Power & CAN HAT (your custom board)
- 4-Channel Amp Module (separate board)
- Raspberry Pi 4 or 5
- **Car-specific ISO harness adapter** (~$15)
  - Example for 2013 WRX: Metra 70-8113
  - Search: "[Your car] to ISO 10487 adapter"
- **OBD-II Y-splitter cable** (~$10) OR **OBD-II extension cable** (~$8)
  - Examples: Veepeak OBD2 Splitter, EXZA HHOBD Y-Cable
- 6-pin JST-XH cable (HAT to amp module) - included or DIY

### Tools
- Phillips screwdriver
- Wire stripper/crimper (if making custom cables)
- Multimeter (for testing)

---

## Part 1: CAN Bus Connection (3 Options)

The HAT has **two CAN connectors** for maximum flexibility:
- **J4:** Female OBD-II connector (plug-and-play)
- **J5:** 2-pin screw terminal (backup/custom)

Choose the option that works best for your setup.

---

### **Option A: OBD-II Y-Splitter (Recommended for Most Users)**

**Best for:** Standard installations, keeping OBD-II port accessible

**What to buy:**
- OBD-II Y-splitter cable (1 female → 2 male)
- Cost: $8-12 on Amazon

**Installation:**
1. Locate your car's OBD-II port (usually under driver-side dash)
2. Plug the Y-splitter female end into the car's OBD-II port
3. Plug one male end into the HAT's **J4 connector**
4. Leave the other male end free for scan tools

**Wiring:**
```
Car OBD-II Port
      ↓
  Y-Splitter (female)
      ↓
   ┌──┴──┐
   ↓     ↓
  HAT   Free port
  (J4)  (for scan tool)
```

**Pros:**
✅ Plug-and-play - no wiring needed
✅ Keeps OBD-II port accessible
✅ Easy to remove/reinstall

**Cons:**
❌ Y-splitter cable might be visible
❌ Limited by OBD-II port location

---

### **Option B: OBD-II Extension Cable (Cleanest)**

**Best for:** Relocating OBD-II port closer to head unit

**What to buy:**
- OBD-II extension cable (male → female)
- Length: 3ft-6ft depending on routing
- Cost: $8-15 on Amazon

**Installation:**
1. Plug extension cable male end into car's OBD-II port
2. Route cable from OBD-II port to head unit location
3. Plug extension cable female end into HAT's **J4 connector**

**Wiring:**
```
Car OBD-II Port → [Extension Cable] → HAT (J4)
```

**Pros:**
✅ Clean installation
✅ Plug-and-play
✅ Cable can be hidden/routed cleanly

**Cons:**
❌ OBD-II port relocated (need splitter for scan tools)
❌ Slightly more expensive

---

### **Option C: Direct Wire to Screw Terminal (Advanced)**

**Best for:** Custom setups, tapping into Seicane harness, permanent installation

**What you need:**
- 22-24AWG wire (twisted pair recommended)
- Wire strippers
- Access to CAN High/Low signals

**CAN Signal Sources:**
1. **Seicane harness:** Pins 11 (CAN TX) and 12 (CAN RX)
2. **OBD-II port:** Manually wire to pins 6 (CANH) and 14 (CANL)
3. **CAN bus tap:** Splice into existing CAN wiring

**Installation:**
1. Identify CAN High (CANH) and CAN Low (CANL) wires
2. Strip wire ends
3. Connect to HAT's **J5 screw terminal:**
   - Pin 1: CAN High (CANH)
   - Pin 2: CAN Low (CANL)
4. Tighten screw terminals

**Wiring:**
```
CAN Source → Twisted pair → J5 Screw Terminal
  CANH     ───────────────→ Pin 1
  CANL     ───────────────→ Pin 2
```

**Pros:**
✅ Permanent, no dongles
✅ Can tap Seicane harness directly
✅ Cleaner than OBD-II cables

**Cons:**
❌ Requires wire splicing/crimping
❌ More advanced installation

---

## Part 2: Power Connection (ISO 10487-A)

The HAT uses a standard ISO 10487-A 8-pin connector for power.

**What to buy:**
- Car-specific to ISO adapter harness
- Example for Subaru WRX: **Metra 70-8113** ($12-15)
- Search: "[Your car make/model/year] to ISO 10487 adapter"

**Installation:**
1. Disconnect car battery (safety first!)
2. Remove head unit or access wiring harness
3. Locate car's power harness connector
4. Plug car harness into adapter's car-side connector
5. Plug adapter's ISO-side connector into HAT's **J1 (ISO A connector)**

**What it provides:**
- Pin 4: +12V Battery (constant power)
- Pin 7: +12V ACC (ignition-switched power)
- Pin 8: Ground

**The HAT automatically:**
- Powers on when ignition turns on
- Starts 45-second shutdown timer when ignition turns off
- Cuts power after timer expires

---

## Part 3: Speaker Connection (ISO 10487-B on Amp Module)

The separate amp module uses ISO 10487-B for speaker outputs.

**What to use:**
- Same adapter harness from Part 2 (includes both power AND speaker connectors)

**Installation:**
1. Adapter harness has two ISO connectors:
   - **ISO A (8-pin):** Power → Goes to HAT J1
   - **ISO B (8-pin):** Speakers → Goes to Amp Module J3
2. Plug ISO B connector into amp module's **J3 connector**

**Speakers connected:**
- Front Left (FL)
- Front Right (FR)
- Rear Left (RL)
- Rear Right (RR)

---

## Part 4: Audio Connection (HAT to Amp Module)

Connect the HAT's audio output to the amp module's input.

**Cable:**
- 6-pin JST-XH cable (male on both ends)
- Can make custom or buy pre-made
- Length: ~6-12 inches depending on layout

**Installation:**
1. Plug one end into HAT's **J7 connector** (6-pin audio output)
2. Plug other end into amp module's **J1 connector** (6-pin audio input)

**Signals:**
- Pin 1: Front Left
- Pin 2: Front Right
- Pin 3: Rear Left
- Pin 4: Rear Right
- Pin 5, 6: Ground

---

## Part 5: Mount and Assemble

### HAT Installation
1. Mount HAT onto Raspberry Pi GPIO header
2. Ensure all 40 pins are aligned and seated
3. HAT should sit flush on Pi

### Amp Module Placement
- Mount separately in head unit enclosure
- Needs airflow for cooling (50W+ output)
- Keep away from Pi (heat management)

### Final Connections Checklist
- [ ] ISO A (power) → HAT J1
- [ ] ISO B (speakers) → Amp J3
- [ ] OBD-II or screw terminal (CAN) → HAT J4 or J5
- [ ] 6-pin audio cable → HAT J7 to Amp J1
- [ ] Fan connector (optional) → HAT J6

---

## Part 6: First Power-On

### Before Connecting to Car

**Bench test with bench power supply (recommended):**
1. Apply 12V to ISO A connector (adapter harness)
2. Verify HAT power LED lights up
3. Check 5V rail with multimeter
4. No smoke = good!

### In-Car Testing Sequence

**Test 1: Power On**
1. Turn ignition to ACC position
2. HAT power LED should light
3. Pi should boot

**Test 2: Shutdown Timer**
1. With Pi running, turn ignition off
2. Pi should stay powered for 45 seconds
3. Timer LED on HAT should blink during countdown
4. After 45s, power should cut (Pi shuts down)

**Test 3: CAN Bus**
1. Pi should boot
2. Run: `candump can0` (if can0 configured)
3. Should see CAN messages from car
4. If no messages, check termination jumper JP1

**Test 4: Audio**
1. Run: `speaker-test -c 4 -t wav`
2. Should hear sound from all 4 speakers
3. Test front left, front right, rear left, rear right

---

## Troubleshooting

### No Power to Pi
- Check ISO A connector fully seated
- Verify car battery is charged
- Check fuse F1 on HAT (should be intact)
- Measure 12V at J1 pin 4 with multimeter

### Pi Won't Shut Down After Ignition Off
- ATtiny85 might need reprogramming
- Check timer LED - should blink during countdown
- Verify optoisolator U2 is working (ACC signal)

### No CAN Messages
- Check OBD-II cable fully plugged in
- Verify car is running (some cars only send CAN when engine on)
- Try closing termination jumper JP1
- Run: `ip link show can0` - should say "UP"

### No Audio
- Check 6-pin JST cable between HAT and amp
- Verify amp has 12V power
- Run: `aplay -l` - should show PCM5142 device
- Check speaker wiring polarity

### Speakers Distort or Cut Out
- Check amp isn't overheating
- Verify 12V power is stable (not dropping under load)
- Reduce volume
- Check speaker impedance (should be 4Ω)

---

## Software Configuration

See separate software setup guide for:
- Enabling I2S audio (PCM5142 DAC)
- Configuring CAN interface (MCP2515)
- Setting up shutdown scripts
- Installing OpenDash or other software

---

## Safety Notes

⚠️ **Important:**
- Always disconnect car battery before wiring
- Never short power pins with metal tools
- Check polarity before connecting power
- Use proper gauge wire for high-current connections
- Ensure no exposed wire that could short to chassis

---

## Getting Help

If you have issues:
1. Check wiring against this guide
2. Verify all connections are secure
3. Test with multimeter (12V, 5V, 3.3V rails)
4. Check PROJECT_STATUS.md for common issues
5. Post on GitHub issues with:
   - Photos of your setup
   - Voltage measurements
   - Error messages / symptoms

---

## Next Steps

Once everything is working:
1. Mount securely in dash
2. Route cables cleanly
3. Install final head unit/display
4. Configure OpenDash software
5. Enjoy your custom digital dash!

Happy building! 🚗⚡
