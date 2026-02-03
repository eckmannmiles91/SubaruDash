#!/usr/bin/env python3
"""
Fix Power HAT schematic by removing CAN-specific labels and fixing connections.

Based on the main combined schematic as source of truth.
"""

import re
from pathlib import Path

# Labels that belong ONLY to CAN HAT (remove from Power HAT)
CAN_ONLY_LABELS = {
    'SPI_MOSI', 'SPI_MISO', 'SPI_SCLK', 'SPI_CE0',
    'CAN_TX', 'CAN_RX', 'CAN_INT',
    'CANH', 'CANL', 'CANH_U5', 'CANL_U5',
    'OSC1', 'OSC2',
    'LED1_ANODE', 'LED2_ANODE', 'LED3_ANODE',
    'AUDIO_L_OUT', 'AUDIO_R_OUT', 'AUDIO_L+', 'AUDIO_L-', 'AUDIO_R+', 'AUDIO_R-',
}

# Labels that belong to Power HAT (keep these)
POWER_HAT_LABELS = {
    # Power rails
    '+12V', '12V_IGN', '12V_FUSED', '12V_SWITCHED', '12V_ACC',
    '+5V', '+3.3V', 'GND', 'GROUND',
    # TPS54560 buck converter
    'VIN', 'VOUT', 'SW', 'BOOT', 'COMP', 'FB', 'EN', 'SS', 'RT_CLK',
    'U1_COMP', 'COMP_RC', 'U1_BOOT', 'U1_SW', 'U1_FB',
    # MOSFET control
    'GATE_CTRL', 'Q1_GATE', 'Q2_GATE',
    # ATtiny85 signals
    'HEARTBEAT_LED', 'TIMER_LED', 'SHUTDOWN_REQ', 'IGN_DETECT', 'RESET',
    'PB0', 'PB1', 'PB2', 'PB3', 'PB4', 'PB5',
    # Optocoupler
    'R6_OUT',
    # Fan
    'FAN_PWM', 'FAN-', 'FAN+',
    # Crystal
    'XTAL1', 'XTAL2',
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


def extract_label_name(block):
    """Extract the label name from a label or global_label block."""
    # For (label "NAME" or (global_label "NAME"
    match = re.search(r'\((?:label|global_label)\s+"([^"]+)"', block)
    if match:
        return match.group(1)
    return None


def should_remove_label(label_name):
    """Determine if a label should be removed from Power HAT."""
    if label_name is None:
        return False

    # Remove if it's a CAN-only label
    if label_name in CAN_ONLY_LABELS:
        return True

    # Keep if it's a Power HAT label
    if label_name in POWER_HAT_LABELS:
        return False

    # Keep power-related labels
    if any(x in label_name for x in ['12V', '5V', '3.3V', 'GND', 'VIN', 'VOUT']):
        return False

    # Keep ATtiny-related labels
    if any(x in label_name for x in ['LED', 'TIMER', 'HEARTBEAT', 'SHUTDOWN', 'IGN', 'RESET', 'GATE']):
        return False

    # Default: keep unknown labels (safer)
    return False


def parse_blocks(content):
    """Parse schematic into header, lib_symbols, body blocks, and footer."""
    lines = content.split('\n')

    # Find lib_symbols section
    header_end = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('(lib_symbols'):
            header_end = i
            break

    header = '\n'.join(lines[:header_end])

    # Find end of lib_symbols
    lib_start = header_end
    paren_depth = 0
    lib_end = lib_start
    for i in range(lib_start, len(lines)):
        paren_depth += lines[i].count('(') - lines[i].count(')')
        if paren_depth == 0 and i > lib_start:
            lib_end = i + 1
            break

    lib_symbols = '\n'.join(lines[lib_start:lib_end])

    # Parse remaining content into blocks
    body_content = '\n'.join(lines[lib_end:])

    return header, lib_symbols, body_content


def filter_labels_from_content(content, label_type='label'):
    """Remove unwanted labels from content."""
    pattern = rf'\t\({label_type}\s+"[^"]+"\s*\n(?:\t\t[^\n]+\n)*\t\)'

    def should_keep(match):
        block = match.group(0)
        name = extract_label_name(block)
        if should_remove_label(name):
            print(f"  Removing {label_type}: {name}")
            return ''
        return block

    # More robust approach - find and filter each label block
    lines = content.split('\n')
    result_lines = []
    i = 0
    removed_count = 0

    while i < len(lines):
        line = lines[i]

        # Check if this starts a label block
        if line.strip().startswith(f'({label_type} "'):
            # Extract the label name
            match = re.search(rf'\({label_type}\s+"([^"]+)"', line)
            if match:
                label_name = match.group(1)

                # Collect the entire block
                block_lines = [line]
                paren_depth = line.count('(') - line.count(')')
                i += 1

                while i < len(lines) and paren_depth > 0:
                    block_lines.append(lines[i])
                    paren_depth += lines[i].count('(') - lines[i].count(')')
                    i += 1

                # Decide whether to keep
                if should_remove_label(label_name):
                    print(f"  Removing {label_type}: {label_name}")
                    removed_count += 1
                    continue  # Skip this block
                else:
                    result_lines.extend(block_lines)
                continue

        result_lines.append(line)
        i += 1

    return '\n'.join(result_lines), removed_count


def fix_power_hat():
    """Main function to fix the Power HAT schematic."""
    script_dir = Path(__file__).parent
    power_hat_sch = script_dir / "power-hat" / "power-hat.kicad_sch"

    if not power_hat_sch.exists():
        print(f"Error: {power_hat_sch} not found")
        return

    print("=" * 60)
    print("Power HAT Schematic Fixer")
    print("=" * 60)

    # Read schematic
    content = read_schematic(power_hat_sch)
    print(f"Read {len(content)} bytes")

    # Count labels before
    label_count_before = content.count('(label "')
    glabel_count_before = content.count('(global_label "')
    print(f"\nBefore: {label_count_before} labels, {glabel_count_before} global_labels")

    # Filter regular labels
    print("\nProcessing labels...")
    content, removed_labels = filter_labels_from_content(content, 'label')

    # Filter global labels
    print("\nProcessing global_labels...")
    content, removed_glabels = filter_labels_from_content(content, 'global_label')

    # Count after
    label_count_after = content.count('(label "')
    glabel_count_after = content.count('(global_label "')
    print(f"\nAfter: {label_count_after} labels, {glabel_count_after} global_labels")
    print(f"Removed: {removed_labels} labels, {removed_glabels} global_labels")

    # Write updated schematic
    write_schematic(power_hat_sch, content)

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print("\nRemaining tasks (do manually in KiCad):")
    print("1. Wire J2 Pi header pins to appropriate signals or add no-connects")
    print("2. Add PWR_FLAG symbols to power nets (+5V, +3.3V, GND)")
    print("3. Connect any remaining floating component pins")
    print("4. Run ERC again to verify")


if __name__ == "__main__":
    fix_power_hat()
