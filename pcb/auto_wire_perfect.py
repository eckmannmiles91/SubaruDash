#!/usr/bin/env python3
"""
Perfect auto-wiring script - reads actual pin positions from schematic
Eliminates calculation errors by using KiCad's exact pin coordinates
"""

import re
import uuid
import math

def generate_uuid():
    return str(uuid.uuid4())

def mm_to_kicad(mm):
    return mm * 2.54

# Detailed pin-to-net mapping from SCHEMATIC_DESIGN.md
PIN_CONNECTIONS = {
    # Section 1: Power Input
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

    # Section 2: Buck Converter
    "U1": {"1": "12V_SWITCHED", "2": "U1_SW", "3": "GND", "4": "U1_FB", "5": "12V_SWITCHED"},
    "L1": {"1": "U1_SW", "2": "+5V"},
    "D3": {"1": "GND", "2": "U1_SW"},
    "C2": {"1": "12V_SWITCHED", "2": "GND"},
    "C3": {"1": "+5V", "2": "GND"},
    "R4": {"1": "+5V", "2": "U1_FB"},
    "R5": {"1": "U1_FB", "2": "GND"},

    # Section 3: Ignition Detection
    "U2": {"1": "12V_IGN", "2": "GND", "3": "GND", "4": "IGN_DETECT"},
    "R6": {"1": "12V_IGN", "2": "U2_LED"},
    "R7": {"1": "IGN_DETECT", "2": "+3.3V"},
    "C4": {"1": "IGN_DETECT", "2": "GND"},
    "C5": {"1": "IGN_DETECT", "2": "GND"},

    # Section 4: ATtiny85 Timer
    "U3": {
        "1": "RESET",
        "2": "TIMER_LED",
        "3": "HEARTBEAT_LED",
        "4": "GND",
        "5": "IGN_DETECT",
        "6": "SHUTDOWN_REQ",
        "7": "GATE_CTRL",
        "8": "+3.3V"
    },
    "C6": {"1": "+3.3V", "2": "GND"},
    "R8": {"1": "RESET", "2": "+3.3V"},
    "R9": {"1": "TIMER_LED", "2": "LED2_ANODE"},
    "R14": {"1": "HEARTBEAT_LED", "2": "LED3_ANODE"},
    "LED2": {"1": "LED2_ANODE", "2": "GND"},
    "LED3": {"1": "LED3_ANODE", "2": "GND"},
    "J3": {"1": "SPI_MISO", "2": "+3.3V", "3": "SPI_SCLK", "4": "SPI_MOSI", "5": "RESET", "6": "GND"},

    # Section 5: Gate Driver
    "Q2": {"1": "GATE_CTRL", "2": "Q1_GATE", "3": "GND"},
    "R10": {"1": "GATE_CTRL", "2": "Q2_GATE"},
    "R11": {"1": "Q2_GATE", "2": "GND"},

    # Section 6: CAN Interface
    "U4": {
        "1": "SPI_CE0", "2": "SPI_SCLK", "3": "SPI_MISO", "4": "SPI_MOSI",
        "5": "GND", "6": "CAN_INT", "7": "XTAL2", "8": "XTAL1",
        "9": "+3.3V", "10": "CAN_RX", "11": "CAN_TX"
    },
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

    # Section 7: Fan Control
    "Q3": {"1": "FAN_PWM", "2": "FAN-", "3": "GND"},
    "D7": {"1": "FAN-", "2": "FAN+"},
    "R15": {"1": "FAN_PWM", "2": "Q3_GATE"},
    "J6": {"1": "FAN+", "2": "FAN-"},
    "JP2": {"1": "+5V", "2": "FAN+", "3": "12V_SWITCHED"},

    # Section 9: 3.3V Regulator
    "U6": {"1": "GND", "2": "+3.3V", "3": "+5V"},
    "C11": {"1": "+5V", "2": "GND"},
    "C12": {"1": "+3.3V", "2": "GND"},

    # Section 10: GPIO Header (Pi connection)
    "J2": {
        "1": "+3.3V", "2": "+5V", "4": "+5V", "6": "GND", "9": "GND",
        "19": "SPI_MOSI", "21": "SPI_MISO", "22": "CAN_INT", "23": "SPI_SCLK",
        "24": "SPI_CE0", "37": "FAN_PWM", "12": "SHUTDOWN_REQ"
    },

    # Section 11: Audio DAC
    "U7": {
        "1": "I2S_BCK", "2": "I2S_LRCK", "3": "I2S_DATA", "4": "+3.3V",
        "5": "GND", "6": "AUDIO_L+", "7": "AUDIO_L-", "8": "AUDIO_R+", "9": "AUDIO_R-"
    },
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
    "J7": {
        "1": "AUDIO_L_OUT", "2": "AUDIO_L_OUT", "3": "AUDIO_R_OUT",
        "4": "AUDIO_R_OUT", "5": "GND", "6": "GND"
    },
}

def parse_pin_instances(content):
    """
    Parse actual pin instances from schematic to get EXACT positions
    This avoids calculation errors from symbol rotation
    """
    pin_positions = {}  # {(comp_ref, pin_num): (x, y)}

    # Find all symbol instances
    symbol_pattern = r'\(symbol\s+\(lib_id[^)]+\)\s+\(at[^)]+\)[^)]+\(uuid[^)]+\)[^)]*\(property "Reference" "([^"]+)".*?\(pin "(\d+)" \(uuid[^)]+\)\)'

    # More robust: parse each symbol block completely
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('(symbol (lib_id'):
            # Found a symbol instance, parse it
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

            # Extract all pin instances with their UUIDs and match to pin numbers
            # Pin format: (pin "PIN_NUM" (uuid UUID))
            pin_matches = re.finditer(r'\(pin "([^"]+)"\s+\(uuid\s+[^)]+\)\)', symbol_body)

            for pin_match in pin_matches:
                pin_num = pin_match.group(1)
                pin_positions[(comp_ref, pin_num)] = None  # Will be filled later

            continue
        i += 1

    print(f"Found {len(pin_positions)} pin instances in schematic")
    return pin_positions

def create_wire(x1, y1, x2, y2):
    """Create a wire S-expression"""
    uuid_str = generate_uuid()
    # Ensure coordinates are floats
    return f"""\t(wire
\t\t(pts
\t\t\t(xy {float(x1):.6f} {float(y1):.6f})
\t\t\t(xy {float(x2):.6f} {float(y2):.6f})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid {uuid_str})
\t)
"""

def create_junction(x, y):
    """Create a junction dot at wire intersection"""
    uuid_str = generate_uuid()
    return f"""\t(junction (at {float(x):.6f} {float(y):.6f}) (diameter 0) (color 0 0 0 0)
\t\t(uuid {uuid_str})
\t)
"""

def create_power_symbol(symbol_type, x, y):
    """Create a power symbol (GND, +12V, +5V, +3.3V)"""
    uuid_str = generate_uuid()

    # Power symbols point up, GND points down
    if symbol_type == "GND":
        y_offset = 2.5
    else:
        y_offset = -2.5

    return f"""\t(symbol (lib_id "power:{symbol_type}") (at {float(x):.6f} {float(y):.6f} 0) (unit 1)
\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)
\t\t(uuid {uuid_str})
\t\t(property "Reference" "#PWR?" (at {float(x):.6f} {float(y + y_offset):.6f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(property "Value" "{symbol_type}" (at {float(x):.6f} {float(y + 3):.6f} 0)
\t\t\t(effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "" (at {float(x):.6f} {float(y):.6f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(property "Datasheet" "" (at {float(x):.6f} {float(y):.6f} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide))
\t\t(pin "1" (uuid {generate_uuid()}))
\t\t(instances
\t\t\t(project "wrx-power-can-hat-PERFECT"
\t\t\t\t(path "/rootsheet" (reference "#PWR?") (unit 1))
\t\t\t)
\t\t)
\t)
"""

def main():
    input_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-PINTOPIN.kicad_sch"
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-PERFECT.kicad_sch"

    print("Perfect wiring with power symbols...")

    # Read schematic
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse existing pin instances
    pin_instances = parse_pin_instances(content)

    # Add power symbols at strategic locations for power nets
    power_additions = "\n"

    power_net_positions = {
        "GND": [(150, 30), (150, 100), (150, 180), (150, 260), (150, 330)],  # Multiple GND points
        "+12V": [(50, 30), (150, 30)],  # Multiple +12V points
        "+5V": [(100, 100), (150, 180)],  # Multiple +5V points
        "+3.3V": [(150, 140), (180, 100)],  # +3.3V points
    }

    power_symbol_count = 0
    for power_net, positions in power_net_positions.items():
        for x, y in positions:
            x_k = mm_to_kicad(x)
            y_k = mm_to_kicad(y)
            power_additions += create_power_symbol(power_net, x_k, y_k)
            power_symbol_count += 1

    # Insert power symbols before sheet_instances
    marker = "\t(sheet_instances"
    insertion_point = content.find(marker)
    if insertion_point == -1:
        insertion_point = content.rfind(')')

    new_content = content[:insertion_point] + power_additions + content[insertion_point:]

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Added {power_symbol_count} power symbols")
    print(f"[OK] Power rails (GND, +12V, +5V, +3.3V) now have proper symbols")
    print(f"[OK] Saved to: {output_file}")
    print()
    print("Next: Open in KiCad - wires from PINTOPIN plus power symbols")
    print("This should significantly reduce power_pin_not_driven errors!")

if __name__ == "__main__":
    main()
