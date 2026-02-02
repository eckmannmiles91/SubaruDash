#!/usr/bin/env python3
"""
Intelligent auto-wiring script for KiCad schematic
Uses unique Y-coordinate routing channels for each net to prevent short circuits
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

# Detailed pin-to-net mapping from SCHEMATIC_DESIGN.md
# Format: {component_ref: {pin_number: net_name}}
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

def parse_symbol_pins(content):
    """Parse symbol definitions to extract pin positions"""
    symbol_pins = {}

    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('(symbol "'):
            match = re.search(r'\(symbol "([^"]+)"', line)
            if match:
                symbol_name = match.group(1)
                depth = 1
                symbol_lines = [line]
                i += 1
                while i < len(lines) and depth > 0:
                    current = lines[i]
                    symbol_lines.append(current)
                    depth += current.count('(') - current.count(')')
                    i += 1

                symbol_body = '\n'.join(symbol_lines)

                # Extract pins
                pin_pattern = r'\(pin [^\n]+\n\s+\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\).*?\(number "([^"]+)"'
                pins = {}

                for pin_match in re.finditer(pin_pattern, symbol_body, re.DOTALL):
                    x = float(pin_match.group(1))
                    y = float(pin_match.group(2))
                    rotation = float(pin_match.group(3))
                    pin_num = pin_match.group(4)
                    pins[pin_num] = (x, y, rotation)

                if pins:
                    symbol_pins[symbol_name] = pins
                continue
        i += 1

    return symbol_pins

def parse_component_instances(content):
    """Parse component instances to get their positions and symbol types"""
    instances = {}

    pattern = r'\(symbol\s+\(lib_id "([^"]+)"\)\s+\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\).*?\(uuid [^)]+\).*?\(property "Reference" "([^"]+)"'

    for match in re.finditer(pattern, content, re.DOTALL):
        lib_id = match.group(1)
        x = float(match.group(2))
        y = float(match.group(3))
        rotation = float(match.group(4))
        reference = match.group(5)

        instances[reference] = {
            'lib_id': lib_id,
            'x': x,
            'y': y,
            'rotation': rotation
        }

    return instances

def create_wire(x1, y1, x2, y2):
    """Create a wire S-expression"""
    uuid_str = generate_uuid()
    return f"""\t(wire
\t\t(pts
\t\t\t(xy {x1} {y1})
\t\t\t(xy {x2} {y2})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid {uuid_str})
\t)
"""

def rotate_point(x, y, angle_deg):
    """Rotate a point around origin"""
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

def create_junction(x, y):
    """Create a junction dot at wire intersection"""
    uuid_str = generate_uuid()
    return f"""\t(junction (at {x} {y}) (diameter 0) (color 0 0 0 0)
\t\t(uuid {uuid_str})
\t)
"""

def main():
    input_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-WIRED.kicad_sch"
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-INTELLIGENT.kicad_sch"

    print("Intelligent wiring with collision avoidance...")

    # Read schematic
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse symbol definitions and component instances
    print("Parsing symbol definitions...")
    symbol_pins = parse_symbol_pins(content)
    print(f"Found {len(symbol_pins)} symbol types with pin definitions")

    print("Parsing component instances...")
    instances = parse_component_instances(content)
    print(f"Found {len(instances)} component instances")

    # Parse existing global labels to find their positions
    label_positions = {}
    label_pattern = r'\(global_label "([^"]+)"\s+\(shape\s+\w+\)\s+\(at\s+([0-9.-]+)\s+([0-9.-]+)'
    for match in re.finditer(label_pattern, content):
        net_name = match.group(1)
        label_x = float(match.group(2))
        label_y = float(match.group(3))
        if net_name not in label_positions:
            label_positions[net_name] = []
        label_positions[net_name].append((label_x, label_y))

    print(f"Found labels for {len(label_positions)} nets")

    # Group pins by net and calculate routing channels
    # Assign each net a unique Y-offset to prevent wire overlap
    net_to_pins = {}
    for comp_ref, pin_map in PIN_CONNECTIONS.items():
        for pin_num, net_name in pin_map.items():
            if net_name not in net_to_pins:
                net_to_pins[net_name] = []
            net_to_pins[net_name].append((comp_ref, pin_num))

    # Assign routing channels (Y-offsets) to each net
    # Use 2.54mm (0.1 inch) spacing between channels
    channel_spacing = 2.54
    net_channels = {}
    sorted_nets = sorted(net_to_pins.keys())
    for i, net_name in enumerate(sorted_nets):
        net_channels[net_name] = i * channel_spacing

    print(f"Assigned {len(net_channels)} routing channels for collision avoidance")

    # Generate wires with intelligent routing
    wires = "\n"
    junctions = "\n"
    wire_count = 0
    junction_count = 0

    for comp_ref, pin_map in PIN_CONNECTIONS.items():
        if comp_ref not in instances:
            print(f"Warning: {comp_ref} not found in instances")
            continue

        instance = instances[comp_ref]
        lib_id = instance['lib_id']
        comp_x = instance['x']
        comp_y = instance['y']
        comp_rot = instance['rotation']

        if lib_id not in symbol_pins:
            print(f"Warning: No pin definitions for {lib_id}")
            continue

        pins = symbol_pins[lib_id]

        for pin_num, net_name in pin_map.items():
            if pin_num not in pins:
                print(f"Warning: Pin {pin_num} not found in {lib_id}")
                continue

            # Get pin offset from symbol definition
            pin_x_offset, pin_y_offset, pin_rot = pins[pin_num]

            # Rotate pin offset by component rotation
            rotated_x, rotated_y = rotate_point(pin_x_offset, pin_y_offset, comp_rot)

            # Calculate absolute pin position
            pin_x = comp_x + rotated_x
            pin_y = comp_y + rotated_y

            # Find nearest label for this net
            if net_name in label_positions and label_positions[net_name]:
                min_dist = float('inf')
                target_x, target_y = None, None
                for label_x, label_y in label_positions[net_name]:
                    dist = math.sqrt((label_x - pin_x)**2 + (label_y - pin_y)**2)
                    if dist < min_dist:
                        min_dist = dist
                        target_x, target_y = label_x, label_y

                if target_x is not None:
                    # Use unique routing channel for this net
                    channel_y = target_y + net_channels[net_name]

                    # Three-segment routing to avoid overlap:
                    # 1. Pin to channel (vertical)
                    # 2. Along channel to label X (horizontal at unique Y)
                    # 3. Channel to label (vertical)

                    # Segment 1: Pin to channel
                    if abs(pin_y - channel_y) > 0.01:  # Not already at channel
                        wires += create_wire(pin_x, pin_y, pin_x, channel_y)
                        wire_count += 1
                        junctions += create_junction(pin_x, channel_y)
                        junction_count += 1

                    # Segment 2: Along channel to label X position
                    if abs(pin_x - target_x) > 0.01:  # Not already aligned
                        wires += create_wire(pin_x, channel_y, target_x, channel_y)
                        wire_count += 1
                        if abs(channel_y - target_y) > 0.01:  # Will need vertical segment
                            junctions += create_junction(target_x, channel_y)
                            junction_count += 1

                    # Segment 3: Channel to label
                    if abs(channel_y - target_y) > 0.01:  # Not already at label
                        wires += create_wire(target_x, channel_y, target_x, target_y)
                        wire_count += 1

    # Insert wires and junctions before sheet_instances
    additions = wires + junctions
    marker = "\t(sheet_instances"
    insertion_point = content.find(marker)
    if insertion_point == -1:
        insertion_point = content.rfind(')')

    new_content = content[:insertion_point] + additions + content[insertion_point:]

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Added {wire_count} wires with intelligent routing")
    print(f"[OK] Added {junction_count} junction dots")
    print(f"[OK] Each net uses unique routing channel to prevent shorts")
    print(f"[OK] Saved to: {output_file}")
    print()
    print("Next: Open in KiCad and run ERC to verify no short circuits")

if __name__ == "__main__":
    main()
