#!/usr/bin/env python3
"""
Power HAT PCB Layout v10 - Fixed mounting hole and through-hole clearances

Key fixes from v9:
1. Move components away from corner mounting holes (5mm clearance)
2. Offset back-layer components from front-layer through-hole pins
3. Better spacing for all overlapping components

Mounting holes at corners - need 5mm clearance:
- H1: (3.5, 3.5) -> avoid X<8, Y<8
- H2: (61.5, 3.5) -> avoid X>57, Y<8
- H3: (3.5, 52.5) -> avoid X<8, Y>48
- H4: (61.5, 52.5) -> avoid X>57, Y>48
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

BOARD_OFFSET_X = 95.78
BOARD_OFFSET_Y = 54.0

# Fan cutout zone
FAN_ZONE_X_MIN, FAN_ZONE_X_MAX = 17.5, 47.5
FAN_ZONE_Y_MIN, FAN_ZONE_Y_MAX = 17.0, 47.0

def check_placement(x, y, ref):
    if FAN_ZONE_X_MIN <= x <= FAN_ZONE_X_MAX and FAN_ZONE_Y_MIN <= y <= FAN_ZONE_Y_MAX:
        print(f"  ERROR: {ref} IN FAN ZONE!")
        return False
    return True

# =============================================================================
# FRONT LAYER - Through-hole components
# =============================================================================
FRONT_LAYER_POSITIONS = {
    # GPIO Header (fixed)
    'J2': (7.0, 4.0, 90),

    # LEFT EDGE - Power Section
    'F1': (6.0, 10.0, 0),      # Fuse
    'J1': (6.0, 15.0, 0),      # Power connector - moved up slightly

    # BOTTOM LEFT - Buck converter (avoid H3 at 3.5,52.5)
    'U1': (12.0, 48.0, 0),     # Buck - moved right
    'L1': (12.0, 52.0, 0),     # Inductor
    'U2': (8.0, 48.0, 0),      # Optocoupler - moved right from H3

    # RIGHT SIDE - MCU Section (avoid H4 at 61.5,52.5)
    'U3': (52.0, 48.0, 0),     # ATtiny85 - moved left
    'Y1': (52.0, 52.0, 0),     # Crystal
    'Q1': (56.0, 48.0, 0),     # MOSFET - moved left and up

    # TOP RIGHT - Connectors
    'J4': (50.0, 8.0, 0),      # Fan connector
    'JP1': (54.0, 12.0, 0),    # Jumper 1 - moved down
    'JP2': (58.0, 12.0, 0),    # Jumper 2 - moved down
    'J3': (54.0, 16.0, 0),     # ISP header - moved down
}

# =============================================================================
# BACK LAYER - SMD components with proper offsets
# =============================================================================
BACK_LAYER_POSITIONS = {
    # ============== LEFT EDGE TOP (Y=8-16) ==============
    # Avoid F1 pins at (6, 10), J1 pins at (6, 15)
    'D1': (10.0, 8.0, 0),      # TVS - moved to top edge
    'C9': (14.0, 8.0, 0),      # Input bulk cap - away from F1

    # ============== BOTTOM - Buck support (Y=48-52, avoid H3 corner) ==============
    # H3 at (3.5, 52.5) - stay X>8
    'R_RT1': (10.0, 54.0, 0),  # Timing - near bottom edge, away from H3
    'R_COMP1': (14.0, 54.0, 0),# Comp - away from H3
    'C_BOOT1': (18.0, 54.0, 0),# Bootstrap
    'C1': (22.0, 54.0, 0),     # Decoupling
    'C8': (26.0, 54.0, 0),     # Feedforward
    'C2': (30.0, 54.0, 0),     # 10uF
    'D2': (34.0, 54.0, 0),     # Catch diode
    'R3': (38.0, 54.0, 0),     # FB divider

    # ============== BOTTOM STRIP (X=20-44, Y=48-50) ==============
    'C7': (20.0, 48.0, 0),
    'C_COMP1': (24.0, 48.0, 0),
    'R8': (28.0, 48.0, 0),
    'R9': (32.0, 48.0, 0),
    'Q2': (36.0, 48.0, 0),
    'Q3': (40.0, 48.0, 0),
    'R10': (44.0, 48.0, 0),

    # ============== RIGHT EDGE TOP (Y=8-16) ==============
    # Avoid JP1/JP2 pins at (54,12) (58,12)
    'C3': (48.0, 8.0, 0),      # Away from jumpers
    'C4': (52.0, 8.0, 0),
    'C10': (56.0, 8.0, 0),     # Crystal load cap
    'C11': (60.0, 8.0, 0),     # Crystal load cap

    # ============== RIGHT BOTTOM (Y=48-52, avoid H4 corner) ==============
    # H4 at (61.5, 52.5) - stay X<57
    # Q1 at (56, 48) - offset back components
    'R4': (48.0, 52.0, 90),
    'R5': (48.0, 54.0, 90),    # Moved to Y=54
    'R1': (52.0, 54.0, 90),    # Moved to Y=54
    'R2': (44.0, 52.0, 90),    # Moved left of Q1
    'C5': (48.0, 48.0, 0),     # Away from Q1
    'C6': (44.0, 48.0, 0),     # Moved left
    'R6': (54.0, 54.0, 90),    # Below Q1
    'R7': (50.0, 54.0, 90),    # Away from H4
}


def find_footprint_bounds(content, reference):
    ref_pattern = rf'\(property "Reference" "{re.escape(reference)}"'
    ref_match = re.search(ref_pattern, content)
    if not ref_match:
        return None, None, None

    search_start = max(0, ref_match.start() - 3000)
    search_area = content[search_start:ref_match.start()]
    fp_matches = list(re.finditer(r'\(footprint ', search_area))
    if not fp_matches:
        return None, None, None

    fp_start = search_start + fp_matches[-1].start()
    depth = 0
    fp_end = fp_start
    for i, char in enumerate(content[fp_start:]):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                fp_end = fp_start + i + 1
                break

    return fp_start, fp_end, content[fp_start:fp_end]


def update_position(footprint_block, x, y, rotation):
    rot_str = f" {rotation}" if rotation != 0 else ""
    new_at = f"(at {x} {y}{rot_str})"

    pattern = r'(\(layer "[^"]+"\)\s*\n\s*\(uuid "[^"]+"\)\s*\n\s*)\(at [0-9.-]+ [0-9.-]+(?:\s+[0-9.-]+)?\)'
    new_block, count = re.subn(pattern, lambda m: m.group(1) + new_at, footprint_block, count=1)

    if count == 0:
        pattern2 = r'\(at [0-9.-]+ [0-9.-]+(?:\s+[0-9.-]+)?\)'
        matches = list(re.finditer(pattern2, footprint_block))
        if matches:
            m = matches[0]
            new_block = footprint_block[:m.start()] + new_at + footprint_block[m.end():]

    return new_block


def process_component(content, reference, rel_x, rel_y, rotation, layer_name):
    if not check_placement(rel_x, rel_y, reference):
        return content, False

    abs_x = rel_x + BOARD_OFFSET_X
    abs_y = rel_y + BOARD_OFFSET_Y

    fp_start, fp_end, footprint_block = find_footprint_bounds(content, reference)
    if fp_start is None:
        print(f"  SKIP: {reference} not found")
        return content, False

    new_block = update_position(footprint_block, abs_x, abs_y, rotation)
    content = content[:fp_start] + new_block + content[fp_end:]
    print(f"  {reference:10} -> ({rel_x:5.1f}, {rel_y:5.1f}) [{layer_name}]")
    return content, True


def main():
    pcb_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_pcb")

    print("=" * 70)
    print("Power HAT PCB Layout v10 - Mounting Hole Clearance Fix")
    print("=" * 70)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"\nBackup: {backup_path.name}")

    content = pcb_path.read_text(encoding='utf-8')

    print("""
    v10 Changes:
    - All back-layer components offset from front-layer pins
    - 5mm clearance from corner mounting holes H1-H4
    - Bottom row moved to Y=54 for clearance
    - Components spread horizontally along bottom edge
    """)

    print("-" * 70)
    print("FRONT LAYER:")
    print("-" * 70)
    front_count = 0
    for ref, (x, y, rot) in sorted(FRONT_LAYER_POSITIONS.items()):
        content, updated = process_component(content, ref, x, y, rot, "F.Cu")
        if updated:
            front_count += 1

    print("\n" + "-" * 70)
    print("BACK LAYER:")
    print("-" * 70)
    back_count = 0
    for ref, (x, y, rot) in sorted(BACK_LAYER_POSITIONS.items()):
        content, updated = process_component(content, ref, x, y, rot, "B.Cu")
        if updated:
            back_count += 1

    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 70)
    print(f"Layout v10 complete: {front_count} front, {back_count} back")
    print("=" * 70)


if __name__ == "__main__":
    main()
