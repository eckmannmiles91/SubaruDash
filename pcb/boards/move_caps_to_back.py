#!/usr/bin/env python3
"""
Move all capacitors to the back (bottom) layer of the PCB.

This script finds all footprints with reference starting with "C"
and changes their layer from F.Cu to B.Cu.
"""

import re
import shutil
from pathlib import Path
from datetime import datetime


def flip_footprint_to_back(content, reference):
    """
    Flip a footprint from F.Cu to B.Cu (front to back).

    This changes:
    - (layer "F.Cu") -> (layer "B.Cu")
    - All F.* layers to B.* layers within the footprint
    """
    # Find the footprint block for this reference
    ref_pattern = rf'\(property "Reference" "{re.escape(reference)}"'
    ref_match = re.search(ref_pattern, content)

    if not ref_match:
        print(f"  SKIP: {reference} not found")
        return content, False

    # Find the start of this footprint (search backwards for "(footprint")
    search_start = max(0, ref_match.start() - 2000)
    search_area = content[search_start:ref_match.start()]

    # Find the last "(footprint" before the reference
    fp_matches = list(re.finditer(r'\(footprint ', search_area))
    if not fp_matches:
        print(f"  WARNING: Could not find footprint start for {reference}")
        return content, False

    fp_start = search_start + fp_matches[-1].start()

    # Find the end of this footprint by counting parentheses
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

    # Extract the footprint block
    footprint_block = content[fp_start:fp_end]

    # Check if already on back layer
    if '(layer "B.Cu")' in footprint_block[:200]:
        print(f"  SKIP: {reference} already on back layer")
        return content, False

    # Flip all layer references within this footprint
    new_block = footprint_block

    # Main layer declaration (near the start)
    new_block = re.sub(r'\(layer "F\.Cu"\)', '(layer "B.Cu")', new_block, count=1)

    # Silkscreen layers
    new_block = new_block.replace('(layer "F.SilkS")', '(layer "B.SilkS")')
    new_block = new_block.replace('"F.SilkS"', '"B.SilkS"')

    # Fab layers
    new_block = new_block.replace('(layer "F.Fab")', '(layer "B.Fab")')
    new_block = new_block.replace('"F.Fab"', '"B.Fab"')

    # Courtyard layers
    new_block = new_block.replace('(layer "F.CrtYd")', '(layer "B.CrtYd")')
    new_block = new_block.replace('"F.CrtYd"', '"B.CrtYd"')

    # Paste layers
    new_block = new_block.replace('"F.Paste"', '"B.Paste"')

    # Mask layers
    new_block = new_block.replace('"F.Mask"', '"B.Mask"')

    # Adhesive layers
    new_block = new_block.replace('"F.Adhes"', '"B.Adhes"')

    # Replace the footprint block in content
    content = content[:fp_start] + new_block + content[fp_end:]

    print(f"  {reference:10} -> B.Cu (flipped to back)")
    return content, True


def main():
    pcb_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_pcb")

    print("=" * 60)
    print("Moving Capacitors to Back Layer")
    print("=" * 60)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"\nBackup: {backup_path.name}")

    content = pcb_path.read_text(encoding='utf-8')

    # Find all capacitor references (C1, C2, C3, etc.)
    cap_pattern = r'\(property "Reference" "(C[0-9]+)"'
    cap_refs = re.findall(cap_pattern, content)
    cap_refs = sorted(set(cap_refs), key=lambda x: int(re.search(r'\d+', x).group()))

    print(f"\nFound {len(cap_refs)} capacitors: {', '.join(cap_refs)}")
    print("\nFlipping to back layer:")
    print("-" * 40)

    flipped_count = 0
    for ref in cap_refs:
        content, flipped = flip_footprint_to_back(content, ref)
        if flipped:
            flipped_count += 1

    # Write updated PCB
    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 60)
    print(f"Done! Flipped {flipped_count} capacitors to back layer.")
    print("=" * 60)
    print("""
Next steps in KiCad:
  1. Reload PCB (close and reopen)
  2. Press 'B' to view back layer
  3. Verify capacitor positions make sense
  4. Adjust positions as needed (they may need repositioning)

Note: Capacitors are now mirrored. You may want to adjust
their X positions so they align with their connected ICs.
""")


if __name__ == "__main__":
    main()
