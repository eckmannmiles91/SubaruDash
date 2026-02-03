#!/usr/bin/env python3
"""
Power HAT PCB Layout Script

Creates a properly laid out Power HAT PCB with:
- 65mm x 56mm board outline (Raspberry Pi HAT standard)
- Mounting holes at standard positions
- Components organized by function
- Pi GPIO header positioned correctly for stacking

This script directly modifies the .kicad_pcb file.
"""

import re
import shutil
import uuid
from pathlib import Path
from datetime import datetime

# Board dimensions (Raspberry Pi HAT standard)
BOARD_WIDTH = 65.0
BOARD_HEIGHT = 56.0

# Mounting hole positions (M2.5)
MOUNTING_HOLES = [
    (3.5, 3.5),
    (61.5, 3.5),
    (3.5, 52.5),
    (61.5, 52.5),
]

# Component placements (x, y, rotation in degrees)
# Organized by functional groups
COMPONENT_POSITIONS = {
    # ============== Pi GPIO Header ==============
    # Right side of board, running vertically
    # Pin 1 at top-right, header extends downward
    'J2': (58.0, 5.0, 90),  # 2x20 header, rotated 90° to run vertically

    # ============== Vehicle Power Input (top-left) ==============
    'J1': (12.0, 12.0, 0),   # Molex Mini-Fit Jr 2x4 - vehicle harness
    'F1': (25.0, 8.0, 0),    # Blade fuse holder
    'D1': (25.0, 16.0, 0),   # Input protection diode (SMB)

    # ============== Buck Converter Section (left-center) ==============
    # TPS54560 and supporting components
    'U1': (18.0, 28.0, 0),   # TPS54560 buck converter IC
    'L1': (28.0, 28.0, 0),   # Power inductor (6045)
    'D2': (28.0, 22.0, 180), # Catch diode (SMA)

    # Input capacitors - close to U1 VIN
    'C2': (10.0, 28.0, 90),  # Input bulk cap
    'C8': (10.0, 32.0, 90),  # Input cap 2
    'C9': (10.0, 36.0, 90),  # Input cap 3

    # Output capacitor - close to L1 output
    'C5': (36.0, 28.0, 90),  # Output cap

    # Bootstrap and compensation
    'C1': (18.0, 22.0, 0),   # Bootstrap cap (close to BOOT pin)
    'C_BOOT1': (22.0, 22.0, 0),  # Additional boot cap

    # Compensation network - close to COMP pin
    'C3': (12.0, 22.0, 0),   # Comp cap
    'C4': (14.0, 35.0, 0),   # Comp cap 2
    'C6': (16.0, 35.0, 0),   # Comp cap 3
    'C7': (18.0, 35.0, 0),   # Comp cap 4
    'C_COMP1': (20.0, 35.0, 0),  # Comp network

    # Feedback divider - close to FB pin
    'R1': (24.0, 35.0, 90),  # FB top
    'R2': (27.0, 35.0, 90),  # FB bottom

    # Timing resistor
    'R_RT1': (14.0, 22.0, 90),  # RT/CLK resistor

    # Other buck converter resistors
    'R3': (30.0, 35.0, 90),
    'R_COMP1': (33.0, 35.0, 90),

    # ============== ATtiny85 MCU Section (center) ==============
    'U3': (38.0, 45.0, 0),   # ATtiny85 DIP-8
    'Y1': (30.0, 45.0, 0),   # Crystal for ATtiny

    # MCU support components
    'R4': (32.0, 50.0, 0),   # Pull-up/down
    'R5': (35.0, 50.0, 0),   # Pull-up/down
    'R6': (38.0, 50.0, 0),   # Current limit
    'R7': (41.0, 50.0, 0),   # Current limit

    # ============== Optocoupler & Ignition Sense (bottom-left) ==============
    'U2': (12.0, 48.0, 0),   # Optocoupler DIP-4
    'R8': (20.0, 48.0, 0),   # Opto LED resistor
    'R9': (20.0, 52.0, 0),   # Opto output resistor

    # ============== MOSFET Power Switching (center-bottom) ==============
    'Q1': (25.0, 48.0, 0),   # Main power MOSFET TO-220
    'Q2': (48.0, 42.0, 0),   # Gate driver MOSFET SOT-23
    'Q3': (48.0, 46.0, 0),   # Gate driver MOSFET SOT-23
    'R10': (44.0, 42.0, 90), # Gate resistor

    # ============== Connectors (edges) ==============
    'J3': (48.0, 8.0, 0),    # 2x3 header (debug/aux)
    'J4': (8.0, 42.0, 90),   # 1x2 header (fan)

    # ============== Jumpers ==============
    'JP1': (40.0, 8.0, 0),   # Config jumper
    'JP2': (44.0, 8.0, 0),   # Config jumper
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


def create_mounting_hole(x, y):
    """Create a mounting hole footprint."""
    return f'''	(footprint "MountingHole:MountingHole_2.7mm_M2.5"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at {x} {y})
		(descr "Mounting Hole 2.7mm, M2.5")
		(tags "mounting hole 2.7mm m2.5")
		(property "Reference" "H{int(x)}{int(y)}"
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


def update_footprint_position(content, reference, x, y, rotation):
    """Update the position of a footprint by reference."""
    # Pattern to find the footprint and its position
    # We need to find the footprint block that contains this reference

    # First, find all footprint blocks
    footprint_pattern = r'(\(footprint "[^"]+"\s*\n\s*\(layer "[^"]+"\)\s*\n\s*\(uuid "[^"]+"\)\s*\n\s*)\(at ([0-9.]+) ([0-9.]+)(?:\s+([0-9.]+))?\)'

    def replace_position(match):
        # Check if this footprint has the reference we're looking for
        # We need to look ahead in the content to find the Reference property
        start_pos = match.start()
        # Find the end of this footprint (matching parentheses)
        # For simplicity, search for the Reference property nearby
        search_area = content[start_pos:start_pos + 2000]
        ref_match = re.search(r'\(property "Reference" "' + re.escape(reference) + '"', search_area)

        if ref_match:
            # This is the footprint we want to update
            prefix = match.group(1)
            rot_str = f" {rotation}" if rotation != 0 else ""
            return f'{prefix}(at {x} {y}{rot_str})'
        else:
            # Not our footprint, return unchanged
            return match.group(0)

    # This approach is too fragile. Let's use a different method.
    # Find the specific footprint by looking for the reference, then backtrack to find the (at ...) line

    # Find the reference property
    ref_pattern = rf'\(property "Reference" "{re.escape(reference)}"'
    ref_match = re.search(ref_pattern, content)

    if not ref_match:
        print(f"  WARNING: {reference} not found in PCB")
        return content

    # Search backwards from the reference to find the (at x y) line
    search_start = max(0, ref_match.start() - 500)
    search_area = content[search_start:ref_match.start()]

    # Find the last (at x y) or (at x y rot) in this area
    at_pattern = r'\(at [0-9.]+ [0-9.]+(?:\s+[0-9.]+)?\)'
    at_matches = list(re.finditer(at_pattern, search_area))

    if not at_matches:
        print(f"  WARNING: Could not find position for {reference}")
        return content

    # Get the last match (closest to the reference)
    last_at = at_matches[-1]
    actual_pos = search_start + last_at.start()
    actual_end = search_start + last_at.end()

    # Create new position string
    rot_str = f" {rotation}" if rotation != 0 else ""
    new_at = f"(at {x} {y}{rot_str})"

    # Replace
    content = content[:actual_pos] + new_at + content[actual_end:]
    print(f"  Placed {reference} at ({x}, {y}) rot={rotation}°")

    return content


def main():
    pcb_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_pcb")

    print("=" * 60)
    print("Power HAT PCB Layout Script")
    print("=" * 60)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"\nBackup created: {backup_path.name}")

    # Read PCB content
    content = pcb_path.read_text(encoding='utf-8')

    # Update component positions
    print("\nPlacing components...")
    for ref, (x, y, rot) in COMPONENT_POSITIONS.items():
        content = update_footprint_position(content, ref, x, y, rot)

    # Add board outline if not present
    if 'Edge.Cuts' not in content or 'gr_line' not in content:
        print("\nAdding board outline...")
        outline = create_board_outline()
        # Insert before the closing parenthesis
        insert_pos = content.rfind('\n)')
        if insert_pos != -1:
            content = content[:insert_pos] + '\n' + outline + content[insert_pos:]
            print(f"  Board outline: {BOARD_WIDTH}mm x {BOARD_HEIGHT}mm")
    else:
        # Check if outline already exists, if so update it
        print("\nUpdating board outline...")
        # Remove existing gr_line on Edge.Cuts
        content = re.sub(r'\t\(gr_line\s*\n\s*\(start[^)]+\)\s*\n\s*\(end[^)]+\)\s*\n\s*\(stroke[^)]+\([^)]+\)\s*\)\s*\n\s*\(layer "Edge\.Cuts"\)\s*\n\s*\(uuid "[^"]+"\)\s*\n\s*\)', '', content)
        # Add new outline
        outline = create_board_outline()
        insert_pos = content.rfind('\n)')
        if insert_pos != -1:
            content = content[:insert_pos] + '\n' + outline + content[insert_pos:]
            print(f"  Board outline: {BOARD_WIDTH}mm x {BOARD_HEIGHT}mm")

    # Add mounting holes
    print("\nAdding mounting holes...")
    mounting_holes_content = ""
    for x, y in MOUNTING_HOLES:
        mounting_holes_content += '\n' + create_mounting_hole(x, y)
        print(f"  Mounting hole at ({x}, {y}) mm")

    # Insert mounting holes before closing paren
    insert_pos = content.rfind('\n)')
    if insert_pos != -1:
        content = content[:insert_pos] + mounting_holes_content + content[insert_pos:]

    # Write updated PCB
    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 60)
    print("Layout complete!")
    print("=" * 60)
    print(f"\nUpdated: {pcb_path}")
    print("\nNext steps in KiCad:")
    print("1. Open the PCB in KiCad")
    print("2. Press 'V' to view all layers")
    print("3. Check component positions and adjust as needed")
    print("4. Add copper zones (GND pour on B.Cu)")
    print("5. Route traces")
    print("6. Run DRC")


if __name__ == "__main__":
    main()
