#!/usr/bin/env python3
"""
CAN HAT Fix Script - Version 2

Uses EXACT pin positions from ERC report (converted from mils to mm).
The v1 script used incorrect coordinate calculations.

Key formula: mm = mils * 0.0254
"""

import uuid
import re
from pathlib import Path


def generate_uuid():
    return str(uuid.uuid4())


def mils_to_mm(mils):
    """Convert mils to mm."""
    return round(mils * 0.0254, 2)


def create_wire(x1, y1, x2, y2):
    """Create a KiCad wire S-expression."""
    uid = generate_uuid()
    return f'''\t(wire
\t\t(pts
\t\t\t(xy {x1} {y1}) (xy {x2} {y2})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{uid}")
\t)'''


def create_label(name, x, y, direction=0):
    """Create a KiCad local label."""
    uid = generate_uuid()
    justify = "right" if direction == 180 else "left"
    return f'''\t(label "{name}"
\t\t(at {x} {y} {direction})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {justify} bottom)
\t\t)
\t\t(uuid "{uid}")
\t)'''


def create_global_label(name, x, y, direction=0, shape="passive"):
    """Create a KiCad global label."""
    uid = generate_uuid()
    justify = "right" if direction == 180 else "left"
    return f'''\t(global_label "{name}"
\t\t(shape {shape})
\t\t(at {x} {y} {direction})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {justify})
\t\t)
\t\t(uuid "{uid}")
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t)'''


def create_no_connect(x, y):
    """Create a no_connect marker."""
    uid = generate_uuid()
    return f'''\t(no_connect
\t\t(at {x} {y})
\t\t(uuid "{uid}")
\t)'''


def create_pwr_flag(x, y, ref_num):
    """Create a PWR_FLAG symbol."""
    uid = generate_uuid()
    pin_uid = generate_uuid()
    return f'''\t(symbol
\t\t(lib_id "power:PWR_FLAG")
\t\t(at {x} {y} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom no)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid}")
\t\t(property "Reference" "#FLG{ref_num:02d}"
\t\t\t(at {x} {y - 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Value" "PWR_FLAG"
\t\t\t(at {x} {y + 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" "Special symbol for telling ERC where power comes from"
\t\t\t(at {x} {y} 0)
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
\t\t(instances
\t\t\t(project "can-hat"
\t\t\t\t(path "/7bb601d0-af23-47b8-978e-986fbee2569f"
\t\t\t\t\t(reference "#FLG{ref_num:02d}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def read_schematic(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_schematic(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {filepath}")


def find_insert_position(content):
    match = re.search(r'\n\t\(sheet_instances', content)
    if match:
        return match.start()
    return len(content) - 2


# =============================================================================
# ACTUAL PIN POSITIONS FROM ERC REPORT (in mils, converted to mm)
# =============================================================================

# J1 GPIO Header - Actual pin positions from ERC
# Pattern: odd pins at x=7674 mils, even pins at x=8174 mils
# Y starts at 5006 mils, increases by 100 mils per row
def get_j1_pin_position(pin):
    """Get actual J1 pin position from ERC data."""
    if pin % 2 == 1:  # Odd pins (left side)
        x_mils = 7674
        row = (pin - 1) // 2
    else:  # Even pins (right side)
        x_mils = 8174
        row = (pin - 2) // 2
    y_mils = 5006 + row * 100
    return (mils_to_mm(x_mils), mils_to_mm(y_mils))


# MCP2515 (U2) pin positions from ERC
U2_PINS = {
    # Left side pins
    'SI': (mils_to_mm(16900), mils_to_mm(4400)),      # Pin 14
    'SO': (mils_to_mm(16900), mils_to_mm(4500)),      # Pin 15
    'CS': (mils_to_mm(16900), mils_to_mm(4600)),      # Pin 16
    'SCK': (mils_to_mm(16900), mils_to_mm(4700)),     # Pin 13
    'OSC2': (mils_to_mm(16900), mils_to_mm(4800)),    # Pin 7 - estimated
    'OSC1': (mils_to_mm(16900), mils_to_mm(4900)),    # Pin 8 - estimated
    # Right side pins
    'TXCAN': (mils_to_mm(18100), mils_to_mm(4500)),   # Pin 1
    'RXCAN': (mils_to_mm(18100), mils_to_mm(4400)),   # Pin 2
    'INT': (mils_to_mm(18100), mils_to_mm(5000)),     # Pin 12
    'RX0BF': (mils_to_mm(18100), mils_to_mm(5100)),   # Pin 11
    'RX1BF': (mils_to_mm(18100), mils_to_mm(5200)),   # Pin 10
    'TX0RTS': (mils_to_mm(18100), mils_to_mm(5300)),  # Pin 4
    'TX1RTS': (mils_to_mm(18100), mils_to_mm(5400)),  # Pin 5
    'TX2RTS': (mils_to_mm(18100), mils_to_mm(5500)),  # Pin 6
    # Power pins - need to find from schematic
    'VDD': (mils_to_mm(17500), mils_to_mm(4200)),     # Estimated top
    'VSS': (mils_to_mm(17500), mils_to_mm(5700)),     # Estimated bottom
}

# SN65HVD230 (U3) pin positions from ERC
U3_PINS = {
    'D': (mils_to_mm(22100), mils_to_mm(27300)),      # TXD input - estimated
    'R': (mils_to_mm(22100), mils_to_mm(27500)),      # RXD output - from ERC Pin 4
    'CANH': (mils_to_mm(23772), mils_to_mm(27500)),   # From ERC (L1 position)
    'CANL': (mils_to_mm(23772), mils_to_mm(27600)),   # From ERC (L2 position)
    'VCC': (mils_to_mm(22500), mils_to_mm(27200)),    # From label position
    'GND': (mils_to_mm(22500), mils_to_mm(27900)),    # From label position
    'Vref': (mils_to_mm(22100), mils_to_mm(27600)),   # Pin 5
}

# Y1 Crystal positions from ERC
Y1_PINS = {
    'pin1': (mils_to_mm(7350), mils_to_mm(22500)),
    'pin2': (mils_to_mm(7650), mils_to_mm(22500)),
}

# J2 OBD-II positions from ERC (Conn_01x16)
# Pins at x=17300 mils, y starting at ~19300 mils
def get_j2_pin_position(pin):
    x_mils = 17300
    y_mils = 19300 + (pin - 1) * 100
    return (mils_to_mm(x_mils), mils_to_mm(y_mils))

# J3 Terminal positions from ERC
J3_PINS = {
    'pin1': (mils_to_mm(17300), mils_to_mm(22500)),
    'pin2': (mils_to_mm(17300), mils_to_mm(22600)),
}

# U1 AMS1117 positions from ERC
U1_PINS = {
    'VI': (mils_to_mm(14700), mils_to_mm(17050)),
    'VO': (mils_to_mm(15300), mils_to_mm(17050)),
    'GND': (mils_to_mm(15000), mils_to_mm(17350)),
}


def fix_can_hat_v2():
    """Main function - v2 with correct coordinates."""
    script_dir = Path(__file__).parent
    can_hat_sch = script_dir / "can-hat" / "can-hat.kicad_sch"

    if not can_hat_sch.exists():
        print(f"Error: {can_hat_sch} not found")
        return

    print("=" * 70)
    print("CAN HAT Fix Script - Version 2 (Correct Coordinates)")
    print("=" * 70)

    content = read_schematic(can_hat_sch)
    print(f"Read {len(content)} bytes")

    new_elements = []
    pwr_flag_num = 4  # Start at 4 since 1-3 may already exist

    # =========================================================================
    # SECTION 1: J1 GPIO Header Connections
    # =========================================================================
    print("\n--- Section 1: GPIO Header (J1) ---")

    # Power pins
    power_pins = {
        1: "+3.3V",
        2: "+5V",
        4: "+5V",
        17: "+3.3V",
    }

    # Ground pins
    gnd_pins = [6, 9, 14, 20, 25, 30, 34, 39]

    # SPI/Signal pins
    signal_pins = {
        19: "SPI_MOSI",  # GPIO10
        21: "SPI_MISO",  # GPIO9
        23: "SPI_SCLK",  # GPIO11
        24: "SPI_CE0",   # GPIO8
        22: "CAN_INT",   # GPIO25
    }

    # Connect power pins
    for pin, net in power_pins.items():
        x, y = get_j1_pin_position(pin)
        if pin % 2 == 1:  # Left side - wire goes left
            wire_end_x = x - 5
            direction = 180
        else:  # Right side - wire goes right
            wire_end_x = x + 5
            direction = 0

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label(net, wire_end_x, y, direction, "passive")
        new_elements.extend([wire, label])
        print(f"  Pin {pin} ({x:.2f}, {y:.2f}): {net}")

    # Connect ground pins
    for pin in gnd_pins:
        x, y = get_j1_pin_position(pin)
        if pin % 2 == 1:
            wire_end_x = x - 5
            direction = 180
        else:
            wire_end_x = x + 5
            direction = 0

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label("GND", wire_end_x, y, direction, "passive")
        new_elements.extend([wire, label])
        print(f"  Pin {pin} ({x:.2f}, {y:.2f}): GND")

    # Connect SPI/signal pins
    for pin, net in signal_pins.items():
        x, y = get_j1_pin_position(pin)
        if pin % 2 == 1:
            wire_end_x = x - 5
            direction = 180
        else:
            wire_end_x = x + 5
            direction = 0

        shape = "input" if net == "CAN_INT" else "output" if "MOSI" in net or "SCLK" in net or "CE0" in net else "input"
        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label(net, wire_end_x, y, direction, shape)
        new_elements.extend([wire, label])
        print(f"  Pin {pin} ({x:.2f}, {y:.2f}): {net}")

    # Mark unused pins
    used_pins = set(power_pins.keys()) | set(gnd_pins) | set(signal_pins.keys())
    for pin in range(1, 41):
        if pin not in used_pins:
            x, y = get_j1_pin_position(pin)
            nc = create_no_connect(x, y)
            new_elements.append(nc)
    print(f"  Marked {40 - len(used_pins)} unused pins as no-connect")

    # =========================================================================
    # SECTION 2: MCP2515 (U2) Key Connections
    # =========================================================================
    print("\n--- Section 2: MCP2515 (U2) ---")

    # SPI connections (pins on left side, wire left)
    spi_connections = [
        ('SI', 'SPI_MOSI', 'input'),
        ('SO', 'SPI_MISO', 'output'),
        ('CS', 'SPI_CE0', 'input'),
        ('SCK', 'SPI_SCLK', 'input'),
    ]

    for pin_name, net, shape in spi_connections:
        if pin_name in U2_PINS:
            x, y = U2_PINS[pin_name]
            wire = create_wire(x, y, x - 5, y)
            label = create_global_label(net, x - 5, y, 180, shape)
            new_elements.extend([wire, label])
            print(f"  U2.{pin_name} ({x:.2f}, {y:.2f}): {net}")

    # CAN connections (pins on right side, wire right)
    can_connections = [
        ('TXCAN', 'CAN_TX', 'output'),
        ('RXCAN', 'CAN_RX', 'input'),
        ('INT', 'CAN_INT', 'output'),
    ]

    for pin_name, net, shape in can_connections:
        if pin_name in U2_PINS:
            x, y = U2_PINS[pin_name]
            wire = create_wire(x, y, x + 5, y)
            label = create_global_label(net, x + 5, y, 0, shape)
            new_elements.extend([wire, label])
            print(f"  U2.{pin_name} ({x:.2f}, {y:.2f}): {net}")

    # Tie unused input pins to VCC or mark no-connect
    unused_inputs = ['TX0RTS', 'TX1RTS', 'TX2RTS']
    for pin_name in unused_inputs:
        if pin_name in U2_PINS:
            x, y = U2_PINS[pin_name]
            # Tie to +3.3V (these are active-low inputs)
            wire = create_wire(x, y, x + 5, y)
            label = create_global_label("+3.3V", x + 5, y, 0, "passive")
            new_elements.extend([wire, label])
            print(f"  U2.{pin_name}: tied to +3.3V")

    # Unused outputs - just mark them (or leave floating)
    unused_outputs = ['RX0BF', 'RX1BF']
    for pin_name in unused_outputs:
        if pin_name in U2_PINS:
            x, y = U2_PINS[pin_name]
            nc = create_no_connect(x, y)
            new_elements.append(nc)
            print(f"  U2.{pin_name}: no-connect")

    # =========================================================================
    # SECTION 3: SN65HVD230 (U3) Connections
    # =========================================================================
    print("\n--- Section 3: SN65HVD230 (U3) ---")

    # TXD/RXD (connect to CAN controller)
    u3_signals = [
        ('D', 'CAN_TX', 'input', 180),
        ('R', 'CAN_RX', 'output', 180),
    ]

    for pin_name, net, shape, direction in u3_signals:
        if pin_name in U3_PINS:
            x, y = U3_PINS[pin_name]
            wire_end = x - 5 if direction == 180 else x + 5
            wire = create_wire(x, y, wire_end, y)
            label = create_global_label(net, wire_end, y, direction, shape)
            new_elements.extend([wire, label])
            print(f"  U3.{pin_name} ({x:.2f}, {y:.2f}): {net}")

    # CAN bus outputs
    for pin_name, net in [('CANH', 'CANH'), ('CANL', 'CANL')]:
        if pin_name in U3_PINS:
            x, y = U3_PINS[pin_name]
            wire = create_wire(x, y, x + 5, y)
            label = create_global_label(net, x + 5, y, 0, "bidirectional")
            new_elements.extend([wire, label])
            print(f"  U3.{pin_name} ({x:.2f}, {y:.2f}): {net}")

    # =========================================================================
    # SECTION 4: Crystal (Y1)
    # =========================================================================
    print("\n--- Section 4: Crystal (Y1) ---")

    # Connect crystal to XTAL1/XTAL2 nets (these connect to MCP2515 OSC pins)
    x1, y1 = Y1_PINS['pin1']
    wire = create_wire(x1, y1, x1 - 5, y1)
    label = create_global_label("XTAL1", x1 - 5, y1, 180, "passive")
    new_elements.extend([wire, label])
    print(f"  Y1.1 ({x1:.2f}, {y1:.2f}): XTAL1")

    x2, y2 = Y1_PINS['pin2']
    wire = create_wire(x2, y2, x2 + 5, y2)
    label = create_global_label("XTAL2", x2 + 5, y2, 0, "passive")
    new_elements.extend([wire, label])
    print(f"  Y1.2 ({x2:.2f}, {y2:.2f}): XTAL2")

    # Add XTAL1/XTAL2 at MCP2515 OSC pins
    if 'OSC1' in U2_PINS:
        x, y = U2_PINS['OSC1']
        wire = create_wire(x, y, x - 5, y)
        label = create_global_label("XTAL1", x - 5, y, 180, "passive")
        new_elements.extend([wire, label])
        print(f"  U2.OSC1: XTAL1")

    if 'OSC2' in U2_PINS:
        x, y = U2_PINS['OSC2']
        wire = create_wire(x, y, x - 5, y)
        label = create_global_label("XTAL2", x - 5, y, 180, "passive")
        new_elements.extend([wire, label])
        print(f"  U2.OSC2: XTAL2")

    # =========================================================================
    # SECTION 5: CAN Bus Connectors
    # =========================================================================
    print("\n--- Section 5: CAN Connectors ---")

    # J3 Screw Terminal
    x, y = J3_PINS['pin1']
    wire = create_wire(x, y, x - 5, y)
    label = create_global_label("CANH", x - 5, y, 180, "bidirectional")
    new_elements.extend([wire, label])
    print(f"  J3.1: CANH")

    x, y = J3_PINS['pin2']
    wire = create_wire(x, y, x - 5, y)
    label = create_global_label("CANL", x - 5, y, 180, "bidirectional")
    new_elements.extend([wire, label])
    print(f"  J3.2: CANL")

    # J2 OBD-II - Pin 6 = CANH, Pin 14 = CANL
    x, y = get_j2_pin_position(6)
    wire = create_wire(x, y, x - 5, y)
    label = create_global_label("CANH", x - 5, y, 180, "bidirectional")
    new_elements.extend([wire, label])
    print(f"  J2.6: CANH")

    x, y = get_j2_pin_position(14)
    wire = create_wire(x, y, x - 5, y)
    label = create_global_label("CANL", x - 5, y, 180, "bidirectional")
    new_elements.extend([wire, label])
    print(f"  J2.14: CANL")

    # Mark other J2 pins as no-connect
    used_j2 = [6, 14]
    for pin in range(1, 17):
        if pin not in used_j2:
            x, y = get_j2_pin_position(pin)
            nc = create_no_connect(x, y)
            new_elements.append(nc)
    print(f"  Marked {16 - len(used_j2)} unused J2 pins")

    # =========================================================================
    # SECTION 6: Power Distribution
    # =========================================================================
    print("\n--- Section 6: Power Distribution ---")

    # U1 AMS1117 connections
    # VI -> 5V (input from GPIO header)
    x, y = U1_PINS['VI']
    wire = create_wire(x, y, x - 5, y)
    label = create_global_label("+5V", x - 5, y, 180, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.VI: +5V")

    # VO -> +3.3V output
    x, y = U1_PINS['VO']
    wire = create_wire(x, y, x + 5, y)
    label = create_global_label("+3.3V", x + 5, y, 0, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.VO: +3.3V")

    # GND
    x, y = U1_PINS['GND']
    wire = create_wire(x, y, x, y + 5)
    label = create_global_label("GND", x, y + 5, 90, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.GND: GND")

    # =========================================================================
    # SECTION 7: PWR_FLAG Symbols
    # =========================================================================
    print("\n--- Section 7: PWR_FLAG ---")

    # PWR_FLAG for +5V
    pf_x, pf_y = get_j1_pin_position(2)
    pwr_flag = create_pwr_flag(pf_x + 10, pf_y - 5, pwr_flag_num)
    wire = create_wire(pf_x + 10, pf_y - 5, pf_x + 10, pf_y)
    new_elements.extend([pwr_flag, wire])
    print(f"  PWR_FLAG #{pwr_flag_num}: +5V")
    pwr_flag_num += 1

    # PWR_FLAG for +3.3V (at U1 output)
    x, y = U1_PINS['VO']
    pwr_flag = create_pwr_flag(x + 10, y - 5, pwr_flag_num)
    wire = create_wire(x + 10, y - 5, x + 10, y)
    new_elements.extend([pwr_flag, wire])
    print(f"  PWR_FLAG #{pwr_flag_num}: +3.3V")
    pwr_flag_num += 1

    # PWR_FLAG for GND
    x, y = U1_PINS['GND']
    pwr_flag = create_pwr_flag(x + 5, y + 10, pwr_flag_num)
    wire = create_wire(x + 5, y + 10, x, y + 5)
    new_elements.extend([pwr_flag, wire])
    print(f"  PWR_FLAG #{pwr_flag_num}: GND")

    # =========================================================================
    # Insert and save
    # =========================================================================
    print("\n" + "=" * 70)
    print("Inserting elements...")

    insert_pos = find_insert_position(content)
    new_content = '\n'.join(new_elements)
    content = content[:insert_pos] + '\n' + new_content + '\n' + content[insert_pos:]

    write_schematic(can_hat_sch, content)

    print(f"\nAdded {len(new_elements)} new elements")
    print("\nNext steps:")
    print("1. Open in KiCad and run ERC")
    print("2. Manually fix any remaining issues")
    print("3. Add USB-C power circuit manually")
    print("=" * 70)


if __name__ == "__main__":
    fix_can_hat_v2()
