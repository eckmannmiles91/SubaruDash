#!/usr/bin/env python3
"""
Fix Power HAT v16: Connect HEARTBEAT_LED and TIMER_LED using EXACT pin positions from ERC

ERC_21 shows actual pin positions:
- U3 Pin 5 at (10600 mils, 19700 mils) = (269.24, 500.38) mm
- U3 Pin 6 at (10600 mils, 19800 mils) = (269.24, 502.92) mm

J2 Pin positions (header at 200, 150):
- Pin 11 at approximately (196.19, 138.57) mm
- Pin 13 at approximately (196.19, 141.11) mm

This script removes all previous HEARTBEAT_LED/TIMER_LED labels and wires,
then adds properly positioned ones.
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

def create_wire(x1, y1, x2, y2):
    """Create a wire between two points."""
    return f'''	(wire
		(pts
			(xy {x1} {y1}) (xy {x2} {y2})
		)
		(stroke
			(width 0)
			(type default)
		)
		(uuid "{generate_uuid()}")
	)'''

def main():
    schematic_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_sch")

    # Create backup
    backup_path = schematic_path.parent / "power-hat-BACKUP16.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"Created backup: {backup_path}")

    content = schematic_path.read_text(encoding='utf-8')

    # Step 1: Remove ALL existing HEARTBEAT_LED and TIMER_LED global labels
    label_pattern = r'\t\(global_label "(HEARTBEAT_LED|TIMER_LED)".*?\n\t\)'
    matches = list(re.finditer(label_pattern, content, re.DOTALL))
    print(f"Found {len(matches)} HEARTBEAT_LED/TIMER_LED labels to remove")
    for match in reversed(matches):
        content = content[:match.start()] + content[match.end():]

    # Step 2: Remove wires that were added for these signals
    # Wires near U3 area (around 266-272, 500-503)
    # Wires near J2 area (around 191-197, 138-142)
    wire_patterns = [
        r'\t\(wire\s*\n\t\t\(pts\s*\n\t\t\t\(xy 26[6-9]\.[0-9]+ 50[0-3]\.[0-9]+\).*?\n\t\)',
        r'\t\(wire\s*\n\t\t\(pts\s*\n\t\t\t\(xy 27[0-2]\.[0-9]+ 50[0-3]\.[0-9]+\).*?\n\t\)',
        r'\t\(wire\s*\n\t\t\(pts\s*\n\t\t\t\(xy 19[1-7]\.[0-9]+ 1(38|39|40|41|42)\.[0-9]+\).*?\n\t\)',
    ]
    for pattern in wire_patterns:
        matches = list(re.finditer(pattern, content, re.DOTALL))
        if matches:
            print(f"Removing {len(matches)} wires matching pattern")
            for match in reversed(matches):
                content = content[:match.start()] + content[match.end():]

    # === Add new connections using EXACT positions from ERC ===

    # U3 Pin 5 (PB0/HEARTBEAT_LED): EXACT position from ERC = (269.24, 500.38)
    # U3 Pin 6 (PB1/TIMER_LED): EXACT position from ERC = (269.24, 502.92)
    u3_pin5_x, u3_pin5_y = 269.24, 500.38
    u3_pin6_x, u3_pin6_y = 269.24, 502.92

    # Label position: 5mm to the right of pin
    u3_label_x = u3_pin5_x + 5.08  # 274.32

    # J2 at (200, 150), left pins at x = 200 - 3.81 = 196.19
    # But let's check: the script said 196.19, and ERC showed wires at 196.19 (7724 mils)
    # 7724 mils = 196.19 mm, so that's correct for J2 left side pin x position
    # Pin 11 y: Pin 1 is at 150 - 24.13 = 125.87, Pin 11 = 125.87 + 5*2.54 = 138.57
    # Pin 13 y: 125.87 + 6*2.54 = 141.11
    j2_pin_x = 196.19
    j2_pin11_y = 138.57
    j2_pin13_y = 141.11

    # Label position: 5mm to the left of pin
    j2_label_x = j2_pin_x - 5.08  # 191.11

    # Create elements
    # U3 side: wire from pin to label, label pointing right
    wire_u3_hb = create_wire(u3_pin5_x, u3_pin5_y, u3_label_x, u3_pin5_y)
    wire_u3_tm = create_wire(u3_pin6_x, u3_pin6_y, u3_label_x, u3_pin6_y)
    label_u3_hb = create_global_label("HEARTBEAT_LED", u3_label_x, u3_pin5_y, 0, "left")
    label_u3_tm = create_global_label("TIMER_LED", u3_label_x, u3_pin6_y, 0, "left")

    # J2 side: wire from pin to label, label pointing left (180 deg)
    wire_j2_hb = create_wire(j2_pin_x, j2_pin11_y, j2_label_x, j2_pin11_y)
    wire_j2_tm = create_wire(j2_pin_x, j2_pin13_y, j2_label_x, j2_pin13_y)
    label_j2_hb = create_global_label("HEARTBEAT_LED", j2_label_x, j2_pin11_y, 180, "right")
    label_j2_tm = create_global_label("TIMER_LED", j2_label_x, j2_pin13_y, 180, "right")

    # Find insertion point for labels (after last global_label)
    label_insert_pattern = r'(\t\(global_label "[^"]+"\s*\n.*?\n\t\))'
    matches = list(re.finditer(label_insert_pattern, content, re.DOTALL))
    if matches:
        insert_pos = matches[-1].end()
        all_labels = "\n".join([label_u3_hb, label_u3_tm, label_j2_hb, label_j2_tm])
        content = content[:insert_pos] + "\n" + all_labels + content[insert_pos:]
        print("Added 4 global labels")

    # Find insertion point for wires (after last wire)
    wire_insert_pattern = r'(\t\(wire\s*\n\t\t\(pts\s*\n.*?\n\t\))'
    matches = list(re.finditer(wire_insert_pattern, content, re.DOTALL))
    if matches:
        insert_pos = matches[-1].end()
        all_wires = "\n".join([wire_u3_hb, wire_u3_tm, wire_j2_hb, wire_j2_tm])
        content = content[:insert_pos] + "\n" + all_wires + content[insert_pos:]
        print("Added 4 wires")

    # Write updated schematic
    schematic_path.write_text(content, encoding='utf-8')
    print(f"\nUpdated schematic: {schematic_path}")
    print("\nConnections:")
    print(f"  U3 Pin 5 ({u3_pin5_x}, {u3_pin5_y}) --wire--> HEARTBEAT_LED label ({u3_label_x}, {u3_pin5_y})")
    print(f"  U3 Pin 6 ({u3_pin6_x}, {u3_pin6_y}) --wire--> TIMER_LED label ({u3_label_x}, {u3_pin6_y})")
    print(f"  J2 Pin 11 ({j2_pin_x}, {j2_pin11_y}) --wire--> HEARTBEAT_LED label ({j2_label_x}, {j2_pin11_y})")
    print(f"  J2 Pin 13 ({j2_pin_x}, {j2_pin13_y}) --wire--> TIMER_LED label ({j2_label_x}, {j2_pin13_y})")

if __name__ == "__main__":
    main()
