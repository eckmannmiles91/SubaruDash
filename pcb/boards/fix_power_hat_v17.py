#!/usr/bin/env python3
"""
Fix Power HAT v17: Clean up ERC warnings

Addressing:
1. Remove dangling global labels that serve no purpose:
   - Q2_GATE (not connected to anything)
   - R6_OUT (not connected to anything)
   - FAN+ (if orphan)

2. Remove orphan wires with unconnected endpoints

3. Remove duplicate HEARTBEAT_LED/TIMER_LED labels at J2 that aren't connecting
   (keep only the ones at U3 side that are working)
"""

import re
import shutil
from pathlib import Path

def main():
    schematic_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_sch")

    # Create backup
    backup_path = schematic_path.parent / "power-hat-BACKUP17.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"Created backup: {backup_path}")

    content = schematic_path.read_text(encoding='utf-8')
    original_len = len(content)

    # 1. Remove dangling global labels: Q2_GATE, R6_OUT
    # These appear to be orphan labels not connected to anything useful
    labels_to_remove = ['Q2_GATE', 'R6_OUT']

    for label_name in labels_to_remove:
        pattern = rf'\t\(global_label "{label_name}".*?\n\t\)'
        matches = list(re.finditer(pattern, content, re.DOTALL))
        if matches:
            print(f"Removing {len(matches)} dangling '{label_name}' global label(s)")
            for match in reversed(matches):
                content = content[:match.start()] + content[match.end():]

    # 2. Remove the J2-side HEARTBEAT_LED and TIMER_LED labels and their wires
    # These are at approximately (191, 138) and (191, 141) - they're causing warnings
    # The U3-side labels (at 274, 500) are the ones that work

    # Remove J2-side labels (around x=191, y=138-141)
    # Convert mils to mm: 7524 mils = 191.11 mm
    j2_label_pattern = r'\t\(global_label "(HEARTBEAT_LED|TIMER_LED)"\s*\n\t\t\(shape input\)\s*\n\t\t\(at 191\.[0-9]+ 1(38|41)\.[0-9]+ 180\).*?\n\t\)'
    matches = list(re.finditer(j2_label_pattern, content, re.DOTALL))
    if matches:
        print(f"Removing {len(matches)} J2-side HEARTBEAT/TIMER labels")
        for match in reversed(matches):
            content = content[:match.start()] + content[match.end():]

    # Remove J2-side wires for these signals (around x=191-196, y=138-141)
    j2_wire_pattern = r'\t\(wire\s*\n\t\t\(pts\s*\n\t\t\t\(xy 19[1-6]\.[0-9]+ 1(38|41)\.[0-9]+\) \(xy 19[1-6]\.[0-9]+ 1(38|41)\.[0-9]+\)\s*\n\t\t\).*?\n\t\)'
    matches = list(re.finditer(j2_wire_pattern, content, re.DOTALL))
    if matches:
        print(f"Removing {len(matches)} J2-side wires")
        for match in reversed(matches):
            content = content[:match.start()] + content[match.end():]

    # 3. Check for short orphan wires (length ~9 mils = very short)
    # Wire at (16650 mils, 5800 mils) with length 9 mils
    # 16650 mils = 422.91 mm, 5800 mils = 147.32 mm
    short_wire_pattern = r'\t\(wire\s*\n\t\t\(pts\s*\n\t\t\t\(xy 422\.[0-9]+ 147\.[0-9]+\) \(xy 42[23]\.[0-9]+ 147\.[0-9]+\)\s*\n\t\t\).*?\n\t\)'
    matches = list(re.finditer(short_wire_pattern, content, re.DOTALL))
    if matches:
        print(f"Removing {len(matches)} short orphan wire(s)")
        for match in reversed(matches):
            content = content[:match.start()] + content[match.end():]

    # Write if changed
    if len(content) != original_len:
        schematic_path.write_text(content, encoding='utf-8')
        print(f"\nUpdated schematic: {schematic_path}")
        print(f"Removed {original_len - len(content)} characters")
    else:
        print("\nNo changes made - patterns may not have matched")

if __name__ == "__main__":
    main()
