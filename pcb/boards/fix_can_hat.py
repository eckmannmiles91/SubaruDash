#!/usr/bin/env python3
"""
CAN HAT Fix Script - Complete wiring and USB-C power input.

This script:
1. Adds USB-C power input circuit with diode OR'ing for bench testing
2. Connects GPIO header pins (SPI, interrupt, power)
3. Wires MCP2515 CAN controller
4. Wires SN65HVD230 CAN transceiver
5. Adds power distribution and PWR_FLAG symbols
"""

import uuid
import re
from pathlib import Path


# =============================================================================
# Component Positions (from schematic exploration)
# =============================================================================
J1_POS = (200, 150)          # GPIO 40-pin header (Conn_02x20_Odd_Even)
U2_POS = (444.5, 127)        # MCP2515 CAN controller
U3_POS = (571.5, 698.5)      # SN65HVD230 CAN transceiver
U1_POS = (381, 433.07)       # AMS1117-3.3 voltage regulator
J2_POS = (444.5, 508)        # OBD-II 16-pin connector
J3_POS = (444.5, 571.5)      # CAN screw terminal
Y1_POS = (190.5, 571.5)      # Crystal (8MHz)

# Schematic UUID (from file header)
SCHEMATIC_UUID = "7bb601d0-af23-47b8-978e-986fbee2569f"

# USB-C circuit positions (new components)
J5_POS = (80, 430)           # USB-C connector
D1_POS = (130, 415)          # Schottky diode from USB
D2_POS = (130, 450)          # Schottky diode from GPIO
C12_POS = (95, 460)          # USB input capacitor
F2_POS = (105, 415)          # Polyfuse


# =============================================================================
# Helper Functions
# =============================================================================
def generate_uuid():
    """Generate a KiCad-style UUID."""
    return str(uuid.uuid4())


def create_wire(x1, y1, x2, y2):
    """Create a KiCad wire S-expression."""
    uid = generate_uuid()
    return f'''\t(wire
\t\t(pts
\t\t\t(xy {x1} {y1}) (xy {x2} {y2})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{uid}")
\t)'''


def create_label(name, x, y, direction=0):
    """Create a KiCad local label S-expression."""
    uid = generate_uuid()
    justify = "right" if direction == 180 else "left"
    return f'''\t(label "{name}"
\t\t(at {x} {y} {direction})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {justify} bottom)
\t\t)
\t\t(uuid "{uid}")
\t)'''


def create_global_label(name, x, y, direction=0, shape="passive"):
    """Create a KiCad global label S-expression."""
    uid = generate_uuid()
    justify = "right" if direction == 180 else "left"
    return f'''\t(global_label "{name}"
\t\t(shape {shape})
\t\t(at {x} {y} {direction})
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify {justify})
\t\t)
\t\t(uuid "{uid}")
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t)'''


def create_no_connect(x, y):
    """Create a KiCad no_connect S-expression."""
    uid = generate_uuid()
    return f'''\t(no_connect
\t\t(at {x} {y})
\t\t(uuid "{uid}")
\t)'''


def create_pwr_flag(x, y, ref_num):
    """Create a PWR_FLAG symbol to mark power source."""
    uid = generate_uuid()
    pin_uid = generate_uuid()
    return f'''\t(symbol
\t\t(lib_id "power:PWR_FLAG")
\t\t(at {x} {y} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom no)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid}")
\t\t(property "Reference" "#FLG{ref_num:02d}"
\t\t\t(at {x} {y - 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Value" "PWR_FLAG"
\t\t\t(at {x} {y + 2.54} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(property "Description" "Special symbol for telling ERC where power comes from"
\t\t\t(at {x} {y} 0)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(hide yes)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{pin_uid}")
\t\t)
\t\t(instances
\t\t\t(project "can-hat"
\t\t\t\t(path "/{SCHEMATIC_UUID}"
\t\t\t\t\t(reference "#FLG{ref_num:02d}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)'''


def get_gpio_pin_position(pin_number):
    """
    Calculate position for a Conn_02x20_Odd_Even connector pin.
    J1 is at (200, 150).
    Odd pins on left, even pins on right.
    Pin spacing: 2.54mm
    """
    j1_x, j1_y = J1_POS
    if pin_number % 2 == 1:  # Odd pins on left
        row = (pin_number - 1) // 2
        x = j1_x - 2.54
    else:  # Even pins on right
        row = (pin_number - 2) // 2
        x = j1_x + 2.54
    y = j1_y + row * 2.54
    return (round(x, 2), round(y, 2))


def read_schematic(filepath):
    """Read the schematic file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_schematic(filepath, content):
    """Write the schematic file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {filepath}")


def find_insert_position(content):
    """Find position to insert new elements (before sheet_instances)."""
    match = re.search(r'\n\t\(sheet_instances', content)
    if match:
        return match.start()
    return len(content) - 2


# =============================================================================
# Main Fix Function
# =============================================================================
def fix_can_hat():
    """Main function to fix CAN HAT schematic."""
    script_dir = Path(__file__).parent
    can_hat_sch = script_dir / "can-hat" / "can-hat.kicad_sch"

    if not can_hat_sch.exists():
        print(f"Error: {can_hat_sch} not found")
        return

    print("=" * 70)
    print("CAN HAT Fix Script - Complete Wiring + USB-C Power Input")
    print("=" * 70)

    # Read schematic
    content = read_schematic(can_hat_sch)
    print(f"Read {len(content)} bytes from {can_hat_sch.name}")

    new_elements = []
    pwr_flag_num = 1

    # =========================================================================
    # SECTION 1: GPIO Header (J1) Connections
    # =========================================================================
    print("\n--- Section 1: GPIO Header Connections ---")

    # Power pins
    power_pins = {
        1: ("+3.3V", "passive"),   # 3.3V power
        2: ("+5V", "passive"),     # 5V power
        4: ("+5V", "passive"),     # 5V power
        17: ("+3.3V", "passive"),  # 3.3V power
    }

    # Ground pins
    gnd_pins = [6, 9, 14, 20, 25, 30, 34, 39]

    # SPI pins (directly connected via global labels)
    spi_pins = {
        19: ("SPI_MOSI", "output"),   # GPIO10 - MOSI
        21: ("SPI_MISO", "input"),    # GPIO9 - MISO
        23: ("SPI_SCLK", "output"),   # GPIO11 - SCLK
        24: ("SPI_CE0", "output"),    # GPIO8 - Chip Select
        22: ("CAN_INT", "input"),     # GPIO25 - Interrupt
    }

    # Connect power pins
    for pin, (net_name, shape) in power_pins.items():
        x, y = get_gpio_pin_position(pin)
        # Wire extends 5mm from pin
        if pin % 2 == 1:  # Left side - wire goes left
            wire_end_x = x - 5
            direction = 180
        else:  # Right side - wire goes right
            wire_end_x = x + 5
            direction = 0

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label(net_name, wire_end_x, y, direction, shape)
        new_elements.extend([wire, label])
        print(f"  Pin {pin}: {net_name} at ({x}, {y})")

    # Connect ground pins
    for pin in gnd_pins:
        x, y = get_gpio_pin_position(pin)
        if pin % 2 == 1:
            wire_end_x = x - 5
            direction = 180
        else:
            wire_end_x = x + 5
            direction = 0

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label("GND", wire_end_x, y, direction, "passive")
        new_elements.extend([wire, label])
        print(f"  Pin {pin}: GND at ({x}, {y})")

    # Connect SPI/interrupt pins
    for pin, (net_name, shape) in spi_pins.items():
        x, y = get_gpio_pin_position(pin)
        if pin % 2 == 1:
            wire_end_x = x - 5
            direction = 180
        else:
            wire_end_x = x + 5
            direction = 0

        wire = create_wire(x, y, wire_end_x, y)
        label = create_global_label(net_name, wire_end_x, y, direction, shape)
        new_elements.extend([wire, label])
        print(f"  Pin {pin}: {net_name} at ({x}, {y})")

    # Mark unused pins with no_connect
    used_pins = set(power_pins.keys()) | set(gnd_pins) | set(spi_pins.keys())
    unused_pins = [p for p in range(1, 41) if p not in used_pins]

    print(f"\n  Marking {len(unused_pins)} unused pins as no-connect...")
    for pin in unused_pins:
        x, y = get_gpio_pin_position(pin)
        nc = create_no_connect(x, y)
        new_elements.append(nc)

    # =========================================================================
    # SECTION 2: MCP2515 (U2) Connections
    # =========================================================================
    print("\n--- Section 2: MCP2515 CAN Controller Connections ---")

    # MCP2515 pin offsets from component center (444.5, 127)
    # Based on MCP2515-xSO symbol (SOIC-18)
    u2_x, u2_y = U2_POS

    mcp2515_connections = [
        # (pin_name, offset_x, offset_y, net_name, direction, shape)
        ("SI", -15.24, 2.54, "SPI_MOSI", 180, "input"),
        ("SO", -15.24, 0, "SPI_MISO", 180, "output"),
        ("SCK", -15.24, -2.54, "SPI_SCLK", 180, "input"),
        ("~CS", -15.24, -5.08, "SPI_CE0", 180, "input"),
        ("~INT", 15.24, -5.08, "CAN_INT", 0, "output"),
        ("TXCAN", 15.24, 5.08, "CAN_TX", 0, "output"),
        ("RXCAN", 15.24, 2.54, "CAN_RX", 0, "input"),
        ("OSC1", -15.24, -12.7, "XTAL1", 180, "passive"),
        ("OSC2", -15.24, -10.16, "XTAL2", 180, "passive"),
        ("VDD", 0, -17.78, "+3.3V", 270, "passive"),
        ("VSS", 0, 17.78, "GND", 90, "passive"),
    ]

    for pin_name, off_x, off_y, net_name, direction, shape in mcp2515_connections:
        pin_x = u2_x + off_x
        pin_y = u2_y + off_y

        # Wire extension
        if direction == 0:  # Right
            wire_end_x = pin_x + 5
            wire_end_y = pin_y
        elif direction == 180:  # Left
            wire_end_x = pin_x - 5
            wire_end_y = pin_y
        elif direction == 90:  # Down
            wire_end_x = pin_x
            wire_end_y = pin_y + 5
        else:  # Up (270)
            wire_end_x = pin_x
            wire_end_y = pin_y - 5

        wire = create_wire(pin_x, pin_y, wire_end_x, wire_end_y)
        label = create_global_label(net_name, wire_end_x, wire_end_y, direction, shape)
        new_elements.extend([wire, label])
        print(f"  U2.{pin_name}: {net_name}")

    # =========================================================================
    # SECTION 3: SN65HVD230 (U3) Connections
    # =========================================================================
    print("\n--- Section 3: SN65HVD230 CAN Transceiver Connections ---")

    u3_x, u3_y = U3_POS

    # SN65HVD230 pin offsets (SOIC-8)
    sn65_connections = [
        # (pin_name, offset_x, offset_y, net_name, direction, shape)
        ("D", -7.62, 2.54, "CAN_TX", 180, "input"),
        ("R", -7.62, -2.54, "CAN_RX", 180, "output"),
        ("CANH", 7.62, 2.54, "CANH", 0, "bidirectional"),
        ("CANL", 7.62, -2.54, "CANL", 0, "bidirectional"),
        ("VCC", 0, -7.62, "+3.3V", 270, "passive"),
        ("GND", 0, 7.62, "GND", 90, "passive"),
    ]

    for pin_name, off_x, off_y, net_name, direction, shape in sn65_connections:
        pin_x = u3_x + off_x
        pin_y = u3_y + off_y

        if direction == 0:
            wire_end_x = pin_x + 5
            wire_end_y = pin_y
        elif direction == 180:
            wire_end_x = pin_x - 5
            wire_end_y = pin_y
        elif direction == 90:
            wire_end_x = pin_x
            wire_end_y = pin_y + 5
        else:
            wire_end_x = pin_x
            wire_end_y = pin_y - 5

        wire = create_wire(pin_x, pin_y, wire_end_x, wire_end_y)
        label = create_global_label(net_name, wire_end_x, wire_end_y, direction, shape)
        new_elements.extend([wire, label])
        print(f"  U3.{pin_name}: {net_name}")

    # =========================================================================
    # SECTION 4: CAN Bus Connectors (J2 OBD-II, J3 Terminal)
    # =========================================================================
    print("\n--- Section 4: CAN Bus Connector Connections ---")

    # J2 OBD-II (Conn_01x16) - pins are vertically stacked at 2.54mm spacing
    # Pin 1 at top, Pin 16 at bottom
    j2_x, j2_y = J2_POS

    # Connect Pin 6 (CANH) and Pin 14 (CANL)
    # Pins are on left side of connector, going down from top
    j2_pin6_y = j2_y + (6 - 1) * 2.54  # Pin 6
    j2_pin14_y = j2_y + (14 - 1) * 2.54  # Pin 14
    j2_pin4_y = j2_y + (4 - 1) * 2.54   # Pin 4 (GND)

    # CANH to J2 Pin 6
    wire = create_wire(j2_x - 2.54, j2_pin6_y, j2_x - 7.62, j2_pin6_y)
    label = create_global_label("CANH", j2_x - 7.62, j2_pin6_y, 180, "bidirectional")
    new_elements.extend([wire, label])
    print(f"  J2 Pin 6: CANH")

    # CANL to J2 Pin 14
    wire = create_wire(j2_x - 2.54, j2_pin14_y, j2_x - 7.62, j2_pin14_y)
    label = create_global_label("CANL", j2_x - 7.62, j2_pin14_y, 180, "bidirectional")
    new_elements.extend([wire, label])
    print(f"  J2 Pin 14: CANL")

    # GND to J2 Pin 4 (optional chassis ground)
    wire = create_wire(j2_x - 2.54, j2_pin4_y, j2_x - 7.62, j2_pin4_y)
    label = create_global_label("GND", j2_x - 7.62, j2_pin4_y, 180, "passive")
    new_elements.extend([wire, label])
    print(f"  J2 Pin 4: GND (chassis)")

    # Mark other J2 pins as no-connect
    used_j2_pins = [4, 6, 14]
    for pin in range(1, 17):
        if pin not in used_j2_pins:
            pin_y = j2_y + (pin - 1) * 2.54
            nc = create_no_connect(j2_x - 2.54, pin_y)
            new_elements.append(nc)
    print(f"  Marked {16 - len(used_j2_pins)} unused J2 pins as no-connect")

    # J3 Screw Terminal (2-pin)
    j3_x, j3_y = J3_POS

    # Pin 1 = CANH, Pin 2 = CANL
    wire = create_wire(j3_x - 2.54, j3_y, j3_x - 7.62, j3_y)
    label = create_global_label("CANH", j3_x - 7.62, j3_y, 180, "bidirectional")
    new_elements.extend([wire, label])
    print(f"  J3 Pin 1: CANH")

    wire = create_wire(j3_x - 2.54, j3_y + 2.54, j3_x - 7.62, j3_y + 2.54)
    label = create_global_label("CANL", j3_x - 7.62, j3_y + 2.54, 180, "bidirectional")
    new_elements.extend([wire, label])
    print(f"  J3 Pin 2: CANL")

    # =========================================================================
    # SECTION 5: Crystal (Y1) Connections
    # =========================================================================
    print("\n--- Section 5: Crystal Connections ---")

    y1_x, y1_y = Y1_POS

    # Crystal has two pins, typically at +/- 2.54mm from center
    # Pin 1 (left) -> XTAL1, Pin 2 (right) -> XTAL2
    y1_pin1_x = y1_x - 2.54
    y1_pin2_x = y1_x + 2.54

    wire = create_wire(y1_pin1_x, y1_y, y1_pin1_x - 5, y1_y)
    label = create_global_label("XTAL1", y1_pin1_x - 5, y1_y, 180, "passive")
    new_elements.extend([wire, label])
    print(f"  Y1 Pin 1: XTAL1")

    wire = create_wire(y1_pin2_x, y1_y, y1_pin2_x + 5, y1_y)
    label = create_global_label("XTAL2", y1_pin2_x + 5, y1_y, 0, "passive")
    new_elements.extend([wire, label])
    print(f"  Y1 Pin 2: XTAL2")

    # =========================================================================
    # SECTION 6: Power Distribution (AMS1117)
    # =========================================================================
    print("\n--- Section 6: Power Distribution ---")

    u1_x, u1_y = U1_POS

    # AMS1117 pins: VI (input), GND, VO (output)
    # Typical offsets for SOT-223
    # VI on left, VO on right, GND at bottom

    # VI (input) - connect to 5V_BUS
    wire = create_wire(u1_x - 5.08, u1_y, u1_x - 10.16, u1_y)
    label = create_global_label("5V_BUS", u1_x - 10.16, u1_y, 180, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.VI: 5V_BUS (from diode OR)")

    # VO (output) - connect to +3.3V
    wire = create_wire(u1_x + 5.08, u1_y, u1_x + 10.16, u1_y)
    label = create_global_label("+3.3V", u1_x + 10.16, u1_y, 0, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.VO: +3.3V")

    # GND
    wire = create_wire(u1_x, u1_y + 5.08, u1_x, u1_y + 10.16)
    label = create_global_label("GND", u1_x, u1_y + 10.16, 90, "passive")
    new_elements.extend([wire, label])
    print(f"  U1.GND: GND")

    # =========================================================================
    # SECTION 7: PWR_FLAG Symbols
    # =========================================================================
    print("\n--- Section 7: PWR_FLAG Symbols ---")

    # Add PWR_FLAG for +5V (at GPIO header area)
    pwr_5v_x, pwr_5v_y = get_gpio_pin_position(2)
    pwr_flag = create_pwr_flag(pwr_5v_x + 10, pwr_5v_y - 5, pwr_flag_num)
    wire = create_wire(pwr_5v_x + 10, pwr_5v_y - 5, pwr_5v_x + 10, pwr_5v_y)
    label = create_global_label("+5V", pwr_5v_x + 10, pwr_5v_y, 0, "passive")
    new_elements.extend([pwr_flag, wire, label])
    print(f"  PWR_FLAG #{pwr_flag_num}: +5V")
    pwr_flag_num += 1

    # Add PWR_FLAG for +3.3V (at U1 output)
    pwr_flag = create_pwr_flag(u1_x + 15, u1_y - 5, pwr_flag_num)
    wire = create_wire(u1_x + 15, u1_y - 5, u1_x + 15, u1_y)
    label = create_global_label("+3.3V", u1_x + 15, u1_y, 0, "passive")
    new_elements.extend([pwr_flag, wire, label])
    print(f"  PWR_FLAG #{pwr_flag_num}: +3.3V")
    pwr_flag_num += 1

    # Add PWR_FLAG for GND
    pwr_flag = create_pwr_flag(u1_x + 5, u1_y + 15, pwr_flag_num)
    wire = create_wire(u1_x + 5, u1_y + 15, u1_x, u1_y + 10.16)
    label = create_global_label("GND", u1_x + 5, u1_y + 15, 90, "passive")
    new_elements.extend([pwr_flag, wire, label])
    print(f"  PWR_FLAG #{pwr_flag_num}: GND")
    pwr_flag_num += 1

    # =========================================================================
    # SECTION 8: USB-C Power Circuit (New Components)
    # =========================================================================
    print("\n--- Section 8: USB-C Power Circuit ---")
    print("  NOTE: USB-C components need to be added manually in KiCad")
    print("  The script adds net labels for the power OR'ing circuit:")

    # Add labels for USB-C power circuit connection points
    # These will connect to manually placed USB-C, diodes, etc.

    # USB_VBUS net (from USB-C)
    wire = create_wire(J5_POS[0] + 10, J5_POS[1], J5_POS[0] + 15, J5_POS[1])
    label = create_global_label("USB_VBUS", J5_POS[0] + 15, J5_POS[1], 0, "passive")
    new_elements.extend([wire, label])
    print(f"  USB_VBUS label at ({J5_POS[0] + 15}, {J5_POS[1]})")

    # 5V_BUS net (output of diode OR)
    wire = create_wire(D1_POS[0] + 15, D1_POS[1] + 17.5, D1_POS[0] + 20, D1_POS[1] + 17.5)
    label = create_global_label("5V_BUS", D1_POS[0] + 20, D1_POS[1] + 17.5, 0, "passive")
    new_elements.extend([wire, label])
    print(f"  5V_BUS label at ({D1_POS[0] + 20}, {D1_POS[1] + 17.5})")

    # Connect GPIO +5V to 5V_BUS (through D2)
    # This label will connect to the diode circuit
    gpio_5v_x, gpio_5v_y = get_gpio_pin_position(2)
    wire = create_wire(gpio_5v_x + 5, gpio_5v_y, gpio_5v_x + 10, gpio_5v_y)
    label = create_global_label("GPIO_5V", gpio_5v_x + 10, gpio_5v_y, 0, "passive")
    new_elements.extend([wire, label])
    print(f"  GPIO_5V label (for D2 input)")

    print("\n  Manual steps needed:")
    print("  1. Add USB-C connector (J5) at ~(80, 430)")
    print("  2. Add SS34 diodes D1, D2 at ~(130, 415) and (130, 450)")
    print("  3. Add 10uF capacitor C12 near USB-C")
    print("  4. Add 500mA polyfuse F2 between USB-C and D1")
    print("  5. Connect: USB_VBUS -> F2 -> D1 anode")
    print("  6. Connect: GPIO_5V -> D2 anode")
    print("  7. Connect: D1 cathode + D2 cathode -> 5V_BUS")

    # =========================================================================
    # Insert all elements into schematic
    # =========================================================================
    print("\n" + "=" * 70)
    print("Inserting connections into schematic...")

    insert_pos = find_insert_position(content)
    new_content = '\n'.join(new_elements)
    content = content[:insert_pos] + '\n' + new_content + '\n' + content[insert_pos:]

    # Write updated schematic
    write_schematic(can_hat_sch, content)

    print("\n" + "=" * 70)
    print("DONE!")
    print("=" * 70)
    print(f"\nAdded {len(new_elements)} new schematic elements")
    print("\nNext steps:")
    print("1. Open can-hat/can-hat.kicad_sch in KiCad")
    print("2. Run ERC (Tools -> Electrical Rules Checker)")
    print("3. Manually add USB-C power circuit components")
    print("4. Fix any remaining ERC errors")
    print("5. Verify connections visually")


if __name__ == "__main__":
    fix_can_hat()
