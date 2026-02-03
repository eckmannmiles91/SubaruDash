#!/usr/bin/env python3
"""
Power HAT PCB Layout Script v2 - Improved spacing

Changes from v1:
- J2 GPIO header repositioned to run vertically along right edge
- Power section components spread out more (5-8mm spacing)
- Q1 TO-220 given more clearance (moved to dedicated area)
- Better organization of capacitor groups
- MCU section reorganized with more breathing room
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
# IMPROVED LAYOUT with better spacing
COMPONENT_POSITIONS = {
    # ============== Pi GPIO Header (RIGHT EDGE, VERTICAL) ==============
    # 2x20 header at 2.54mm pitch = ~51mm long
    # Position so it runs vertically along right edge
    # Pin 1 at top-right, extending downward
    'J2': (58.0, 3.5, 90),  # Right edge, starts at top

    # ============== Vehicle Power Input (TOP-LEFT) ==============
    # Molex connector for vehicle harness - needs clearance for wires
    'J1': (10.0, 10.0, 0),   # Molex Mini-Fit Jr 2x4
    'F1': (28.0, 6.0, 0),    # Blade fuse - near input
    'D1': (28.0, 14.0, 0),   # Input protection diode (SMB)

    # ============== Buck Converter Section (LEFT-CENTER) ==============
    # TPS54560 CRITICAL LAYOUT: VIN caps close, SW-L1 short, output cap close
    # Spread components with 6-8mm spacing for routing

    'U1': (18.0, 26.0, 0),   # TPS54560 buck converter (center of power section)

    # Input capacitors - LEFT of U1, close to VIN pins
    'C2': (8.0, 24.0, 0),    # Main input bulk cap (1206)
    'C8': (8.0, 28.0, 0),    # Input cap 2 (1206)
    'C9': (8.0, 32.0, 0),    # Input cap 3 (1206)

    # Inductor - RIGHT of U1, close to SW pin (CRITICAL - keep short!)
    'L1': (30.0, 26.0, 0),   # Power inductor (6045) - 6mm from U1

    # Catch diode - between U1.SW and GND, close to L1
    'D2': (24.0, 32.0, 0),   # Schottky diode (SMA)

    # Output capacitor - RIGHT of L1, at output node
    'C5': (40.0, 26.0, 0),   # Output cap (1206) - close to L1 output

    # Bootstrap cap - ABOVE U1, close to BOOT pin
    'C1': (14.0, 20.0, 0),   # Bootstrap cap (0805)
    'C_BOOT1': (18.0, 20.0, 0),  # Additional boot cap

    # Compensation network - BELOW U1, close to COMP pin
    'C3': (14.0, 32.0, 0),   # Comp cap
    'C_COMP1': (18.0, 32.0, 0),  # Comp network cap
    'R_COMP1': (22.0, 38.0, 0),  # Comp resistor

    # Timing resistor - near RT/CLK pin
    'R_RT1': (10.0, 20.0, 0),  # RT resistor

    # Feedback divider - near FB pin (right side of U1)
    'R1': (26.0, 20.0, 90),  # FB divider top
    'R2': (30.0, 20.0, 90),  # FB divider bottom

    # Additional passives near power section
    'C4': (34.0, 20.0, 0),   # Decoupling
    'C6': (38.0, 20.0, 0),   # Decoupling
    'C7': (42.0, 20.0, 0),   # Decoupling
    'R3': (34.0, 32.0, 0),   # Support resistor

    # ============== ATtiny85 MCU Section (CENTER-RIGHT) ==============
    # DIP-8 package needs ~10mm x 8mm, plus crystal
    'U3': (44.0, 38.0, 0),   # ATtiny85 DIP-8
    'Y1': (36.0, 38.0, 0),   # Crystal HC49 (if used)

    # MCU support resistors - spread below U3
    'R4': (36.0, 44.0, 0),   # Pull-up/config
    'R5': (40.0, 44.0, 0),   # Pull-up/config
    'R6': (44.0, 44.0, 0),   # LED current limit
    'R7': (48.0, 44.0, 0),   # LED current limit

    # ============== Optocoupler Section (BOTTOM-LEFT) ==============
    # LTV-817 for ignition detection - isolated from vehicle
    'U2': (10.0, 46.0, 0),   # Optocoupler DIP-4
    'R8': (18.0, 44.0, 0),   # Opto LED resistor
    'R9': (18.0, 48.0, 0),   # Opto output pull-up

    # ============== Power MOSFET Section (BOTTOM-CENTER) ==============
    # Q1 is TO-220 - needs ~15mm x 10mm clearance, heat dissipation
    'Q1': (28.0, 48.0, 0),   # Main power MOSFET (TO-220) - dedicated area

    # Small signal MOSFETs for gate drive
    'Q2': (38.0, 50.0, 0),   # Gate driver (SOT-23)
    'Q3': (42.0, 50.0, 0),   # Gate driver (SOT-23)
    'R10': (46.0, 50.0, 0),  # Gate resistor

    # ============== Auxiliary Connectors (EDGES) ==============
    'J3': (48.0, 6.0, 0),    # 2x3 ISP/debug header - top edge
    'J4': (6.0, 38.0, 90),   # Fan connector - left edge

    # ============== Jumpers (TOP, BETWEEN J1 AND J2) ==============
    'JP1': (38.0, 6.0, 0),   # Config jumper
    'JP2': (42.0, 10.0, 0),  # Config jumper (3-pin)
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


def create_mounting_hole(x, y, idx):
    """Create a mounting hole footprint."""
    return f'''	(footprint "MountingHole:MountingHole_2.7mm_M2.5"
		(layer "F.Cu")
		(uuid "{generate_uuid()}")
		(at {x} {y})
		(descr "Mounting Hole 2.7mm, M2.5")
		(tags "mounting hole 2.7mm m2.5")
		(property "Reference" "H{idx}"
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
    print(f"  {reference:12} -> ({x:5.1f}, {y:5.1f}) rot={rotation}°")

    return content


def remove_existing_mounting_holes(content):
    """Remove any existing mounting hole footprints."""
    # Pattern to match mounting hole footprints
    pattern = r'\t\(footprint "MountingHole:MountingHole_2\.7mm_M2\.5".*?\t\)\n'
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
    print("Power HAT PCB Layout Script v2 - Improved Spacing")
    print("=" * 60)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"\nBackup: {backup_path.name}")

    # Read PCB content
    content = pcb_path.read_text(encoding='utf-8')

    # Remove existing board outline and mounting holes for clean slate
    print("\nCleaning existing layout elements...")
    content = remove_existing_board_outline(content)
    content = remove_existing_mounting_holes(content)

    # Update component positions
    print("\nPlacing components:")
    print("-" * 40)
    for ref, (x, y, rot) in sorted(COMPONENT_POSITIONS.items()):
        content = update_footprint_position(content, ref, x, y, rot)

    # Add board outline
    print("\nAdding board outline...")
    outline = create_board_outline()
    insert_pos = content.rfind('\n)')
    if insert_pos != -1:
        content = content[:insert_pos] + '\n' + outline + content[insert_pos:]
        print(f"  Board: {BOARD_WIDTH}mm x {BOARD_HEIGHT}mm")

    # Add mounting holes
    print("\nAdding mounting holes...")
    for idx, (x, y) in enumerate(MOUNTING_HOLES, 1):
        hole = create_mounting_hole(x, y, idx)
        insert_pos = content.rfind('\n)')
        content = content[:insert_pos] + '\n' + hole + content[insert_pos:]
        print(f"  H{idx}: ({x}, {y}) mm")

    # Write updated PCB
    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 60)
    print("Layout v2 complete!")
    print("=" * 60)

    print("""
Component Groups:
  - Power Input (J1, F1, D1): Top-left corner
  - Buck Converter (U1, L1, D2, caps): Left-center, spread out
  - GPIO Header (J2): Right edge, vertical
  - MCU (U3, Y1): Center-right
  - Optocoupler (U2): Bottom-left
  - Power MOSFET (Q1): Bottom-center with clearance

Next steps in KiCad:
  1. Open PCB and verify layout
  2. Add GND pour on B.Cu layer
  3. Route power traces (1.5-2mm width for 12V/5V)
  4. Route signal traces (0.3-0.5mm width)
  5. Run DRC
""")


if __name__ == "__main__":
    main()
