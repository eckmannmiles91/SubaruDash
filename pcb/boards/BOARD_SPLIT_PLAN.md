# SubaruDash 3-Board Design

## Overview

The original combined design has been split into 3 focused boards:

1. **Power HAT** - Vehicle power management (Better X735)
2. **CAN HAT** - CAN bus interface for OBD-II
3. **DAC/Amp Module** - Audio output with 4x50W amplification

---

## Board 1: Power HAT (power-hat/)

### Purpose
Automotive-grade power management with safe shutdown for Raspberry Pi.

### Components from Original Schematic

| Ref | Component | Function |
|-----|-----------|----------|
| U1 | TPS54560BDDA | 12V → 5V @ 5A buck converter |
| U2 | LTV-817S | Optocoupler (ignition isolation) |
| U3 | ATtiny85 | Shutdown timing controller |
| Q1 | IRLB8721PBF | Main power MOSFET |
| Q2 | 2N7002 | Gate control MOSFET |
| Q3 | 2N7002 | Gate control MOSFET |
| F1 | Fuse holder | 5A automotive fuse |
| D1 | SS34 | Catch diode |
| D2 | SMBJ18A | TVS protection |
| L1 | 22µH | Buck inductor |
| J1 | Molex 8-pin | Vehicle harness input |
| J2 | 2x20 header | Pi GPIO connection |
| J6 | 2-pin | Fan PWM output |
| JP1 | Jumper | Configuration |

### Capacitors
- C1, C_BOOT1: Bootstrap
- C2: Output bulk
- C5: Soft-start
- C6, C7, C_COMP1: Compensation
- C8: Feedforward
- C10, C20: Input bulk

### Resistors
- R1, R6: Voltage dividers
- R4, R5: Feedback (1%)
- R10, R_COMP1: Compensation
- R_RT1: Timing
- R19, R20, R21: Gate drive

### Pi GPIO Signals
- 5V power output
- SHUTDOWN_REQ (to Pi)
- IGN_DETECT (to Pi)
- FAN_PWM (from Pi)
- GATE_CTRL (from Pi)

---

## Board 2: CAN HAT (can-hat/)

### Purpose
CAN bus interface for reading OBD-II data from vehicle.

### Components from Original Schematic

| Ref | Component | Function |
|-----|-----------|----------|
| U4 | MCP2515 | SPI CAN controller |
| U5 | SN65HVD230 | CAN transceiver |
| U6 | AMS1117-3.3 | 3.3V LDO regulator |
| Y1 | 16MHz crystal | MCP2515 clock |
| L2 | Ferrite | CANH filter |
| L3 | Ferrite | CANL filter |
| J2 | 2x20 header | Pi GPIO connection |
| J3 | OBD-II/screw | CAN bus connector |
| J4 | 2-pin terminal | CAN termination |
| LED1-3 | LEDs | Status indicators |

### Capacitors
- C3, C4: LDO in/out
- C11, C12: Crystal load
- C13-C17: Decoupling

### Resistors
- R11-R17: LED current limiting, pull-ups
- R18: CAN termination (120Ω)

### Pi GPIO Signals
- SPI: MOSI, MISO, SCLK, CE0
- CAN_INT (interrupt to Pi)
- 5V, 3.3V, GND

---

## Board 3: DAC/Amp Module (dac-amp/)

### Purpose
High-quality 4-channel audio output with 50W per channel amplification.

### NEW Components (not in original schematic)

| Ref | Component | Function |
|-----|-----------|----------|
| U1 | PCM5142 | Quad I2S DAC |
| U2 | TPA3116D2 | Class D amp (FL/FR) |
| U3 | TPA3116D2 | Class D amp (RL/RR) |
| J1 | 6-pin JST | I2S input from Pi |
| J2 | 2-pin | 12V power input |
| J3 | ISO 10487-B | Speaker outputs |

### Pi Signals (via cable)
- I2S: BCK, LRCK, DIN
- GND

### Power
- 12V direct from vehicle (for amps)
- 3.3V/5V derived locally (for DAC)

---

## Inter-Board Connections

```
┌─────────────────┐
│   Vehicle 12V   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     5V      ┌─────────────────┐
│  Board 1:       │────────────→│  Raspberry Pi   │
│  Power HAT      │◄───GPIO────→│                 │
└─────────────────┘             └────────┬────────┘
                                    SPI  │  I2S
                                         │
              ┌──────────────────────────┼──────────────────┐
              │                          │                  │
              ▼                          ▼                  ▼
┌─────────────────┐             ┌─────────────────┐  ┌─────────────┐
│  Board 2:       │             │  Board 3:       │  │  Vehicle    │
│  CAN HAT        │             │  DAC/Amp        │  │  12V        │
└────────┬────────┘             └────────┬────────┘  └──────┬──────┘
         │                               │                  │
         ▼                               │                  │
┌─────────────────┐                      │                  │
│   OBD-II Port   │                      ▼                  │
└─────────────────┘             ┌─────────────────┐         │
                                │   4 Speakers    │◄────────┘
                                └─────────────────┘
```

---

## File Structure

```
pcb/boards/
├── BOARD_SPLIT_PLAN.md (this file)
├── power-hat/
│   ├── power-hat.kicad_pro
│   ├── power-hat.kicad_sch
│   └── power-hat.kicad_pcb
├── can-hat/
│   ├── can-hat.kicad_pro
│   ├── can-hat.kicad_sch
│   └── can-hat.kicad_pcb
└── dac-amp/
    ├── dac-amp.kicad_pro
    ├── dac-amp.kicad_sch
    └── dac-amp.kicad_pcb
```

---

## Development Priority

1. **CAN HAT** (simplest, test CAN functionality first)
2. **Power HAT** (critical path, complex layout)
3. **DAC/Amp Module** (can use off-the-shelf TPA3116 board initially)

---

## Notes

- Each board has its own Pi header (J2) for stacking or separate connection
- Power HAT and CAN HAT can stack on Pi
- DAC/Amp connects via I2S cable (not a HAT)
- All boards sized for easy manufacturing (JLCPCB, PCBWay, etc.)
