#!/usr/bin/env python3
"""
CAN HAT PCB Layout Script v3 - Direct text replacement approach
"""

import re

# Board boundaries
BOARD_LEFT = 114.685
BOARD_RIGHT = 179.685
BOARD_TOP = 32.57
BOARD_BOTTOM = 88.57

# Components to move to back layer (SMD passives)
BACK_LAYER = {'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11',
              'R2', 'R3', 'R6', 'L1', 'L2'}

# Component positions (x, y, angle)
POS = {
    # Front - ICs/connectors
    'J1': (BOARD_LEFT + 4.77, BOARD_TOP + 4.77, 0),
    'U1': (BOARD_LEFT + 15, BOARD_TOP + 25, 0),
    'U2': (BOARD_LEFT + 32, BOARD_TOP + 28, 0),
    'U3': (BOARD_LEFT + 50, BOARD_TOP + 28, 0),
    'Y1': (BOARD_LEFT + 32, BOARD_TOP + 40, 0),
    'J2': (BOARD_RIGHT - 12, BOARD_TOP + 35, 90),
    'J3': (BOARD_LEFT + 45, BOARD_BOTTOM - 10, 0),
    'J4': (BOARD_LEFT + 12, BOARD_BOTTOM - 18, 0),
    'LED1': (BOARD_RIGHT - 8, BOARD_TOP + 15, 0),
    'LED2': (BOARD_RIGHT - 8, BOARD_TOP + 20, 0),
    'LED3': (BOARD_RIGHT - 8, BOARD_TOP + 25, 0),
    # Back - SMD passives
    'C1': (BOARD_LEFT + 12, BOARD_TOP + 22, 0),
    'C3': (BOARD_LEFT + 18, BOARD_TOP + 22, 0),
    'C4': (BOARD_LEFT + 28, BOARD_TOP + 24, 0),
    'C5': (BOARD_LEFT + 30, BOARD_TOP + 43, 0),
    'C6': (BOARD_LEFT + 34, BOARD_TOP + 43, 0),
    'C7': (BOARD_LEFT + 36, BOARD_TOP + 24, 0),
    'C8': (BOARD_LEFT + 47, BOARD_TOP + 24, 0),
    'C9': (BOARD_LEFT + 53, BOARD_TOP + 24, 0),
    'C10': (BOARD_LEFT + 47, BOARD_TOP + 35, 0),
    'C11': (BOARD_LEFT + 53, BOARD_TOP + 35, 0),
    'R2': (BOARD_LEFT + 42, BOARD_TOP + 18, 0),
    'R3': (BOARD_LEFT + 48, BOARD_TOP + 18, 0),
    'R6': (BOARD_LEFT + 54, BOARD_TOP + 18, 0),
    'L1': (BOARD_LEFT + 22, BOARD_TOP + 30, 0),
    'L2': (BOARD_LEFT + 22, BOARD_TOP + 35, 0),
    # Mounting holes
    'H1': (BOARD_LEFT + 3.5, BOARD_TOP + 3.5, 0),
    'H2': (BOARD_RIGHT - 3.5, BOARD_TOP + 3.5, 0),
    'H3': (BOARD_LEFT + 3.5, BOARD_BOTTOM - 3.5, 0),
    'H4': (BOARD_RIGHT - 3.5, BOARD_BOTTOM - 3.5, 0),
}

def find_footprint_blocks(content):
    """Find all footprint blocks and their references."""
    blocks = []
    depth = 0
    start = -1

    i = 0
    while i < len(content):
        if content[i:i+11] == '(footprint ':
            if depth == 0:
                start = i
            depth += 1
        elif content[i] == '(':
            if start >= 0:
                depth += 1
        elif content[i] == ')':
            if start >= 0:
                depth -= 1
                if depth == 0:
                    block = content[start:i+1]
                    # Find reference in block
                    ref_match = re.search(r'\(property "Reference" "([^"]+)"', block)
                    if ref_match:
                        blocks.append((start, i+1, ref_match.group(1), block))
                    start = -1
        i += 1

    return blocks

def update_block(block, ref, x, y, angle, to_back):
    """Update a footprint block with new position and optionally move to back."""

    # Update main layer (first occurrence after footprint name)
    if to_back:
        # Change footprint layer
        block = re.sub(r'(\(footprint "[^"]+"\s*\n\s*)\(layer "F\.Cu"\)',
                      r'\1(layer "B.Cu")', block, count=1)
        # Change SMD pad layers
        block = block.replace('(layers "F.Cu" "F.Mask" "F.Paste")',
                             '(layers "B.Cu" "B.Mask" "B.Paste")')
        # Change silkscreen
        block = block.replace('(layer "F.SilkS")', '(layer "B.SilkS")')
        block = block.replace('(layer "F.CrtYd")', '(layer "B.CrtYd")')
        block = block.replace('(layer "F.Fab")', '(layer "B.Fab")')

    # Update position - find the (at x y) or (at x y angle) right after uuid
    if angle != 0:
        block = re.sub(r'(\(uuid "[^"]+"\)\s*\n\s*)\(at [0-9.-]+ [0-9.-]+( [0-9.-]+)?\)',
                      rf'\1(at {x} {y} {angle})', block, count=1)
    else:
        block = re.sub(r'(\(uuid "[^"]+"\)\s*\n\s*)\(at [0-9.-]+ [0-9.-]+( [0-9.-]+)?\)',
                      rf'\1(at {x} {y})', block, count=1)

    return block

def main():
    with open('can-hat.kicad_pcb', 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = find_footprint_blocks(content)
    print(f"Found {len(blocks)} footprints")

    # Process in reverse order to maintain positions
    for start, end, ref, block in reversed(blocks):
        if ref in POS:
            x, y, angle = POS[ref]
            to_back = ref in BACK_LAYER
            layer = 'B.Cu' if to_back else 'F.Cu'

            new_block = update_block(block, ref, x, y, angle, to_back)
            content = content[:start] + new_block + content[end:]
            print(f"Updated {ref}: ({x:.1f}, {y:.1f}) on {layer}")

    with open('can-hat.kicad_pcb', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nDone! Board: ({BOARD_LEFT}, {BOARD_TOP}) to ({BOARD_RIGHT}, {BOARD_BOTTOM})")

if __name__ == '__main__':
    main()
