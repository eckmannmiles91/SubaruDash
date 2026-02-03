#!/usr/bin/env python3
"""
Fix Power HAT v13: Add no_connect symbols for U3 pins 5 and 6

ERC_19 shows 2 errors after removing orphan labels:
1. U3 Pin 5 [AREF/PB0] at (269.24, 500.38) - not connected
2. U3 Pin 6 [PB1] at (269.24, 502.92) - not connected

These ATtiny85 GPIO pins are intentionally unused. Add no_connect markers.
"""

import re
import shutil
import uuid
from pathlib import Path

def generate_uuid():
    return str(uuid.uuid4())

def create_no_connect(x, y):
    """Create a no_connect symbol at the given position."""
    return f'''	(no_connect
		(at {x} {y})
		(uuid "{generate_uuid()}")
	)'''

def main():
    schematic_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_sch")

    # Create backup
    backup_path = schematic_path.parent / "power-hat-BACKUP13.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Read schematic
    content = schematic_path.read_text(encoding='utf-8')

    # Pin positions (from ERC report: mils converted to mm)
    # 10600 mils = 269.24 mm, 19700 mils = 500.38 mm, 19800 mils = 502.92 mm
    pin5_pos = (269.24, 500.38)  # U3 Pin 5 - PB0
    pin6_pos = (269.24, 502.92)  # U3 Pin 6 - PB1

    # Create no_connect symbols
    nc_pin5 = create_no_connect(pin5_pos[0], pin5_pos[1])
    nc_pin6 = create_no_connect(pin6_pos[0], pin6_pos[1])

    # Find a good place to insert - after existing no_connect symbols
    # Look for the last no_connect block
    no_connect_pattern = r'(\t\(no_connect\s*\n\t\t\(at [^\)]+\)\s*\n\t\t\(uuid "[^"]+"\)\s*\n\t\))'
    matches = list(re.finditer(no_connect_pattern, content))

    if matches:
        # Insert after the last no_connect
        last_match = matches[-1]
        insert_pos = last_match.end()
        content = content[:insert_pos] + "\n" + nc_pin5 + "\n" + nc_pin6 + content[insert_pos:]
        print(f"Added no_connect at ({pin5_pos[0]}, {pin5_pos[1]}) for U3 Pin 5 (PB0)")
        print(f"Added no_connect at ({pin6_pos[0]}, {pin6_pos[1]}) for U3 Pin 6 (PB1)")
    else:
        print("ERROR: Could not find existing no_connect symbols to insert after")
        print("Trying alternate insertion point...")

        # Try inserting before the first (wire block
        wire_match = re.search(r'\n\t\(wire\s*\n', content)
        if wire_match:
            insert_pos = wire_match.start()
            content = content[:insert_pos] + "\n" + nc_pin5 + "\n" + nc_pin6 + content[insert_pos:]
            print(f"Added no_connect symbols before wire section")
        else:
            print("ERROR: Could not find suitable insertion point")
            return

    # Write updated schematic
    schematic_path.write_text(content, encoding='utf-8')
    print(f"\nUpdated schematic saved: {schematic_path}")
    print("Please run ERC in KiCad to verify fixes.")

if __name__ == "__main__":
    main()
