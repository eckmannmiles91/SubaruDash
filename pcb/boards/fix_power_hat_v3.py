#!/usr/bin/env python3
"""
Add PWR_FLAG symbols to Power HAT schematic - Version 3.

Adds PWR_FLAG symbols to fix "power pin not driven" ERC errors.
"""

import re
import uuid
from pathlib import Path


def generate_uuid():
    """Generate a KiCad-style UUID."""
    return str(uuid.uuid4())


def create_pwr_flag_symbol(x, y, ref_num):
    """Create a PWR_FLAG symbol S-expression."""
    uid = generate_uuid()
    pin_uid = generate_uuid()
    return f'''	(symbol
		(lib_id "power:PWR_FLAG")
		(at {x} {y} 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom no)
		(on_board yes)
		(dnp no)
		(uuid "{uid}")
		(property "Reference" "#FLG{ref_num:02d}"
			(at {x} {y - 2.54} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Value" "PWR_FLAG"
			(at {x} {y + 2.54} 0)
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
			(uuid "{pin_uid}")
		)
		(instances
			(project "power-hat"
				(path "/29b54e26-6a52-4b51-8c39-076401b40ee9"
					(reference "#FLG{ref_num:02d}")
					(unit 1)
				)
			)
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


def create_global_label(name, x, y, direction=0):
    """Create a KiCad global_label S-expression."""
    uid = generate_uuid()
    if direction == 180:
        justify = "right"
    else:
        justify = "left"

    return f'''	(global_label "{name}"
		(shape passive)
		(at {x} {y} {direction})
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify {justify})
		)
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


def ensure_pwr_flag_lib_symbol(content):
    """Ensure PWR_FLAG library symbol exists in lib_symbols section."""
    if 'power:PWR_FLAG' in content and '(symbol "power:PWR_FLAG"' in content:
        print("   PWR_FLAG library symbol already exists")
        return content

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

    # Find end of lib_symbols section
    lib_symbols_match = re.search(r'\(lib_symbols\n', content)
    if lib_symbols_match:
        # Find the closing of lib_symbols section
        # Count parentheses to find where lib_symbols ends
        start = lib_symbols_match.start()
        depth = 0
        i = start
        found_start = False
        while i < len(content):
            if content[i] == '(':
                depth += 1
                found_start = True
            elif content[i] == ')':
                depth -= 1
                if found_start and depth == 0:
                    # Insert before closing paren of lib_symbols
                    content = content[:i] + pwr_flag_lib + '\n\t' + content[i:]
                    print("   Added PWR_FLAG library symbol")
                    break
            i += 1

    return content


def find_insert_position(content):
    """Find position to insert new elements (before sheet_instances)."""
    match = re.search(r'\n\t\(sheet_instances', content)
    if match:
        return match.start()
    return len(content) - 2


def fix_power_hat():
    """Main function to add PWR_FLAG symbols."""
    script_dir = Path(__file__).parent
    power_hat_sch = script_dir / "power-hat" / "power-hat.kicad_sch"

    if not power_hat_sch.exists():
        print(f"Error: {power_hat_sch} not found")
        return

    print("=" * 60)
    print("Power HAT Fix - Version 3 (PWR_FLAG Symbols)")
    print("=" * 60)

    # Read schematic
    content = read_schematic(power_hat_sch)
    print(f"Read {len(content)} bytes")

    # Step 1: Ensure PWR_FLAG library symbol exists
    print("\n1. Checking PWR_FLAG library symbol...")
    content = ensure_pwr_flag_lib_symbol(content)

    # Step 2: Add PWR_FLAG symbols near power nets
    # We'll place them near the J2 power labels we added
    # J2 Pin 2 (+5V): (207.62, 127.14) -> place PWR_FLAG at (215, 127.14)
    # J2 Pin 1 (+3.3V): (194.92, 127.14) -> place PWR_FLAG at (185, 127.14)
    # J2 Pin 6 (GND): (207.62, 132.22) -> place PWR_FLAG at (215, 132.22)

    print("\n2. Adding PWR_FLAG symbols for power nets...")
    new_elements = []

    # PWR_FLAG for +5V (near J2 pin 2)
    pwr_flag_5v = create_pwr_flag_symbol(218, 127.14, 1)
    wire_5v = create_wire(212.62, 127.14, 218, 127.14)
    new_elements.append(pwr_flag_5v)
    new_elements.append(wire_5v)
    print("   Added PWR_FLAG for +5V at (218, 127.14)")

    # PWR_FLAG for +3.3V (near J2 pin 1)
    pwr_flag_3v3 = create_pwr_flag_symbol(183, 127.14, 2)
    wire_3v3 = create_wire(189.92, 127.14, 183, 127.14)
    new_elements.append(pwr_flag_3v3)
    new_elements.append(wire_3v3)
    print("   Added PWR_FLAG for +3.3V at (183, 127.14)")

    # PWR_FLAG for GND (near J2 pin 6)
    pwr_flag_gnd = create_pwr_flag_symbol(218, 132.22, 3)
    wire_gnd = create_wire(212.62, 132.22, 218, 132.22)
    new_elements.append(pwr_flag_gnd)
    new_elements.append(wire_gnd)
    print("   Added PWR_FLAG for GND at (218, 132.22)")

    # Step 3: Insert new elements
    print("\n3. Inserting elements into schematic...")
    insert_pos = find_insert_position(content)
    new_content = '\n'.join(new_elements)
    content = content[:insert_pos] + '\n' + new_content + '\n' + content[insert_pos:]

    # Write updated schematic
    write_schematic(power_hat_sch, content)

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print("\nRemaining manual tasks in KiCad:")
    print("1. Connect J1 (12V input) pins to 12V_IGN label")
    print("2. Connect F1 (fuse) in the 12V path")
    print("3. Connect U1 VIN to 12V_FUSED, output to +5V")
    print("4. Connect U3 VCC to +3.3V")
    print("5. Wire any remaining floating components")


if __name__ == "__main__":
    fix_power_hat()
