#!/usr/bin/env python3
"""
CAN HAT Fix Script - Version 4.

Uses 2 decimal place precision matching KiCad's internal format.
Calculates positions from symbol positions + library offsets.

Key coordinates (from schematic):
- J1 (GPIO header): symbol at (200, 150) mm
  - Odd pins (1,3,5...39): x = 194.92 mm (200 - 5.08)
  - Even pins (2,4,6...40): x = 207.62 mm (200 + 7.62)
  - Pin 1 y = 127.15 mm, each row +2.54 mm

- U2 (MCP2515): symbol at (444.5, 127) mm
- U3 (SN65HVD230): symbol at (571.5, 698.5) mm
- Y1 (Crystal): symbol at (190.5, 571.5) mm
- U1 (AMS1117): around (393.7, 431.8) mm
"""

import uuid
import re
from pathlib import Path


def generate_uuid():
    """Generate a KiCad-style UUID."""
    return str(uuid.uuid4())


def fmt(val):
    """Format coordinate to 2 decimal places, trimming unnecessary zeros."""
    result = f"{val:.2f}"
    # Remove trailing zeros after decimal point
    if '.' in result:
        result = result.rstrip('0').rstrip('.')
    return result


def create_wire(x1, y1, x2, y2):
    """Create a KiCad wire S-expression."""
    uid = generate_uuid()
    return f'''\t(wire
\t\t(pts
\t\t\t(xy {fmt(x1)} {fmt(y1)}) (xy {fmt(x2)} {fmt(y2)})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{uid}")
\t)'''


def create_global_label(name, x, y, direction=180):
    """Create a KiCad global label S-expression."""
    uid = generate_uuid()
    # direction: 0=right, 90=up, 180=left, 270=down
    justify = "right" if direction == 180 else "left"
    shape = "input" if direction == 180 else "output"
    return f'''\t(global_label "{name}"
\t\t(shape {shape})
\t\t(at {fmt(x)} {fmt(y)} {direction})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {justify})
\t\t)
\t\t(uuid "{uid}")
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
\t\t\t(at {fmt(x)} {fmt(y)} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t)'''


def create_label(name, x, y, direction=180):
    """Create a KiCad local label S-expression."""
    uid = generate_uuid()
    return f'''\t(label "{name}"
\t\t(at {fmt(x)} {fmt(y)} {direction})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify left)
\t\t)
\t\t(uuid "{uid}")
\t)'''


def create_no_connect(x, y):
    """Create a KiCad no-connect flag."""
    uid = generate_uuid()
    return f'''\t(no_connect
\t\t(at {fmt(x)} {fmt(y)})
\t\t(uuid "{uid}")
\t)'''


def create_pwr_flag(x, y):
    """Create a PWR_FLAG symbol."""
    uid = generate_uuid()
    pin_uid = generate_uuid()
    return f'''\t(symbol
\t\t(lib_id "power:PWR_FLAG")
\t\t(at {fmt(x)} {fmt(y)} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid}")
\t\t(property "Reference" "#FLG0{generate_uuid()[:2]}"
\t\t\t(at {fmt(x)} {fmt(y - 2.54)} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Value" "PWR_FLAG"
\t\t\t(at {fmt(x)} {fmt(y - 5.08)} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {fmt(x)} {fmt(y)} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {fmt(x)} {fmt(y)} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {fmt(x)} {fmt(y)} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{pin_uid}")
\t\t)
\t)'''


def read_schematic(filepath):
    """Read the schematic file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_schematic(filepath, content):
    """Write the schematic file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {filepath}")


def find_insert_position(content):
    """Find position to insert new elements (before sheet_instances)."""
    match = re.search(r'\n\t\(sheet_instances', content)
    if match:
        return match.start()
    return len(content) - 2


# =============================================================================
# J1 GPIO Header Pin Positions
# Symbol at (200, 150), Conn_02x20_Odd_Even
# =============================================================================
def get_j1_pin_pos(pin_num):
    """
    Get J1 pin position in mm.
    Odd pins (1,3,5...39) on left, Even pins (2,4,6...40) on right.
    """
    symbol_x = 200.0
    symbol_y = 150.0

    # Library offsets for Conn_02x20_Odd_Even
    odd_x_offset = -5.08   # Left side
    even_x_offset = 7.62   # Right side
    y_base_offset = -22.85 # Pin 1/2 row offset from symbol center
    row_pitch = 2.54       # Vertical spacing

    if pin_num % 2 == 1:  # Odd pin (left side)
        x = symbol_x + odd_x_offset  # 194.92
        row = (pin_num - 1) // 2
    else:  # Even pin (right side)
        x = symbol_x + even_x_offset  # 207.62
        row = (pin_num - 2) // 2

    y = symbol_y + y_base_offset + row * row_pitch

    return (round(x, 2), round(y, 2))


# Raspberry Pi GPIO pin assignments
GPIO_ASSIGNMENTS = {
    # Power pins
    1: '+3.3V',
    2: '+5V',
    4: '+5V',
    17: '+3.3V',
    # Ground pins
    6: 'GND',
    9: 'GND',
    14: 'GND',
    20: 'GND',
    25: 'GND',
    30: 'GND',
    34: 'GND',
    39: 'GND',
    # SPI pins
    19: 'SPI_MOSI',  # GPIO10
    21: 'SPI_MISO',  # GPIO9
    23: 'SPI_SCLK',  # GPIO11
    24: 'SPI_CE0',   # GPIO8
    # CAN interrupt
    22: 'CAN_INT',   # GPIO25
}


def fix_can_hat():
    """Main function to fix CAN HAT schematic."""
    script_dir = Path(__file__).parent
    can_hat_sch = script_dir / "can-hat" / "can-hat.kicad_sch"

    if not can_hat_sch.exists():
        print(f"Error: {can_hat_sch} not found")
        return

    print("=" * 70)
    print("CAN HAT Fix Script - Version 4 (2 Decimal Precision)")
    print("=" * 70)

    content = read_schematic(can_hat_sch)
    print(f"Read {len(content)} bytes")

    new_elements = []

    # =========================================================================
    # Section 1: GPIO Header (J1) Connections
    # =========================================================================
    print("\n--- Section 1: GPIO Header (J1) ---")

    for pin in range(1, 41):
        pin_x, pin_y = get_j1_pin_pos(pin)

        if pin in GPIO_ASSIGNMENTS:
            signal = GPIO_ASSIGNMENTS[pin]

            # Wire extends from pin: left for odd pins, right for even
            if pin % 2 == 1:  # Odd pin - wire goes left
                wire_end_x = pin_x - 5.08
                label_x = wire_end_x
                label_dir = 0  # Label points right (toward pin)
            else:  # Even pin - wire goes right
                wire_end_x = pin_x + 5.08
                label_x = wire_end_x
                label_dir = 180  # Label points left (toward pin)

            # Create wire from pin to label position
            wire = create_wire(pin_x, pin_y, wire_end_x, pin_y)
            new_elements.append(wire)

            # Create global label at wire end
            label = create_global_label(signal, label_x, pin_y, label_dir)
            new_elements.append(label)

            print(f"  Pin {pin}: {signal}")
        else:
            # Unused pin - add no_connect directly at pin position
            nc = create_no_connect(pin_x, pin_y)
            new_elements.append(nc)

    unused_count = 40 - len(GPIO_ASSIGNMENTS)
    print(f"  {unused_count} pins marked no-connect")

    # =========================================================================
    # Section 2: MCP2515 (U2) Connections
    # Use local labels at pins, they'll connect via global labels from GPIO
    # =========================================================================
    print("\n--- Section 2: MCP2515 (U2) ---")

    # U2 positions from ERC (in mils, convert to mm)
    # Left side pins at x=16900 mils = 429.26 mm
    # Right side pins at x=18100 mils = 459.74 mm
    u2_left_x = 429.26
    u2_right_x = 459.74

    # U2 pin Y positions (from ERC report, convert mils to mm)
    u2_pins = {
        # Left side (active low signals, directly from schematic)
        'SI': (u2_left_x, 111.76),       # Pin 14 - SPI data in
        'SO': (u2_left_x, 114.30),       # Pin 15 - SPI data out
        'CS': (u2_left_x, 116.84),       # Pin 16 - Chip select
        'SCK': (u2_left_x, 119.38),      # Pin 13 - SPI clock
        'INT': (u2_right_x, 127.00),     # Pin 12 - Interrupt out
        'TXCAN': (u2_right_x, 111.76),   # Pin 1 - CAN TX
        'RXCAN': (u2_right_x, 114.30),   # Pin 2 - CAN RX
        'OSC1': (u2_left_x, 149.86),     # Pin 8 - Crystal input
        'OSC2': (u2_left_x, 147.32),     # Pin 7 - Crystal output
        'TX0RTS': (u2_left_x, 121.92),   # Pin 4
        'TX1RTS': (u2_left_x, 124.46),   # Pin 5
        'TX2RTS': (u2_left_x, 127.00),   # Pin 6
        'RX0BF': (u2_right_x, 124.46),   # Pin 10
        'RX1BF': (u2_right_x, 121.92),   # Pin 11
        'CLKOUT': (u2_left_x, 137.16),   # Pin 3
    }

    # Connect SPI signals using local labels on wires
    spi_connections = [
        ('SI', 'SPI_MOSI', 180),
        ('SO', 'SPI_MISO', 180),
        ('CS', 'SPI_CE0', 180),
        ('SCK', 'SPI_SCLK', 180),
        ('INT', 'CAN_INT', 0),
        ('TXCAN', 'CAN_TX', 0),
        ('RXCAN', 'CAN_RX', 0),
    ]

    for u2_pin, signal, direction in spi_connections:
        px, py = u2_pins[u2_pin]
        if direction == 180:  # Wire goes left
            wire_end_x = px - 5.08
        else:  # Wire goes right
            wire_end_x = px + 5.08

        wire = create_wire(px, py, wire_end_x, py)
        new_elements.append(wire)
        label = create_label(signal, wire_end_x, py, direction)
        new_elements.append(label)
        print(f"  U2.{u2_pin}: {signal}")

    # Crystal connections
    osc_connections = [
        ('OSC1', 'OSC1', 180),
        ('OSC2', 'OSC2', 180),
    ]
    for u2_pin, signal, direction in osc_connections:
        px, py = u2_pins[u2_pin]
        wire_end_x = px - 5.08
        wire = create_wire(px, py, wire_end_x, py)
        new_elements.append(wire)
        label = create_label(signal, wire_end_x, py, 180)
        new_elements.append(label)
        print(f"  U2.{u2_pin}: {signal}")

    # TX*RTS pins tie high (through resistor to +3.3V or directly)
    for pin in ['TX0RTS', 'TX1RTS', 'TX2RTS']:
        px, py = u2_pins[pin]
        wire_end_x = px - 5.08
        wire = create_wire(px, py, wire_end_x, py)
        new_elements.append(wire)
        label = create_global_label('+3.3V', wire_end_x, py, 180)
        new_elements.append(label)
        print(f"  U2.{pin}: +3.3V (tied high)")

    # RX*BF pins - no connect
    for pin in ['RX0BF', 'RX1BF']:
        px, py = u2_pins[pin]
        nc = create_no_connect(px, py)
        new_elements.append(nc)
        print(f"  U2.{pin}: no-connect")

    # CLKOUT - no connect
    px, py = u2_pins['CLKOUT']
    nc = create_no_connect(px, py)
    new_elements.append(nc)
    print(f"  U2.CLKOUT: no-connect")

    # =========================================================================
    # Section 3: SN65HVD230 (U3) Connections
    # =========================================================================
    print("\n--- Section 3: SN65HVD230 (U3) ---")

    # U3 positions (from ERC, in mm)
    # Left pins at x=22100 mils = 561.34 mm
    # Right pins at x=22400 mils = 568.96 mm
    u3_left_x = 561.34
    u3_right_x = 568.96

    u3_pins = {
        'D': (u3_left_x, 693.42),      # Pin 1 - Driver input (from CAN controller TX)
        'GND': (u3_left_x, 695.96),    # Pin 2 - Ground
        'VCC': (u3_left_x, 698.50),    # Pin 3 - Power supply
        'R': (u3_left_x, 701.04),      # Pin 4 - Receiver output (to CAN controller RX)
        'Vref': (u3_right_x, 701.04),  # Pin 5 - Reference voltage out
        'CANL': (u3_right_x, 698.50),  # Pin 6 - CAN Low
        'CANH': (u3_right_x, 695.96),  # Pin 7 - CAN High
        'RS': (u3_right_x, 693.42),    # Pin 8 - Slope control
    }

    # Connect D to CAN_TX (from MCP2515)
    px, py = u3_pins['D']
    wire = create_wire(px, py, px - 5.08, py)
    new_elements.append(wire)
    label = create_label('CAN_TX', px - 5.08, py, 180)
    new_elements.append(label)
    print(f"  U3.D: CAN_TX")

    # Connect R to CAN_RX (to MCP2515)
    px, py = u3_pins['R']
    wire = create_wire(px, py, px - 5.08, py)
    new_elements.append(wire)
    label = create_label('CAN_RX', px - 5.08, py, 180)
    new_elements.append(label)
    print(f"  U3.R: CAN_RX")

    # CANH and CANL to bus connectors
    px, py = u3_pins['CANH']
    wire = create_wire(px, py, px + 5.08, py)
    new_elements.append(wire)
    label = create_global_label('CANH', px + 5.08, py, 0)
    new_elements.append(label)
    print(f"  U3.CANH: CANH")

    px, py = u3_pins['CANL']
    wire = create_wire(px, py, px + 5.08, py)
    new_elements.append(wire)
    label = create_global_label('CANL', px + 5.08, py, 0)
    new_elements.append(label)
    print(f"  U3.CANL: CANL")

    # VCC to +3.3V
    px, py = u3_pins['VCC']
    wire = create_wire(px, py, px - 5.08, py)
    new_elements.append(wire)
    label = create_global_label('+3.3V', px - 5.08, py, 180)
    new_elements.append(label)
    print(f"  U3.VCC: +3.3V")

    # GND
    px, py = u3_pins['GND']
    wire = create_wire(px, py, px - 5.08, py)
    new_elements.append(wire)
    label = create_global_label('GND', px - 5.08, py, 180)
    new_elements.append(label)
    print(f"  U3.GND: GND")

    # RS to GND for high-speed mode
    px, py = u3_pins['RS']
    wire = create_wire(px, py, px + 5.08, py)
    new_elements.append(wire)
    label = create_global_label('GND', px + 5.08, py, 0)
    new_elements.append(label)
    print(f"  U3.RS: GND (high-speed mode)")

    # Vref - no connect (not using as reference)
    px, py = u3_pins['Vref']
    nc = create_no_connect(px, py)
    new_elements.append(nc)
    print(f"  U3.Vref: no-connect")

    # =========================================================================
    # Section 4: Crystal (Y1) Connections
    # =========================================================================
    print("\n--- Section 4: Crystal (Y1) ---")

    # Y1 from ERC: pins at (7350, 22500) and (7650, 22500) mils
    y1_pin1_x = 186.69  # 7350 mils
    y1_pin2_x = 194.31  # 7650 mils
    y1_y = 571.5        # 22500 mils

    # OSC1 connects to Y1 pin 1
    wire = create_wire(y1_pin1_x, y1_y, y1_pin1_x - 5.08, y1_y)
    new_elements.append(wire)
    label = create_label('OSC1', y1_pin1_x - 5.08, y1_y, 180)
    new_elements.append(label)
    print(f"  Y1.1: OSC1")

    # OSC2 connects to Y1 pin 2
    wire = create_wire(y1_pin2_x, y1_y, y1_pin2_x + 5.08, y1_y)
    new_elements.append(wire)
    label = create_label('OSC2', y1_pin2_x + 5.08, y1_y, 0)
    new_elements.append(label)
    print(f"  Y1.2: OSC2")

    # =========================================================================
    # Section 5: CAN Bus Connectors (J2, J3)
    # =========================================================================
    print("\n--- Section 5: CAN Connectors ---")

    # J3 (screw terminal) - from schematic around (444.5, 571.5)
    # 3-pin terminal: pin 1 = CANH, pin 2 = CANL, pin 3 = GND
    j3_x = 444.5
    j3_pin1_y = 569.0   # CANH
    j3_pin2_y = 571.5   # CANL
    j3_pin3_y = 574.0   # GND

    # J3 pin 1 -> CANH
    wire = create_wire(j3_x - 2.54, j3_pin1_y, j3_x - 7.62, j3_pin1_y)
    new_elements.append(wire)
    label = create_global_label('CANH', j3_x - 7.62, j3_pin1_y, 180)
    new_elements.append(label)
    print(f"  J3.pin1: CANH")

    # J3 pin 2 -> CANL
    wire = create_wire(j3_x - 2.54, j3_pin2_y, j3_x - 7.62, j3_pin2_y)
    new_elements.append(wire)
    label = create_global_label('CANL', j3_x - 7.62, j3_pin2_y, 180)
    new_elements.append(label)
    print(f"  J3.pin2: CANL")

    # J3 pin 3 -> GND
    wire = create_wire(j3_x - 2.54, j3_pin3_y, j3_x - 7.62, j3_pin3_y)
    new_elements.append(wire)
    label = create_global_label('GND', j3_x - 7.62, j3_pin3_y, 180)
    new_elements.append(label)
    print(f"  J3.pin3: GND")

    # J2 (OBD-II connector) - 16 pins
    # Standard OBD-II CAN pins: 6 = CANH, 14 = CANL
    # Other pins unused - mark no-connect
    # J2 around (444.5, 508)
    j2_x = 444.5
    j2_base_y = 490.0
    j2_pitch = 2.54

    for pin in range(1, 17):
        pin_y = j2_base_y + (pin - 1) * j2_pitch

        if pin == 6:  # CANH
            wire = create_wire(j2_x - 2.54, pin_y, j2_x - 7.62, pin_y)
            new_elements.append(wire)
            label = create_global_label('CANH', j2_x - 7.62, pin_y, 180)
            new_elements.append(label)
            print(f"  J2.{pin}: CANH")
        elif pin == 14:  # CANL
            wire = create_wire(j2_x - 2.54, pin_y, j2_x - 7.62, pin_y)
            new_elements.append(wire)
            label = create_global_label('CANL', j2_x - 7.62, pin_y, 180)
            new_elements.append(label)
            print(f"  J2.{pin}: CANL")
        elif pin == 4 or pin == 5:  # Chassis ground, signal ground
            wire = create_wire(j2_x - 2.54, pin_y, j2_x - 7.62, pin_y)
            new_elements.append(wire)
            label = create_global_label('GND', j2_x - 7.62, pin_y, 180)
            new_elements.append(label)
            print(f"  J2.{pin}: GND")
        else:
            nc = create_no_connect(j2_x - 2.54, pin_y)
            new_elements.append(nc)

    print(f"  12 J2 pins marked no-connect")

    # =========================================================================
    # Section 6: AMS1117 (U1) Power Connections
    # =========================================================================
    print("\n--- Section 6: U1 AMS1117 Power ---")

    # U1 from schematic - need to check actual position
    # Typical AMS1117 pinout: 1=GND/ADJ, 2=VO, 3=VI
    u1_x = 393.7
    u1_vi_y = 424.18     # VI (input)
    u1_vo_y = 431.8      # VO (output)
    u1_gnd_y = 439.42    # GND

    # VI -> +5V
    wire = create_wire(u1_x - 3.81, u1_vi_y, u1_x - 8.89, u1_vi_y)
    new_elements.append(wire)
    label = create_global_label('+5V', u1_x - 8.89, u1_vi_y, 180)
    new_elements.append(label)
    print(f"  U1.VI: +5V")

    # VO -> +3.3V
    wire = create_wire(u1_x + 3.81, u1_vo_y, u1_x + 8.89, u1_vo_y)
    new_elements.append(wire)
    label = create_global_label('+3.3V', u1_x + 8.89, u1_vo_y, 0)
    new_elements.append(label)
    print(f"  U1.VO: +3.3V")

    # GND
    wire = create_wire(u1_x, u1_gnd_y + 2.54, u1_x, u1_gnd_y + 7.62)
    new_elements.append(wire)
    label = create_global_label('GND', u1_x, u1_gnd_y + 7.62, 270)
    new_elements.append(label)
    print(f"  U1.GND: GND")

    # =========================================================================
    # Insert all new elements
    # =========================================================================
    print("\n" + "=" * 70)
    print("Inserting elements...")

    insert_pos = find_insert_position(content)
    new_content = '\n'.join(new_elements)
    content = content[:insert_pos] + '\n' + new_content + '\n' + content[insert_pos:]

    write_schematic(can_hat_sch, content)

    print(f"\nAdded {len(new_elements)} new elements")
    print("\nRun ERC in KiCad to verify")
    print("=" * 70)


if __name__ == "__main__":
    fix_can_hat()
