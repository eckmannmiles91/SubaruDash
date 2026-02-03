#!/usr/bin/env python3
"""
CAN HAT Fix Script - Version 3

FIXES from v2:
- Use FULL PRECISION coordinates (no rounding) to match exact pin positions
- Use mils directly and convert only at output time
- Avoid the CANH/GND short circuit bug
"""

import uuid
import re
from pathlib import Path


def generate_uuid():
    return str(uuid.uuid4())


def mils_to_mm(mils):
    """Convert mils to mm with FULL precision (no rounding)."""
    return mils * 0.0254


def create_wire(x1, y1, x2, y2):
    """Create a KiCad wire."""
    uid = generate_uuid()
    return f'''\t(wire
\t\t(pts
\t\t\t(xy {x1:.4f} {y1:.4f}) (xy {x2:.4f} {y2:.4f})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{uid}")
\t)'''


def create_global_label(name, x, y, direction=0, shape="passive"):
    """Create a global label."""
    uid = generate_uuid()
    justify = "right" if direction == 180 else "left"
    return f'''\t(global_label "{name}"
\t\t(shape {shape})
\t\t(at {x:.4f} {y:.4f} {direction})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {justify})
\t\t)
\t\t(uuid "{uid}")
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
\t\t\t(at {x:.4f} {y:.4f} 0)
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
\t\t(at {x:.4f} {y:.4f})
\t\t(uuid "{uid}")
\t)'''


def create_pwr_flag(x, y, ref_num):
    """Create a PWR_FLAG symbol."""
    uid = generate_uuid()
    pin_uid = generate_uuid()
    return f'''\t(symbol
\t\t(lib_id "power:PWR_FLAG")
\t\t(at {x:.4f} {y:.4f} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom no)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid}")
\t\t(property "Reference" "#FLG{ref_num:02d}"
\t\t\t(at {x:.4f} {y - 2.54:.4f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Value" "PWR_FLAG"
\t\t\t(at {x:.4f} {y + 2.54:.4f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x:.4f} {y:.4f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x:.4f} {y:.4f} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" "Special symbol for telling ERC where power comes from"
\t\t\t(at {x:.4f} {y:.4f} 0)
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
# PIN POSITIONS IN MILS (from ERC report) - Will convert at output time
# =============================================================================

# J1 GPIO Header pin positions
def get_j1_pin_mils(pin):
    """Get J1 pin position in mils."""
    if pin % 2 == 1:  # Odd pins (left side)
        x = 7674
        row = (pin - 1) // 2
    else:  # Even pins (right side)
        x = 8174
        row = (pin - 2) // 2
    y = 5006 + row * 100
    return (x, y)


# MCP2515 (U2) - positions from ERC in mils
# These are the ACTUAL pin positions from the error messages
U2_PINS_MILS = {
    # Left side (pins 13-16, 7-8)
    'SI': (16900, 4400),      # Pin 14 - SPI MOSI input
    'SO': (16900, 4500),      # Pin 15 - SPI MISO output
    'CS': (16900, 4600),      # Pin 16 - Chip Select
    'SCK': (16900, 4700),     # Pin 13 - SPI Clock
    # OSC pins - estimated from OSC labels in schematic
    'OSC2': (16900, 4800),    # Pin 7
    'OSC1': (16900, 4900),    # Pin 8
    # Right side pins
    'TXCAN': (18100, 4500),   # Pin 1 - CAN TX to transceiver
    'RXCAN': (18100, 4400),   # Pin 2 - CAN RX from transceiver
    'INT': (18100, 5000),     # Pin 12 - Interrupt output
    'RX0BF': (18100, 5100),   # Pin 11 - Buffer full flag (unused)
    'RX1BF': (18100, 5200),   # Pin 10 - Buffer full flag (unused)
    'TX0RTS': (18100, 5300),  # Pin 4 - Request to send (tie high)
    'TX1RTS': (18100, 5400),  # Pin 5 - Request to send (tie high)
    'TX2RTS': (18100, 5500),  # Pin 6 - Request to send (tie high)
}

# SN65HVD230 (U3) - from ERC
U3_PINS_MILS = {
    'D': (22100, 27300),      # TXD input (from MCP2515)
    'R': (22100, 27500),      # RXD output (to MCP2515)
    'CANH': (23772, 27500),   # CAN High output (via L1)
    'CANL': (23772, 27600),   # CAN Low output (via L2)
    'Vref': (22100, 27600),   # Vref output (unused)
}

# Y1 Crystal - from ERC
Y1_PINS_MILS = {
    'pin1': (7350, 22500),
    'pin2': (7650, 22500),
}

# J2 OBD-II connector
def get_j2_pin_mils(pin):
    """J2 pins at x=17300, y=19300 + (pin-1)*100"""
    return (17300, 19300 + (pin - 1) * 100)

# J3 Terminal
J3_PINS_MILS = {
    'pin1': (17300, 22500),
    'pin2': (17300, 22600),
}

# U1 AMS1117 - from ERC
U1_PINS_MILS = {
    'VI': (14700, 17050),     # Input (5V)
    'VO': (15300, 17050),     # Output (3.3V)
    'GND': (15000, 17350),    # Ground
}


def fix_can_hat_v3():
    """V3 with precise coordinates."""
    script_dir = Path(__file__).parent
    can_hat_sch = script_dir / "can-hat" / "can-hat.kicad_sch"

    if not can_hat_sch.exists():
        print(f"Error: {can_hat_sch} not found")
        return

    print("=" * 70)
    print("CAN HAT Fix Script - Version 3 (Full Precision)")
    print("=" * 70)

    content = read_schematic(can_hat_sch)
    print(f"Read {len(content)} bytes")

    new_elements = []
    pwr_flag_num = 4

    # Wire length in mils (will be converted to mm)
    WIRE_LEN = 200  # 200 mils = 5.08mm

    # =========================================================================
    # SECTION 1: J1 GPIO Header
    # =========================================================================
    print("\n--- Section 1: GPIO Header (J1) ---")

    power_pins = {1: "+3.3V", 2: "+5V", 4: "+5V", 17: "+3.3V"}
    gnd_pins = [6, 9, 14, 20, 25, 30, 34, 39]
    signal_pins = {
        19: ("SPI_MOSI", "output"),
        21: ("SPI_MISO", "input"),
        23: ("SPI_SCLK", "output"),
        24: ("SPI_CE0", "output"),
        22: ("CAN_INT", "input"),
    }

    # Power pins
    for pin, net in power_pins.items():
        x_mils, y_mils = get_j1_pin_mils(pin)
        x = mils_to_mm(x_mils)
        y = mils_to_mm(y_mils)

        if pin % 2 == 1:  # Left - wire goes left
            wire_end_x = mils_to_mm(x_mils - WIRE_LEN)
            direction = 180
        else:  # Right - wire goes right
            wire_end_x = mils_to_mm(x_mils + WIRE_LEN)
            direction = 0

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label(net, wire_end_x, y, direction, "passive")
        new_elements.extend([wire, label])
        print(f"  Pin {pin}: {net}")

    # Ground pins
    for pin in gnd_pins:
        x_mils, y_mils = get_j1_pin_mils(pin)
        x = mils_to_mm(x_mils)
        y = mils_to_mm(y_mils)

        if pin % 2 == 1:
            wire_end_x = mils_to_mm(x_mils - WIRE_LEN)
            direction = 180
        else:
            wire_end_x = mils_to_mm(x_mils + WIRE_LEN)
            direction = 0

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label("GND", wire_end_x, y, direction, "passive")
        new_elements.extend([wire, label])
        print(f"  Pin {pin}: GND")

    # Signal pins
    for pin, (net, shape) in signal_pins.items():
        x_mils, y_mils = get_j1_pin_mils(pin)
        x = mils_to_mm(x_mils)
        y = mils_to_mm(y_mils)

        if pin % 2 == 1:
            wire_end_x = mils_to_mm(x_mils - WIRE_LEN)
            direction = 180
        else:
            wire_end_x = mils_to_mm(x_mils + WIRE_LEN)
            direction = 0

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label(net, wire_end_x, y, direction, shape)
        new_elements.extend([wire, label])
        print(f"  Pin {pin}: {net}")

    # Unused pins - no_connect
    used = set(power_pins.keys()) | set(gnd_pins) | set(signal_pins.keys())
    for pin in range(1, 41):
        if pin not in used:
            x_mils, y_mils = get_j1_pin_mils(pin)
            nc = create_no_connect(mils_to_mm(x_mils), mils_to_mm(y_mils))
            new_elements.append(nc)
    print(f"  {40 - len(used)} pins marked no-connect")

    # =========================================================================
    # SECTION 2: MCP2515 (U2)
    # =========================================================================
    print("\n--- Section 2: MCP2515 (U2) ---")

    # SPI connections (left side pins - wire goes left)
    spi = [('SI', 'SPI_MOSI', 'input'), ('SO', 'SPI_MISO', 'output'),
           ('CS', 'SPI_CE0', 'input'), ('SCK', 'SPI_SCLK', 'input')]

    for pin, net, shape in spi:
        if pin in U2_PINS_MILS:
            x_mils, y_mils = U2_PINS_MILS[pin]
            x = mils_to_mm(x_mils)
            y = mils_to_mm(y_mils)
            wire_end_x = mils_to_mm(x_mils - WIRE_LEN)

            wire = create_wire(x, y, wire_end_x, y)
            label = create_global_label(net, wire_end_x, y, 180, shape)
            new_elements.extend([wire, label])
            print(f"  U2.{pin}: {net}")

    # CAN/INT connections (right side pins - wire goes right)
    can_pins = [('TXCAN', 'CAN_TX', 'output'), ('RXCAN', 'CAN_RX', 'input'),
                ('INT', 'CAN_INT', 'output')]

    for pin, net, shape in can_pins:
        if pin in U2_PINS_MILS:
            x_mils, y_mils = U2_PINS_MILS[pin]
            x = mils_to_mm(x_mils)
            y = mils_to_mm(y_mils)
            wire_end_x = mils_to_mm(x_mils + WIRE_LEN)

            wire = create_wire(x, y, wire_end_x, y)
            label = create_global_label(net, wire_end_x, y, 0, shape)
            new_elements.extend([wire, label])
            print(f"  U2.{pin}: {net}")

    # TXnRTS pins - tie to +3.3V (active low, we don't use them)
    for pin in ['TX0RTS', 'TX1RTS', 'TX2RTS']:
        if pin in U2_PINS_MILS:
            x_mils, y_mils = U2_PINS_MILS[pin]
            x = mils_to_mm(x_mils)
            y = mils_to_mm(y_mils)
            wire_end_x = mils_to_mm(x_mils + WIRE_LEN)

            wire = create_wire(x, y, wire_end_x, y)
            label = create_global_label("+3.3V", wire_end_x, y, 0, "passive")
            new_elements.extend([wire, label])
            print(f"  U2.{pin}: +3.3V (tied high)")

    # RXnBF pins - no connect (buffer full outputs, unused)
    for pin in ['RX0BF', 'RX1BF']:
        if pin in U2_PINS_MILS:
            x_mils, y_mils = U2_PINS_MILS[pin]
            nc = create_no_connect(mils_to_mm(x_mils), mils_to_mm(y_mils))
            new_elements.append(nc)
            print(f"  U2.{pin}: no-connect")

    # Oscillator pins
    for pin in ['OSC1', 'OSC2']:
        if pin in U2_PINS_MILS:
            x_mils, y_mils = U2_PINS_MILS[pin]
            x = mils_to_mm(x_mils)
            y = mils_to_mm(y_mils)
            wire_end_x = mils_to_mm(x_mils - WIRE_LEN)

            wire = create_wire(x, y, wire_end_x, y)
            label = create_global_label(pin, wire_end_x, y, 180, "passive")
            new_elements.extend([wire, label])
            print(f"  U2.{pin}: {pin}")

    # =========================================================================
    # SECTION 3: SN65HVD230 (U3)
    # =========================================================================
    print("\n--- Section 3: SN65HVD230 (U3) ---")

    # D and R pins (left side)
    u3_signals = [('D', 'CAN_TX', 'input'), ('R', 'CAN_RX', 'output')]
    for pin, net, shape in u3_signals:
        if pin in U3_PINS_MILS:
            x_mils, y_mils = U3_PINS_MILS[pin]
            x = mils_to_mm(x_mils)
            y = mils_to_mm(y_mils)
            wire_end_x = mils_to_mm(x_mils - WIRE_LEN)

            wire = create_wire(x, y, wire_end_x, y)
            label = create_global_label(net, wire_end_x, y, 180, shape)
            new_elements.extend([wire, label])
            print(f"  U3.{pin}: {net}")

    # CANH/CANL outputs (right side, through inductors L1/L2)
    for pin, net in [('CANH', 'CANH'), ('CANL', 'CANL')]:
        if pin in U3_PINS_MILS:
            x_mils, y_mils = U3_PINS_MILS[pin]
            x = mils_to_mm(x_mils)
            y = mils_to_mm(y_mils)
            wire_end_x = mils_to_mm(x_mils + WIRE_LEN)

            wire = create_wire(x, y, wire_end_x, y)
            label = create_global_label(net, wire_end_x, y, 0, "bidirectional")
            new_elements.extend([wire, label])
            print(f"  U3.{pin}: {net}")

    # Vref - no connect (reference output, not used)
    if 'Vref' in U3_PINS_MILS:
        x_mils, y_mils = U3_PINS_MILS['Vref']
        nc = create_no_connect(mils_to_mm(x_mils), mils_to_mm(y_mils))
        new_elements.append(nc)
        print(f"  U3.Vref: no-connect")

    # =========================================================================
    # SECTION 4: Crystal (Y1)
    # =========================================================================
    print("\n--- Section 4: Crystal (Y1) ---")

    x1_mils, y1_mils = Y1_PINS_MILS['pin1']
    x = mils_to_mm(x1_mils)
    y = mils_to_mm(y1_mils)
    wire_end_x = mils_to_mm(x1_mils - WIRE_LEN)

    wire = create_wire(x, y, wire_end_x, y)
    label = create_global_label("OSC1", wire_end_x, y, 180, "passive")
    new_elements.extend([wire, label])
    print(f"  Y1.1: OSC1")

    x2_mils, y2_mils = Y1_PINS_MILS['pin2']
    x = mils_to_mm(x2_mils)
    y = mils_to_mm(y2_mils)
    wire_end_x = mils_to_mm(x2_mils + WIRE_LEN)

    wire = create_wire(x, y, wire_end_x, y)
    label = create_global_label("OSC2", wire_end_x, y, 0, "passive")
    new_elements.extend([wire, label])
    print(f"  Y1.2: OSC2")

    # =========================================================================
    # SECTION 5: CAN Connectors
    # =========================================================================
    print("\n--- Section 5: CAN Connectors ---")

    # J3 Screw Terminal
    for pin_name, net in [('pin1', 'CANH'), ('pin2', 'CANL')]:
        x_mils, y_mils = J3_PINS_MILS[pin_name]
        x = mils_to_mm(x_mils)
        y = mils_to_mm(y_mils)
        wire_end_x = mils_to_mm(x_mils - WIRE_LEN)

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label(net, wire_end_x, y, 180, "bidirectional")
        new_elements.extend([wire, label])
        print(f"  J3.{pin_name}: {net}")

    # J2 OBD-II (Pin 6 = CANH, Pin 14 = CANL)
    for pin, net in [(6, 'CANH'), (14, 'CANL')]:
        x_mils, y_mils = get_j2_pin_mils(pin)
        x = mils_to_mm(x_mils)
        y = mils_to_mm(y_mils)
        wire_end_x = mils_to_mm(x_mils - WIRE_LEN)

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label(net, wire_end_x, y, 180, "bidirectional")
        new_elements.extend([wire, label])
        print(f"  J2.{pin}: {net}")

    # J2 unused pins - no connect
    used_j2 = [6, 14]
    for pin in range(1, 17):
        if pin not in used_j2:
            x_mils, y_mils = get_j2_pin_mils(pin)
            nc = create_no_connect(mils_to_mm(x_mils), mils_to_mm(y_mils))
            new_elements.append(nc)
    print(f"  {16 - len(used_j2)} J2 pins marked no-connect")

    # =========================================================================
    # SECTION 6: Power Distribution (U1 AMS1117)
    # =========================================================================
    print("\n--- Section 6: U1 AMS1117 Power ---")

    # VI -> +5V
    x_mils, y_mils = U1_PINS_MILS['VI']
    x = mils_to_mm(x_mils)
    y = mils_to_mm(y_mils)
    wire_end_x = mils_to_mm(x_mils - WIRE_LEN)

    wire = create_wire(x, y, wire_end_x, y)
    label = create_global_label("+5V", wire_end_x, y, 180, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.VI: +5V")

    # VO -> +3.3V
    x_mils, y_mils = U1_PINS_MILS['VO']
    x = mils_to_mm(x_mils)
    y = mils_to_mm(y_mils)
    wire_end_x = mils_to_mm(x_mils + WIRE_LEN)

    wire = create_wire(x, y, wire_end_x, y)
    label = create_global_label("+3.3V", wire_end_x, y, 0, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.VO: +3.3V")

    # GND
    x_mils, y_mils = U1_PINS_MILS['GND']
    x = mils_to_mm(x_mils)
    y = mils_to_mm(y_mils)
    wire_end_y = mils_to_mm(y_mils + WIRE_LEN)

    wire = create_wire(x, y, x, wire_end_y)
    label = create_global_label("GND", x, wire_end_y, 90, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.GND: GND")

    # =========================================================================
    # SECTION 7: PWR_FLAG
    # =========================================================================
    print("\n--- Section 7: PWR_FLAG ---")

    # PWR_FLAG for +5V at GPIO header
    x_mils, y_mils = get_j1_pin_mils(2)
    pf_x = mils_to_mm(x_mils + 400)  # 400 mils to the right
    pf_y = mils_to_mm(y_mils - 200)  # 200 mils up

    pwr_flag = create_pwr_flag(pf_x, pf_y, pwr_flag_num)
    wire = create_wire(pf_x, pf_y, pf_x, mils_to_mm(y_mils))
    label2 = create_global_label("+5V", pf_x, mils_to_mm(y_mils), 0, "passive")
    new_elements.extend([pwr_flag, wire, label2])
    print(f"  PWR_FLAG #{pwr_flag_num}: +5V")
    pwr_flag_num += 1

    # PWR_FLAG for +3.3V at U1 output
    x_mils, y_mils = U1_PINS_MILS['VO']
    pf_x = mils_to_mm(x_mils + 400)
    pf_y = mils_to_mm(y_mils - 200)

    pwr_flag = create_pwr_flag(pf_x, pf_y, pwr_flag_num)
    wire = create_wire(pf_x, pf_y, pf_x, mils_to_mm(y_mils))
    label2 = create_global_label("+3.3V", pf_x, mils_to_mm(y_mils), 0, "passive")
    new_elements.extend([pwr_flag, wire, label2])
    print(f"  PWR_FLAG #{pwr_flag_num}: +3.3V")
    pwr_flag_num += 1

    # PWR_FLAG for GND
    x_mils, y_mils = U1_PINS_MILS['GND']
    pf_x = mils_to_mm(x_mils + 200)
    pf_y = mils_to_mm(y_mils + 400)

    pwr_flag = create_pwr_flag(pf_x, pf_y, pwr_flag_num)
    wire = create_wire(pf_x, pf_y, mils_to_mm(x_mils), mils_to_mm(y_mils + WIRE_LEN))
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
    print("\nRun ERC in KiCad to verify")
    print("=" * 70)


if __name__ == "__main__":
    fix_can_hat_v3()
