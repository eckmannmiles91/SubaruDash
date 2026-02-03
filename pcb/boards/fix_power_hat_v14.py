#!/usr/bin/env python3
"""
Fix Power HAT v14: Connect U3 pins 5,6 (HEARTBEAT_LED, TIMER_LED) to J2 GPIO pins

Instead of no_connect, properly wire ATtiny85 outputs to Pi GPIO header:
- U3 Pin 5 (PB0) -> HEARTBEAT_LED -> J2 Pin 11 (GPIO17)
- U3 Pin 6 (PB1) -> TIMER_LED -> J2 Pin 13 (GPIO27)

This allows the Pi to monitor ATtiny85 status signals.
"""

import re
import shutil
import uuid
from pathlib import Path

def generate_uuid():
    return str(uuid.uuid4())

def create_global_label(name, x, y, orientation=0, justify="left"):
    """Create a global label at the given position."""
    justify_str = f'(justify {justify})' if justify else ''
    return f'''	(global_label "{name}"
		(shape input)
		(at {x} {y} {orientation})
		(fields_autoplaced yes)
		(effects
			(font
				(size 1.27 1.27)
			)
			{justify_str}
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
    backup_path = schematic_path.parent / "power-hat-BACKUP14.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Read schematic
    content = schematic_path.read_text(encoding='utf-8')

    # U3 pin positions (from ERC report)
    u3_pin5_x, u3_pin5_y = 269.24, 500.38  # PB0 - HEARTBEAT_LED
    u3_pin6_x, u3_pin6_y = 269.24, 502.92  # PB1 - TIMER_LED

    # J2 (Pi header) is at (200, 150), Conn_02x20_Odd_Even
    # Pin 1 at relative (-3.81, -24.13) from center = (196.19, 125.87)
    # Odd pins on left (x=196.19), even pins on right (x=203.81)
    # Pin spacing: 2.54mm vertically
    # Pin 11 (GPIO17): y = 125.87 + (5 * 2.54) = 138.57
    # Pin 13 (GPIO27): y = 125.87 + (6 * 2.54) = 141.11
    j2_left_x = 196.19
    j2_pin11_y = 125.87 + (5 * 2.54)  # 138.57 - GPIO17
    j2_pin13_y = 125.87 + (6 * 2.54)  # 141.11 - GPIO27

    # Wire endpoint (slightly left of pin for label placement)
    wire_end_x = j2_left_x - 5.08  # 191.11

    # Step 1: Remove no_connect symbols at U3 pins 5 and 6
    # Pattern for no_connect at specific positions
    nc_pattern = r'\t\(no_connect\s*\n\t\t\(at 269\.24 (500\.38|502\.92)\)\s*\n\t\t\(uuid "[^"]+"\)\s*\n\t\)\n?'

    matches = list(re.finditer(nc_pattern, content))
    if matches:
        print(f"Found {len(matches)} no_connect symbol(s) to remove")
        # Remove in reverse order to preserve positions
        for match in reversed(matches):
            content = content[:match.start()] + content[match.end():]
        print("Removed no_connect symbols")
    else:
        print("No no_connect symbols found at U3 pin positions (may already be removed)")

    # Step 2: Add global labels at U3 pins (pointing right, toward the pins)
    # These connect U3 outputs to the net
    label_heartbeat_u3 = create_global_label("HEARTBEAT_LED", u3_pin5_x, u3_pin5_y, 0, "left")
    label_timer_u3 = create_global_label("TIMER_LED", u3_pin6_x, u3_pin6_y, 0, "left")

    # Step 3: Add global labels at J2 pins (pointing left, 180 degrees)
    # These connect the net to GPIO pins
    label_heartbeat_j2 = create_global_label("HEARTBEAT_LED", wire_end_x, j2_pin11_y, 0, "left")
    label_timer_j2 = create_global_label("TIMER_LED", wire_end_x, j2_pin13_y, 0, "left")

    # Step 4: Add wires from J2 pins to labels
    wire_heartbeat = create_wire(j2_left_x, j2_pin11_y, wire_end_x, j2_pin11_y)
    wire_timer = create_wire(j2_left_x, j2_pin13_y, wire_end_x, j2_pin13_y)

    # Find insertion point - after last global_label
    global_label_pattern = r'(\t\(global_label "[^"]+"\s*\n.*?\n\t\))'
    matches = list(re.finditer(global_label_pattern, content, re.DOTALL))

    if matches:
        insert_pos = matches[-1].end()
        new_content = (
            content[:insert_pos] + "\n" +
            label_heartbeat_u3 + "\n" +
            label_timer_u3 + "\n" +
            label_heartbeat_j2 + "\n" +
            label_timer_j2 + "\n" +
            content[insert_pos:]
        )
        content = new_content
        print("Added global labels for HEARTBEAT_LED and TIMER_LED")
    else:
        print("ERROR: Could not find insertion point for global labels")
        return

    # Find insertion point for wires - after last wire
    wire_pattern = r'(\t\(wire\s*\n\t\t\(pts\s*\n.*?\n\t\))'
    matches = list(re.finditer(wire_pattern, content, re.DOTALL))

    if matches:
        insert_pos = matches[-1].end()
        new_content = (
            content[:insert_pos] + "\n" +
            wire_heartbeat + "\n" +
            wire_timer + "\n" +
            content[insert_pos:]
        )
        content = new_content
        print("Added wires to J2 pins 11 (GPIO17) and 13 (GPIO27)")
    else:
        print("WARNING: Could not find insertion point for wires")

    # Write updated schematic
    schematic_path.write_text(content, encoding='utf-8')
    print(f"\nUpdated schematic saved: {schematic_path}")
    print("\nGPIO Assignments:")
    print("  HEARTBEAT_LED (U3 PB0) -> J2 Pin 11 (GPIO17)")
    print("  TIMER_LED (U3 PB1) -> J2 Pin 13 (GPIO27)")
    print("\nPlease run ERC in KiCad to verify fixes.")

if __name__ == "__main__":
    main()
