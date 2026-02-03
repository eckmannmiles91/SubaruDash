#!/usr/bin/env python3
"""
CAN HAT Fix Script - Version 5.

Uses EXACT coordinates from working Power HAT schematic.
Key discovery: Pin 1 y position is 127.14, NOT 127.15!

GPIO Header (J1/J2) at (200, 150):
- Odd pins (1,3,5...39): x = 194.92
- Even pins (2,4,6...40): x = 207.62
- Pin 1/2 y = 127.14
- Row pitch = 2.54 mm
"""

import uuid
import re
from pathlib import Path


def generate_uuid():
    """Generate a KiCad-style UUID."""
    return str(uuid.uuid4())


def create_wire(x1, y1, x2, y2):
    """Create a KiCad wire S-expression with exact coordinates."""
    uid = generate_uuid()
    # Format numbers: use integer if whole, otherwise 2 decimal places
    def fmt(v):
        if v == int(v):
            return str(int(v))
        return f"{v:.2f}"
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
    """Create a KiCad global label."""
    uid = generate_uuid()
    def fmt(v):
        if v == int(v):
            return str(int(v))
        return f"{v:.2f}"
    justify = "right" if direction == 180 else "left"
    return f'''\t(global_label "{name}"
\t\t(shape input)
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


def create_no_connect(x, y):
    """Create a KiCad no-connect flag."""
    uid = generate_uuid()
    def fmt(v):
        if v == int(v):
            return str(int(v))
        return f"{v:.2f}"
    return f'''\t(no_connect
\t\t(at {fmt(x)} {fmt(y)})
\t\t(uuid "{uid}")
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
# EXACT GPIO Pin Positions (from working Power HAT schematic)
# =============================================================================
def get_j1_pin_pos(pin_num):
    """
    Get J1 pin position in mm.
    EXACT values from working Power HAT schematic.
    """
    # Base Y position for pin 1/2 row
    y_base = 127.14
    row_pitch = 2.54

    if pin_num % 2 == 1:  # Odd pin (left side)
        x = 194.92
        row = (pin_num - 1) // 2
    else:  # Even pin (right side)
        x = 207.62
        row = (pin_num - 2) // 2

    y = y_base + row * row_pitch
    return (x, y)


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
    # SPI pins (directly - no intermediary labels)
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
    print("CAN HAT Fix Script - Version 5 (EXACT Power HAT coordinates)")
    print("=" * 70)

    content = read_schematic(can_hat_sch)
    print(f"Read {len(content)} bytes")

    new_elements = []

    # =========================================================================
    # GPIO Header (J1) - Using EXACT working coordinates
    # =========================================================================
    print("\n--- Section 1: GPIO Header (J1) ---")

    for pin in range(1, 41):
        pin_x, pin_y = get_j1_pin_pos(pin)

        if pin in GPIO_ASSIGNMENTS:
            signal = GPIO_ASSIGNMENTS[pin]

            # Wire length: 5mm from pin
            if pin % 2 == 1:  # Odd pin - wire goes LEFT
                wire_end_x = pin_x - 5
                label_x = wire_end_x
                label_dir = 0  # Label arrow points right toward pin
            else:  # Even pin - wire goes RIGHT
                wire_end_x = pin_x + 5
                label_x = wire_end_x
                label_dir = 180  # Label arrow points left toward pin

            wire = create_wire(pin_x, pin_y, wire_end_x, pin_y)
            new_elements.append(wire)

            label = create_global_label(signal, label_x, pin_y, label_dir)
            new_elements.append(label)

            print(f"  Pin {pin} ({pin_x}, {pin_y}): {signal}")
        else:
            # Unused pin - no_connect at exact pin position
            nc = create_no_connect(pin_x, pin_y)
            new_elements.append(nc)

    print(f"  {40 - len(GPIO_ASSIGNMENTS)} pins marked no-connect")

    # =========================================================================
    # Insert elements
    # =========================================================================
    print("\n" + "=" * 70)
    print("Inserting elements...")

    insert_pos = find_insert_position(content)
    new_content = '\n'.join(new_elements)
    content = content[:insert_pos] + '\n' + new_content + '\n' + content[insert_pos:]

    write_schematic(can_hat_sch, content)

    print(f"\nAdded {len(new_elements)} new elements (GPIO only)")
    print("\n*** IMPORTANT ***")
    print("This v5 script ONLY connects the GPIO header.")
    print("After verifying GPIO connections work, run additional scripts for:")
    print("  - MCP2515 (U2) connections")
    print("  - SN65HVD230 (U3) connections")
    print("  - Crystal (Y1) connections")
    print("  - CAN bus connectors (J2, J3)")
    print("  - Power distribution (U1)")
    print("\nRun ERC in KiCad to verify GPIO connections")
    print("=" * 70)


if __name__ == "__main__":
    fix_can_hat()
