# SubaruDash Pi HAT Stack - GPIO Allocation

This document tracks GPIO pin usage across all three stackable HAT boards.
**All boards share the same 40-pin header** - signals pass through the stack.

## Master GPIO Allocation Table

| GPIO | Pin | Board | Signal | Direction | Description |
|------|-----|-------|--------|-----------|-------------|
| 2 | 3 | DAC/Amp | I2C_SDA | Bidir | PCM5142 I2C data |
| 3 | 5 | DAC/Amp | I2C_SCL | Output | PCM5142 I2C clock |
| 4 | 7 | Power | SHUTDOWN_REQ | Pi→ATtiny | Request graceful shutdown |
| 5 | 29 | - | - | - | **Available** |
| 6 | 31 | - | - | - | **Available** |
| 7 | 26 | - | SPI_CE1 | - | **Available** (alt SPI) |
| 8 | 24 | CAN | SPI_CE0 | Output | MCP2515 chip select |
| 9 | 21 | CAN | SPI_MISO | Input | MCP2515 data out |
| 10 | 19 | CAN | SPI_MOSI | Output | MCP2515 data in |
| 11 | 23 | CAN | SPI_SCLK | Output | MCP2515 clock |
| 12 | 32 | Power | FAN_PWM | Pi→Fan | PWM fan speed control (25kHz) |
| 13 | 33 | Power | FAN_TACH | Fan→Pi | Fan tachometer (2 pulses/rev) |
| 14 | 8 | - | UART_TXD | - | Reserved (serial console) |
| 15 | 10 | - | UART_RXD | - | Reserved (serial console) |
| 16 | 36 | - | - | - | **Available** |
| 17 | 11 | Power | HEARTBEAT_LED | ATtiny→Pi | ATtiny85 heartbeat status |
| 18 | 12 | DAC/Amp | I2S_BCK | Output | PCM5142 bit clock |
| 19 | 35 | DAC/Amp | I2S_LRCK | Output | PCM5142 L/R clock |
| 20 | 38 | - | - | - | **Available** |
| 21 | 40 | DAC/Amp | I2S_DOUT | Output | PCM5142 audio data |
| 22 | 15 | Power | IGN_DETECT | Opto→Pi | Ignition state (isolated) |
| 23 | 16 | - | - | - | **Available** |
| 24 | 18 | - | - | - | **Available** |
| 25 | 22 | CAN | CAN_INT | Input | MCP2515 interrupt |
| 26 | 37 | - | - | - | **Available** |
| 27 | 13 | Power | TIMER_LED | ATtiny→Pi | ATtiny85 timer status |

## Power Pins (shared across all boards)

| Pin | Signal | Notes |
|-----|--------|-------|
| 1 | +3.3V | From Pi (or LDO on Power HAT) |
| 2, 4 | +5V | From TPS54560 on Power HAT |
| 6, 9, 14, 20, 25, 30, 34, 39 | GND | Common ground |
| 17 | +3.3V | From Pi |

## Board-Specific Signals

### Power HAT
| Signal | GPIO | Pin | Description |
|--------|------|-----|-------------|
| SHUTDOWN_REQ | 4 | 7 | Pi requests ATtiny85 to initiate shutdown sequence |
| HEARTBEAT_LED | 17 | 11 | ATtiny85 alive indicator (active = running) |
| IGN_DETECT | 22 | 15 | Ignition on/off state from optocoupler |
| TIMER_LED | 27 | 13 | Shutdown timer countdown indicator |
| FAN_PWM | 12 | 32 | Pi outputs 25kHz PWM for fan speed control |
| FAN_TACH | 13 | 33 | Fan tachometer input (2 pulses per revolution) |

**Internal signals (not on GPIO header):**
- GATE_CTRL: ATtiny85 → MOSFET gate driver
- RESET: Power-on reset for ATtiny85
- XTAL1/XTAL2: ATtiny85 crystal oscillator
- 12V_ACC, 12V_FUSED, 12V_SWITCHED, 12V_IGN: Power rails

### CAN HAT
| Signal | GPIO | Pin | Description |
|--------|------|-----|-------------|
| SPI_MOSI | 10 | 19 | SPI data to MCP2515 |
| SPI_MISO | 9 | 21 | SPI data from MCP2515 |
| SPI_SCLK | 11 | 23 | SPI clock |
| SPI_CE0 | 8 | 24 | MCP2515 chip select |
| CAN_INT | 25 | 22 | MCP2515 interrupt (active low) |

**Internal signals:**
- CANH, CANL: CAN bus differential pair (to J2 OBD-II and J3 screw terminal)
- CAN_TX, CAN_RX: MCP2515 to SN65HVD230 transceiver
- OSC1, OSC2: 16MHz crystal (Y1) for MCP2515 timing
- +3.3V local: From AMS1117-3.3 (U1) regulator, fed by +5V from GPIO header

### DAC/Amp HAT
| Signal | GPIO | Pin | Description |
|--------|------|-----|-------------|
| I2S_BCK | 18 | 12 | Bit clock to PCM5142 |
| I2S_LRCK | 19 | 35 | Left/Right word clock |
| I2S_DOUT | 21 | 40 | Audio data to PCM5142 |
| I2C_SDA | 2 | 3 | PCM5142 configuration data |
| I2C_SCL | 3 | 5 | PCM5142 configuration clock |

**Internal signals:**
- OUTL+/-, OUTR+/-: Differential audio to TPA3116D2 amps
- Speaker outputs: 4× 50W channels

## Available GPIOs for Future Use

| GPIO | Pin | Notes |
|------|-----|-------|
| 5 | 29 | General purpose |
| 6 | 31 | General purpose |
| 7 | 26 | SPI CE1 (if needed for second SPI device) |
| 16 | 36 | General purpose |
| 20 | 38 | General purpose |
| 23 | 16 | General purpose |
| 24 | 18 | General purpose |
| 26 | 37 | General purpose |

## Notes

1. **SPI Bus**: Used by CAN HAT only. CE1 (GPIO7) available if second SPI device needed.
2. **I2C Bus**: Used by DAC/Amp for PCM5142 configuration. Other I2C devices can share.
3. **I2S**: Directly driven by Pi's hardware I2S interface.
4. **UART**: Pins 8/10 (GPIO14/15) reserved for debug console, not used by HATs.
5. **PWM Fan Control**: GPIO12 (hardware PWM) controls fan speed, GPIO13 reads tachometer for RPM monitoring.

## Schematic Verification Status

| Board | ERC Errors | ERC Warnings | Status |
|-------|------------|--------------|--------|
| Power HAT | 0 | 49 | ✅ Verified |
| CAN HAT | 0 | 48 | ✅ Verified |
| DAC/Amp HAT | TBD | TBD | Pending |

### Inter-Board Connectivity Verified:
- **Power**: +5V from TPS54560 (Power HAT) → GPIO pins 2/4 → AMS1117-3.3 (CAN HAT)
- **Ground**: Shared across all boards via GPIO pins 6, 9, 14, 20, 25, 30, 34, 39
- **SPI Bus**: Pi ↔ MCP2515 via GPIO 8-11 (no conflicts)
- **Power Signals**: GPIO 4, 17, 22, 27 for ATtiny85 communication (no conflicts)

## Revision History

| Date | Change |
|------|--------|
| 2026-02-03 | Initial GPIO allocation for 3-board stack |
| 2026-02-03 | DAC/Amp HAT schematic complete: Added 40-pin GPIO header (J7), wired I2S (BCK→Pin12, LRCK→Pin35, DOUT→Pin40), I2C (SDA→Pin3, SCL→Pin5), power distribution, DAC-to-amp differential audio, speaker outputs (J3-J6), control pins |
| 2026-02-03 | CAN HAT schematic complete (0 ERC errors): U1 AMS1117-3.3 with PWR_FLAG for power, Y1 16MHz crystal wired to MCP2515, LED status indicators (R2/R3) grounded, J2 OBD-II connector with CANH/CANL/GND, SPI bus and CAN_INT connected to 40-pin GPIO header |
| 2026-02-03 | Power HAT schematic verified (0 ERC errors): TPS54560 buck converter, ATtiny85 power sequencing, LTV-817S optocoupler for ignition detection, IRLB8721 power MOSFET, all GPIO signals connected to 40-pin header |
| 2026-02-03 | Full verification: Both CAN HAT and Power HAT pass ERC with 0 errors, inter-board power and signal routing confirmed compatible |
| 2026-02-03 | Power HAT fan control: GPIO12 (FAN_PWM) and GPIO13 (FAN_TACH) allocated for 4-pin PWM fan. Pi controls fan based on CPU temperature. |
