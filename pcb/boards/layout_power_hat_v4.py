#!/usr/bin/env python3
"""
Power HAT PCB Layout Script v4 - Improved component spacing

Changes from v3:
- Moved R1, R2, R3 further left to avoid fan airflow zone
- Moved D2 further left to avoid FH1 zone
- Moved U3 to proper position (56, 26) away from FH2
- Moved R4-R7 slightly further right to avoid FH2 zone
- Added clearance checks for all fan mounting holes

30mm fan specifications:
- Fan size: 30x30x10mm
- Mounting hole spacing: 24mm (diagonal)
- Fan center: (32.5, 32)
- Mounting holes: (20.5, 20), (44.5, 20), (20.5, 44), (44.5, 44)

Clearance zones (5mm radius around each M3 hole):
- FH1: X 15.5-25.5, Y 15-25
- FH2: X 39.5-49.5, Y 15-25
- FH3: X 15.5-25.5, Y 39-49
- FH4: X 39.5-49.5, Y 39-49
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
FAN_CENTER = (32.5, 32)
FAN_HOLE_SPACING = 24.0
FAN_MOUNTING_HOLES = [
    (FAN_CENTER[0] - FAN_HOLE_SPACING/2, FAN_CENTER[1] - FAN_HOLE_SPACING/2),  # 20.5, 20
    (FAN_CENTER[0] + FAN_HOLE_SPACING/2, FAN_CENTER[1] - FAN_HOLE_SPACING/2),  # 44.5, 20
    (FAN_CENTER[0] - FAN_HOLE_SPACING/2, FAN_CENTER[1] + FAN_HOLE_SPACING/2),  # 20.5, 44
    (FAN_CENTER[0] + FAN_HOLE_SPACING/2, FAN_CENTER[1] + FAN_HOLE_SPACING/2),  # 44.5, 44
]

# Fan hole clearance radius (for M3 screw head)
FAN_HOLE_CLEARANCE = 5.0

def check_fan_clearance(x, y, component_name):
    """Check if component position conflicts with fan mounting holes."""
    for i, (hx, hy) in enumerate(FAN_MOUNTING_HOLES, 1):
        dist = ((x - hx)**2 + (y - hy)**2)**0.5
        if dist < FAN_HOLE_CLEARANCE:
            print(f"  WARNING: {component_name} at ({x}, {y}) conflicts with FH{i} at ({hx}, {hy}), distance={dist:.1f}mm")
            return False
    return True

# Component placements (x, y, rotation in degrees)
# V4 layout with improved spacing around fan mounting holes
COMPONENT_POSITIONS = {
    # ============== GPIO Header (TOP EDGE, HORIZONTAL) ==============
    # 2x20 header at 2.54mm pitch = ~51mm long
    # At 90° rotation, it runs horizontally
    'J2': (7.0, 3.5, 90),  # Horizontal along top, pin 1 at left

    # ============== Power Input (TOP-LEFT, below header) ==============
    'J1': (8.0, 14.0, 0),    # Molex Mini-Fit Jr - vehicle harness
    'F1': (8.0, 8.0, 0),     # Blade fuse - at edge for access
    'D1': (17.0, 14.0, 0),   # Input protection diode - moved left

    # ============== Buck Converter (LEFT SIDE, below J1) ==============
    # Keep well clear of fan area
    'U1': (8.0, 26.0, 0),    # TPS54560 buck converter - moved left
    'L1': (8.0, 34.0, 90),   # Power inductor - below U1
    'D2': (15.0, 26.0, 0),   # Catch diode - moved left of FH1 zone

    # Input capacitors - vertical stack on far left edge
    'C2': (3.5, 22.0, 90),   # Input cap - flush left
    'C8': (3.5, 28.0, 90),   # Input cap - flush left
    'C9': (3.5, 34.0, 90),   # Input cap - flush left

    # Output capacitor
    'C5': (3.5, 40.0, 90),   # Output cap - flush left

    # Bootstrap and timing near U1
    'C1': (8.0, 20.0, 0),    # Bootstrap cap - aligned with U1
    'C_BOOT1': (12.0, 20.0, 0),

    # Compensation network - moved to bottom left, clear of fan
    'C3': (15.0, 20.0, 0),   # Comp cap
    'C4': (3.5, 46.0, 90),   # Below fan zone
    'C6': (7.0, 46.0, 90),   # Below fan zone
    'C7': (10.5, 46.0, 90),  # Below fan zone
    'C_COMP1': (14.0, 46.0, 90),

    # Feedback and timing resistors - MOVED LEFT of fan zone
    'R1': (14.0, 34.0, 0),   # Moved from (18, 34) to avoid fan
    'R2': (14.0, 38.0, 0),   # Moved from (18, 38) to avoid fan
    'R3': (14.0, 42.0, 0),   # Moved from (18, 42) to avoid FH3
    'R_RT1': (12.0, 26.0, 0),
    'R_COMP1': (12.0, 30.0, 0),

    # ============== MCU Section (RIGHT SIDE) ==============
    # Move U3 down from (55.38, 21) to (56, 28) to clear FH2 zone
    'U3': (56.0, 28.0, 0),   # ATtiny85 DIP-8 - moved down from 21
    'Y1': (56.0, 38.0, 0),   # Crystal - moved down to stay near U3

    # MCU resistors - MOVED RIGHT to clear FH2 zone
    'R4': (52.0, 28.0, 90),  # Moved from (50, 26) to (52, 28)
    'R5': (52.0, 32.0, 90),  # Moved down
    'R6': (52.0, 36.0, 90),  # Moved down
    'R7': (52.0, 40.0, 90),  # Moved down

    # ============== Power Switching (BOTTOM-RIGHT) ==============
    # Clear of fan mounting holes
    'Q1': (58.0, 48.0, 0),   # Main MOSFET TO-220 - moved right
    'Q2': (50.0, 48.0, 0),   # Gate driver SOT-23 - moved right
    'Q3': (50.0, 52.0, 0),   # Gate driver SOT-23 - moved right
    'R10': (54.0, 52.0, 0),  # Gate resistor - moved right

    # ============== Optocoupler (BOTTOM-LEFT) ==============
    'U2': (8.0, 52.0, 0),    # LTV-817S DIP-4
    'R8': (14.0, 50.0, 0),   # Opto resistors - moved left
    'R9': (14.0, 54.0, 0),   # Moved to edge

    # ============== Connectors & Jumpers (TOP AREA) ==============
    'J3': (58.0, 10.0, 0),   # ISP/debug header - top right
    'J4': (28.0, 10.0, 0),   # Fan connector (4-pin) - moved down slightly
    'JP1': (34.0, 10.0, 0),  # Config jumpers - moved right of J4
    'JP2': (40.0, 10.0, 0),  # Moved slightly
}


def generate_uuid():
    """Generate a UUID for KiCad elements."""
    return str(uuid.uuid4())


def update_footprint_position(content, reference, x, y, rotation):
    """Update the position of a footprint by reference."""
    ref_pattern = rf'\(property "Reference" "{re.escape(reference)}"'
    ref_match = re.search(ref_pattern, content)

    if not ref_match:
        print(f"  SKIP: {reference} not found in PCB")
        return content

    # Check fan clearance
    check_fan_clearance(x, y, reference)

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


def main():
    pcb_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_pcb")

    print("=" * 60)
    print("Power HAT PCB Layout v4 - Improved Fan Clearance")
    print("=" * 60)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"\nBackup: {backup_path.name}")

    content = pcb_path.read_text(encoding='utf-8')

    # Update component positions
    print("\nPlacing components (v4 improved spacing):")
    print("-" * 50)
    for ref, (x, y, rot) in sorted(COMPONENT_POSITIONS.items()):
        content = update_footprint_position(content, ref, x, y, rot)

    # Write updated PCB
    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 60)
    print("Layout v4 complete!")
    print("=" * 60)

    print(f"""
Layout Summary v4:
  - GPIO header (J2): Horizontal along top edge
  - 30mm fan area: Centered at {FAN_CENTER}
  - Power section: Far left side (U1, L1, caps) - clear of fan
  - MCU section: Far right side (U3, Y1) - moved down to clear FH2
  - Power switching: Bottom-right (Q1, Q2, Q3)
  - Fan connector (J4): Top center at (28, 10)

Key changes from v3:
  - R1, R2, R3: Moved from X=18 to X=14 (clear of fan zone)
  - D2: Moved from (18, 26) to (15, 26) (clear of FH1)
  - U3: Moved from Y=21 to Y=28 (clear of FH2)
  - R4-R7: Moved from X=50 to X=52 and shifted down
  - All capacitors on left edge pushed to X=3.5

Next steps in KiCad:
  1. Reload PCB (close and reopen)
  2. Verify component positions don't overlap
  3. Run DRC to check clearances
  4. Route traces
""")


if __name__ == "__main__":
    main()
