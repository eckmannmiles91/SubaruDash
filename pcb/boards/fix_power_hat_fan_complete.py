#!/usr/bin/env python3
"""
Fix Power HAT: Complete fan wiring for 4-pin PWM fan connector

Fixes ERC errors by:
1. Wiring J4 Pin 3 (TACH) to FAN_TACH signal -> GPIO13 (Pin 33)
2. Wiring J4 Pin 4 (PWM) to FAN_PWM signal -> GPIO12 (Pin 32)

Standard 4-pin PWM fan pinout:
- Pin 1: GND (already wired)
- Pin 2: +12V/FAN+ (already wired)
- Pin 3: TACH (fan speed feedback) -> GPIO13
- Pin 4: PWM (speed control) -> GPIO12
"""

import re
import shutil
import uuid
from pathlib import Path
from datetime import datetime


def generate_uuid():
    """Generate a UUID for KiCad elements."""
    return str(uuid.uuid4())


def create_global_label(name, x, y, rotation=0, shape="passive"):
    """Create a global label element."""
    justify = "left" if rotation == 0 else "right" if rotation == 180 else "left"
    return f'''	(global_label "{name}"
		(shape {shape})
		(at {x} {y} {rotation})
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
	)
'''


def create_wire(x1, y1, x2, y2):
    """Create a wire element."""
    return f'''	(wire
		(pts
			(xy {x1} {y1}) (xy {x2} {y2})
		)
		(stroke
			(width 0)
			(type default)
		)
		(uuid "{generate_uuid()}")
	)
'''


def remove_no_connect_by_position(content, x, y):
    """Remove a no_connect marker at the specified position."""
    # Pattern to match no_connect at specific position
    pattern = rf'\(no_connect\s*\n\s*\(at {re.escape(str(x))} {re.escape(str(y))}\)\s*\n\s*\(uuid "[^"]+"\)\s*\n\s*\)'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + content[match.end():]
        print(f"  Removed no_connect at ({x}, {y})")
        return content, True
    print(f"  WARNING: no_connect at ({x}, {y}) not found")
    return content, False


def main():
    schematic_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_sch")

    print("=" * 60)
    print("Power HAT Fan Wiring Fix - Complete 4-pin PWM Support")
    print("=" * 60)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = schematic_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"\nBackup: {backup_path.name}")

    content = schematic_path.read_text(encoding='utf-8')

    # ===============================================
    # Step 1: Add labels at J4 pins 3 and 4
    # ===============================================
    print("\nStep 1: Adding labels at J4 (fan connector)...")

    # J4 is at (635, 571.5)
    # Pin positions (X = 629.92, which is 635 - 5.08 for pin offset):
    # Pin 1: Y = 568.96 (GND - already wired)
    # Pin 2: Y = 571.5  (FAN+ - already wired)
    # Pin 3: Y = 574.04 (TACH - needs wire) - 571.5 + 2.54
    # Pin 4: Y = 576.58 (PWM - needs wire)  - 571.5 + 5.08

    # Add wire from J4 Pin 4 to label position
    wire_j4_pin4 = create_wire(629.92, 576.58, 624.84, 576.58)
    # Add FAN_PWM label at J4 Pin 4
    label_fan_pwm_j4 = create_global_label("FAN_PWM", 624.84, 576.58, 180, "passive")

    # Add wire from J4 Pin 3 to label position
    wire_j4_pin3 = create_wire(629.92, 574.04, 624.84, 574.04)
    # Add FAN_TACH label at J4 Pin 3
    label_fan_tach_j4 = create_global_label("FAN_TACH", 624.84, 574.04, 180, "passive")

    print(f"  FAN_PWM label at J4 Pin 4 (624.84, 576.58)")
    print(f"  FAN_TACH label at J4 Pin 3 (624.84, 574.04)")

    # ===============================================
    # Step 2: Remove no_connects at GPIO12 and GPIO13
    # ===============================================
    print("\nStep 2: Removing no_connect markers at GPIO pins...")

    # GPIO12 (Pin 32) at (207.62, 165.24)
    content, removed1 = remove_no_connect_by_position(content, 207.62, 165.24)

    # GPIO13 (Pin 33) at (194.92, 167.78)
    content, removed2 = remove_no_connect_by_position(content, 194.92, 167.78)

    # ===============================================
    # Step 3: Add wires and labels at J2 GPIO pins
    # ===============================================
    print("\nStep 3: Adding wires and labels at J2 GPIO pins...")

    # GPIO12 (Pin 32) - FAN_PWM output
    wire_gpio12 = create_wire(207.62, 165.24, 212.62, 165.24)
    label_fan_pwm_gpio = create_global_label("FAN_PWM", 212.62, 165.24, 180, "passive")
    print(f"  FAN_PWM at GPIO12 (Pin 32) - (212.62, 165.24)")

    # GPIO13 (Pin 33) - FAN_TACH input
    wire_gpio13 = create_wire(194.92, 167.78, 189.92, 167.78)
    label_fan_tach_gpio = create_global_label("FAN_TACH", 189.92, 167.78, 0, "input")
    print(f"  FAN_TACH at GPIO13 (Pin 33) - (189.92, 167.78)")

    # ===============================================
    # Step 4: Insert all new elements
    # ===============================================
    print("\nStep 4: Inserting new schematic elements...")

    # Find the position to insert (before the closing parenthesis)
    # We'll insert after the last wire element for cleaner organization
    insert_pos = content.rfind('\n)')

    new_elements = (
        wire_j4_pin4 +
        wire_j4_pin3 +
        label_fan_pwm_j4 +
        label_fan_tach_j4 +
        wire_gpio12 +
        wire_gpio13 +
        label_fan_pwm_gpio +
        label_fan_tach_gpio
    )

    content = content[:insert_pos] + new_elements + content[insert_pos:]

    # ===============================================
    # Step 5: Write updated schematic
    # ===============================================
    schematic_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 60)
    print("Fan wiring complete!")
    print("=" * 60)

    print("""
Summary of changes:
  J4 (4-pin PWM fan connector):
    - Pin 1: GND (unchanged)
    - Pin 2: FAN+ (unchanged)
    - Pin 3: FAN_TACH -> GPIO13 (Pin 33)
    - Pin 4: FAN_PWM -> GPIO12 (Pin 32)

  J2 (GPIO header):
    - Pin 32 (GPIO12): FAN_PWM output (Pi generates PWM)
    - Pin 33 (GPIO13): FAN_TACH input (Pi reads RPM)

Next steps:
  1. Open schematic in KiCad and verify connections
  2. Run ERC - should show 0 errors for J4
  3. Update PCB from schematic
  4. Update GPIO_ALLOCATION.md to document new signals
""")


if __name__ == "__main__":
    main()
