#!/usr/bin/env python3
"""
Power HAT PCB Layout Script v3 - X735-style with 30mm fan

Key design changes:
- GPIO header (J2) horizontal along TOP edge
- 30mm fan area in center of board
- Components arranged around fan
- Fan mounting holes included

30mm fan specifications:
- Fan size: 30x30x10mm
- Mounting hole spacing: 24mm (diagonal)
- Mounting holes at corners of 24mm square
"""

import re
import shutil
import uuid
from pathlib import Path
from datetime import datetime

# Board dimensions (Raspberry Pi HAT standard)
BOARD_WIDTH = 65.0
BOARD_HEIGHT = 56.0

# HAT Mounting hole positions (M2.5)
MOUNTING_HOLES = [
    (3.5, 3.5),
    (61.5, 3.5),
    (3.5, 52.5),
    (61.5, 52.5),
]

# 30mm fan mounting holes (24mm spacing, centered on board)
# Center at (32.5, 30)
FAN_CENTER = (32.5, 32)
FAN_HOLE_SPACING = 24.0
FAN_MOUNTING_HOLES = [
    (FAN_CENTER[0] - FAN_HOLE_SPACING/2, FAN_CENTER[1] - FAN_HOLE_SPACING/2),
    (FAN_CENTER[0] + FAN_HOLE_SPACING/2, FAN_CENTER[1] - FAN_HOLE_SPACING/2),
    (FAN_CENTER[0] - FAN_HOLE_SPACING/2, FAN_CENTER[1] + FAN_HOLE_SPACING/2),
    (FAN_CENTER[0] + FAN_HOLE_SPACING/2, FAN_CENTER[1] + FAN_HOLE_SPACING/2),
]

# Component placements (x, y, rotation in degrees)
# X735-style layout with 30mm fan in center
COMPONENT_POSITIONS = {
    # ============== GPIO Header (TOP EDGE, HORIZONTAL) ==============
    # 2x20 header at 2.54mm pitch = ~51mm long
    # At 90° rotation, it runs horizontally
    # Position so it spans most of top edge, avoiding mounting holes
    'J2': (7.0, 3.5, 90),  # Horizontal along top, pin 1 at left

    # ============== Power Input (TOP-LEFT, below header) ==============
    'J1': (8.0, 14.0, 0),    # Molex Mini-Fit Jr - vehicle harness
    'F1': (8.0, 8.0, 0),     # Blade fuse - at edge for access
    'D1': (20.0, 14.0, 0),   # Input protection diode

    # ============== Buck Converter (LEFT SIDE, below J1) ==============
    # Keep away from fan area
    'U1': (10.0, 26.0, 0),   # TPS54560 buck converter
    'L1': (10.0, 34.0, 90),  # Power inductor - below U1
    'D2': (18.0, 26.0, 0),   # Catch diode near U1

    # Input capacitors - vertical stack on far left
    'C2': (4.0, 22.0, 90),   # Input cap
    'C8': (4.0, 28.0, 90),   # Input cap
    'C9': (4.0, 34.0, 90),   # Input cap

    # Output capacitor
    'C5': (4.0, 40.0, 90),   # Output cap

    # Bootstrap and timing near U1
    'C1': (10.0, 20.0, 0),   # Bootstrap cap
    'C_BOOT1': (14.0, 20.0, 0),

    # Compensation network
    'C3': (18.0, 20.0, 0),
    'C4': (4.0, 46.0, 90),
    'C6': (8.0, 46.0, 90),
    'C7': (12.0, 46.0, 90),
    'C_COMP1': (16.0, 46.0, 90),

    # Feedback and timing resistors
    'R1': (18.0, 34.0, 0),
    'R2': (18.0, 38.0, 0),
    'R3': (18.0, 42.0, 0),
    'R_RT1': (14.0, 26.0, 0),
    'R_COMP1': (14.0, 30.0, 0),

    # ============== MCU Section (RIGHT SIDE) ==============
    'U3': (56.0, 26.0, 0),   # ATtiny85 DIP-8
    'Y1': (56.0, 36.0, 0),   # Crystal

    # MCU resistors - below U3
    'R4': (50.0, 26.0, 90),
    'R5': (50.0, 30.0, 90),
    'R6': (50.0, 34.0, 90),
    'R7': (50.0, 38.0, 90),

    # ============== Power Switching (BOTTOM-RIGHT) ==============
    'Q1': (56.0, 48.0, 0),   # Main MOSFET TO-220
    'Q2': (48.0, 48.0, 0),   # Gate driver SOT-23
    'Q3': (48.0, 52.0, 0),   # Gate driver SOT-23
    'R10': (52.0, 52.0, 0),  # Gate resistor

    # ============== Optocoupler (BOTTOM-LEFT) ==============
    'U2': (8.0, 52.0, 0),    # LTV-817S DIP-4
    'R8': (16.0, 50.0, 0),   # Opto resistors
    'R9': (16.0, 54.0, 0),

    # ============== Connectors & Jumpers (TOP AREA) ==============
    'J3': (58.0, 10.0, 0),   # ISP/debug header - top right
    'J4': (28.0, 8.0, 0),    # Fan connector (4-pin) - accessible at top
    'JP1': (36.0, 8.0, 0),   # Config jumpers - near center top
    'JP2': (42.0, 8.0, 0),
}


def generate_uuid():
    """Generate a UUID for KiCad elements."""
    return str(uuid.uuid4())


def create_board_outline():
    """Create board outline elements for Edge.Cuts layer."""
    lines = []
    corners = [
        (0, 0),
        (BOARD_WIDTH, 0),
        (BOARD_WIDTH, BOARD_HEIGHT),
        (0, BOARD_HEIGHT),
    ]

    for i in range(4):
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % 4]
        line = f'''	(gr_line
		(start {x1} {y1})
		(end {x2} {y2})
		(stroke
			(width 0.15)
			(type solid)
		)
		(layer "Edge.Cuts")
		(uuid "{generate_uuid()}")
	)'''
        lines.append(line)

    return '\n'.join(lines)


def create_mounting_hole(x, y, name):
    """Create a mounting hole footprint."""
    return f'''	(footprint "MountingHole:MountingHole_2.7mm_M2.5"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at {x} {y})
		(descr "Mounting Hole 2.7mm, M2.5")
		(tags "mounting hole 2.7mm m2.5")
		(property "Reference" "{name}"
			(at 0 -3.2 0)
			(layer "F.SilkS")
			(hide yes)
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1 1)
					(thickness 0.15)
				)
			)
		)
		(property "Value" "MountingHole"
			(at 0 3.2 0)
			(layer "F.Fab")
			(hide yes)
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1 1)
					(thickness 0.15)
				)
			)
		)
		(property "Footprint" "MountingHole:MountingHole_2.7mm_M2.5"
			(at 0 0 0)
			(layer "F.Fab")
			(hide yes)
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1.27 1.27)
					(thickness 0.15)
				)
			)
		)
		(attr exclude_from_pos_files exclude_from_bom)
		(fp_circle
			(center 0 0)
			(end 2.7 0)
			(stroke
				(width 0.15)
				(type solid)
			)
			(fill none)
			(layer "Cmts.User")
			(uuid "{generate_uuid()}")
		)
		(fp_circle
			(center 0 0)
			(end 2.95 0)
			(stroke
				(width 0.05)
				(type solid)
			)
			(fill none)
			(layer "F.CrtYd")
			(uuid "{generate_uuid()}")
		)
		(pad "1" thru_hole circle
			(at 0 0)
			(size 5.4 5.4)
			(drill 2.7)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(uuid "{generate_uuid()}")
		)
		(embedded_fonts no)
	)'''


def create_fan_mounting_hole(x, y, name):
    """Create a smaller mounting hole for fan (M3)."""
    return f'''	(footprint "MountingHole:MountingHole_3.2mm_M3"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at {x} {y})
		(descr "Mounting Hole 3.2mm, M3")
		(tags "mounting hole 3.2mm m3")
		(property "Reference" "{name}"
			(at 0 -3.2 0)
			(layer "F.SilkS")
			(hide yes)
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1 1)
					(thickness 0.15)
				)
			)
		)
		(property "Value" "FanMount"
			(at 0 3.2 0)
			(layer "F.Fab")
			(hide yes)
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1 1)
					(thickness 0.15)
				)
			)
		)
		(property "Footprint" "MountingHole:MountingHole_3.2mm_M3"
			(at 0 0 0)
			(layer "F.Fab")
			(hide yes)
			(uuid "{generate_uuid()}")
			(effects
				(font
					(size 1.27 1.27)
					(thickness 0.15)
				)
			)
		)
		(attr exclude_from_pos_files exclude_from_bom)
		(fp_circle
			(center 0 0)
			(end 3.2 0)
			(stroke
				(width 0.15)
				(type solid)
			)
			(fill none)
			(layer "Cmts.User")
			(uuid "{generate_uuid()}")
		)
		(pad "1" thru_hole circle
			(at 0 0)
			(size 6.4 6.4)
			(drill 3.2)
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(uuid "{generate_uuid()}")
		)
		(embedded_fonts no)
	)'''


def update_footprint_position(content, reference, x, y, rotation):
    """Update the position of a footprint by reference."""
    ref_pattern = rf'\(property "Reference" "{re.escape(reference)}"'
    ref_match = re.search(ref_pattern, content)

    if not ref_match:
        print(f"  WARNING: {reference} not found")
        return content

    search_start = max(0, ref_match.start() - 500)
    search_area = content[search_start:ref_match.start()]

    at_pattern = r'\(at [0-9.]+ [0-9.]+(?:\s+[0-9.]+)?\)'
    at_matches = list(re.finditer(at_pattern, search_area))

    if not at_matches:
        print(f"  WARNING: No position for {reference}")
        return content

    last_at = at_matches[-1]
    actual_pos = search_start + last_at.start()
    actual_end = search_start + last_at.end()

    rot_str = f" {rotation}" if rotation != 0 else ""
    new_at = f"(at {x} {y}{rot_str})"

    content = content[:actual_pos] + new_at + content[actual_end:]
    print(f"  {reference:10} -> ({x:5.1f}, {y:5.1f}) rot={rotation}")

    return content


def remove_existing_mounting_holes(content):
    """Remove existing mounting hole footprints."""
    pattern = r'\t\(footprint "MountingHole:MountingHole_[^"]+_M[0-9.]+".*?\t\)\n'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content


def remove_existing_board_outline(content):
    """Remove existing board outline."""
    pattern = r'\t\(gr_line\s*\n\s*\(start[^)]+\)\s*\n\s*\(end[^)]+\)\s*\n\s*\(stroke[^)]+\([^)]+\)\s*\)\s*\n\s*\(layer "Edge\.Cuts"\)\s*\n\s*\(uuid "[^"]+"\)\s*\n\s*\)'
    content = re.sub(pattern, '', content)
    return content


def main():
    pcb_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_pcb")

    print("=" * 60)
    print("Power HAT PCB Layout v3 - X735-style with 30mm Fan")
    print("=" * 60)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"\nBackup: {backup_path.name}")

    content = pcb_path.read_text(encoding='utf-8')

    # Clean up existing elements
    print("\nCleaning existing layout...")
    content = remove_existing_board_outline(content)
    content = remove_existing_mounting_holes(content)

    # Update component positions
    print("\nPlacing components:")
    print("-" * 45)
    for ref, (x, y, rot) in sorted(COMPONENT_POSITIONS.items()):
        content = update_footprint_position(content, ref, x, y, rot)

    # Add board outline
    print("\nAdding board outline...")
    outline = create_board_outline()
    insert_pos = content.rfind('\n)')
    content = content[:insert_pos] + '\n' + outline + content[insert_pos:]
    print(f"  Board: {BOARD_WIDTH}mm x {BOARD_HEIGHT}mm")

    # Add HAT mounting holes
    print("\nAdding HAT mounting holes (M2.5)...")
    for idx, (x, y) in enumerate(MOUNTING_HOLES, 1):
        hole = create_mounting_hole(x, y, f"H{idx}")
        insert_pos = content.rfind('\n)')
        content = content[:insert_pos] + '\n' + hole + content[insert_pos:]
        print(f"  H{idx}: ({x}, {y})")

    # Add fan mounting holes
    print("\nAdding 30mm fan mounting holes (M3)...")
    for idx, (x, y) in enumerate(FAN_MOUNTING_HOLES, 1):
        hole = create_fan_mounting_hole(x, y, f"FH{idx}")
        insert_pos = content.rfind('\n)')
        content = content[:insert_pos] + '\n' + hole + content[insert_pos:]
        print(f"  FH{idx}: ({x:.1f}, {y:.1f})")

    # Write updated PCB
    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 60)
    print("Layout v3 complete!")
    print("=" * 60)

    print(f"""
Layout Summary:
  - GPIO header (J2): Horizontal along top edge
  - 30mm fan area: Centered at ({FAN_CENTER[0]}, {FAN_CENTER[1]})
  - Power section: Left side (U1, L1, caps)
  - MCU section: Right side (U3, Y1)
  - Power switching: Bottom-right (Q1, Q2, Q3)
  - Fan connector (J4): Top center, accessible

Fan mounting holes at:
  {FAN_MOUNTING_HOLES}

Next steps in KiCad:
  1. Reload PCB (close and reopen)
  2. Verify component positions
  3. Add GND pour on B.Cu
  4. Route traces
  5. Run DRC
""")


if __name__ == "__main__":
    main()
