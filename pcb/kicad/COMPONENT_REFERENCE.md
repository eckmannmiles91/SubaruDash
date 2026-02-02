# KiCad Component Quick Reference

Use this table when placing components in KiCad schematic.

## Component Placement Checklist

| Ref | Value | KiCad Symbol | Footprint | Section |
|-----|-------|--------------|-----------|---------|
| **POWER INPUT** |
| F1 | 5A PTC | Device:Fuse | Fuse:Fuse_1206_3216Metric | 1 |
| D1 | SMBJ18A | Device:D_TVS | Diode_SMD:D_SMB | 1 |
| D2 | SS34 | Device:D_Schottky | Diode_SMD:D_SMA | 1 |
| Q1 | IRF9540N | Transistor_FET:IRF9540N | Package_TO_SOT_THT:TO-220-3_Vertical | 1 |
| R1 | 1kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 1 |
| R2 | 10kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 1 |
| R3 | 100Ω | Device:R | Resistor_SMD:R_0805_2012Metric | 1 |
| C1 | 100µF 25V | Device:CP | Capacitor_THT:CP_Radial_D6.3mm_P2.50mm | 1 |
| LED1 | Green | Device:LED | LED_SMD:LED_0805_2012Metric | 1 |
| J1 | 12V_IN | Connector:Screw_Terminal_01x02 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal | 1 |
| **BUCK CONVERTER** |
| U1 | LM2596S-5.0 | Regulator_Switching:LM2596S-5 | Package_TO_SOT_SMD:TO-263-5_TabPin3 | 2 |
| L1 | 33µH | Device:L | Inductor_SMD:L_12x12mm_H8mm | 2 |
| D3 | SS54 | Device:D_Schottky | Diode_SMD:D_SMA | 2 |
| C2 | 100µF 25V | Device:CP | Capacitor_THT:CP_Radial_D6.3mm_P2.50mm | 2 |
| C3 | 220µF 16V | Device:CP | Capacitor_THT:CP_Radial_D6.3mm_P2.50mm | 2 |
| R4 | 1.5kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 2 |
| R5 | 1kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 2 |
| **IGNITION DETECTION** |
| U2 | LTV-817S | Isolator:LTV-817S | Package_SO:SOP-4_4.4x2.6mm_P1.27mm | 3 |
| R6 | 1kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 3 |
| R7 | 10kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 3 |
| C4 | 100nF | Device:C | Capacitor_SMD:C_0805_2012Metric | 3 |
| C5 | 10µF | Device:C | Capacitor_SMD:C_0805_2012Metric | 3 |
| **TIMER CIRCUIT** |
| U3 | ATtiny85-20PU | MCU_Microchip_ATtiny:ATtiny85-20PU | Package_DIP:DIP-8_W7.62mm_Socket | 4 |
| C6 | 100nF | Device:C | Capacitor_SMD:C_0805_2012Metric | 4 |
| R8 | 10kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 4 |
| R9 | 470Ω | Device:R | Resistor_SMD:R_0805_2012Metric | 4 |
| R14 | 470Ω | Device:R | Resistor_SMD:R_0805_2012Metric | 4 |
| LED2 | Red | Device:LED | LED_SMD:LED_0805_2012Metric | 4 |
| LED3 | Yellow | Device:LED | LED_SMD:LED_0805_2012Metric | 4 |
| J3 | ISP | Connector_Generic:Conn_02x03_Odd_Even | Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical | 4 |
| **GATE DRIVER** |
| Q2 | 2N7002 | Transistor_FET:2N7002 | Package_TO_SOT_SMD:SOT-23 | 5 |
| R10 | 470Ω | Device:R | Resistor_SMD:R_0805_2012Metric | 5 |
| R11 | 10kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 5 |
| **CAN INTERFACE** |
| U4 | MCP2515-I/SO | Interface_CAN_LIN:MCP2515-I_SO | Package_SO:SOIC-18W_7.5x11.6mm_P1.27mm | 6 |
| U5 | SN65HVD230 | Interface_CAN_LIN:SN65HVD230 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | 6 |
| Y1 | 8MHz | Device:Crystal | Crystal:Crystal_SMD_5032-2Pin_5.0x3.2mm | 6 |
| C7 | 100nF | Device:C | Capacitor_SMD:C_0805_2012Metric | 6 |
| C8 | 100nF | Device:C | Capacitor_SMD:C_0805_2012Metric | 6 |
| C9 | 22pF | Device:C | Capacitor_SMD:C_0805_2012Metric | 6 |
| C10 | 22pF | Device:C | Capacitor_SMD:C_0805_2012Metric | 6 |
| R12 | 10kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 6 |
| R13 | 120Ω | Device:R | Resistor_SMD:R_0805_2012Metric | 6 |
| J4 | CANH | Connector:Screw_Terminal_01x01 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-1_1x01_P5.00mm_Horizontal | 6 |
| J5 | CANL | Connector:Screw_Terminal_01x01 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-1_1x01_P5.00mm_Horizontal | 6 |
| JP1 | Jumper | Connector_Generic:Conn_01x02 | Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical | 6 |
| **FAN CONTROL** |
| Q3 | 2N7002 | Transistor_FET:2N7002 | Package_TO_SOT_SMD:SOT-23 | 7 |
| D7 | 1N4148 | Device:D | Diode_SMD:D_SOD-323 | 7 |
| R15 | 1kΩ | Device:R | Resistor_SMD:R_0805_2012Metric | 7 |
| J6 | FAN | Connector_JST:JST_XH_B2B-XH-A | Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical | 7 |
| JP2 | 5V/12V_SEL | Connector_Generic:Conn_01x03 | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | 7 |
| **3.3V REGULATOR** |
| U6 | AMS1117-3.3 | Regulator_Linear:AMS1117-3.3 | Package_TO_SOT_SMD:SOT-223-3_TabPin2 | 9 |
| C11 | 10µF | Device:C | Capacitor_SMD:C_0805_2012Metric | 9 |
| C12 | 10µF | Device:C | Capacitor_SMD:C_0805_2012Metric | 9 |
| **GPIO HEADER** |
| J2 | Pi_GPIO | Connector_Generic:Conn_02x20_Odd_Even | Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical | 10 |

## Net Labels to Add

Add these global labels (press **L** in schematic):

### Power Nets
- `+12V` - 12V input power
- `+5V` - 5V regulated output
- `+3.3V` - 3.3V regulated output
- `GND` - Common ground

### Signal Nets
- `12V_IN` - Raw 12V from screw terminal
- `12V_PROTECTED` - 12V after fuse and TVS
- `12V_SWITCHED` - 12V after P-FET (controlled)
- `5V_OUT` - Buck converter output
- `12V_IGN` - Ignition input (from car ACC wire)
- `IGNITION_DETECT` - Optoisolator output to ATtiny85
- `POWER_CTRL` - ATtiny85 output to gate driver
- `SHUTDOWN_SIG` - Pi GPIO to ATtiny85 (shutdown request)
- `CAN_INT` - MCP2515 interrupt to Pi
- `SPI_MOSI` - Pi to MCP2515
- `SPI_MISO` - MCP2515 to Pi
- `SPI_SCLK` - Pi to MCP2515
- `SPI_CE0` - Pi to MCP2515 (chip select)
- `CAN_TXD` - MCP2515 to SN65HVD230
- `CAN_RXD` - SN65HVD230 to MCP2515
- `CANH` - CAN bus high
- `CANL` - CAN bus low
- `FAN_PWM` - Pi GPIO 17 to fan driver

## GPIO Pin Mapping

Connect these Pi GPIO header pins to the following nets:

| Pin # | Name | Net Label | Direction | Notes |
|-------|------|-----------|-----------|-------|
| 1 | 3.3V | +3.3V | Power | From Pi (or use our regulator) |
| 2 | 5V | +5V | Power | **TO Pi** (from our buck converter) |
| 4 | 5V | +5V | Power | **TO Pi** (parallel) |
| 6 | GND | GND | Ground | Common ground |
| 9 | GND | GND | Ground | Common ground |
| 12 | GPIO 18 | X735_SHUTDOWN | Input | (Reserved for X735 compatibility) |
| 17 | GPIO 17 | FAN_PWM | Output | PWM fan control |
| 19 | GPIO 10 | SPI_MOSI | Output | To MCP2515 |
| 21 | GPIO 9 | SPI_MISO | Input | From MCP2515 |
| 22 | GPIO 25 | CAN_INT | Input | MCP2515 interrupt |
| 23 | GPIO 11 | SPI_SCLK | Output | To MCP2515 |
| 24 | GPIO 8 | SPI_CE0 | Output | MCP2515 chip select |
| 37 | GPIO 26 | IGNITION_DETECT | Input | From optoisolator |

**Note:** All other pins can be left unconnected or connected to GND for unused inputs.

## Power Symbol Usage

Place these power symbols in schematic (press **P**, type name):

- `GND` - Use for all ground connections
- `+12V` - Use for 12V power rail
- `+5V` - Use for 5V power rail
- `+3.3V` - Use for 3.3V power rail

**Tip:** Place one instance near each IC and copy (Ctrl+C, Ctrl+V) as needed.

## Common Footprint Alternatives

If exact footprints aren't found, use these alternatives:

| Component | Preferred | Alternative |
|-----------|-----------|-------------|
| 0805 Resistor | Resistor_SMD:R_0805_2012Metric | Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder |
| 0805 Capacitor | Capacitor_SMD:C_0805_2012Metric | Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder |
| DIP-8 Socket | Package_DIP:DIP-8_W7.62mm_Socket | Package_DIP:DIP-8_W7.62mm_LongPads |
| Screw Terminal | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2 | TerminalBlock:TerminalBlock_bornier-2_P5.08mm |

**HandSolder footprints** have larger pads - easier for hand soldering!

## Tips

1. **Start with power section first** - ensures all components can be powered
2. **Use net labels liberally** - makes wiring cleaner than direct wires
3. **Group related components** - place ICs with their bypass caps and resistors nearby
4. **Run ERC frequently** - catch errors early
5. **Save often** - KiCad autosaves, but manual saves are safer

## ERC (Electrical Rules Check) Common Issues

Before moving to PCB:

- ✓ All power pins connected to power nets
- ✓ All input pins have drivers (connected to outputs)
- ✓ No floating nets (wires not connected to pins)
- ✓ All ICs have bypass capacitors
- ✓ Crystal has load capacitors

Run **Inspect → Electrical Rules Checker** to verify.
