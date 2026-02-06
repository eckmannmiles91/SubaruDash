# Raspberry Pi GPIO Connection Guide

## J1 Connector Pinout (8-pin connector)

### Critical Connections for CAN Interface

Since J1 is only an 8-pin connector, we'll wire the essential signals for CAN bus operation:

| J1 Pin | Signal Name | Direction | Description |
|--------|-------------|-----------|-------------|
| 1 | +3.3V | Power | 3.3V power supply from Pi |
| 2 | GND | Power | Ground return |
| 3 | SPI_MOSI | Input | SPI Master Out, Slave In (Pi → MCP2515) |
| 4 | SPI_MISO | Output | SPI Master In, Slave Out (MCP2515 → Pi) |
| 5 | SPI_SCLK | Input | SPI Clock (Pi → MCP2515) |
| 6 | SPI_CE0 | Input | SPI Chip Enable (Pi → MCP2515) |
| 7 | CAN_INT | Output | CAN Interrupt (MCP2515 → Pi) |
| 8 | SHUTDOWN_REQ | Output | Shutdown request (ATtiny85 → Pi) |

---

## Raspberry Pi GPIO Pin Mapping

When this HAT plugs into a Raspberry Pi 40-pin header:

### Power Connections:
- **Pin 1 (3.3V)** or **Pin 17 (3.3V)** → J1 Pin 1 (+3.3V)
- **Pin 6 (GND)** or any GND pin → J1 Pin 2 (GND)

### SPI Bus (Hardware SPI0):
- **Pin 19 (GPIO 10, MOSI)** → J1 Pin 3 (SPI_MOSI)
- **Pin 21 (GPIO 9, MISO)** → J1 Pin 4 (SPI_MISO)
- **Pin 23 (GPIO 11, SCLK)** → J1 Pin 5 (SPI_SCLK)
- **Pin 24 (GPIO 8, CE0)** → J1 Pin 6 (SPI_CE0)

### Control Signals:
- **Pin 22 (GPIO 25)** → J1 Pin 7 (CAN_INT)
- **Pin 18 (GPIO 24)** → J1 Pin 8 (SHUTDOWN_REQ)

---

## Additional Signals (Not connected via J1)

These signals from the CAN components don't fit in the 8-pin J1 connector.
Options:
1. Add a second connector (J2) for these signals
2. Wire them directly if HAT design allows
3. Leave unconnected if not needed

### ATtiny85 Control Signals:
- **GATE_CTRL** - MOSFET gate control (could go to GPIO 23, Pin 16)
- **IGN_DETECT** - Ignition detection input (needs 12V divider)
- **HEARTBEAT_LED** - Status LED (add LED + resistor)
- **TIMER_LED** - Timer LED (add LED + resistor)
- **RESET** - Reset pin for ISP programming

---

## Wiring Steps

1. Ensure J1 is properly defined with 8 pins
2. Label each J1 pin with the appropriate signal name
3. These labels will connect to the global labels from U3, U4, U5
4. Add power connections (+3.3V, GND)

---

## Software Configuration (Raspberry Pi)

After hardware is complete, enable SPI on the Raspberry Pi:

```bash
# Enable SPI interface
sudo raspi-config
# Navigate to: Interface Options → SPI → Enable

# Load MCP2515 kernel module
sudo modprobe can
sudo modprobe can-raw
sudo modprobe mcp251x

# Configure CAN interface
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up
```

---

**Note:** This assumes a standard Raspberry Pi HAT design where J1 connects to the Pi's GPIO header.
