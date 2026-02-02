#!/usr/bin/env python3
"""
Automatically add No Connect flags to unused pins
Based on PIN_CONNECTIONS dictionary from the design
"""

import re
import uuid

def generate_uuid():
    return str(uuid.uuid4())

# Pin connections from design - only these pins should be connected
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

def find_all_component_pins(content):
    """Parse schematic to find all component pins"""
    component_pins = {}  # {comp_ref: [list of pin numbers]}

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('(symbol (lib_id'):
            # Found a symbol instance
            depth = 1
            symbol_lines = [line]
            i += 1
            while i < len(lines) and depth > 0:
                current = lines[i]
                symbol_lines.append(current)
                depth += current.count('(') - current.count(')')
                i += 1

            symbol_body = '\n'.join(symbol_lines)

            # Extract reference
            ref_match = re.search(r'\(property "Reference" "([^"]+)"', symbol_body)
            if not ref_match:
                continue

            comp_ref = ref_match.group(1)

            # Skip power symbols
            if comp_ref.startswith('#PWR'):
                continue

            # Extract all pin numbers
            pin_matches = re.finditer(r'\(pin "([^"]+)"\s+\(uuid\s+[^)]+\)\)', symbol_body)
            pins = [pin_match.group(1) for pin_match in pin_matches]

            if pins:
                component_pins[comp_ref] = pins

            continue
        i += 1

    return component_pins

def create_no_connect(x, y):
    """Create a no_connect S-expression"""
    uuid_str = generate_uuid()
    return f'\t(no_connect (at {float(x):.6f} {float(y):.6f}) (uuid {uuid_str}))\n'

def find_pin_location(content, comp_ref, pin_num):
    """Find the coordinates of a specific pin from ERC-style position info"""
    # Try to find in symbol definition or use approximation
    # For now, return None - we'll add no_connects without coordinates
    return None

def main():
    input_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-PINTOPIN.kicad_sch"
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-NOCONNECTS.kicad_sch"

    print("Adding No Connect flags to unused pins...")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all component pins in the schematic
    all_pins = find_all_component_pins(content)

    print(f"Found {len(all_pins)} components in schematic")

    # Determine which pins need No Connect
    no_connect_count = 0
    pins_to_mark = []

    for comp_ref, all_pin_nums in all_pins.items():
        if comp_ref in PIN_CONNECTIONS:
            used_pins = set(PIN_CONNECTIONS[comp_ref].keys())
            all_pins_set = set(all_pin_nums)
            unused_pins = all_pins_set - used_pins

            if unused_pins:
                print(f"{comp_ref}: {len(unused_pins)} unused pins: {sorted(unused_pins)}")
                for pin_num in unused_pins:
                    pins_to_mark.append((comp_ref, pin_num))
                    no_connect_count += 1

    print(f"\nNeed to add No Connect to {no_connect_count} pins")
    print("\nNOTE: This script identifies which pins need No Connect flags,")
    print("but adding them programmatically requires pin coordinate information.")
    print("\nManual approach is still needed in KiCad:")
    print("1. Press 'Q' to activate No Connect tool")
    print("2. Click on each unused pin")
    print("\nOR we can fix the major wiring issues first with global labels")

    # Write the analysis
    with open("C:/Users/eckma/projects/SubaruDash/pcb/no_connect_analysis.txt", 'w') as f:
        f.write("Pins that need No Connect flags:\n\n")
        for comp_ref, pin_num in sorted(pins_to_mark):
            f.write(f"{comp_ref} pin {pin_num}\n")

    print("\nSaved analysis to no_connect_analysis.txt")

if __name__ == "__main__":
    main()
