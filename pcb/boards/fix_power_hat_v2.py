#!/usr/bin/env python3
"""
Complete fix for Power HAT schematic - Version 2.

Fixes J2 Pi header connections using CORRECT pin positions based on
Conn_02x20_Odd_Even symbol definition.
"""

import re
import uuid
from pathlib import Path

# J2 symbol position in schematic
J2_X = 200.0
J2_Y = 150.0

# Pin offsets from Conn_02x20_Odd_Even symbol definition
# Odd pins (left column): x = -5.08, direction 0
# Even pins (right column): x = +7.62, direction 180
ODD_PIN_X_OFFSET = -5.08
EVEN_PIN_X_OFFSET = 7.62

# Y offsets for pins (starting from pin 1/2 at top)
# Pins 1,2 at y=22.86, decreasing by 2.54 for each row
PIN_Y_OFFSETS = {
    1: 22.86, 2: 22.86,
    3: 20.32, 4: 20.32,
    5: 17.78, 6: 17.78,
    7: 15.24, 8: 15.24,
    9: 12.70, 10: 12.70,
    11: 10.16, 12: 10.16,
    13: 7.62, 14: 7.62,
    15: 5.08, 16: 5.08,
    17: 2.54, 18: 2.54,
    19: 0.00, 20: 0.00,
    21: -2.54, 22: -2.54,
    23: -5.08, 24: -5.08,
    25: -7.62, 26: -7.62,
    27: -10.16, 28: -10.16,
    29: -12.70, 30: -12.70,
    31: -15.24, 32: -15.24,
    33: -17.78, 34: -17.78,
    35: -20.32, 36: -20.32,
    37: -22.86, 38: -22.86,
    39: -25.40, 40: -25.40,
}

# Raspberry Pi GPIO header pinout for Power HAT
# Pin number -> (signal_name or None for NC, label_type)
PI_PINOUT = {
    1: ('+3.3V', 'power'),
    2: ('+5V', 'power'),
    3: (None, 'nc'),      # GPIO2 SDA
    4: ('+5V', 'power'),
    5: (None, 'nc'),      # GPIO3 SCL
    6: ('GND', 'power'),
    7: (None, 'nc'),      # GPIO4
    8: (None, 'nc'),      # GPIO14 TXD
    9: ('GND', 'power'),
    10: (None, 'nc'),     # GPIO15 RXD
    11: (None, 'nc'),     # GPIO17
    12: (None, 'nc'),     # GPIO18
    13: (None, 'nc'),     # GPIO27
    14: ('GND', 'power'),
    15: ('SHUTDOWN_REQ', 'signal'),  # GPIO22 - shutdown signal to Pi
    16: (None, 'nc'),     # GPIO23
    17: ('+3.3V', 'power'),
    18: (None, 'nc'),     # GPIO24
    19: (None, 'nc'),     # GPIO10 MOSI - not used on Power HAT
    20: ('GND', 'power'),
    21: (None, 'nc'),     # GPIO9 MISO
    22: (None, 'nc'),     # GPIO25
    23: (None, 'nc'),     # GPIO11 SCLK
    24: (None, 'nc'),     # GPIO8 CE0
    25: ('GND', 'power'),
    26: (None, 'nc'),     # GPIO7 CE1
    27: (None, 'nc'),     # ID_SD EEPROM
    28: (None, 'nc'),     # ID_SC EEPROM
    29: (None, 'nc'),     # GPIO5
    30: ('GND', 'power'),
    31: (None, 'nc'),     # GPIO6
    32: (None, 'nc'),     # GPIO12 PWM
    33: (None, 'nc'),     # GPIO13 PWM
    34: ('GND', 'power'),
    35: (None, 'nc'),     # GPIO19
    36: (None, 'nc'),     # GPIO16
    37: (None, 'nc'),     # GPIO26
    38: (None, 'nc'),     # GPIO20
    39: ('GND', 'power'),
    40: (None, 'nc'),     # GPIO21
}


def get_pin_position(pin_num):
    """Calculate actual pin position in schematic coordinates."""
    y_offset = PIN_Y_OFFSETS[pin_num]

    if pin_num % 2 == 1:  # Odd pin (left column)
        x = J2_X + ODD_PIN_X_OFFSET
    else:  # Even pin (right column)
        x = J2_X + EVEN_PIN_X_OFFSET

    # In KiCad schematic, Y offset is subtracted (Y increases downward in symbol coords)
    y = J2_Y - y_offset

    return (x, y)


def generate_uuid():
    """Generate a KiCad-style UUID."""
    return str(uuid.uuid4())


def create_wire(x1, y1, x2, y2):
    """Create a KiCad wire S-expression."""
    uid = generate_uuid()
    return f'''	(wire
		(pts
			(xy {x1} {y1}) (xy {x2} {y2})
		)
		(stroke
			(width 0)
			(type default)
		)
		(uuid "{uid}")
	)'''


def create_label(name, x, y, direction=0):
    """Create a KiCad label S-expression."""
    uid = generate_uuid()
    # Adjust justification based on direction
    if direction == 180:
        justify = "right"
    else:
        justify = "left"

    return f'''	(label "{name}"
		(at {x} {y} {direction})
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify {justify} bottom)
		)
		(uuid "{uid}")
	)'''


def create_global_label(name, x, y, direction=0, shape="passive"):
    """Create a KiCad global_label S-expression."""
    uid = generate_uuid()
    if direction == 180:
        justify = "right"
    else:
        justify = "left"

    return f'''	(global_label "{name}"
		(shape {shape})
		(at {x} {y} {direction})
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify {justify})
		)
		(uuid "{uid}")
	)'''


def create_no_connect(x, y):
    """Create a KiCad no_connect S-expression."""
    uid = generate_uuid()
    return f'''	(no_connect
		(at {x} {y})
		(uuid "{uid}")
	)'''


def read_schematic(filepath):
    """Read the schematic file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_schematic(filepath, content):
    """Write the schematic file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {filepath}")


def remove_old_j2_elements(content):
    """Remove old incorrectly-placed J2 connection elements."""
    lines = content.split('\n')
    result_lines = []
    skip_block = False
    paren_depth = 0
    removed_count = 0

    # Positions that were incorrectly added (around 197.46, 150 to 202.54, 200)
    bad_x_range = (190, 220)
    bad_y_range = (145, 210)

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for wire, label, global_label, no_connect, or PWR_FLAG symbol blocks
        if any(line.strip().startswith(x) for x in ['(wire', '(label', '(global_label', '(no_connect']):
            # Look for position in this block
            block_lines = [line]
            paren_depth = line.count('(') - line.count(')')
            i += 1

            while i < len(lines) and paren_depth > 0:
                block_lines.append(lines[i])
                paren_depth += lines[i].count('(') - lines[i].count(')')
                i += 1

            block = '\n'.join(block_lines)

            # Check if position is in the bad range
            pos_match = re.search(r'\(at\s+([\d.]+)\s+([\d.]+)', block)
            xy_match = re.search(r'\(xy\s+([\d.]+)\s+([\d.]+)', block)

            is_bad = False
            if pos_match:
                x, y = float(pos_match.group(1)), float(pos_match.group(2))
                if bad_x_range[0] <= x <= bad_x_range[1] and bad_y_range[0] <= y <= bad_y_range[1]:
                    is_bad = True
            if xy_match and not is_bad:
                x, y = float(xy_match.group(1)), float(xy_match.group(2))
                if bad_x_range[0] <= x <= bad_x_range[1] and bad_y_range[0] <= y <= bad_y_range[1]:
                    is_bad = True

            if is_bad:
                removed_count += 1
                continue

            result_lines.extend(block_lines)
            continue

        # Check for PWR_FLAG symbols (our bad ones have specific reference patterns)
        if line.strip().startswith('(symbol') and i + 1 < len(lines):
            block_lines = [line]
            paren_depth = line.count('(') - line.count(')')
            i += 1

            while i < len(lines) and paren_depth > 0:
                block_lines.append(lines[i])
                paren_depth += lines[i].count('(') - lines[i].count(')')
                i += 1

            block = '\n'.join(block_lines)

            # Check if this is a PWR_FLAG we added (at positions around 215, 150-160)
            if 'power:PWR_FLAG' in block:
                pos_match = re.search(r'\(at\s+([\d.]+)\s+([\d.]+)', block)
                if pos_match:
                    x, y = float(pos_match.group(1)), float(pos_match.group(2))
                    if 210 <= x <= 220 and 145 <= y <= 165:
                        removed_count += 1
                        continue

            result_lines.extend(block_lines)
            continue

        result_lines.append(line)
        i += 1

    return '\n'.join(result_lines), removed_count


def find_insert_position(content):
    """Find position to insert new elements (before sheet_instances)."""
    match = re.search(r'\n\t\(sheet_instances', content)
    if match:
        return match.start()
    return len(content) - 2  # Before final closing paren


def fix_power_hat():
    """Main function to fix the Power HAT schematic."""
    script_dir = Path(__file__).parent
    power_hat_sch = script_dir / "power-hat" / "power-hat.kicad_sch"

    if not power_hat_sch.exists():
        print(f"Error: {power_hat_sch} not found")
        return

    print("=" * 60)
    print("Power HAT Fix - Version 2 (Correct Pin Positions)")
    print("=" * 60)

    # Read schematic
    content = read_schematic(power_hat_sch)
    print(f"Read {len(content)} bytes")

    # Step 1: Remove old incorrectly-placed elements
    print("\n1. Removing old incorrectly-placed elements...")
    content, removed = remove_old_j2_elements(content)
    print(f"   Removed {removed} elements")

    # Step 2: Generate new elements at correct positions
    print("\n2. Generating J2 connections at correct pin positions...")
    new_elements = []

    labels_added = 0
    nc_added = 0

    for pin_num, (signal, label_type) in PI_PINOUT.items():
        x, y = get_pin_position(pin_num)

        if label_type == 'nc':
            # Add no-connect directly at pin position
            nc = create_no_connect(x, y)
            new_elements.append(nc)
            nc_added += 1
        else:
            # Add wire and label
            if pin_num % 2 == 1:  # Odd pin (left side)
                wire_end_x = x - 5
                direction = 0
            else:  # Even pin (right side)
                wire_end_x = x + 5
                direction = 180

            wire = create_wire(x, y, wire_end_x, y)
            new_elements.append(wire)

            # Use global labels for power signals
            label = create_global_label(signal, wire_end_x, y, direction, "passive")
            new_elements.append(label)
            labels_added += 1

            if label_type == 'power':
                print(f"   Pin {pin_num}: {signal} at ({x:.2f}, {y:.2f})")
            else:
                print(f"   Pin {pin_num}: {signal} (signal) at ({x:.2f}, {y:.2f})")

    print(f"\n   Added {labels_added} labels, {nc_added} no-connects")

    # Step 3: Insert new elements
    print("\n3. Inserting new elements into schematic...")
    insert_pos = find_insert_position(content)
    new_content = '\n'.join(new_elements)
    content = content[:insert_pos] + '\n' + new_content + '\n' + content[insert_pos:]

    # Write updated schematic
    write_schematic(power_hat_sch, content)

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open power-hat.kicad_sch in KiCad")
    print("2. Run ERC to verify J2 is now connected")
    print("3. Add PWR_FLAG symbols near the power connections")
    print("4. Fix remaining component connections (J1, F1, U1, U3, etc.)")


if __name__ == "__main__":
    fix_power_hat()
