#!/usr/bin/env python3
"""
Fix Power HAT v15: Properly connect HEARTBEAT_LED and TIMER_LED

v14 added labels but they're not connecting to pins. This script:
1. Removes the dangling labels and wires from v14
2. Adds wire stubs from U3 pins 5,6 to labels
3. Adds wire stubs from J2 pins 11,13 to labels

U3 ATtiny85 at (254, 508):
- Pin 5 (PB0): right side, 5th from top
- Pin 6 (PB1): right side, 6th from top

J2 Pi header at (200, 150):
- Pin 11 (GPIO17): left column, 6th row
- Pin 13 (GPIO27): left column, 7th row
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
    backup_path = schematic_path.parent / "power-hat-BACKUP15.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"Created backup: {backup_path}")

    content = schematic_path.read_text(encoding='utf-8')

    # Step 1: Remove v14's dangling HEARTBEAT_LED and TIMER_LED global labels
    # Pattern for global_label blocks
    patterns_to_remove = [
        # HEARTBEAT_LED labels (both at U3 and J2)
        r'\t\(global_label "HEARTBEAT_LED".*?\n\t\)',
        # TIMER_LED labels (both at U3 and J2)
        r'\t\(global_label "TIMER_LED".*?\n\t\)',
    ]

    for pattern in patterns_to_remove:
        matches = list(re.finditer(pattern, content, re.DOTALL))
        print(f"Found {len(matches)} matches for pattern")
        for match in reversed(matches):
            content = content[:match.start()] + content[match.end():]

    # Step 2: Remove v14's dangling wires near J2 (around 191-196, 138-141)
    # These are the wires with unconnected endpoints
    wire_pattern = r'\t\(wire\s*\n\t\t\(pts\s*\n\t\t\t\(xy 19[1-6]\.[0-9]+ 1(38|41)\.[0-9]+\).*?\n\t\)'
    matches = list(re.finditer(wire_pattern, content, re.DOTALL))
    print(f"Found {len(matches)} J2 area wires to remove")
    for match in reversed(matches):
        content = content[:match.start()] + content[match.end():]

    # === Now add proper connections ===

    # U3 ATtiny85 at (254, 508)
    # Symbol is 25.4mm wide (±12.7 from center)
    # Right side pins at x = 254 + 12.7 = 266.7
    # Pin 5 (PB0) is at relative y = +7.62 from center = 508 - 7.62 = 500.38
    # Pin 6 (PB1) is at relative y = +5.08 from center = 508 - 5.08 = 502.92

    u3_pin5_x = 266.7  # Right edge of symbol
    u3_pin5_y = 500.38
    u3_pin6_x = 266.7
    u3_pin6_y = 502.92

    # Label position (5mm to the right of pin)
    u3_label_x = u3_pin5_x + 5.08

    # J2 Pi header at (200, 150)
    # Left pins at x = 200 - 3.81 = 196.19
    # Pin 1 at y = 150 - 24.13 = 125.87
    # Pin 11 at y = 125.87 + (5 * 2.54) = 138.57
    # Pin 13 at y = 125.87 + (6 * 2.54) = 141.11

    j2_pin_x = 196.19
    j2_pin11_y = 125.87 + (5 * 2.54)  # 138.57
    j2_pin13_y = 125.87 + (6 * 2.54)  # 141.11

    # Label position (5mm to the left of pin)
    j2_label_x = j2_pin_x - 5.08  # 191.11

    # Create wires and labels for U3 side
    # Wire from U3 pin to label position
    wire_u3_heartbeat = create_wire(u3_pin5_x, u3_pin5_y, u3_label_x, u3_pin5_y)
    wire_u3_timer = create_wire(u3_pin6_x, u3_pin6_y, u3_label_x, u3_pin6_y)

    # Labels at end of U3 wires (pointing right, 0 degrees)
    label_u3_heartbeat = create_global_label("HEARTBEAT_LED", u3_label_x, u3_pin5_y, 0, "left")
    label_u3_timer = create_global_label("TIMER_LED", u3_label_x, u3_pin6_y, 0, "left")

    # Create wires and labels for J2 side
    # Wire from J2 pin to label position
    wire_j2_heartbeat = create_wire(j2_pin_x, j2_pin11_y, j2_label_x, j2_pin11_y)
    wire_j2_timer = create_wire(j2_pin_x, j2_pin13_y, j2_label_x, j2_pin13_y)

    # Labels at end of J2 wires (pointing left, 180 degrees)
    label_j2_heartbeat = create_global_label("HEARTBEAT_LED", j2_label_x, j2_pin11_y, 180, "right")
    label_j2_timer = create_global_label("TIMER_LED", j2_label_x, j2_pin13_y, 180, "right")

    # Find insertion points
    # Insert labels after last global_label
    global_label_pattern = r'(\t\(global_label "[^"]+"\s*\n.*?\n\t\))'
    matches = list(re.finditer(global_label_pattern, content, re.DOTALL))

    if matches:
        insert_pos = matches[-1].end()
        labels_to_add = "\n".join([
            label_u3_heartbeat,
            label_u3_timer,
            label_j2_heartbeat,
            label_j2_timer
        ])
        content = content[:insert_pos] + "\n" + labels_to_add + content[insert_pos:]
        print("Added 4 global labels")

    # Insert wires after last wire
    wire_pattern = r'(\t\(wire\s*\n\t\t\(pts\s*\n.*?\n\t\))'
    matches = list(re.finditer(wire_pattern, content, re.DOTALL))

    if matches:
        insert_pos = matches[-1].end()
        wires_to_add = "\n".join([
            wire_u3_heartbeat,
            wire_u3_timer,
            wire_j2_heartbeat,
            wire_j2_timer
        ])
        content = content[:insert_pos] + "\n" + wires_to_add + content[insert_pos:]
        print("Added 4 wires")

    # Write updated schematic
    schematic_path.write_text(content, encoding='utf-8')
    print(f"\nUpdated schematic saved: {schematic_path}")
    print("\nConnections made:")
    print(f"  U3 Pin 5 (PB0) at ({u3_pin5_x}, {u3_pin5_y}) -> HEARTBEAT_LED -> J2 Pin 11 at ({j2_pin_x}, {j2_pin11_y})")
    print(f"  U3 Pin 6 (PB1) at ({u3_pin6_x}, {u3_pin6_y}) -> TIMER_LED -> J2 Pin 13 at ({j2_pin_x}, {j2_pin13_y})")
    print("\nRun ERC in KiCad to verify.")

if __name__ == "__main__":
    main()
