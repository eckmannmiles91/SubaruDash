# WRX Power & CAN HAT - Custom PCB Design

Custom Raspberry Pi HAT combining power management, ignition detection, CAN bus interface, and safe shutdown for automotive installations.

---

## Overview

This custom PCB replaces 5+ separate modules with a single, compact Raspberry Pi HAT:
- ✅ X735-style power management (12V → 5V, safe shutdown, fan control)
- ✅ PC817 ignition detection circuit
- ✅ DROK-style shutdown delay timer
- ✅ MCP2515 CAN bus interface with 3.3V logic
- ✅ Status LEDs and voltage monitoring

**Form Factor:** Raspberry Pi HAT (standard 40-pin GPIO header)
**Target Use:** Car installation for 2013 Subaru WRX with OpenDash

---

## Feature Specification

### 1. Power Management
**Input:**
- 12V automotive power (9V-16V operating range)
- Reverse polarity protection (P-channel MOSFET or Schottky diode)
- Overvoltage protection (TVS diode, 18V clamp)
- Automotive-grade input filter capacitors

**12V → 5V Buck Converter:**
- **IC Recommendation:** Texas Instruments LM2596S or Murata OKI-78SR-5/1.5-W36-C
- **Output:** 5V @ 3A minimum (5A preferred for Pi 5 + peripherals)
- **Efficiency:** >85% typical
- **Features:**
  - Soft-start to prevent inrush current
  - Thermal shutdown protection
  - Short circuit protection

**Power Control:**
- High-side P-channel MOSFET (controlled by timer circuit)
- Low-Rds(on) to minimize voltage drop (<50mΩ)
- Recommended: IRF9540 or similar (23A, 100V, automotive-grade)

**Safe Shutdown Circuit:**
- Monitors GPIO 18 from Pi (safe shutdown signal)
- When GPIO 18 goes HIGH, cuts power after Pi halts
- MOSFET gate driver circuit for clean switching

### 2. Ignition Detection (Replaces PC817)
**Circuit:**
- SMD optoisolator: LTV-817S (surface mount PC817 equivalent)
- Input: 12V ignition signal (ACC wire)
- Current limiting resistor: 1kΩ, 1/4W
- Output pull-up resistor: 10kΩ to 3.3V
- Output: GPIO 26 (active LOW when ignition ON)

**Protection:**
- Input diode for reverse voltage protection
- Filtering capacitor (100nF ceramic) for noise immunity
- Schmitt trigger buffer for clean digital signal (optional)

### 3. Shutdown Delay Timer (Replaces DROK)
**Fixed 45-Second Timer Circuit:**

**Option A: 555 Timer (Simple)**
- NE555 or TLC555 (CMOS, lower power)
- RC timing network: R = 4.7MΩ, C = 10µF → ~45 seconds
- Triggered by ignition OFF (falling edge detection)
- Output controls power MOSFET gate

**Option B: ATtiny85 Microcontroller (Flexible)**
- Programmable delay via firmware (default 45 seconds)
- Can add features: voltage monitoring, LED sequences, etc.
- ~$1 component, easy to program via Arduino
- **Recommended** for future expandability

**Functionality:**
1. Ignition ON → Timer reset, power MOSFET enabled
2. Ignition OFF detected → Start 45-second countdown
3. GPIO 26 HIGH triggers shutdown signal to Pi
4. After 45 seconds → Cut power via MOSFET (if Pi hasn't already signaled)
5. Power stays off until ignition ON again

**Safety Feature:**
- If Pi signals shutdown complete (GPIO 18 HIGH) before timer expires, cut power immediately
- Prevents unnecessary drain if shutdown completes early

### 4. CAN Bus Interface
**MCP2515 CAN Controller:**
- **IC:** MCP2515-I/SO (SOIC-18 package)
- **Crystal:** 8MHz (through-hole or SMD)
- **Interface:** SPI to Raspberry Pi (GPIO 8, 9, 10, 11, 25)
- **Logic Level:** 3.3V compatible (no level shifter needed!)

**CAN Transceiver:**
- **IC:** SN65HVD230 (3.3V compatible) or TJA1050 with level shifters
- **Recommended:** SN65HVD230 (eliminates need for logic level conversion)
- **Termination:** 120Ω resistor with jumper (JP1) - user can enable/disable
- **Protection:** ESD protection diodes on CAN-H and CAN-L lines

**Connections:**
- **Screw terminals** (2-position, 5mm pitch) for CAN-H and CAN-L
- Labeled silkscreen markings
- Optional: Additional screw terminal for CAN GND

**SPI Connections to Pi:**
- CS: GPIO 8 (Pin 24)
- MISO: GPIO 9 (Pin 21)
- MOSI: GPIO 10 (Pin 19)
- SCK: GPIO 11 (Pin 23)
- INT: GPIO 25 (Pin 22)

### 5. Fan Control (PWM)
**Fan Header:**
- 2-pin JST-XH connector or standard 0.1" header
- PWM signal: GPIO 17 (Pi Pin 11)
- Power: 5V or 12V selectable via jumper (JP2)
  - 5V mode: Powered from buck converter
  - 12V mode: Powered from automotive 12V input
- N-channel MOSFET driver (2N7002 or similar) for PWM switching
- Flyback diode for inductive load protection
- Max current: 1A (sufficient for most 12V/5V fans)

**PWM Control:**
- Software-controlled via GPIO 17 (same as X735)
- Compatible with existing OpenDash/X735 fan control scripts
- Frequency: 25kHz typical (adjustable in software)

### 6. Status LEDs
**LED Indicators:**
1. **Power LED** (Green) - 5V rail active
2. **Ignition LED** (Yellow) - Ignition signal detected
3. **CAN Activity LED** (Blue) - CAN bus traffic (connected to MCP2515 TX/RX pins)
4. **Shutdown LED** (Red) - Timer active or shutdown in progress

**Implementation:**
- 0603 or 0805 SMD LEDs
- 1kΩ current limiting resistors
- Positioned on board edge for visibility

### 7. Voltage Monitoring (Optional)
**Simple Implementation:**
- Resistive voltage divider (12V → 3.3V range)
- Connected to Pi ADC (if using Pi 5 - needs external ADC otherwise)
- **Easier Alternative:** ATtiny85 has built-in ADC
  - Monitor 12V input via voltage divider
  - Can signal low voltage condition via LED or GPIO

**Not critical for MVP** - can be added in future revision

### 8. Real-Time Clock (RTC)
**What is RTC?**
A Real-Time Clock keeps accurate time even when the Pi is powered off. Useful for:
- Logging timestamps when Pi boots (knows what time it is without internet)
- Scheduling events (e.g., periodic data logging)
- Maintaining system time in car (no GPS or network needed)

**Recommendation:** Skip RTC for V1.0
- Adds complexity (battery holder, I2C chip, configuration)
- OpenDash likely gets time from GPS or phone (Android Auto/CarPlay)
- Can add in future revision if needed

**If you want it later:**
- IC: DS3231 (I2C, highly accurate, built-in temperature compensation)
- Battery: CR1220 coin cell holder
- I2C address: 0x68 (doesn't conflict with common peripherals)

---

## Board Layout Specifications

### Physical Dimensions
- **Size:** 85mm x 56mm (standard Raspberry Pi HAT size)
- **Mounting holes:** 4x 2.75mm holes in HAT standard positions
- **Thickness:** 1.6mm FR4
- **Layers:** 4-layer PCB
  - Layer 1: Top - Component side, signal routing
  - Layer 2: Ground plane (GND)
  - Layer 3: Power plane (5V, 3.3V split)
  - Layer 4: Bottom - Signal routing, high-current 12V traces

### Connector Placement
**Top Edge (away from Pi):**
- 12V input screw terminal (2-position, 5mm pitch)
- CAN-H/CAN-L screw terminals (2-position, 5mm pitch)
- Fan header (2-pin JST-XH or 0.1" header)

**Bottom Edge (Pi side):**
- 40-pin GPIO header (standard 2x20, 0.1" pitch)
- Stacking header option for future expansion

**Component Side:**
- All SMD components on top
- Status LEDs near board edge for visibility
- Jumpers (JP1: CAN termination, JP2: Fan voltage select)

### Trace Width Guidelines
- **12V input traces:** 2mm wide (handle 5A comfortably)
- **5V power traces:** 1.5mm wide (handle 3A+)
- **3.3V traces:** 0.5mm wide
- **Signal traces:** 0.25mm wide (adequate for SPI, low-speed digital)
- **Ground pour:** Flood fill on layer 2, stitched with vias

### Thermal Considerations
- Buck converter IC: Add thermal relief, potentially small heatsink pad
- Power MOSFET: Wide copper pour for heat dissipation
- Keep high-power components away from Pi GPIO header (prevent heat transfer)

---

## Component Selection & BOM

### Major Components

| Component | Part Number | Qty | Unit Cost | Notes |
|-----------|-------------|-----|-----------|-------|
| Buck Converter IC | LM2596S-5.0 | 1 | $2.50 | 3A capable, automotive temp range |
| Inductor (Buck) | 33µH, 5A | 1 | $1.00 | SMD or through-hole |
| P-Channel MOSFET | IRF9540 or Si4435DDY | 1 | $1.50 | High-side power switch |
| MCP2515 CAN Controller | MCP2515-I/SO | 1 | $2.00 | SOIC-18 package |
| CAN Transceiver | SN65HVD230DR | 1 | $1.20 | 3.3V, SOIC-8 |
| Crystal (8MHz) | ABM3-8.000MHZ | 1 | $0.50 | For MCP2515 |
| Optoisolator | LTV-817S | 1 | $0.40 | SMD version of PC817 |
| 555 Timer | NE555D or TLC555CD | 1 | $0.30 | SOIC-8 |
| *OR* ATtiny85 | ATtiny85-20SU | 1 | $1.20 | SOIC-8 (if using micro timer) |
| N-Channel MOSFET (Fan) | 2N7002 | 1 | $0.15 | SOT-23 |
| Voltage Regulator 3.3V | AMS1117-3.3 | 1 | $0.30 | For Pi can provide, but backup |
| TVS Diode (12V clamp) | SMBJ18A | 1 | $0.40 | Overvoltage protection |
| Schottky Diode | 1N5822 | 2 | $0.30 | Reverse polarity, flyback |
| 40-pin GPIO Header | 2x20 female | 1 | $2.00 | Tall stacking header optional |
| Screw Terminals | 5mm, 2-pos | 3 | $0.60 | 12V in, CAN-H/L, Fan |
| LEDs (0805 SMD) | Various colors | 4 | $0.10 | Status indicators |
| Resistors (0805) | Various | ~20 | $0.02 | Pull-ups, current limiting |
| Capacitors (0805/1206) | Various | ~15 | $0.10 | Filter, bulk, decoupling |
| Jumpers | 2-pin 0.1" header | 2 | $0.20 | CAN term, Fan voltage |

**Estimated Total BOM Cost:** $25-35 per board (single quantity, Digi-Key/Mouser)
**PCB Cost:** $4-6 per board (JLCPCB, minimum order 5 boards = $20-30 total)

**Grand Total (5 boards):** ~$150-200 for first batch (you'd have 4 spare boards)

---

## Schematic Design Sections

### Section 1: Power Input & Protection
```
12V_IN ──[Fuse 5A]──┬──[TVS Diode to GND]──┬──[Reverse Polarity Protection]──┬── 12V_PROTECTED
                     │                      │                                  │
                     └──[LED + Resistor]────┘                                  │
                                                                                │
12V_PROTECTED ───[P-FET Controlled by Timer]──[Buck Converter]─── 5V_OUT @ 3A │
                                                                                │
                                                                                └── Fan 12V option
```

### Section 2: Timer & Shutdown Control
```
Ignition Signal (12V) ──[1kΩ]──[LTV-817 LED]──GND
                                      │
                        LTV-817 Transistor ──[10kΩ to 3.3V]── GPIO 26 (Ignition Detect)
                                      │
                                      └──[Trigger to 555/ATtiny Timer]

Timer Output ──[Gate Driver]── P-FET Gate (Power Control)
                                      │
                           Pi GPIO 18 ─┴─ (Safe Shutdown Signal - can override timer)
```

### Section 3: CAN Bus Interface
```
                              ┌──────────────┐
    Pi GPIO 8  (CS)   ───────→│              │
    Pi GPIO 9  (MISO) ←───────│   MCP2515    │
    Pi GPIO 10 (MOSI) ───────→│   CAN Ctrl   │
    Pi GPIO 11 (SCK)  ───────→│              │
    Pi GPIO 25 (INT)  ←───────│              │
                              │   (8MHz Xtal)│
                              └──────┬───────┘
                                     │ TX/RX
                              ┌──────┴───────┐
                              │  SN65HVD230  │
                              │  Transceiver │
                              └──┬─────────┬─┘
                                 │         │
                              CAN-H     CAN-L ──[120Ω Jumper]── CAN-H
                                 │         │
                              Screw     Screw
                              Term      Term
```

### Section 4: Fan Control
```
Pi GPIO 17 (PWM) ──[1kΩ]──[2N7002 Gate]──┬── Fan GND
                                          │
                        [Jumper JP2] ─────┼── 5V or 12V select
                                          │
                        Fan + ────────────┘
                        Fan - ────[Flyback Diode]──GND
```

---

## PCB Design Tools & Resources

### Recommended EDA Software
1. **KiCad** (Free, Open Source) - Recommended
   - Professional-grade schematic capture & PCB layout
   - Extensive component libraries
   - 3D viewer for board visualization
   - [Download](https://www.kicad.org/)

2. **EasyEDA** (Free, Web-based)
   - Integrated with JLCPCB ordering
   - Component libraries from LCSC (cheap parts)
   - Simpler learning curve

3. **Fusion 360 + Eagle** (Free for hobbyists)
   - Professional Autodesk tool
   - Good for 3D integration

### PCB Fabrication Options
**JLCPCB** (Recommended)
- 5 boards: ~$20-30 shipped (2-layer)
- 5 boards: ~$40-50 shipped (4-layer)
- 1-2 week delivery
- Optional SMT assembly (PCBA) service available

**PCBWay**
- Similar pricing to JLCPCB
- Good for 4-layer boards
- Faster shipping options

**OSH Park** (USA)
- Premium quality, Made in USA
- Higher cost (~$100 for 3 boards)
- Beautiful purple solder mask
- Great for prototypes

### Component Sourcing
- **Digi-Key** - Fast shipping, reliable, great for prototyping
- **Mouser** - Similar to Digi-Key
- **LCSC** - Cheaper components, pairs well with JLCPCB assembly
- **Amazon** - Connectors, headers, jumpers (faster delivery)

---

## Development Plan

### Phase 1: Schematic Design (Week 1-2)
- [x] Define requirements (this document)
- [ ] Create KiCad project
- [ ] Draw schematic sections:
  - [ ] Power input & buck converter
  - [ ] Timer circuit (555 or ATtiny85)
  - [ ] Ignition detection (optoisolator)
  - [ ] CAN interface (MCP2515 + SN65HVD230)
  - [ ] Fan control circuit
  - [ ] Status LEDs
  - [ ] GPIO header connection
- [ ] Electrical rules check (ERC)
- [ ] Peer review schematic

### Phase 2: PCB Layout (Week 2-3)
- [ ] Component footprint selection
- [ ] Board outline (HAT dimensions)
- [ ] Component placement:
  - [ ] 40-pin header (bottom, centered)
  - [ ] Power components (top left)
  - [ ] CAN interface (top right)
  - [ ] Screw terminals (top edge)
  - [ ] LEDs (board edge)
- [ ] Trace routing:
  - [ ] High-current power traces first
  - [ ] SPI signals (impedance matching)
  - [ ] CAN differential pair (controlled impedance)
  - [ ] Ground pour
- [ ] Design rule check (DRC)
- [ ] 3D visualization

### Phase 3: Prototype & Testing (Week 4-5)
- [ ] Order PCBs from JLCPCB (5 boards)
- [ ] Order components from Digi-Key/Mouser
- [ ] Hand-solder prototype (or use PCBA service for first build)
- [ ] Bench testing:
  - [ ] Power input protection test (reverse voltage, overvoltage)
  - [ ] Buck converter output (5V @ load)
  - [ ] Timer circuit (45-second delay verification)
  - [ ] Ignition detection (12V → GPIO logic levels)
  - [ ] CAN interface (SocketCAN detection, loopback test)
  - [ ] Fan PWM control
- [ ] Integration testing with Raspberry Pi 5
- [ ] Car installation testing (non-critical first!)

### Phase 4: Refinement (Week 6+)
- [ ] Fix any issues found in testing
- [ ] PCB revision 1.1 if needed
- [ ] Documentation:
  - [ ] Assembly instructions
  - [ ] Installation guide
  - [ ] Software configuration
  - [ ] Troubleshooting guide
- [ ] Final production run

---

## Design Considerations & Trade-offs

### Why 4-Layer PCB?
**Pros:**
- Better power distribution (dedicated power/ground planes)
- Lower noise and EMI (critical for automotive environment)
- Easier routing (more space for traces)
- Better thermal performance

**Cons:**
- Higher cost (~2x vs 2-layer)
- Longer manufacturing time

**Decision:** Use 4-layer for prototype. If cost is critical, can potentially simplify to 2-layer in future revision.

### Timer Circuit: 555 vs ATtiny85?
**555 Timer:**
- ✅ Simple, proven design
- ✅ Fewer components
- ✅ Easier to debug (analog circuit)
- ❌ Fixed delay (requires hardware change to adjust)
- ❌ Limited features

**ATtiny85 Microcontroller:**
- ✅ Programmable delay (easy to change in firmware)
- ✅ Can add features: voltage monitoring, smart shutdown, LED patterns
- ✅ Built-in ADC for voltage sensing
- ✅ Only ~$0.90 more expensive than 555
- ❌ Requires programming (one-time, via Arduino)
- ❌ Slightly more complex schematic

**Recommendation:** Use **ATtiny85** for flexibility. Can program it once and forget it, but opens door for future enhancements.

### CAN Transceiver: TJA1050 vs SN65HVD230?
**TJA1050 (5V):**
- ❌ Requires bidirectional level shifters for SPI (adds complexity)
- ✅ More common in automotive applications
- ✅ Slightly cheaper

**SN65HVD230 (3.3V):**
- ✅ Direct connection to Pi GPIO (no level shifters needed!)
- ✅ Simpler PCB design
- ✅ Lower power consumption
- ❌ Slightly less common
- ❌ $0.20 more expensive

**Recommendation:** Use **SN65HVD230** to eliminate level shifters. Simpler = more reliable.

### Fan Power: 5V or 12V?
**Solution:** Make it jumper-selectable (JP2)
- 5V mode: For 5V fans (quieter, lower power)
- 12V mode: For 12V fans (more powerful, standard automotive)

Most automotive fans are 12V, but having the option is nice.

---

## Software Integration

### OpenDash Configuration
The HAT should be compatible with existing X735 scripts with minimal changes:

**GPIO Assignments:**
```python
# Power management
SHUTDOWN_SIGNAL_PIN = 18  # Pi signals shutdown complete
IGNITION_DETECT_PIN = 26  # Input: LOW = ignition ON

# Fan control
FAN_PWM_PIN = 17  # PWM output for fan speed

# CAN interface
# Uses SPI0: GPIO 8 (CS), 9 (MISO), 10 (MOSI), 11 (SCK)
CAN_INT_PIN = 25  # MCP2515 interrupt
```

**Service Files:**
- Ignition monitor service (monitors GPIO 26)
- Fan control service (PWM on GPIO 17, temperature-based)
- CAN interface (SocketCAN configuration)

Can reuse/adapt existing scripts from your OpenDash `car-power` directory.

### Device Tree Overlays
**In `/boot/firmware/config.txt`:**
```bash
# Enable SPI for MCP2515
dtparam=spi=on

# MCP2515 CAN interface
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25

# Fan PWM (GPIO 17)
dtoverlay=pwm-2chan,pin2=13,func2=4

# Ignition detection (GPIO 26 with pull-up)
gpio=26=ip,pu
```

---

## Next Steps

### Immediate Actions:
1. **Review this specification** - Any changes or additions?
2. **Choose timer approach** - 555 or ATtiny85? (Recommend ATtiny85)
3. **Decide on RTC** - Skip for V1.0? (Recommend skip)
4. **Set up KiCad** - Download and install if not already

### I Can Help With:
- **Schematic design** - Draw complete schematics in KiCad
- **Component selection** - Specific part numbers for BOM
- **PCB layout** - Design the board layout
- **Firmware** - Write ATtiny85 code for timer (if using micro)
- **Testing procedures** - Step-by-step testing checklist
- **Documentation** - Assembly and installation guides

### Your Decision Points:
1. Proceed with custom PCB design?
2. Want me to start on schematics?
3. Any features to add/remove?
4. Timeline - when would you want prototype boards?

This would be a **really cool project** and make your WRX installation super clean! The HAT would be reusable for other car projects too.

---

## References

- [Raspberry Pi HAT Design Guide](https://github.com/raspberrypi/hats)
- [MCP2515 Datasheet](http://ww1.microchip.com/downloads/en/DeviceDoc/MCP2515-Stand-Alone-CAN-Controller-with-SPI-20001801J.pdf)
- [SN65HVD230 Datasheet](https://www.ti.com/lit/ds/symlink/sn65hvd230.pdf)
- [LM2596 Buck Converter Datasheet](https://www.ti.com/lit/ds/symlink/lm2596.pdf)
- [ATtiny85 Datasheet](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf)
- [KiCad Getting Started](https://docs.kicad.org/7.0/en/getting_started_in_kicad/getting_started_in_kicad.html)
