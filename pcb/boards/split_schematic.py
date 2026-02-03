#!/usr/bin/env python3
"""
Split the combined SubaruDash schematic into 3 separate board schematics.

Board 1: Power HAT - TPS54560, ATtiny85, shutdown circuit
Board 2: CAN HAT - MCP2515, SN65HVD230, CAN interface
Board 3: DAC/Amp - PCM5142, TPA3116D2 (new design)

Usage: python split_schematic.py
"""

import re
import os
import uuid
from pathlib import Path

# Define which components go to which board
POWER_HAT_COMPONENTS = {
    # ICs
    'U1',  # TPS54560BDDA
    'U2',  # LTV-817S optocoupler
    'U3',  # ATtiny85
    # MOSFETs
    'Q1',  # IRLB8721PBF
    'Q2',  # 2N7002
    'Q3',  # 2N7002
    # Protection
    'F1',  # Fuse
    'D1',  # Catch diode
    'D2',  # TVS
    # Inductor
    'L1',  # 22µH
    # Capacitors
    'C1', 'C2', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C20',
    'C_BOOT1', 'C_COMP1',
    # Resistors
    'R1', 'R4', 'R5', 'R6', 'R8', 'R9', 'R10', 'R19', 'R20', 'R21',
    'R_COMP1', 'R_RT1',
    # Connectors
    'J1',   # Molex vehicle harness
    'J5',   # ISP header
    'J6',   # FAN
    'JP1', 'JP2',  # Jumpers
    # Crystal for ATtiny (if any)
    'Y2',
}

CAN_HAT_COMPONENTS = {
    # ICs
    'U4',  # MCP2515
    'U5',  # SN65HVD230
    'U6',  # AMS1117-3.3
    # Crystal
    'Y1',  # 16MHz
    # Ferrites
    'L2', 'L3',
    # Capacitors
    'C3', 'C4', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19',
    # Resistors
    'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18',
    # Connectors
    'J3',  # OBD-II
    'J4',  # CAN termination
    'J7',  # Audio (temporary, may remove)
    # LEDs
    'LED1', 'LED2', 'LED3',
}

# J2 (Pi header) will be duplicated for both HATs

def generate_uuid():
    """Generate a new UUID for KiCad."""
    return str(uuid.uuid4())

def read_schematic(filepath):
    """Read the schematic file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_symbol_blocks(content):
    """Extract all symbol blocks from the schematic."""
    symbols = []

    # Use balanced parentheses approach
    lines = content.split('\n')
    in_symbol = False
    current_symbol = []
    paren_depth = 0

    for i, line in enumerate(lines):
        # Look for standalone (symbol line followed by (lib_id on next line
        if line == '\t(symbol':
            # Check if next line has lib_id (component instance, not library def)
            if i + 1 < len(lines) and '(lib_id' in lines[i + 1]:
                in_symbol = True
                current_symbol = [line]
                paren_depth = line.count('(') - line.count(')')
                continue

        if in_symbol:
            current_symbol.append(line)
            paren_depth += line.count('(') - line.count(')')
            if paren_depth <= 0:
                symbols.append('\n'.join(current_symbol))
                in_symbol = False
                current_symbol = []
                paren_depth = 0

    return symbols

def get_symbol_reference(symbol_block):
    """Extract the reference designator from a symbol block."""
    # Look for property "Reference" "XX"
    match = re.search(r'\(property "Reference" "([^"]+)"', symbol_block)
    if match:
        return match.group(1)
    return None

def extract_wires_and_labels(content):
    """Extract all wire and label elements."""
    elements = {
        'wires': [],
        'labels': [],
        'global_labels': [],
        'power_symbols': [],
        'junctions': [],
        'no_connects': [],
        'bus': [],
        'bus_entry': [],
        'polyline': [],
        'text': [],
    }

    lines = content.split('\n')
    current_block = []
    block_type = None
    paren_depth = 0

    type_mapping = {
        '(wire': 'wires',
        '(label': 'labels',
        '(global_label': 'global_labels',
        '(junction': 'junctions',
        '(no_connect': 'no_connects',
        '(bus ': 'bus',
        '(bus_entry': 'bus_entry',
        '(polyline': 'polyline',
        '(text': 'text',
    }

    for line in lines:
        if block_type is None:
            for prefix, btype in type_mapping.items():
                if line.strip().startswith(prefix):
                    block_type = btype
                    current_block = [line]
                    paren_depth = line.count('(') - line.count(')')
                    break
        else:
            current_block.append(line)
            paren_depth += line.count('(') - line.count(')')
            if paren_depth <= 0:
                elements[block_type].append('\n'.join(current_block))
                block_type = None
                current_block = []

    return elements

def extract_lib_symbols(content):
    """Extract the lib_symbols section."""
    match = re.search(r'(\(lib_symbols\n.*?\n\t\))\n', content, re.DOTALL)
    if match:
        return match.group(1)
    return "(lib_symbols\n\t)"

def create_schematic_header(title):
    """Create the header for a new schematic."""
    return f'''(kicad_sch
	(version 20231120)
	(generator "eeschema")
	(generator_version "8.0")
	(uuid "{generate_uuid()}")
	(paper "A4")
	(title_block
		(title "{title}")
		(date "2026-02-02")
		(rev "1.0")
	)
'''

def create_schematic_footer():
    """Create the footer for a schematic."""
    return '''
	(sheet_instances
		(path "/"
			(page "1")
		)
	)
)
'''

def filter_symbols_for_board(symbols, component_set):
    """Filter symbols to include only those for a specific board."""
    filtered = []
    for symbol in symbols:
        ref = get_symbol_reference(symbol)
        if ref and ref in component_set:
            filtered.append(symbol)
    return filtered

def create_pi_header_symbol(ref="J2", x=150, y=100):
    """Create a Raspberry Pi 2x20 header symbol."""
    return f'''
	(symbol
		(lib_id "Connector_Generic:Conn_02x20_Odd_Even")
		(at {x} {y} 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{generate_uuid()}")
		(property "Reference" "{ref}"
			(at {x} {y - 30} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "Raspberry_Pi_GPIO"
			(at {x} {y + 30} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical"
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
		(property "Datasheet" "~"
			(at {x} {y} 0)
			(effects
				(font
					(size 1.27 1.27)
				)
				(hide yes)
			)
		)
	)
'''

def write_schematic(filepath, title, lib_symbols, symbols, elements=None):
    """Write a complete schematic file."""
    content = create_schematic_header(title)
    content += "\n" + lib_symbols + "\n"

    # Add symbols
    for symbol in symbols:
        content += "\n" + symbol

    # Add all wires, labels, and other elements if provided
    if elements:
        for wire in elements.get('wires', []):
            content += "\n" + wire
        for label in elements.get('labels', []):
            content += "\n" + label
        for glabel in elements.get('global_labels', []):
            content += "\n" + glabel
        for junction in elements.get('junctions', []):
            content += "\n" + junction
        for nc in elements.get('no_connects', []):
            content += "\n" + nc
        for bus in elements.get('bus', []):
            content += "\n" + bus
        for be in elements.get('bus_entry', []):
            content += "\n" + be
        for pl in elements.get('polyline', []):
            content += "\n" + pl

    content += create_schematic_footer()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created: {filepath}")

def main():
    # Paths
    script_dir = Path(__file__).parent
    original_sch = script_dir.parent / "wrx-power-can-hat-MANUAL.kicad_sch"

    power_hat_dir = script_dir / "power-hat"
    can_hat_dir = script_dir / "can-hat"
    dac_amp_dir = script_dir / "dac-amp"

    print("=" * 60)
    print("SubaruDash Schematic Splitter")
    print("=" * 60)

    # Read original schematic
    print(f"\nReading: {original_sch}")
    content = read_schematic(original_sch)

    # Extract components
    print("Extracting symbols...")
    symbols = extract_symbol_blocks(content)
    print(f"  Found {len(symbols)} symbols")

    # Extract lib_symbols
    print("Extracting library symbols...")
    lib_symbols = extract_lib_symbols(content)

    # Extract wires and labels
    print("Extracting wires and labels...")
    elements = extract_wires_and_labels(content)
    print(f"  Wires: {len(elements['wires'])}")
    print(f"  Labels: {len(elements['labels'])}")
    print(f"  Global labels: {len(elements['global_labels'])}")

    # Filter for each board
    print("\nFiltering components...")

    power_symbols = filter_symbols_for_board(symbols, POWER_HAT_COMPONENTS)
    print(f"  Power HAT: {len(power_symbols)} components")

    can_symbols = filter_symbols_for_board(symbols, CAN_HAT_COMPONENTS)
    print(f"  CAN HAT: {len(can_symbols)} components")

    # List what we found
    print("\n--- Power HAT Components ---")
    for sym in power_symbols:
        ref = get_symbol_reference(sym)
        if ref:
            print(f"  {ref}")

    print("\n--- CAN HAT Components ---")
    for sym in can_symbols:
        ref = get_symbol_reference(sym)
        if ref:
            print(f"  {ref}")

    # Add Pi header to each HAT
    power_symbols.append(create_pi_header_symbol("J2", 200, 150))
    can_symbols.append(create_pi_header_symbol("J2", 200, 150))

    # Write schematics - include ALL labels since they use label-based connections
    print("\nWriting schematics...")
    print(f"  Including {len(elements['labels'])} labels")
    print(f"  Including {len(elements['global_labels'])} global labels")
    print(f"  Including {len(elements['wires'])} wires")
    print(f"  Including {len(elements['junctions'])} junctions")

    write_schematic(
        power_hat_dir / "power-hat.kicad_sch",
        "SubaruDash Power HAT",
        lib_symbols,
        power_symbols,
        elements  # Include all labels and wires
    )

    write_schematic(
        can_hat_dir / "can-hat.kicad_sch",
        "SubaruDash CAN HAT",
        lib_symbols,
        can_symbols,
        elements  # Include all labels and wires
    )

    # DAC/Amp is a new design - create empty template
    print("\nCreating DAC/Amp template (new design - needs components added)...")
    dac_template = create_schematic_header("SubaruDash DAC/Amp Module")
    dac_template += "\n\t(lib_symbols\n\t)\n"
    dac_template += '''
	(text "DAC/Amp Module - New Design"
		(at 100 50 0)
		(effects
			(font
				(size 5 5)
			)
		)
		(uuid "''' + generate_uuid() + '''")
	)
	(text "Components needed:\\n- PCM5142 Quad I2S DAC\\n- 2x TPA3116D2 Class D Amp\\n- I2S input connector\\n- Speaker output connector\\n- Power regulation"
		(at 100 80 0)
		(effects
			(font
				(size 2 2)
			)
		)
		(uuid "''' + generate_uuid() + '''")
	)
'''
    dac_template += create_schematic_footer()

    with open(dac_amp_dir / "dac-amp.kicad_sch", 'w', encoding='utf-8') as f:
        f.write(dac_template)
    print(f"Created: {dac_amp_dir / 'dac-amp.kicad_sch'}")

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Open each .kicad_pro file in KiCad")
    print("2. Review and connect the components")
    print("3. Add power symbols (+5V, +3.3V, GND)")
    print("4. Run ERC to check for errors")
    print("5. Assign/verify footprints")
    print("6. Create PCB layouts")
    print("\nNote: Wires were not copied - you'll need to reconnect components")
    print("      in each schematic. The component positions are preserved.")

if __name__ == "__main__":
    main()
