#!/usr/bin/env python3
"""
Complete fix for Power HAT schematic.

Adds labels to wire J2 Pi header pins, adds power flags, and removes orphan labels.
Based on Raspberry Pi GPIO pinout for power connections.
"""

import re
import uuid
from pathlib import Path

# Pi GPIO header pin assignments (standard Raspberry Pi pinout)
# Format: pin_number: (signal_name, connect_type)
# connect_type: 'label' for power/signal, 'nc' for no-connect
PI_HEADER_PINOUT = {
    # Power pins
    1: ('+3.3V', 'label'),
    2: ('+5V', 'label'),
    4: ('+5V', 'label'),
    17: ('+3.3V', 'label'),
    # Ground pins
    6: ('GND', 'label'),
    9: ('GND', 'label'),
    14: ('GND', 'label'),
    20: ('GND', 'label'),
    25: ('GND', 'label'),
    30: ('GND', 'label'),
    34: ('GND', 'label'),
    39: ('GND', 'label'),
    # GPIO pins - for Power HAT we'll add SHUTDOWN_REQ on one
    # Pin 22 = GPIO25 - SHUTDOWN_REQ (output from ATtiny85 to Pi)
    # All other GPIOs get no-connect
    3: (None, 'nc'),   # GPIO2 (SDA)
    5: (None, 'nc'),   # GPIO3 (SCL)
    7: (None, 'nc'),   # GPIO4
    8: (None, 'nc'),   # GPIO14 (TXD)
    10: (None, 'nc'),  # GPIO15 (RXD)
    11: (None, 'nc'),  # GPIO17
    12: (None, 'nc'),  # GPIO18
    13: (None, 'nc'),  # GPIO27
    15: ('SHUTDOWN_REQ', 'label'),  # GPIO22 - SHUTDOWN_REQ signal
    16: (None, 'nc'),  # GPIO23
    18: (None, 'nc'),  # GPIO24
    19: (None, 'nc'),  # GPIO10 (SPI_MOSI) - not used on Power HAT
    21: (None, 'nc'),  # GPIO9 (SPI_MISO) - not used on Power HAT
    22: (None, 'nc'),  # GPIO25
    23: (None, 'nc'),  # GPIO11 (SPI_SCLK) - not used on Power HAT
    24: (None, 'nc'),  # GPIO8 (SPI_CE0) - not used on Power HAT
    26: (None, 'nc'),  # GPIO7 (CE1)
    27: (None, 'nc'),  # ID_SD (EEPROM)
    28: (None, 'nc'),  # ID_SC (EEPROM)
    29: (None, 'nc'),  # GPIO5
    31: (None, 'nc'),  # GPIO6
    32: (None, 'nc'),  # GPIO12 (PWM0)
    33: (None, 'nc'),  # GPIO13 (PWM1)
    35: (None, 'nc'),  # GPIO19
    36: (None, 'nc'),  # GPIO16
    37: (None, 'nc'),  # GPIO26
    38: (None, 'nc'),  # GPIO20
    40: (None, 'nc'),  # GPIO21
}

# Labels that should NOT exist in Power HAT (they belong to CAN HAT or DAC)
INVALID_LABELS = {
    'SPI_MOSI', 'SPI_MISO', 'SPI_SCLK', 'SPI_CE0',
    'CAN_TX', 'CAN_RX', 'CAN_INT',
    'CANH', 'CANL', 'CANH_U5', 'CANL_U5',
    'OSC1', 'OSC2',
    'LED1_ANODE', 'LED2_ANODE', 'LED3_ANODE',
    'AUDIO_L_OUT', 'AUDIO_R_OUT', 'AUDIO_L+', 'AUDIO_L-', 'AUDIO_R+', 'AUDIO_R-',
}


def read_schematic(filepath):
    """Read the schematic file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_schematic(filepath, content):
    """Write the schematic file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {filepath}")


def generate_uuid():
    """Generate a KiCad-style UUID."""
    return str(uuid.uuid4())


def get_j2_pin_positions(j2_x, j2_y):
    """
    Calculate pin positions for a 02x20 connector at given position.
    Odd pins on left, even pins on right.
    Pin spacing: 2.54mm (100 mils)
    """
    positions = {}
    pin_spacing = 2.54  # mm

    for pin in range(1, 41):
        if pin % 2 == 1:  # Odd pins on left
            row = (pin - 1) // 2
            x = j2_x - 2.54  # Left side of connector
            y = j2_y + row * pin_spacing
        else:  # Even pins on right
            row = (pin - 2) // 2
            x = j2_x + 2.54  # Right side of connector
            y = j2_y + row * pin_spacing
        positions[pin] = (x, y)

    return positions


def create_label(name, x, y, direction=0):
    """Create a KiCad label S-expression."""
    uid = generate_uuid()
    return f'''	(label "{name}"
		(at {x} {y} {direction})
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left bottom)
		)
		(uuid "{uid}")
	)'''


def create_global_label(name, x, y, direction=0, shape="output"):
    """Create a KiCad global_label S-expression."""
    uid = generate_uuid()
    # Adjust shape based on signal type
    if name in ['+5V', '+3.3V', 'GND']:
        shape = "passive"
    elif name == 'SHUTDOWN_REQ':
        shape = "output"

    return f'''	(global_label "{name}"
		(shape {shape})
		(at {x} {y} {direction})
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify left)
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


def create_pwr_flag(x, y, net_name):
    """Create a PWR_FLAG symbol S-expression."""
    uid = generate_uuid()
    return f'''	(symbol
		(lib_id "power:PWR_FLAG")
		(at {x} {y} 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom no)
		(on_board yes)
		(dnp no)
		(uuid "{uid}")
		(property "Reference" "#FLG0{ord(net_name[0]) % 10}"
			(at {x} {y - 2} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Value" "PWR_FLAG"
			(at {x} {y + 2} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Datasheet" "~"
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Description" "Special symbol for telling ERC where power comes from"
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(pin "1"
			(uuid "{generate_uuid()}")
		)
	)'''


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


def remove_invalid_labels(content):
    """Remove labels that don't belong in Power HAT."""
    lines = content.split('\n')
    result_lines = []
    i = 0
    removed_count = 0

    while i < len(lines):
        line = lines[i]

        # Check if this starts a label or global_label block
        if line.strip().startswith('(label "') or line.strip().startswith('(global_label "'):
            # Extract the label name
            match = re.search(r'\((?:global_)?label\s+"([^"]+)"', line)
            if match:
                label_name = match.group(1)

                # Collect the entire block
                block_lines = [line]
                paren_depth = line.count('(') - line.count(')')
                i += 1

                while i < len(lines) and paren_depth > 0:
                    block_lines.append(lines[i])
                    paren_depth += lines[i].count('(') - lines[i].count(')')
                    i += 1

                # Decide whether to keep
                if label_name in INVALID_LABELS:
                    print(f"  Removing invalid label: {label_name}")
                    removed_count += 1
                    continue  # Skip this block
                else:
                    result_lines.extend(block_lines)
                continue

        result_lines.append(line)
        i += 1

    return '\n'.join(result_lines), removed_count


def find_insert_position(content):
    """Find position to insert new elements (before sheet_instances or at end)."""
    # Look for sheet_instances section
    match = re.search(r'\n\t\(sheet_instances', content)
    if match:
        return match.start()

    # Otherwise, find the last closing paren
    last_paren = content.rfind(')')
    return last_paren if last_paren > 0 else len(content)


def fix_power_hat():
    """Main function to fix the Power HAT schematic."""
    script_dir = Path(__file__).parent
    power_hat_sch = script_dir / "power-hat" / "power-hat.kicad_sch"

    if not power_hat_sch.exists():
        print(f"Error: {power_hat_sch} not found")
        return

    print("=" * 60)
    print("Power HAT Complete Fix")
    print("=" * 60)

    # Read schematic
    content = read_schematic(power_hat_sch)
    print(f"Read {len(content)} bytes")

    # Step 1: Remove invalid labels
    print("\n1. Removing invalid labels...")
    content, removed = remove_invalid_labels(content)
    print(f"   Removed {removed} invalid labels")

    # Step 2: Find J2 position
    print("\n2. Finding J2 Pi header position...")
    j2_match = re.search(r'\(symbol\s*\n\s*\(lib_id\s+"Connector_Generic:Conn_02x20_Odd_Even"\)\s*\n\s*\(at\s+([\d.]+)\s+([\d.]+)', content)
    if not j2_match:
        print("   Error: Could not find J2 position")
        return

    j2_x = float(j2_match.group(1))
    j2_y = float(j2_match.group(2))
    print(f"   J2 at position ({j2_x}, {j2_y})")

    # Calculate pin positions
    pin_positions = get_j2_pin_positions(j2_x, j2_y)

    # Step 3: Generate new elements
    print("\n3. Generating labels and no-connects for J2 pins...")
    new_elements = []

    labels_added = 0
    nc_added = 0

    for pin, (signal, connect_type) in PI_HEADER_PINOUT.items():
        x, y = pin_positions[pin]

        if connect_type == 'label' and signal:
            # For odd pins (left side), label goes to the left
            # For even pins (right side), label goes to the right
            if pin % 2 == 1:
                label_x = x - 5  # Offset to left
                direction = 0
            else:
                label_x = x + 5  # Offset to right
                direction = 180

            # Create a short wire to connect pin to label
            wire = create_wire(x, y, label_x, y)
            new_elements.append(wire)

            # Use global labels for signals that connect across the schematic
            label = create_global_label(signal, label_x, y, direction)
            new_elements.append(label)
            labels_added += 1
            print(f"   Pin {pin}: {signal}")
        elif connect_type == 'nc':
            nc = create_no_connect(x, y)
            new_elements.append(nc)
            nc_added += 1

    print(f"\n   Added {labels_added} labels, {nc_added} no-connects")

    # Step 4: Add PWR_FLAG symbols for power nets
    print("\n4. Adding PWR_FLAG symbols...")
    # Add PWR_FLAG near J2 for +5V, +3.3V, and GND
    pwr_flags = [
        ('+5V', j2_x + 15, j2_y),
        ('+3.3V', j2_x + 15, j2_y + 5),
        ('GND', j2_x + 15, j2_y + 10),
    ]

    for net, x, y in pwr_flags:
        pwr_flag = create_pwr_flag(x, y, net)
        new_elements.append(pwr_flag)

        # Add a wire and label to connect PWR_FLAG
        wire = create_wire(x, y, x + 3, y)
        new_elements.append(wire)

        label = create_global_label(net, x + 3, y, 0)
        new_elements.append(label)
        print(f"   PWR_FLAG for {net}")

    # Step 5: Insert new elements into schematic
    print("\n5. Inserting new elements into schematic...")
    insert_pos = find_insert_position(content)

    new_content = '\n'.join(new_elements)
    content = content[:insert_pos] + '\n' + new_content + '\n' + content[insert_pos:]

    # Step 6: Ensure lib_symbols has PWR_FLAG
    print("\n6. Adding PWR_FLAG to lib_symbols if needed...")
    if 'power:PWR_FLAG' not in content:
        # Add PWR_FLAG library symbol
        pwr_flag_lib = '''
	(symbol "power:PWR_FLAG"
		(power)
		(pin_numbers hide)
		(pin_names
			(offset 0) hide)
		(exclude_from_sim no)
		(in_bom no)
		(on_board yes)
		(property "Reference" "#FLG"
			(at 0 1.905 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Value" "PWR_FLAG"
			(at 0 3.81 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" ""
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Datasheet" "~"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Description" "Special symbol for telling ERC where power comes from"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "ki_keywords" "flag power"
			(at 0 0 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(symbol "PWR_FLAG_0_0"
			(pin power_out line
				(at 0 0 90)
				(length 0)
				(name "pwr"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
				(number "1"
					(effects
						(font
							(size 1.27 1.27)
						)
					)
				)
			)
		)
		(symbol "PWR_FLAG_0_1"
			(polyline
				(pts
					(xy 0 0) (xy 0 1.27) (xy -1.016 1.905) (xy 0 2.54) (xy 1.016 1.905) (xy 0 1.27)
				)
				(stroke
					(width 0)
					(type default)
				)
				(fill
					(type none)
				)
			)
		)
	)'''

        # Insert after (lib_symbols line
        lib_match = re.search(r'\(lib_symbols\n', content)
        if lib_match:
            insert_at = lib_match.end()
            content = content[:insert_at] + pwr_flag_lib + '\n' + content[insert_at:]
            print("   Added PWR_FLAG library symbol")

    # Write updated schematic
    write_schematic(power_hat_sch, content)

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open power-hat.kicad_sch in KiCad")
    print("2. Run ERC to verify remaining issues")
    print("3. Fix any remaining disconnected component pins manually")
    print("4. Verify all power connections are correct")


if __name__ == "__main__":
    fix_power_hat()
