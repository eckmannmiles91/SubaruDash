#!/usr/bin/env python3
"""
Fix Power HAT v18: Restore Q2_GATE and R6_OUT labels

v17 incorrectly removed these labels thinking they were orphans, but they're
actually connected to R9 and R4 pins. Restore them.

ERC_23 errors:
- R9 Pin 2 at (17500 mils, 7650 mils) = (444.5, 194.31) - needs Q2_GATE
- R4 Pin 2 at (12500 mils, 20150 mils) = (317.5, 511.81) - needs R6_OUT
"""

import re
import shutil
import uuid
from pathlib import Path

def generate_uuid():
    return str(uuid.uuid4())

def create_global_label(name, x, y, orientation=0, justify="left"):
    """Create a global label."""
    return f'''	(global_label "{name}"
		(shape input)
		(at {x} {y} {orientation})
		(fields_autoplaced yes)
		(effects
			(font
				(size 1.27 1.27)
			)
			(justify {justify})
		)
		(uuid "{generate_uuid()}")
		(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
	)'''

def main():
    schematic_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_sch")

    # Create backup
    backup_path = schematic_path.parent / "power-hat-BACKUP18.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"Created backup: {backup_path}")

    content = schematic_path.read_text(encoding='utf-8')

    # Restore Q2_GATE at R9 Pin 2 position
    # ERC: (17500 mils, 7650 mils) = (444.5, 194.31)
    q2_gate_label = create_global_label("Q2_GATE", 444.5, 194.31, 0, "left")

    # Restore R6_OUT at R4 Pin 2 position
    # ERC: (12500 mils, 20150 mils) = (317.5, 511.81)
    r6_out_label = create_global_label("R6_OUT", 317.5, 511.81, 0, "left")

    # Find insertion point after last global_label
    label_pattern = r'(\t\(global_label "[^"]+"\s*\n.*?\n\t\))'
    matches = list(re.finditer(label_pattern, content, re.DOTALL))

    if matches:
        insert_pos = matches[-1].end()
        content = content[:insert_pos] + "\n" + q2_gate_label + "\n" + r6_out_label + content[insert_pos:]
        print("Restored Q2_GATE label at (444.5, 194.31)")
        print("Restored R6_OUT label at (317.5, 511.81)")

    # Write updated schematic
    schematic_path.write_text(content, encoding='utf-8')
    print(f"\nUpdated schematic: {schematic_path}")

if __name__ == "__main__":
    main()
