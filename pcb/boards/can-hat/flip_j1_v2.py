#!/usr/bin/env python3
"""
Flip J1 GPIO header along its long axis by swapping pad X positions.
Odd pins (x=0) -> x=2.54, Even pins (x=2.54) -> x=0
"""

import re

def flip_j1(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Find J1 footprint - it's the PinHeader_2x20
    # We need to find pad (at X Y) lines within the J1 block and swap X values

    lines = content.split('\n')
    result = []
    in_j1 = False
    j1_brace_depth = 0
    flipped_count = 0

    for i, line in enumerate(lines):
        # Detect J1 footprint start
        if 'PinHeader_2x20' in line and '(footprint' in line:
            in_j1 = True
            j1_brace_depth = line.count('(') - line.count(')')

        elif in_j1:
            j1_brace_depth += line.count('(') - line.count(')')

            # Look for pad position lines: (at X Y) or (at X Y angle)
            # Only modify if it looks like a pad position (preceded by pad definition)
            at_match = re.match(r'^(\s*)\(at ([0-9.-]+) ([0-9.-]+)(.*)\)(.*)$', line)

            if at_match:
                indent = at_match.group(1)
                x = float(at_match.group(2))
                y = float(at_match.group(3))
                rest = at_match.group(4)  # angle if present
                after = at_match.group(5)

                # Check if previous line was a pad definition
                if i > 0 and '(pad "' in lines[i-1]:
                    # Swap X: 0 <-> 2.54
                    if abs(x) < 0.01:  # x ≈ 0
                        new_x = 2.54
                    elif abs(x - 2.54) < 0.01:  # x ≈ 2.54
                        new_x = 0
                    else:
                        new_x = x  # leave unchanged

                    if new_x != x:
                        line = f'{indent}(at {new_x} {y}{rest}){after}'
                        flipped_count += 1
                        print(f"Flipped: (at {x} {y}) -> (at {new_x} {y})")

            # Check if we've exited J1
            if j1_brace_depth <= 0:
                in_j1 = False

        result.append(line)

    with open(filename, 'w') as f:
        f.write('\n'.join(result))

    print(f"\nFlipped {flipped_count} pads in J1")
    print(f"Saved {filename}")

if __name__ == '__main__':
    flip_j1('can-hat.kicad_pcb')
