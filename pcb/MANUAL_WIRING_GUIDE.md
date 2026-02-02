# Manual Wiring Guide
## WRX Power & CAN HAT - Final Connections

**File:** wrx-power-can-hat-MANUAL.kicad_sch
**Date:** 2026-02-02

---

## How to Add Labels in KiCad

### Method 1: Using the Label Tool (Recommended)
1. Press **L** key (or click the "Add Label" tool)
2. Type the net name (e.g., "+3.3V", "GND", "SPI_MOSI")
3. Click to place the label
4. Move cursor to the component pin
5. Click directly on the pin (should snap/highlight)
6. Press **Esc** when done

### Method 2: Using Global Labels
1. Press **Ctrl+L** (or Tools → Place → Global Label)
2. Type the net name
3. Place directly on the pin

---

## Connections Needed (27 total)

### U4 - MCP2515 CAN Controller (12 connections)

| Pin # | Pin Name | Net Name | Coordinates (mils) | Notes |
|-------|----------|----------|-------------------|-------|
| 14 | SI | SPI_MOSI | 16900, 4400 | SPI data in |
| 15 | SO | SPI_MISO | 16900, 4500 | SPI data out |
| 16 | ~CS | SPI_CE0 | 16900, 4600 | SPI chip select |
| 13 | SCK | SPI_SCLK | 16900, 4700 | SPI clock |
| 7 | OSC2 | XTAL2 | 16900, 5200 | Crystal pin 2 |
| 8 | OSC1 | XTAL1 | 16900, 5300 | Crystal pin 1 |
| 18 | VDD | +3.3V | 17500, 4200 | Power (3.3V) |
| 9 | VSS | GND | 17500, 5800 | Ground |
| 2 | RXCAN | CAN_RX | 18100, 4400 | From transceiver |
| 1 | TXCAN | CAN_TX | 18100, 4500 | To transceiver |
| 12 | ~INT | CAN_INT | 18100, 5000 | Interrupt to Pi |
| 17 | ~RESET | +3.3V | 18100, 5600 | Pull-up resistor |

**Optional (can leave unconnected):**
- Pin 3 (CLKOUT/SOF) - can be no-connect
- Pins 11, 10 (RX0BF, RX1BF) - buffer full outputs, not used
- Pins 4, 5, 6 (TX0RTS, TX1RTS, TX2RTS) - can tie to +3.3V or leave open

---

### U3 - ATtiny85 Microcontroller (8 connections)

| Pin # | Pin Name | Net Name | Coordinates (mils) | Notes |
|-------|----------|----------|-------------------|-------|
| 8 | VCC | +3.3V | 10000, 19400 | Power (3.3V) |
| 5 | AREF/PB0 | HEARTBEAT_LED | 10600, 19700 | Heartbeat LED output |
| 6 | PB1 | TIMER_LED | 10600, 19800 | Timer LED output |
| 7 | PB2 | IGN_DETECT | 10600, 19900 | Ignition input |
| 2 | XTAL1/PB3 | GATE_CTRL | 10600, 20000 | MOSFET gate control |
| 3 | XTAL2/PB4 | SHUTDOWN_REQ | 10600, 20100 | Shutdown signal to Pi |
| 1 | ~RESET/PB5 | RESET | 10600, 20200 | Reset (ISP programming) |
| 4 | GND | GND | 10000, 20600 | Ground |

---

### U5 - SN65HVD230 CAN Transceiver (7 connections)

| Pin # | Pin Name | Net Name | Coordinates (mils) | Notes |
|-------|----------|----------|-------------------|-------|
| 1 | D | CAN_TX | 22100, 27400 | RX from MCP2515 |
| 4 | R | CAN_RX | 22100, 27500 | TX to MCP2515 |
| 3 | VCC | +3.3V | 22500, 27200 | Power (3.3V) |
| 2 | GND | GND | 22500, 27900 | Ground |
| 7 | CANH | CANH | 22900, 27500 | CAN High |
| 6 | CANL | CANL | 22900, 27600 | CAN Low |
| 8 | Rs | GND | 22100, 27700 | Slope control (GND = max speed) |

**Optional:**
- Pin 5 (Vref) - can leave unconnected or add decoupling cap

---

## Step-by-Step Wiring Process

### Start with Power Connections (Easiest)

1. **Add all +3.3V labels:**
   - Press **L**
   - Type: `+3.3V`
   - Place on: U4 Pin 18, U4 Pin 17, U3 Pin 8, U5 Pin 3

2. **Add all GND labels:**
   - Press **L**
   - Type: `GND`
   - Place on: U4 Pin 9, U3 Pin 4, U5 Pin 2, U5 Pin 8

3. **Save:** Press **Ctrl+S**

### Add SPI Connections (U4 to Raspberry Pi)

4. **SPI_MOSI** → U4 Pin 14 (16900, 4400)
5. **SPI_MISO** → U4 Pin 15 (16900, 4500)
6. **SPI_CE0** → U4 Pin 16 (16900, 4600)
7. **SPI_SCLK** → U4 Pin 13 (16900, 4700)
8. **Save:** Press **Ctrl+S**

### Add CAN Connections (Between U4 and U5)

9. **CAN_TX** → U4 Pin 1 (18100, 4500) AND U5 Pin 1 (22100, 27400)
10. **CAN_RX** → U4 Pin 2 (18100, 4400) AND U5 Pin 4 (22100, 27500)
11. **CAN_INT** → U4 Pin 12 (18100, 5000)
12. **CANH** → U5 Pin 7 (22900, 27500)
13. **CANL** → U5 Pin 6 (22900, 27600)
14. **Save:** Press **Ctrl+S**

### Add Crystal Connections (U4)

15. **XTAL1** → U4 Pin 8 (16900, 5300)
16. **XTAL2** → U4 Pin 7 (16900, 5200)
17. **Save:** Press **Ctrl+S**

### Add ATtiny85 Connections (U3)

18. **HEARTBEAT_LED** → U3 Pin 5 (10600, 19700)
19. **TIMER_LED** → U3 Pin 6 (10600, 19800)
20. **IGN_DETECT** → U3 Pin 7 (10600, 19900)
21. **GATE_CTRL** → U3 Pin 2 (10600, 20000)
22. **SHUTDOWN_REQ** → U3 Pin 3 (10600, 20100)
23. **RESET** → U3 Pin 1 (10600, 20200)
24. **Save:** Press **Ctrl+S**

### Final Steps

25. **Delete #PWR05:**
    - Find #PWR05 in the schematic (at 15000, 10000 mils)
    - Click on it
    - Press **Delete** key
    - Confirm deletion

26. **Final Save:** Press **Ctrl+S**

27. **Run ERC:**
    - Inspect → Electrical Rules Checker
    - Run ERC
    - Save report as **ERC_FINAL.rpt**

---

## Tips

- **Zoom in** when placing labels (scroll wheel or View → Zoom In)
- Labels should **snap to pins** when placed correctly (pin will highlight)
- If a label won't snap, try placing it slightly offset and then dragging it
- **Save frequently** (Ctrl+S) to avoid losing work
- You can press **M** to move a misplaced label
- Press **Esc** to cancel current operation

---

## Expected Final Result

After all connections:
- **Target:** Less than 10 errors
- Most remaining errors will be:
  - Optional pins (RX0BF, RX1BF, TX0RTS, etc.)
  - Dangling labels for things connected to Raspberry Pi GPIO
  - These are acceptable and expected!

---

## Verification Checklist

After wiring, verify:
- [ ] All power pins (+3.3V, GND) are connected
- [ ] All SPI pins are labeled
- [ ] CAN_TX and CAN_RX connect U4 to U5
- [ ] CANH and CANL are labeled on U5
- [ ] Crystal pins (XTAL1, XTAL2) are labeled on U4
- [ ] All ATtiny85 pins are labeled
- [ ] #PWR05 is deleted
- [ ] ERC shows significant error reduction

---

**Good luck! Take your time and work through each connection systematically.**
