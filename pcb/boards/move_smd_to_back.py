#!/usr/bin/env python3
"""
Move SMD components to back layer and position strategically.

Components to move:
- All resistors (R1-R10, R_RT1, R_COMP1) - 12 total
- Diodes D1 (SMB), D2 (SMA)
- Gate driver MOSFETs Q2, Q3 (SOT-23)

Strategic placement:
- Position back-layer components directly under their associated front-layer ICs
- This minimizes trace lengths and keeps related components together

Front-layer anchors (must stay on front):
- J1 (8.0, 14.0)   - Power input connector
- U1 (8.0, 26.0)   - TPS54560 buck converter
- L1 (8.0, 34.0)   - Power inductor
- U2 (8.0, 52.0)   - Optocoupler
- U3 (56.0, 28.0)  - ATtiny85 MCU
- Q1 (58.0, 48.0)  - Main power MOSFET (TO-220)

Fan mounting hole clearance zones (5mm radius):
- FH1: X 15.5-25.5, Y 15-25
- FH2: X 39.5-49.5, Y 15-25
- FH3: X 15.5-25.5, Y 39-49
- FH4: X 39.5-49.5, Y 39-49
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

# Back-layer component positions (x, y, rotation)
# Strategically placed under front-layer components
BACK_LAYER_POSITIONS = {
    # ============== Under J1 - Power Input (8.0, 14.0) ==============
    'D1': (10.0, 12.0, 0),      # Input protection diode - near power input

    # ============== Under U1 - Buck Converter (8.0, 26.0) ==============
    'R_RT1': (5.0, 22.0, 0),    # Timing resistor - near RT/CLK pin
    'R_COMP1': (5.0, 26.0, 0),  # Compensation resistor
    'R1': (5.0, 30.0, 0),       # Feedback divider top
    'R2': (5.0, 34.0, 0),       # Feedback divider bottom
    'D2': (12.0, 30.0, 0),      # Catch diode - near SW node
    'R3': (5.0, 38.0, 0),       # Additional resistor

    # ============== Under U3 - ATtiny85 (56.0, 28.0) ==============
    'R4': (58.0, 24.0, 90),     # MCU pull-up/resistor
    'R5': (58.0, 28.0, 90),     # MCU resistor
    'R6': (58.0, 32.0, 90),     # MCU resistor
    'R7': (58.0, 36.0, 90),     # MCU resistor

    # ============== Under U2 - Optocoupler (8.0, 52.0) ==============
    'R8': (5.0, 50.0, 0),       # Opto LED current limit
    'R9': (5.0, 54.0, 0),       # Opto output pull-up

    # ============== Under Q1 - Power MOSFET (58.0, 48.0) ==============
    'Q2': (54.0, 44.0, 0),      # Gate driver MOSFET
    'Q3': (54.0, 48.0, 0),      # Gate driver MOSFET
    'R10': (54.0, 52.0, 0),     # Gate resistor
}

# Fan hole positions for clearance checking
FAN_MOUNTING_HOLES = [
    (20.5, 20),   # FH1
    (44.5, 20),   # FH2
    (20.5, 44),   # FH3
    (44.5, 44),   # FH4
]
FAN_HOLE_CLEARANCE = 5.0


def check_fan_clearance(x, y, ref):
    """Check if position conflicts with fan mounting holes."""
    for i, (hx, hy) in enumerate(FAN_MOUNTING_HOLES, 1):
        dist = ((x - hx)**2 + (y - hy)**2)**0.5
        if dist < FAN_HOLE_CLEARANCE:
            print(f"  WARNING: {ref} at ({x}, {y}) too close to FH{i}!")
            return False
    return True


def find_footprint_bounds(content, reference):
    """Find the start and end positions of a footprint block."""
    ref_pattern = rf'\(property "Reference" "{re.escape(reference)}"'
    ref_match = re.search(ref_pattern, content)

    if not ref_match:
        return None, None, None

    # Search backwards for "(footprint"
    search_start = max(0, ref_match.start() - 3000)
    search_area = content[search_start:ref_match.start()]

    fp_matches = list(re.finditer(r'\(footprint ', search_area))
    if not fp_matches:
        return None, None, None

    fp_start = search_start + fp_matches[-1].start()

    # Find end by counting parentheses
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


def flip_to_back_layer(footprint_block):
    """Convert all F.* layer references to B.* within a footprint."""
    block = footprint_block

    # Main layer declaration
    block = re.sub(r'\(layer "F\.Cu"\)', '(layer "B.Cu")', block)

    # Silkscreen
    block = block.replace('(layer "F.SilkS")', '(layer "B.SilkS")')
    block = block.replace('"F.SilkS"', '"B.SilkS"')

    # Fab layer
    block = block.replace('(layer "F.Fab")', '(layer "B.Fab")')
    block = block.replace('"F.Fab"', '"B.Fab"')

    # Courtyard
    block = block.replace('(layer "F.CrtYd")', '(layer "B.CrtYd")')
    block = block.replace('"F.CrtYd"', '"B.CrtYd"')

    # Paste
    block = block.replace('"F.Paste"', '"B.Paste"')

    # Mask
    block = block.replace('"F.Mask"', '"B.Mask"')

    # Adhesive
    block = block.replace('"F.Adhes"', '"B.Adhes"')

    # Fix pad layers specifically
    def fix_pad_layers(match):
        layers_str = match.group(0)
        layers_str = layers_str.replace('"F.Cu"', '"B.Cu"')
        layers_str = layers_str.replace('"F.Mask"', '"B.Mask"')
        layers_str = layers_str.replace('"F.Paste"', '"B.Paste"')
        return layers_str

    block = re.sub(r'\(layers "[^"]*"[^)]*\)', fix_pad_layers, block)

    return block


def update_position(footprint_block, x, y, rotation):
    """Update the (at x y rot) position in a footprint block."""
    # Find and replace the main (at ...) position (first one after layer declaration)
    rot_str = f" {rotation}" if rotation != 0 else ""
    new_at = f"(at {x} {y}{rot_str})"

    # Replace the first (at x y) or (at x y rot) after the layer line
    pattern = r'(\(layer "[^"]+"\)\s*\n\s*\(uuid "[^"]+"\)\s*\n\s*)\(at [0-9.-]+ [0-9.-]+(?:\s+[0-9.-]+)?\)'

    def replace_at(match):
        return match.group(1) + new_at

    new_block, count = re.subn(pattern, replace_at, footprint_block, count=1)

    if count == 0:
        # Try alternate pattern
        pattern2 = r'\(at [0-9.-]+ [0-9.-]+(?:\s+[0-9.-]+)?\)'
        matches = list(re.finditer(pattern2, footprint_block))
        if matches:
            # Replace first match
            m = matches[0]
            new_block = footprint_block[:m.start()] + new_at + footprint_block[m.end():]

    return new_block


def process_component(content, reference, x, y, rotation):
    """Move a component to back layer and update its position."""
    fp_start, fp_end, footprint_block = find_footprint_bounds(content, reference)

    if fp_start is None:
        print(f"  SKIP: {reference} not found in PCB")
        return content, False

    # Check if already on back
    already_back = '(layer "B.Cu")' in footprint_block[:200]

    # Check fan clearance
    check_fan_clearance(x, y, reference)

    # Flip to back layer
    new_block = flip_to_back_layer(footprint_block)

    # Update position
    new_block = update_position(new_block, x, y, rotation)

    # Replace in content
    content = content[:fp_start] + new_block + content[fp_end:]

    status = "repositioned" if already_back else "flipped + positioned"
    print(f"  {reference:10} -> B.Cu ({x:5.1f}, {y:5.1f}) rot={rotation:3}  [{status}]")

    return content, True


def main():
    pcb_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_pcb")

    print("=" * 70)
    print("Moving SMD Components to Back Layer with Strategic Positioning")
    print("=" * 70)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = pcb_path.parent / f"power-hat-BACKUP-{timestamp}.kicad_pcb"
    shutil.copy(pcb_path, backup_path)
    print(f"\nBackup: {backup_path.name}")

    content = pcb_path.read_text(encoding='utf-8')

    print("\n" + "-" * 70)
    print("Strategic Back-Layer Placement:")
    print("-" * 70)
    print("""
    FRONT (F.Cu)                      BACK (B.Cu) - components underneath
    ============                      ================================

    J1 (power input)    <------------ D1 (input protection)

    U1 (TPS54560)       <------------ R_RT1, R_COMP1 (timing/comp)
                                      R1, R2 (feedback divider)
                                      D2 (catch diode)
                                      R3 (misc)

    U3 (ATtiny85)       <------------ R4, R5, R6, R7 (MCU resistors)

    U2 (optocoupler)    <------------ R8, R9 (opto resistors)

    Q1 (power MOSFET)   <------------ Q2, Q3 (gate drivers)
                                      R10 (gate resistor)
    """)
    print("-" * 70)

    print("\nProcessing components:")
    print("-" * 70)

    moved_count = 0
    for ref, (x, y, rot) in sorted(BACK_LAYER_POSITIONS.items()):
        content, moved = process_component(content, ref, x, y, rot)
        if moved:
            moved_count += 1

    # Write updated PCB
    pcb_path.write_text(content, encoding='utf-8')

    print("\n" + "=" * 70)
    print(f"Done! Processed {moved_count} components to back layer.")
    print("=" * 70)

    print("""
Component Summary:
  - Resistors: R1-R10, R_RT1, R_COMP1 (12 total)
  - Diodes: D1, D2 (2 total)
  - MOSFETs: Q2, Q3 (2 total)

  Total: 16 components moved/repositioned on B.Cu

Layout Strategy:
  - Buck converter passives (R1, R2, R_RT1, R_COMP1, D2) under U1
  - MCU resistors (R4-R7) under U3
  - Opto resistors (R8-R9) under U2
  - Gate driver circuit (Q2, Q3, R10) under Q1
  - Input protection (D1) under J1

Next steps in KiCad:
  1. Close and reopen the PCB file
  2. Press 'B' to view back layer (or use layer visibility)
  3. Verify component positions
  4. Run DRC to check clearances
  5. Route traces (back layer components connect via vias)

Routing tips:
  - Back-layer components need vias to connect to front-layer ICs
  - Keep high-current paths (12V, 5V, GND) on front with pour
  - Signal traces can use back layer freely
  - GND pour on back layer provides good return path
""")


if __name__ == "__main__":
    main()
