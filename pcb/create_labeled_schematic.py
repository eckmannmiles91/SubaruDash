#!/usr/bin/env python3
"""
Create a clean schematic using global labels for all connections
Removes problematic wires and replaces them with labels
Adds No Connect flags to unused pins
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
    pin_locations = {}  # {(comp_ref, pin_num): (x_mils, y_mils)}

    with open(erc_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Parse lines like: @(2300 mils, 4800 mils): Symbol J1 Pin 2 [Pin_2, Passive, Line]
            match = re.search(r'@\((\d+) mils, (\d+) mils\): Symbol (\S+) Pin (\S+)', line)
            if match:
                x_mils = int(match.group(1))
                y_mils = int(match.group(2))
                comp_ref = match.group(3)
                pin_num = match.group(4)
                pin_locations[(comp_ref, pin_num)] = (x_mils, y_mils)

    return pin_locations

def mils_to_mm(mils):
    """Convert mils to mm"""
    return mils * 0.0254

def create_global_label(net_name, x_mils, y_mils):
    """Create a global label at specified position"""
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
    """Create a no_connect flag"""
    uuid_str = generate_uuid()
    x_mm = mils_to_mm(x_mils)
    y_mm = mils_to_mm(y_mils)
    return f"\t(no_connect (at {x_mm:.6f} {y_mm:.6f}) (uuid {uuid_str}))\n"

def create_power_symbol(symbol_type, x_mils, y_mils):
    """Create a power symbol (GND, +12V, +5V, +3.3V)"""
    uuid_str = generate_uuid()
    x_mm = mils_to_mm(x_mils)
    y_mm = mils_to_mm(y_mils)

    # Offset for text placement
    if symbol_type == "GND":
        y_offset = 2.5
    else:
        y_offset = -2.5

    return f"""\t(symbol (lib_id "power:{symbol_type}") (at {x_mm:.6f} {y_mm:.6f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
\t\t(uuid {uuid_str})
\t\t(property "Reference" "#PWR?" (at {x_mm:.6f} {y_mm + y_offset:.6f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(property "Value" "{symbol_type}" (at {x_mm:.6f} {y_mm + 3:.6f} 0)
\t\t\t(effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {x_mm:.6f} {y_mm:.6f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(property "Datasheet" "" (at {x_mm:.6f} {y_mm:.6f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid {generate_uuid()}))
\t\t(instances
\t\t\t(project "wrx-power-can-hat-LABELS"
\t\t\t\t(path "/rootsheet" (reference "#PWR?") (unit 1))
\t\t\t)
\t\t)
\t)
"""

def remove_wires_and_junctions(content):
    """Remove all wire and junction elements from schematic"""
    # Remove wire elements (multi-line)
    content = re.sub(r'\t\(wire\s.*?\n\t\)\n', '', content, flags=re.DOTALL)

    # Remove junction elements (multi-line with nested properties)
    content = re.sub(r'\t\(junction\s+\(at\s+[^)]+\)\s+\(diameter\s+[^)]+\)\s+\(color\s+[^)]+\)\s*\n\s+\(uuid\s+[^)]+\)\s*\n\s+\)\n', '', content, flags=re.DOTALL)

    # Remove no_connect elements (we'll add them back properly)
    content = re.sub(r'\t\(no_connect\s+\(at\s+[^)]+\)\s+\(uuid\s+[^)]+\)\s*\)\n', '', content, flags=re.DOTALL)

    # Remove global_label elements (we'll add them back)
    content = re.sub(r'\t\(global_label\s.*?\n\t\)\n', '', content, flags=re.DOTALL)

    return content

def main():
    input_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-PINTOPIN.kicad_sch"
    erc_file = "C:/Users/eckma/projects/SubaruDash/pcb/ERC.rpt"
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-LABELS.kicad_sch"

    print("Creating clean schematic with global labels...")
    print()

    # Parse ERC to get pin locations
    print("Step 1: Parsing pin locations from ERC report...")
    pin_locations = parse_erc_for_pin_locations(erc_file)
    print(f"  Found {len(pin_locations)} pin locations")

    # Read schematic
    print("\nStep 2: Reading PINTOPIN schematic...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove all wires and junctions
    print("\nStep 3: Removing existing wires and junctions...")
    content = remove_wires_and_junctions(content)

    # Generate global labels and no_connects
    additions = "\n"
    label_count = 0
    no_connect_count = 0
    power_symbol_count = 0

    # Track power nets to add power symbols
    power_nets = {
        "GND": [],
        "+12V": [],
        "+5V": [],
        "+3.3V": []
    }

    print("\nStep 4: Adding global labels for connections...")
    for comp_ref, pin_map in PIN_CONNECTIONS.items():
        for pin_num, net_name in pin_map.items():
            key = (comp_ref, pin_num)
            if key in pin_locations:
                x_mils, y_mils = pin_locations[key]
                additions += create_global_label(net_name, x_mils, y_mils)
                label_count += 1

                # Track power net locations
                if net_name in power_nets:
                    power_nets[net_name].append((x_mils, y_mils))
            else:
                print(f"  WARNING: No location found for {comp_ref} pin {pin_num}")

    print(f"  Added {label_count} global labels")

    print("\nStep 5: Adding No Connect flags to unused pins...")
    for (comp_ref, pin_num), (x_mils, y_mils) in pin_locations.items():
        # Skip power symbols
        if comp_ref.startswith('#PWR'):
            continue

        # Check if this pin should be connected
        if comp_ref in PIN_CONNECTIONS:
            if pin_num not in PIN_CONNECTIONS[comp_ref]:
                # This pin is unused - add no_connect
                additions += create_no_connect(x_mils, y_mils)
                no_connect_count += 1

    print(f"  Added {no_connect_count} No Connect flags")

    print("\nStep 6: Adding power symbols for power nets...")
    for power_type, locations in power_nets.items():
        if locations:
            # Add one power symbol per unique power net location
            # (deduplicate close locations)
            unique_locs = []
            for x, y in locations:
                # Check if we already have a symbol close to this location
                is_duplicate = False
                for ux, uy in unique_locs:
                    if abs(x - ux) < 100 and abs(y - uy) < 100:  # Within 100 mils
                        is_duplicate = True
                        break

                if not is_duplicate:
                    unique_locs.append((x, y))
                    # Offset the power symbol slightly from the pin
                    offset_x = x + 50
                    offset_y = y
                    additions += create_power_symbol(power_type, offset_x, offset_y)
                    power_symbol_count += 1

    print(f"  Added {power_symbol_count} power symbols")

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
    print(f"  - Removed all wires and junctions from PINTOPIN")
    print(f"  - Added {label_count} global labels for connections")
    print(f"  - Added {no_connect_count} No Connect flags for unused pins")
    print(f"  - Added {power_symbol_count} power symbols")
    print()
    print("Next steps:")
    print("1. Open the new schematic in KiCad")
    print("2. Run ERC to verify connections")
    print("3. Run Tools -> Update Schematic from PCB (if PCB exists)")
    print("4. The schematic should have FAR fewer errors!")

if __name__ == "__main__":
    main()
