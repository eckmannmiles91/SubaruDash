#!/usr/bin/env python3
"""
Fix back-layer component positions - apply board offset.

The board origin is at (95.78, 54), not (0, 0).
This script repositions the back-layer components with the correct offset.
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

# Board offset (origin position)
BOARD_OFFSET_X = 95.78
BOARD_OFFSET_Y = 54.0

# Back-layer component positions (relative to board origin)
# These get the offset added to create absolute positions
BACK_LAYER_POSITIONS_RELATIVE = {
    # Under J1 - Power Input (8.0, 14.0)
    'D1': (10.0, 12.0, 0),

    # Under U1 - Buck Converter (8.0, 26.0)
    'R_RT1': (5.0, 22.0, 0),
    'R_COMP1': (5.0, 26.0, 0),
    'R1': (5.0, 30.0, 0),
    'R2': (5.0, 34.0, 0),
    'D2': (12.0, 30.0, 0),
    'R3': (5.0, 38.0, 0),

    # Under U3 - ATtiny85 (56.0, 28.0)
    'R4': (58.0, 24.0, 90),
    'R5': (58.0, 28.0, 90),
    'R6': (58.0, 32.0, 90),
    'R7': (58.0, 36.0, 90),

    # Under U2 - Optocoupler (8.0, 52.0)
    'R8': (5.0, 50.0, 0),
    'R9': (5.0, 54.0, 0),

    # Under Q1 - Power MOSFET (58.0, 48.0)
    'Q2': (54.0, 44.0, 0),
    'Q3': (54.0, 48.0, 0),
    'R10': (54.0, 52.0, 0),
}

# Convert to absolute positions
BACK_LAYER_POSITIONS = {
    ref: (x + BOARD_OFFSET_X, y + BOARD_OFFSET_Y, rot)
    for ref, (x, y, rot) in BACK_LAYER_POSITIONS_RELATIVE.items()
}


def find_footprint_bounds(content, reference):
    """Find the start and end positions of a footprint block."""
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
    """Update the (at x y rot) position in a footprint block."""
    rot_str = f" {rotation}" if rotation != 0 else ""
    new_at = f"(at {x} {y}{rot_str})"

    # Replace the first (at x y) or (at x y rot) after the layer line
    pattern = r'(\(layer "[^"]+"\)\s*\n\s*\(uuid "[^"]+"\)\s*\n\s*)\(at [0-9.-]+ [0-9.-]+(?:\s+[0-9.-]+)?\)'

    def replace_at(match):
        return match.group(1) + new_at

    new_block, count = re.subn(pattern, replace_at, footprint_block, count=1)

    if count == 0:
        pattern2 = r'\(at [0-9.-]+ [0-9.-]+(?:\s+[0-9.-]+)?\)'
        matches = list(re.finditer(pattern2, footprint_block))
        if matches:
            m = matches[0]
            new_block = footprint_block[:m.start()] + new_at + footprint_block[m.end():]

    return new_block


def process_component(content, reference, x, y, rotation):
    """Update component position."""
    fp_start, fp_end, footprint_block = find_footprint_bounds(content, reference)

    if fp_start is None:
        print(f"  SKIP: {reference} not found")
        return content, False

    new_block = update_position(footprint_block, x, y, rotation)
    content = content[:fp_start] + new_block + content[fp_end:]

    # Calculate relative position for display
    rel_x = x - BOARD_OFFSET_X
    rel_y = y - BOARD_OFFSET_Y
    print(f"  {reference:10} -> ({x:6.2f}, {y:6.2f})  [board-relative: ({rel_x:.1f}, {rel_y:.1f})]")

    return content, True


def main():
    pcb_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_pcb")

    print("=" * 70)
    print("Fixing Back-Layer Component Positions")
    print("=" * 70)
    print(f"\nBoard offset: ({BOARD_OFFSET_X}, {BOARD_OFFSET_Y})")

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"Backup: {backup_path.name}")

    content = pcb_path.read_text(encoding='utf-8')

    print("\nRepositioning components:")
    print("-" * 70)

    fixed_count = 0
    for ref, (x, y, rot) in sorted(BACK_LAYER_POSITIONS.items()):
        content, fixed = process_component(content, ref, x, y, rot)
        if fixed:
            fixed_count += 1

    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 70)
    print(f"Done! Repositioned {fixed_count} components.")
    print("=" * 70)
    print("\nReload PCB in KiCad to see corrected positions.")


if __name__ == "__main__":
    main()
