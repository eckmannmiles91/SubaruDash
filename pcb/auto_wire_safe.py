#!/usr/bin/env python3
"""
Safe auto-wiring script - creates short wire stubs only
Relies on global labels for connections (no complex routing)
"""

import re
import uuid
import math

def generate_uuid():
    return str(uuid.uuid4())

def mm_to_kicad(mm):
    return mm * 2.54

# Component positions from generate_schematic.py
COMPONENTS = {
    "F1": (50, 50), "D1": (75, 50), "D2": (100, 50), "Q1": (125, 50),
    "R1": (50, 75), "R2": (75, 75), "R3": (100, 75), "C1": (125, 75),
    "LED1": (150, 75), "J1": (25, 50), "U1": (50, 125), "L1": (75, 125),
    "D3": (100, 125), "C2": (50, 150), "C3": (75, 150), "R4": (100, 150),
    "R5": (125, 150), "U2": (175, 50), "R6": (175, 75), "R7": (200, 75),
    "C4": (225, 75), "C5": (250, 75), "U3": (175, 125), "C6": (175, 150),
    "R8": (200, 150), "R9": (225, 150), "R14": (250, 150), "LED2": (200, 125),
    "LED3": (225, 125), "J3": (250, 125), "Q2": (150, 50), "R10": (150, 75),
    "R11": (175, 50), "U4": (50, 200), "U5": (100, 200), "Y1": (75, 225),
    "C7": (50, 225), "C8": (100, 225), "C9": (125, 225), "C10": (150, 225),
    "R12": (125, 200), "R13": (150, 200), "J4": (175, 200), "J5": (175, 225),
    "JP1": (200, 225), "Q3": (225, 200), "D7": (250, 200), "R15": (225, 225),
    "J6": (250, 225), "JP2": (275, 225), "U6": (50, 275), "C11": (75, 275),
    "C12": (100, 275), "J2": (150, 275), "U7": (225, 275), "C13": (250, 275),
    "C14": (275, 275), "C15": (225, 300), "C16": (250, 300), "C17": (275, 300),
    "C18": (300, 300), "R16": (225, 325), "R17": (250, 325), "R18": (275, 325),
    "R19": (300, 325), "J7": (325, 300),
}

# Simplified - just the nets for labels
NETS = {
    "GND": ["J1", "C1", "C2", "C3", "C6", "C7", "C8", "C9", "C10", "C11", "C12",
            "U1", "U2", "U3", "U4", "U5", "J2", "J3"],
    "+12V": ["J1", "F1", "D1", "Q1"],
    "+5V": ["U1", "C3", "C7", "U3", "U4", "J2"],
    "+3.3V": ["U5", "J2", "C6"],
    "12V_FUSED": ["F1", "D1", "D2", "C1"],
    "12V_SWITCHED": ["D2", "Q1", "U1", "LED1", "R3"],
    "12V_IGN": ["J1", "R6", "U2"],
    "IGN_DETECT": ["U2", "R7", "C4", "C5", "U3", "J2"],
    "SPI_MOSI": ["J2", "U4"],
    "SPI_MISO": ["J2", "U4"],
    "SPI_SCLK": ["J2", "U4"],
    "SPI_CE0": ["J2", "U4"],
    "CAN_INT": ["U4", "J2", "R12"],
    "CAN_TX": ["U4", "U5"],
    "CAN_RX": ["U4", "U5"],
    "CANH": ["U5", "J4", "J5", "R13", "JP1"],
    "CANL": ["U5", "J4", "J5", "R13", "JP1"],
}

def create_global_label(net_name, x, y):
    """Create a global label at position."""
    uuid_str = generate_uuid()
    x_k = mm_to_kicad(x)
    y_k = mm_to_kicad(y)

    return f"""\t(global_label "{net_name}" (shape input) (at {x_k} {y_k} 0)
\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t(uuid {uuid_str})
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x_k} {y_k} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t)
"""

def create_power_symbol(symbol_type, x, y):
    """Create a power symbol (GND, +12V, +5V, +3.3V)"""
    uuid_str = generate_uuid()
    x_k = mm_to_kicad(x)
    y_k = mm_to_kicad(y)

    # Determine y_offset based on symbol type
    if symbol_type == "GND":
        y_offset = 2.5  # GND symbols point down
    else:
        y_offset = -2.5  # Power symbols point up

    return f"""\t(symbol (lib_id "power:{symbol_type}") (at {x_k} {y_k} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
\t\t(uuid {uuid_str})
\t\t(property "Reference" "#PWR?" (at {x_k} {y_k + y_offset} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(property "Value" "{symbol_type}" (at {x_k} {y_k + 3} 0)
\t\t\t(effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x_k} {y_k} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(property "Datasheet" "" (at {x_k} {y_k} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid {generate_uuid()}))
\t\t(instances
\t\t\t(project "wrx-power-can-hat-AUTOWIRED"
\t\t\t\t(path "/rootsheet" (reference "#PWR?") (unit 1))
\t\t\t)
\t\t)
\t)
"""

def main():
    input_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-AUTO.kicad_sch"
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-SAFE.kicad_sch"

    print("Generating safely wired schematic...")

    # Read schematic
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate labels and power symbols
    additions = "\n"
    label_count = 0
    power_symbol_count = 0

    # Place global labels near each component for each net
    for net_name, components in NETS.items():
        for comp_ref in components:
            if comp_ref in COMPONENTS:
                x, y = COMPONENTS[comp_ref]
                # Place label to the right of component
                label_x = x + 15
                label_y = y
                additions += create_global_label(net_name, label_x, label_y)
                label_count += 1

    # Add power symbols at strategic locations for power nets
    power_net_positions = {
        "GND": [(50, 180), (150, 180), (250, 180)],  # Multiple GND points
        "+12V": [(50, 20), (150, 20)],  # Multiple +12V points
        "+5V": [(50, 100), (150, 100)],  # Multiple +5V points
        "+3.3V": [(150, 240)],  # +3.3V point
    }

    for power_net, positions in power_net_positions.items():
        for x, y in positions:
            additions += create_power_symbol(power_net, x, y)
            power_symbol_count += 1

    # Insert additions before sheet_instances section
    marker = "\t(sheet_instances"
    insertion_point = content.find(marker)
    if insertion_point == -1:
        insertion_point = content.rfind(')')

    new_content = content[:insertion_point] + additions + content[insertion_point:]

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Added {label_count} global labels for {len(NETS)} nets")
    print(f"[OK] Added {power_symbol_count} power symbols")
    print(f"[OK] Saved to: {output_file}")
    print()
    print("Next: Open in KiCad and manually connect:")
    print("  1. Drag labels to component pins")
    print("  2. Power symbols connect automatically via matching names")
    print("  3. Labels with same name = electrical connection")

if __name__ == "__main__":
    main()
