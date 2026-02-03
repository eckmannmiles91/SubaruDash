#!/usr/bin/env python3
"""
Fix capacitor pad layers - ensure all C* component pads are on B.Cu
"""

import re
import shutil
from pathlib import Path
from datetime import datetime


def fix_capacitor_pads(content, reference):
    """
    Fix pad layers for a capacitor footprint to be on B.Cu.
    """
    # Find the footprint block for this reference
    ref_pattern = rf'\(property "Reference" "{re.escape(reference)}"'
    ref_match = re.search(ref_pattern, content)

    if not ref_match:
        print(f"  SKIP: {reference} not found")
        return content, False

    # Find the start of this footprint
    search_start = max(0, ref_match.start() - 2000)
    search_area = content[search_start:ref_match.start()]

    fp_matches = list(re.finditer(r'\(footprint ', search_area))
    if not fp_matches:
        print(f"  WARNING: Could not find footprint start for {reference}")
        return content, False

    fp_start = search_start + fp_matches[-1].start()

    # Find the end of this footprint
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

    # Extract and fix the footprint block
    footprint_block = content[fp_start:fp_end]
    original_block = footprint_block

    # Fix main layer if needed
    footprint_block = re.sub(r'\(layer "F\.Cu"\)', '(layer "B.Cu")', footprint_block)

    # Fix ALL pad layers - convert any F.* to B.* in layer definitions
    # Match patterns like: (layers "F.Cu" "F.Mask" "F.Paste") or (layers "F.Cu" "B.Mask" "B.Paste")
    def fix_pad_layers(match):
        layers_str = match.group(0)
        # Replace F.Cu with B.Cu, F.Mask with B.Mask, F.Paste with B.Paste
        layers_str = layers_str.replace('"F.Cu"', '"B.Cu"')
        layers_str = layers_str.replace('"F.Mask"', '"B.Mask"')
        layers_str = layers_str.replace('"F.Paste"', '"B.Paste"')
        return layers_str

    footprint_block = re.sub(r'\(layers "[^"]*"[^)]*\)', fix_pad_layers, footprint_block)

    # Fix silkscreen, fab, courtyard layers
    footprint_block = re.sub(r'\(layer "F\.SilkS"\)', '(layer "B.SilkS")', footprint_block)
    footprint_block = re.sub(r'\(layer "F\.Fab"\)', '(layer "B.Fab")', footprint_block)
    footprint_block = re.sub(r'\(layer "F\.CrtYd"\)', '(layer "B.CrtYd")', footprint_block)

    if footprint_block == original_block:
        print(f"  {reference:10} - no changes needed")
        return content, False

    # Replace in content
    content = content[:fp_start] + footprint_block + content[fp_end:]
    print(f"  {reference:10} -> pads fixed to B.Cu")
    return content, True


def main():
    pcb_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_pcb")

    print("=" * 60)
    print("Fixing Capacitor Pad Layers")
    print("=" * 60)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"\nBackup: {backup_path.name}")

    content = pcb_path.read_text(encoding='utf-8')

    # Find all capacitor references
    cap_pattern = r'\(property "Reference" "(C[0-9]+)"'
    cap_refs = re.findall(cap_pattern, content)
    cap_refs = sorted(set(cap_refs), key=lambda x: int(re.search(r'\d+', x).group()))

    print(f"\nFound {len(cap_refs)} capacitors: {', '.join(cap_refs)}")
    print("\nFixing pad layers:")
    print("-" * 50)

    fixed_count = 0
    for ref in cap_refs:
        content, fixed = fix_capacitor_pads(content, ref)
        if fixed:
            fixed_count += 1

    # Write updated PCB
    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 60)
    print(f"Done! Fixed {fixed_count} capacitor pad layers.")
    print("=" * 60)
    print("""
Now close and reopen the PCB in KiCad.
Capacitors should appear BLUE (back copper layer color).
""")


if __name__ == "__main__":
    main()
