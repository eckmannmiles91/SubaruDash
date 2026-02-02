#!/usr/bin/env python3
"""
Add net labels to KiCad schematic for wiring
Places labels near components based on connection map
"""

import uuid

# Component positions (mm) from generate_schematic.py
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

def mm_to_kicad(mm):
    return mm * 2.54

# Complete connection map from SCHEMATIC_DESIGN.md
# Format: {net_name: [list of component refs that connect to this net]}
NETS = {
    "GND": ["J1", "C1", "C2", "C3", "C6", "C7", "C8", "C9", "C10", "C11", "C12",
            "U1", "U2", "U3", "U4", "U5", "U6", "J2", "J3", "D7"],
    "+12V": ["J1", "F1", "D1", "Q1"],
    "+5V": ["U1", "C3", "C7", "U3", "U4", "U6", "J2"],
    "+3.3V": ["U5", "U6", "J2", "C6"],
    "12V_FUSED": ["F1", "D1", "D2", "C1"],
    "12V_SWITCHED": ["D2", "Q1", "U1", "LED1", "R3"],
    "GATE_CTRL": ["U3", "R10", "Q2"],
    "12V_IGN": ["J1", "R6", "U2"],
    "IGN_DETECT": ["U2", "R7", "C4", "C5", "U3", "J2"],
    "SHUTDOWN_REQ": ["U3", "J2"],
    "TIMER_LED": ["U3", "R9", "LED2"],
    "HEARTBEAT_LED": ["U3", "R14", "LED3"],
    "RESET": ["U3", "R8", "J3"],
    "SPI_MOSI": ["J2", "U4"],
    "SPI_MISO": ["J2", "U4"],
    "SPI_SCLK": ["J2", "U4"],
    "SPI_CE0": ["J2", "U4"],
    "CAN_INT": ["U4", "J2", "R12"],
    "CAN_TX": ["U4", "U5"],
    "CAN_RX": ["U4", "U5"],
    "CANH": ["U5", "J4", "J5", "R13", "JP1"],
    "CANL": ["U5", "J4", "J5", "R13", "JP1"],
    "XTAL1": ["U4", "Y1", "C9"],
    "XTAL2": ["U4", "Y1", "C10"],
    "FAN_PWM": ["J2", "R15", "Q3"],
    "FAN+": ["JP2", "J6"],
    "FAN-": ["Q3", "J6", "D7"],
    "I2S_BCK": ["J2", "U7"],
    "I2S_DATA": ["J2", "U7"],
    "I2S_LRCK": ["J2", "U7"],
    "AUDIO_L+": ["U7", "R16", "C15", "J7"],
    "AUDIO_L-": ["U7", "R17", "C16", "J7"],
    "AUDIO_R+": ["U7", "R18", "C17", "J7"],
    "AUDIO_R-": ["U7", "R19", "C18", "J7"],
}

def generate_uuid():
    return str(uuid.uuid4())

def create_global_label(net_name, x, y):
    """Create a global label at position."""
    uuid_str = generate_uuid()
    x_k = mm_to_kicad(x)
    y_k = mm_to_kicad(y)

    # Try global_label instead of label
    return f"""	(global_label "{net_name}" (shape input) (at {x_k} {y_k} 0)
		(effects (font (size 1.27 1.27)) (justify left))
		(uuid {uuid_str})
		(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x_k} {y_k} 0)
			(effects (font (size 1.27 1.27)) hide)
		)
	)
"""

def main():
    input_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-AUTO.kicad_sch"
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-WIRED.kicad_sch"

    print("Generating wired schematic...")

    # Read existing schematic
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate labels for each net
    labels = "\n"
    total_labels = 0

    for net_name, components in NETS.items():
        for comp_ref in components:
            if comp_ref in COMPONENTS:
                x, y = COMPONENTS[comp_ref]
                # Place label slightly offset from component
                label_x = x + 10
                label_y = y
                labels += create_global_label(net_name, label_x, label_y)
                total_labels += 1

    # Insert labels before sheet_instances section (proper KiCad structure)
    marker = "\t(sheet_instances"
    insertion_point = content.find(marker)
    if insertion_point == -1:
        # Fallback: insert before final closing paren
        insertion_point = content.rfind(')')
    new_content = content[:insertion_point] + labels + content[insertion_point:]

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Added {total_labels} labels for {len(NETS)} nets")
    print(f"[OK] Saved to: {output_file}")
    print()
    print("Next steps:")
    print("1. Open wrx-power-can-hat-WIRED.kicad_sch in KiCad")
    print("2. Labels are placed near each component")
    print("3. Drag labels to connect to the correct component pins")
    print("4. Labels with the same name are automatically connected")

if __name__ == "__main__":
    main()
