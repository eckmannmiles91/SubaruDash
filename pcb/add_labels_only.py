#!/usr/bin/env python3
"""
ADD global labels and no_connects to existing schematic
WITHOUT removing anything - just augment it
"""

import re
import uuid

def generate_uuid():
    return str(uuid.uuid4())

# Pin connections from design specification
PIN_CONNECTIONS = {
    "J1": {"4": "+12V", "7": "12V_IGN", "8": "GND"},
    "F1": {"1": "+12V", "2": "12V_FUSED"},
    "D1": {"1": "12V_FUSED", "2": "GND"},
    "D2": {"1": "12V_FUSED", "2": "12V_SWITCHED"},
    "Q1": {"1": "12V_FUSED", "2": "GATE_CTRL", "3": "12V_SWITCHED"},
    "R1": {"1": "+12V", "2": "GND"},
    "R2": {"1": "12V_FUSED", "2": "GATE_CTRL"},
    "R3": {"1": "12V_SWITCHED", "2": "LED1_ANODE"},
    "C1": {"1": "12V_FUSED", "2": "GND"},
    "LED1": {"1": "LED1_ANODE", "2": "GND"},
    "U1": {"1": "12V_SWITCHED", "2": "U1_SW", "3": "GND", "4": "U1_FB", "5": "12V_SWITCHED"},
    "L1": {"1": "U1_SW", "2": "+5V"},
    "D3": {"1": "GND", "2": "U1_SW"},
    "C2": {"1": "12V_SWITCHED", "2": "GND"},
    "C3": {"1": "+5V", "2": "GND"},
    "R4": {"1": "+5V", "2": "U1_FB"},
    "R5": {"1": "U1_FB", "2": "GND"},
    "U2": {"1": "12V_IGN", "2": "GND", "3": "GND", "4": "IGN_DETECT"},
    "R6": {"1": "12V_IGN", "2": "U2_LED"},
    "R7": {"1": "IGN_DETECT", "2": "+3.3V"},
    "C4": {"1": "IGN_DETECT", "2": "GND"},
    "C5": {"1": "IGN_DETECT", "2": "GND"},
    "U3": {"1": "RESET", "2": "TIMER_LED", "3": "HEARTBEAT_LED", "4": "GND",
           "5": "IGN_DETECT", "6": "SHUTDOWN_REQ", "7": "GATE_CTRL", "8": "+3.3V"},
    "C6": {"1": "+3.3V", "2": "GND"},
    "R8": {"1": "RESET", "2": "+3.3V"},
    "R9": {"1": "TIMER_LED", "2": "LED2_ANODE"},
    "R14": {"1": "HEARTBEAT_LED", "2": "LED3_ANODE"},
    "LED2": {"1": "LED2_ANODE", "2": "GND"},
    "LED3": {"1": "LED3_ANODE", "2": "GND"},
    "J3": {"1": "SPI_MISO", "2": "+3.3V", "3": "SPI_SCLK", "4": "SPI_MOSI", "5": "RESET", "6": "GND"},
    "Q2": {"1": "GATE_CTRL", "2": "Q1_GATE", "3": "GND"},
    "R10": {"1": "GATE_CTRL", "2": "Q2_GATE"},
    "R11": {"1": "Q2_GATE", "2": "GND"},
    "U4": {"1": "SPI_CE0", "2": "SPI_SCLK", "3": "SPI_MISO", "4": "SPI_MOSI",
           "5": "GND", "6": "CAN_INT", "7": "XTAL2", "8": "XTAL1",
           "9": "+3.3V", "10": "CAN_RX", "11": "CAN_TX"},
    "U5": {"1": "CAN_TX", "2": "GND", "3": "+3.3V", "4": "CAN_RX", "5": "CANL", "6": "CANH"},
    "Y1": {"1": "XTAL1", "2": "XTAL2"},
    "C7": {"1": "+3.3V", "2": "GND"},
    "C8": {"1": "+3.3V", "2": "GND"},
    "C9": {"1": "XTAL1", "2": "GND"},
    "C10": {"1": "XTAL2", "2": "GND"},
    "R12": {"1": "CAN_INT", "2": "+3.3V"},
    "R13": {"1": "CANH", "2": "CANL"},
    "J4": {"6": "CANH", "14": "CANL", "4": "GND"},
    "J5": {"1": "CANH", "2": "CANL"},
    "JP1": {"1": "CANH", "2": "CANL"},
    "Q3": {"1": "FAN_PWM", "2": "FAN-", "3": "GND"},
    "D7": {"1": "FAN-", "2": "FAN+"},
    "R15": {"1": "FAN_PWM", "2": "Q3_GATE"},
    "J6": {"1": "FAN+", "2": "FAN-"},
    "JP2": {"1": "+5V", "2": "FAN+", "3": "12V_SWITCHED"},
    "U6": {"1": "GND", "2": "+3.3V", "3": "+5V"},
    "C11": {"1": "+5V", "2": "GND"},
    "C12": {"1": "+3.3V", "2": "GND"},
    "J2": {"1": "+3.3V", "2": "+5V", "4": "+5V", "6": "GND", "9": "GND",
           "19": "SPI_MOSI", "21": "SPI_MISO", "22": "CAN_INT", "23": "SPI_SCLK",
           "24": "SPI_CE0", "37": "FAN_PWM", "12": "SHUTDOWN_REQ"},
    "U7": {"1": "I2S_BCK", "2": "I2S_LRCK", "3": "I2S_DATA", "4": "+3.3V",
           "5": "GND", "6": "AUDIO_L+", "7": "AUDIO_L-", "8": "AUDIO_R+", "9": "AUDIO_R-"},
    "C13": {"1": "+3.3V", "2": "GND"},
    "C14": {"1": "+3.3V", "2": "GND"},
    "C15": {"1": "AUDIO_L+", "2": "AUDIO_L_OUT"},
    "C16": {"1": "AUDIO_L-", "2": "AUDIO_L_OUT"},
    "C17": {"1": "AUDIO_R+", "2": "AUDIO_R_OUT"},
    "C18": {"1": "AUDIO_R-", "2": "AUDIO_R_OUT"},
    "R16": {"1": "AUDIO_L+", "2": "AUDIO_L_OUT"},
    "R17": {"1": "AUDIO_L-", "2": "AUDIO_L_OUT"},
    "R18": {"1": "AUDIO_R+", "2": "AUDIO_R_OUT"},
    "R19": {"1": "AUDIO_R-", "2": "AUDIO_R_OUT"},
    "J7": {"1": "AUDIO_L_OUT", "2": "AUDIO_L_OUT", "3": "AUDIO_R_OUT",
           "4": "AUDIO_R_OUT", "5": "GND", "6": "GND"},
}

def parse_erc_for_pin_locations(erc_file):
    """Extract pin locations from ERC report"""
    pin_locations = {}

    with open(erc_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(r'@\((\d+) mils, (\d+) mils\): Symbol (\S+) Pin (\S+)', line)
            if match:
                x_mils = int(match.group(1))
                y_mils = int(match.group(2))
                comp_ref = match.group(3)
                pin_num = match.group(4)
                pin_locations[(comp_ref, pin_num)] = (x_mils, y_mils)

    return pin_locations

def mils_to_mm(mils):
    return mils * 0.0254

def create_global_label(net_name, x_mils, y_mils):
    uuid_str = generate_uuid()
    x_mm = mils_to_mm(x_mils)
    y_mm = mils_to_mm(y_mils)

    return f"""\t(global_label "{net_name}" (shape input) (at {x_mm:.6f} {y_mm:.6f} 0) (fields_autoplaced yes)
\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t(uuid {uuid_str})
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {x_mm:.6f} {y_mm:.6f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t)
"""

def create_no_connect(x_mils, y_mils):
    uuid_str = generate_uuid()
    x_mm = mils_to_mm(x_mils)
    y_mm = mils_to_mm(y_mils)
    return f"\t(no_connect (at {x_mm:.6f} {y_mm:.6f}) (uuid {uuid_str}))\n"

def main():
    input_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-PINTOPIN.kicad_sch"
    erc_file = "C:/Users/eckma/projects/SubaruDash/pcb/ERC.rpt"
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-AUGMENTED.kicad_sch"

    print("Augmenting PINTOPIN schematic with labels and no_connects...")
    print("(Keeping all existing wires intact)")
    print()

    # Parse ERC to get pin locations
    print("Step 1: Parsing pin locations from ERC report...")
    pin_locations = parse_erc_for_pin_locations(erc_file)
    print(f"  Found {len(pin_locations)} pin locations")

    # Read schematic
    print("\nStep 2: Reading PINTOPIN schematic...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate additions ONLY (no removals)
    additions = "\n"
    label_count = 0
    no_connect_count = 0

    print("\nStep 3: Adding global labels for connections...")
    for comp_ref, pin_map in PIN_CONNECTIONS.items():
        for pin_num, net_name in pin_map.items():
            key = (comp_ref, pin_num)
            if key in pin_locations:
                x_mils, y_mils = pin_locations[key]
                # Place label EXACTLY on pin (no offset) for proper connection
                additions += create_global_label(net_name, x_mils, y_mils)
                label_count += 1

    print(f"  Will add {label_count} global labels")

    print("\nStep 4: Adding No Connect flags to unused pins...")
    for (comp_ref, pin_num), (x_mils, y_mils) in pin_locations.items():
        if comp_ref.startswith('#PWR'):
            continue

        if comp_ref in PIN_CONNECTIONS:
            if pin_num not in PIN_CONNECTIONS[comp_ref]:
                additions += create_no_connect(x_mils, y_mils)
                no_connect_count += 1

    print(f"  Will add {no_connect_count} No Connect flags")

    # Insert additions before sheet_instances
    marker = "\t(sheet_instances"
    insertion_point = content.find(marker)
    if insertion_point == -1:
        insertion_point = content.rfind(')')

    new_content = content[:insertion_point] + additions + content[insertion_point:]

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n{'='*60}")
    print("SUCCESS!")
    print(f"{'='*60}")
    print(f"Output: {output_file}")
    print()
    print("Summary:")
    print(f"  - Kept all existing wires and junctions from PINTOPIN")
    print(f"  - Added {label_count} global labels for connections")
    print(f"  - Added {no_connect_count} No Connect flags for unused pins")
    print()
    print("This schematic should open cleanly and not crash on ERC")

if __name__ == "__main__":
    main()
