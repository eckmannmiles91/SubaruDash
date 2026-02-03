#!/usr/bin/env python3
"""
Fix Power HAT v12: Remove dangling HEARTBEAT_LED and TIMER_LED labels

ERC_18 shows 2 errors:
1. Label 'HEARTBEAT_LED' at (269.24, 500.38) - dangling
2. Label 'TIMER_LED' at (269.24, 502.92) - dangling

These labels are orphaned (no wires, no matching global labels).
This script removes them.
"""

import re
import shutil
from pathlib import Path

def main():
    schematic_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_sch")

    # Create backup
    backup_path = schematic_path.parent / "power-hat-BACKUP12.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Read schematic
    content = schematic_path.read_text(encoding='utf-8')
    original_content = content

    # Pattern to match label blocks
    # Labels look like:
    # (label "HEARTBEAT_LED"
    #     (at 269.24 500.38 0)
    #     (effects
    #         (font
    #             (size 1.27 1.27)
    #         )
    #         (justify left bottom)
    #     )
    #     (uuid "...")
    # )

    # Remove HEARTBEAT_LED label at (269.24, 500.38)
    heartbeat_pattern = r'\t\(label "HEARTBEAT_LED"\s*\n\t\t\(at 269\.24 500\.38 0\).*?\n\t\t\(uuid "[^"]+"\)\s*\n\t\)'

    match = re.search(heartbeat_pattern, content, re.DOTALL)
    if match:
        print(f"Found HEARTBEAT_LED label, removing...")
        content = content[:match.start()] + content[match.end():]
    else:
        print("WARNING: Could not find HEARTBEAT_LED label with expected pattern")
        # Try alternate approach - find and remove
        if '(label "HEARTBEAT_LED"' in content and '269.24 500.38' in content:
            print("Label exists but pattern didn't match, trying alternate removal...")

    # Remove TIMER_LED label at (269.24, 502.92)
    timer_pattern = r'\t\(label "TIMER_LED"\s*\n\t\t\(at 269\.24 502\.92 0\).*?\n\t\t\(uuid "[^"]+"\)\s*\n\t\)'

    match = re.search(timer_pattern, content, re.DOTALL)
    if match:
        print(f"Found TIMER_LED label, removing...")
        content = content[:match.start()] + content[match.end():]
    else:
        print("WARNING: Could not find TIMER_LED label with expected pattern")

    # Check if changes were made
    if content == original_content:
        print("\nNo changes made - patterns may not have matched exactly.")
        print("Trying a more flexible approach...")

        content = original_content
        lines = content.split('\n')
        new_lines = []
        skip_until_close = 0
        removed_count = 0

        i = 0
        while i < len(lines):
            line = lines[i]

            # Check for target labels
            if '(label "HEARTBEAT_LED"' in line or '(label "TIMER_LED"' in line:
                # Check if next line has the target position
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if ('269.24 500.38' in next_line) or ('269.24 502.92' in next_line):
                        # Skip this entire label block
                        label_name = "HEARTBEAT_LED" if "HEARTBEAT_LED" in line else "TIMER_LED"
                        print(f"Removing {label_name} label block starting at line {i+1}")

                        # Count parentheses to find end of block
                        paren_count = line.count('(') - line.count(')')
                        i += 1
                        while i < len(lines) and paren_count > 0:
                            paren_count += lines[i].count('(') - lines[i].count(')')
                            i += 1
                        removed_count += 1
                        continue

            new_lines.append(line)
            i += 1

        if removed_count > 0:
            content = '\n'.join(new_lines)
            print(f"Removed {removed_count} label(s) using flexible approach")

    # Write updated schematic
    if content != original_content:
        schematic_path.write_text(content, encoding='utf-8')
        print(f"\nUpdated schematic saved: {schematic_path}")
        print("Please run ERC in KiCad to verify fixes.")
    else:
        print("\nNo changes were made to the schematic.")
        print("The labels may have a different format than expected.")

if __name__ == "__main__":
    main()
