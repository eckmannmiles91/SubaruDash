#!/usr/bin/env python3
"""
Clean up the split schematics by removing labels and elements that don't belong.

This script filters out:
- Labels for signals that belong to the other board
- Orphaned wires and no-connects
- Elements that reference components not present
"""

import re
import os
from pathlib import Path

# Define which labels/signals belong to each board
POWER_HAT_SIGNALS = {
    # Power signals
    '12V_IGN', '12V_FUSED', '12V_SWITCHED', '12V_ACC',
    '+5V', '+3.3V', 'GND', 'GROUND',
    # TPS54560 signals
    'U1_COMP', 'COMP_RC', 'RT_CLK', 'U1_BOOT', 'U1_SW', 'U1_FB',
    # Gate control
    'GATE_CTRL', 'Q1_GATE', 'Q2_GATE',
    # ATtiny85 signals
    'HEARTBEAT_LED', 'TIMER_LED', 'SHUTDOWN_REQ', 'IGN_DETECT', 'RESET',
    # Optocoupler
    'R6_OUT',
    # Fan
    'FAN_PWM', 'FAN-',
    # Crystal (if ATtiny uses one)
    'XTAL1', 'XTAL2',
}

CAN_HAT_SIGNALS = {
    # Power signals (shared)
    '+5V', '+3.3V', 'GND', 'GROUND', '12V_IN',
    # SPI signals
    'SPI_MOSI', 'SPI_MISO', 'SPI_SCLK', 'SPI_CE0',
    # CAN signals
    'CAN_TX', 'CAN_RX', 'CANH', 'CANL', 'CANH_U5', 'CANL_U5', 'CAN_INT',
    # MCP2515 signals
    'OSC1', 'OSC2',
    # LEDs
    'LED1_ANODE', 'LED2_ANODE', 'LED3_ANODE',
}

# Signals that should be on BOTH boards (shared via Pi header)
SHARED_SIGNALS = {
    '+5V', '+3.3V', 'GND', 'GROUND',
    'SPI_MOSI', 'SPI_MISO', 'SPI_SCLK', 'SPI_CE0',
    'CAN_INT', 'SHUTDOWN_REQ', 'RESET',
}


def read_schematic(filepath):
    """Read the schematic file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_schematic(filepath, content):
    """Write the schematic file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {filepath}")


def get_label_name(block):
    """Extract the label name from a label or global_label block."""
    # Look for the label text - it's usually right after (label or (global_label
    match = re.search(r'\((?:label|global_label)\s+"([^"]+)"', block)
    if match:
        return match.group(1)
    return None


def extract_blocks(content):
    """Extract all schematic blocks by type."""
    blocks = {
        'header': '',
        'lib_symbols': '',
        'symbols': [],
        'wires': [],
        'labels': [],
        'global_labels': [],
        'junctions': [],
        'no_connects': [],
        'bus': [],
        'bus_entry': [],
        'polyline': [],
        'text': [],
        'footer': '',
    }

    lines = content.split('\n')

    # Extract header (everything before lib_symbols)
    header_lines = []
    i = 0
    while i < len(lines) and not lines[i].strip().startswith('(lib_symbols'):
        header_lines.append(lines[i])
        i += 1
    blocks['header'] = '\n'.join(header_lines)

    # Extract lib_symbols section
    if i < len(lines):
        lib_start = i
        paren_depth = lines[i].count('(') - lines[i].count(')')
        lib_lines = [lines[i]]
        i += 1
        while i < len(lines) and paren_depth > 0:
            lib_lines.append(lines[i])
            paren_depth += lines[i].count('(') - lines[i].count(')')
            i += 1
        blocks['lib_symbols'] = '\n'.join(lib_lines)

    # Now parse the rest
    current_block = []
    block_type = None
    paren_depth = 0

    type_mapping = {
        '\t(symbol': 'symbols',
        '(wire': 'wires',
        '(label': 'labels',
        '(global_label': 'global_labels',
        '(junction': 'junctions',
        '(no_connect': 'no_connects',
        '(bus ': 'bus',
        '(bus_entry': 'bus_entry',
        '(polyline': 'polyline',
        '(text': 'text',
        '(sheet_instances': 'footer',
    }

    while i < len(lines):
        line = lines[i]

        if block_type is None:
            for prefix, btype in type_mapping.items():
                if line.strip().startswith(prefix) or line.startswith(prefix):
                    block_type = btype
                    current_block = [line]
                    paren_depth = line.count('(') - line.count(')')
                    break
        else:
            current_block.append(line)
            paren_depth += line.count('(') - line.count(')')
            if paren_depth <= 0:
                block_content = '\n'.join(current_block)
                if block_type == 'footer':
                    blocks['footer'] = block_content
                else:
                    blocks[block_type].append(block_content)
                block_type = None
                current_block = []

        i += 1

    # Handle closing paren
    if ')' in lines[-1] and blocks['footer'] and not blocks['footer'].endswith(')'):
        blocks['footer'] += '\n)'

    return blocks


def filter_labels_for_board(labels, allowed_signals, board_name):
    """Filter labels to only include those for allowed signals."""
    filtered = []
    removed = []

    for label in labels:
        name = get_label_name(label)
        if name:
            if name in allowed_signals:
                filtered.append(label)
            else:
                removed.append(name)
        else:
            # Keep labels we can't parse
            filtered.append(label)

    if removed:
        print(f"  {board_name}: Removed {len(removed)} labels: {', '.join(sorted(set(removed))[:10])}...")

    return filtered


def cleanup_schematic(filepath, allowed_signals, board_name):
    """Clean up a schematic by removing unwanted labels."""
    print(f"\nCleaning up {board_name}...")

    content = read_schematic(filepath)
    blocks = extract_blocks(content)

    print(f"  Found {len(blocks['symbols'])} symbols")
    print(f"  Found {len(blocks['labels'])} labels")
    print(f"  Found {len(blocks['global_labels'])} global labels")
    print(f"  Found {len(blocks['wires'])} wires")
    print(f"  Found {len(blocks['no_connects'])} no-connects")

    # Filter labels
    blocks['labels'] = filter_labels_for_board(blocks['labels'], allowed_signals, board_name)
    blocks['global_labels'] = filter_labels_for_board(blocks['global_labels'], allowed_signals, board_name)

    # Remove most no-connects (they were for the original combined schematic)
    # Keep only a few that might still be valid
    original_nc_count = len(blocks['no_connects'])
    blocks['no_connects'] = []  # Remove all for now - easier to add back in KiCad
    print(f"  Removed {original_nc_count} no-connects (add back as needed in KiCad)")

    print(f"  Keeping {len(blocks['labels'])} labels")
    print(f"  Keeping {len(blocks['global_labels'])} global labels")

    # Reconstruct schematic
    new_content = blocks['header'] + '\n'
    new_content += blocks['lib_symbols'] + '\n'

    for symbol in blocks['symbols']:
        new_content += '\n' + symbol

    for wire in blocks['wires']:
        new_content += '\n' + wire

    for label in blocks['labels']:
        new_content += '\n' + label

    for glabel in blocks['global_labels']:
        new_content += '\n' + glabel

    for junction in blocks['junctions']:
        new_content += '\n' + junction

    for nc in blocks['no_connects']:
        new_content += '\n' + nc

    for bus in blocks['bus']:
        new_content += '\n' + bus

    for be in blocks['bus_entry']:
        new_content += '\n' + be

    for pl in blocks['polyline']:
        new_content += '\n' + pl

    for text in blocks['text']:
        new_content += '\n' + text

    new_content += '\n' + blocks['footer']

    # Ensure proper ending
    if not new_content.strip().endswith(')'):
        new_content = new_content.strip() + '\n)\n'

    write_schematic(filepath, new_content)


def main():
    script_dir = Path(__file__).parent

    power_hat_sch = script_dir / "power-hat" / "power-hat.kicad_sch"
    can_hat_sch = script_dir / "can-hat" / "can-hat.kicad_sch"

    print("=" * 60)
    print("Schematic Cleanup Tool")
    print("=" * 60)

    # Combine board-specific signals with shared signals
    power_signals = POWER_HAT_SIGNALS | SHARED_SIGNALS
    can_signals = CAN_HAT_SIGNALS | SHARED_SIGNALS

    # Clean up Power HAT
    if power_hat_sch.exists():
        cleanup_schematic(power_hat_sch, power_signals, "Power HAT")
    else:
        print(f"Warning: {power_hat_sch} not found")

    # Clean up CAN HAT
    if can_hat_sch.exists():
        cleanup_schematic(can_hat_sch, can_signals, "CAN HAT")
    else:
        print(f"Warning: {can_hat_sch} not found")

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open each schematic in KiCad")
    print("2. Run ERC to see remaining issues")
    print("3. Wire the Pi header (J2) pins to global labels")
    print("4. Add power symbols (+5V, +3.3V, GND)")
    print("5. Add no-connect flags where needed")


if __name__ == "__main__":
    main()
