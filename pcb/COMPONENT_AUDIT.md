# Component Audit - WRX Power & CAN HAT

## Design Requirements vs Actual Schematic

### Power Supply Components

| Ref | **SHOULD BE** | **ACTUALLY IS** | Status |
|-----|---------------|-----------------|--------|
| U1  | LM2596S-5.0 (12V→5V buck converter) | LM2596S-5.0 | ✅ CORRECT |
| U6  | AMS1117-3.3 (5V→3.3V regulator) | AMS1117-3.3 | ✅ CORRECT |

### Control & Logic Components

| Ref | **SHOULD BE** | **ACTUALLY IS** | Status |
|-----|---------------|-----------------|--------|
| U2  | **LTV-817S optoisolator** (ignition detection) | ~~AMS1117-3.3~~ → **LTV-817S** | ✅ FIXED |
| U3  | **ATtiny85 microcontroller** (8-pin, shutdown timer, LED control) | **SN65HVD230 CAN transceiver** | ❌ WRONG! |
| U4  | **MCP2515 CAN controller** (11-pin SPI interface) | LTV-817S optoisolator | ❌ WRONG! |
| U5  | **SN65HVD230 CAN transceiver** (6-pin) | PCM5142 Audio DAC | ❌ WRONG! |
| U7  | **PCM5102/PCM5142 Audio DAC** (I2S interface) | ??? | ❓ UNKNOWN |

### Correct Component Pinouts

#### U3 Should Be: ATtiny85 (8-pin microcontroller)
```
Pin 1: RESET
Pin 2: TIMER_LED (output to LED)
Pin 3: HEARTBEAT_LED (output to LED)
Pin 4: GND
Pin 5: IGN_DETECT (input from U2 optoisolator)
Pin 6: SHUTDOWN_REQ (output to Pi GPIO)
Pin 7: GATE_CTRL (output to power MOSFET gate)
Pin 8: +3.3V (VCC)
```

#### U4 Should Be: MCP2515 (CAN controller, 18-pin DIP or 20-pin SOIC)
```
Pin 1: SPI_CE0 (chip select)
Pin 2: SPI_SCLK (SPI clock)
Pin 3: SPI_MISO (SPI data in)
Pin 4: SPI_MOSI (SPI data out)
Pin 5: GND
Pin 6: CAN_INT (interrupt output)
Pin 7: XTAL2 (crystal pin 2)
Pin 8: XTAL1 (crystal pin 1)
Pin 9: +3.3V (VDD)
Pin 10: CAN_RX (from CAN transceiver)
Pin 11: CAN_TX (to CAN transceiver)
```

#### U5 Should Be: SN65HVD230 (CAN transceiver, 8-pin SOIC)
```
Pin 1: CAN_TX (input from MCP2515)
Pin 2: GND
Pin 3: +3.3V (VCC)
Pin 4: CAN_RX (output to MCP2515)
Pin 5: CANL (CAN bus low)
Pin 6: CANH (CAN bus high)
Pin 7: NC (not connected)
Pin 8: Rs (slope resistor)
```

## Summary

**Total components checked: 7**
- ✅ Correct: 3 (U1, U6, U2-fixed)
- ❌ Wrong: 3 (U3, U4, U5)
- ❓ Unknown: 1 (U7)

## Action Required

The schematic has **major component mismatches**. Components are completely wrong:

1. **U3** has a CAN transceiver but needs a microcontroller
2. **U4** has an optoisolator but needs a CAN controller
3. **U5** has an audio DAC but needs a CAN transceiver

**Recommendation:** Replace all three components (U3, U4, U5) with correct parts before attempting to wire or fix ERC errors.

## Next Steps

1. Replace U3: SN65HVD230 → ATtiny85 (or ATtiny84/85 equivalent)
2. Replace U4: LTV-817S → MCP2515
3. Replace U5: PCM5142 → SN65HVD230
4. Find/verify U7 (should be audio DAC)
5. Update all pin connections for these components
6. Run ERC to verify

---
Generated: 2026-02-02
