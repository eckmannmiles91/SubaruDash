#!/usr/bin/env python3
"""
KiCad Schematic Generator for WRX Power & CAN HAT
Automatically generates component placement for the schematic.

Usage:
    python generate_schematic.py

Output:
    wrx-power-can-hat.kicad_sch (auto-generated schematic)
"""

import uuid
import datetime

# Component definitions from COMPONENT_REFERENCE.md
COMPONENTS = {
    # Section 1: Power Input
    "F1": {"ref": "F1", "value": "5A", "symbol": "Device:Fuse", "x": 50, "y": 50},
    "D1": {"ref": "D1", "value": "SMBJ18A", "symbol": "Device:D_TVS", "x": 75, "y": 50},
    "D2": {"ref": "D2", "value": "SS34", "symbol": "Device:D_Schottky", "x": 100, "y": 50},
    "Q1": {"ref": "Q1", "value": "IRF9540N", "symbol": "Transistor_FET:IRF9540N", "x": 125, "y": 50},
    "R1": {"ref": "R1", "value": "1k", "symbol": "Device:R", "x": 50, "y": 75},
    "R2": {"ref": "R2", "value": "10k", "symbol": "Device:R", "x": 75, "y": 75},
    "R3": {"ref": "R3", "value": "100", "symbol": "Device:R", "x": 100, "y": 75},
    "C1": {"ref": "C1", "value": "100uF", "symbol": "Device:CP", "x": 125, "y": 75},
    "LED1": {"ref": "LED1", "value": "Green", "symbol": "Device:LED", "x": 150, "y": 75},
    "J1": {"ref": "J1", "value": "ISO_A", "symbol": "Connector_Generic:Conn_01x08", "x": 25, "y": 50},

    # Section 2: Buck Converter
    "U1": {"ref": "U1", "value": "LM2596S-5.0", "symbol": "Regulator_Switching:LM2596S-5", "x": 50, "y": 125},
    "L1": {"ref": "L1", "value": "33uH", "symbol": "Device:L", "x": 75, "y": 125},
    "D3": {"ref": "D3", "value": "SS54", "symbol": "Device:D_Schottky", "x": 100, "y": 125},
    "C2": {"ref": "C2", "value": "100uF", "symbol": "Device:CP", "x": 50, "y": 150},
    "C3": {"ref": "C3", "value": "220uF", "symbol": "Device:CP", "x": 75, "y": 150},
    "R4": {"ref": "R4", "value": "1.5k", "symbol": "Device:R", "x": 100, "y": 150},
    "R5": {"ref": "R5", "value": "1k", "symbol": "Device:R", "x": 125, "y": 150},

    # Section 3: Ignition Detection
    "U2": {"ref": "U2", "value": "LTV-817S", "symbol": "Isolator:LTV-817S", "x": 175, "y": 50},
    "R6": {"ref": "R6", "value": "1k", "symbol": "Device:R", "x": 175, "y": 75},
    "R7": {"ref": "R7", "value": "10k", "symbol": "Device:R", "x": 200, "y": 75},
    "C4": {"ref": "C4", "value": "100nF", "symbol": "Device:C", "x": 225, "y": 75},
    "C5": {"ref": "C5", "value": "10uF", "symbol": "Device:C", "x": 250, "y": 75},

    # Section 4: Timer (ATtiny85)
    "U3": {"ref": "U3", "value": "ATtiny85", "symbol": "MCU_Microchip_ATtiny:ATtiny85-20PU", "x": 175, "y": 125},
    "C6": {"ref": "C6", "value": "100nF", "symbol": "Device:C", "x": 175, "y": 150},
    "R8": {"ref": "R8", "value": "10k", "symbol": "Device:R", "x": 200, "y": 150},
    "R9": {"ref": "R9", "value": "470", "symbol": "Device:R", "x": 225, "y": 150},
    "R14": {"ref": "R14", "value": "470", "symbol": "Device:R", "x": 250, "y": 150},
    "LED2": {"ref": "LED2", "value": "Red", "symbol": "Device:LED", "x": 200, "y": 125},
    "LED3": {"ref": "LED3", "value": "Yellow", "symbol": "Device:LED", "x": 225, "y": 125},
    "J3": {"ref": "J3", "value": "ISP", "symbol": "Connector_Generic:Conn_02x03_Odd_Even", "x": 250, "y": 125},

    # Section 5: Gate Driver
    "Q2": {"ref": "Q2", "value": "2N7002", "symbol": "Transistor_FET:2N7002", "x": 150, "y": 50},
    "R10": {"ref": "R10", "value": "470", "symbol": "Device:R", "x": 150, "y": 75},
    "R11": {"ref": "R11", "value": "10k", "symbol": "Device:R", "x": 175, "y": 50},

    # Section 6: CAN Interface
    "U4": {"ref": "U4", "value": "MCP2515", "symbol": "Interface_CAN_LIN:MCP2515-I_SO", "x": 50, "y": 200},
    "U5": {"ref": "U5", "value": "SN65HVD230", "symbol": "Interface_CAN_LIN:SN65HVD230", "x": 100, "y": 200},
    "Y1": {"ref": "Y1", "value": "8MHz", "symbol": "Device:Crystal", "x": 75, "y": 225},
    "C7": {"ref": "C7", "value": "100nF", "symbol": "Device:C", "x": 50, "y": 225},
    "C8": {"ref": "C8", "value": "100nF", "symbol": "Device:C", "x": 100, "y": 225},
    "C9": {"ref": "C9", "value": "22pF", "symbol": "Device:C", "x": 125, "y": 225},
    "C10": {"ref": "C10", "value": "22pF", "symbol": "Device:C", "x": 150, "y": 225},
    "R12": {"ref": "R12", "value": "10k", "symbol": "Device:R", "x": 125, "y": 200},
    "R13": {"ref": "R13", "value": "120", "symbol": "Device:R", "x": 150, "y": 200},
    "J4": {"ref": "J4", "value": "OBD-II", "symbol": "Connector_Generic:Conn_01x16", "x": 175, "y": 200},
    "J5": {"ref": "J5", "value": "CAN_Term", "symbol": "Connector:Screw_Terminal_01x02", "x": 175, "y": 225},
    "JP1": {"ref": "JP1", "value": "Jumper", "symbol": "Connector_Generic:Conn_01x02", "x": 200, "y": 225},

    # Section 7: Fan Control
    "Q3": {"ref": "Q3", "value": "2N7002", "symbol": "Transistor_FET:2N7002", "x": 225, "y": 200},
    "D7": {"ref": "D7", "value": "1N4148", "symbol": "Device:D", "x": 250, "y": 200},
    "R15": {"ref": "R15", "value": "1k", "symbol": "Device:R", "x": 225, "y": 225},
    "J6": {"ref": "J6", "value": "FAN", "symbol": "Connector_Generic:Conn_01x02", "x": 250, "y": 225},
    "JP2": {"ref": "JP2", "value": "5V/12V", "symbol": "Connector_Generic:Conn_01x03", "x": 275, "y": 225},

    # Section 9: 3.3V Regulator
    "U6": {"ref": "U6", "value": "AMS1117-3.3", "symbol": "Regulator_Linear:AMS1117-3.3", "x": 50, "y": 275},
    "C11": {"ref": "C11", "value": "10uF", "symbol": "Device:C", "x": 75, "y": 275},
    "C12": {"ref": "C12", "value": "10uF", "symbol": "Device:C", "x": 100, "y": 275},

    # Section 10: GPIO Header
    "J2": {"ref": "J2", "value": "Pi_GPIO", "symbol": "Connector_Generic:Conn_02x20_Odd_Even", "x": 150, "y": 275},

    # Section 11: Audio DAC
    "U7": {"ref": "U7", "value": "PCM5142", "symbol": "Connector_Generic:Conn_01x16", "x": 225, "y": 275},  # Placeholder symbol
    "C13": {"ref": "C13", "value": "1uF", "symbol": "Device:C", "x": 250, "y": 275},
    "C14": {"ref": "C14", "value": "1uF", "symbol": "Device:C", "x": 275, "y": 275},
    "C15": {"ref": "C15", "value": "2.2uF", "symbol": "Device:C", "x": 225, "y": 300},
    "C16": {"ref": "C16", "value": "2.2uF", "symbol": "Device:C", "x": 250, "y": 300},
    "C17": {"ref": "C17", "value": "2.2uF", "symbol": "Device:C", "x": 275, "y": 300},
    "C18": {"ref": "C18", "value": "2.2uF", "symbol": "Device:C", "x": 300, "y": 300},
    "R16": {"ref": "R16", "value": "1k", "symbol": "Device:R", "x": 225, "y": 325},
    "R17": {"ref": "R17", "value": "1k", "symbol": "Device:R", "x": 250, "y": 325},
    "R18": {"ref": "R18", "value": "1k", "symbol": "Device:R", "x": 275, "y": 325},
    "R19": {"ref": "R19", "value": "1k", "symbol": "Device:R", "x": 300, "y": 325},
    "J7": {"ref": "J7", "value": "Audio", "symbol": "Connector_Generic:Conn_01x06", "x": 325, "y": 300},
}

# Power symbols
POWER_SYMBOLS = [
    {"type": "GND", "x": 25, "y": 100},
    {"type": "GND", "x": 150, "y": 100},
    {"type": "GND", "x": 275, "y": 100},
    {"type": "+12V", "x": 25, "y": 25},
    {"type": "+12V", "x": 150, "y": 25},
    {"type": "+5V", "x": 150, "y": 175},
    {"type": "+3.3V", "x": 25, "y": 250},
]

def generate_uuid():
    """Generate a UUID for KiCad components."""
    return str(uuid.uuid4())

def mm_to_kicad(mm):
    """Convert millimeters to KiCad units (0.001mm)."""
    return mm * 2.54  # KiCad uses 2.54mm grid by default

def create_symbol_instance(comp_data):
    """Generate S-expression for a symbol instance."""
    uuid_str = generate_uuid()
    x = mm_to_kicad(comp_data["x"])
    y = mm_to_kicad(comp_data["y"])

    return f"""  (symbol (lib_id "{comp_data['symbol']}") (at {x} {y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid {uuid_str})
    (property "Reference" "{comp_data['ref']}" (at {x} {y-5} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "{comp_data['value']}" (at {x} {y+5} 0)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" "" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )
"""

def create_power_symbol(power_data):
    """Generate S-expression for a power symbol."""
    uuid_str = generate_uuid()
    x = mm_to_kicad(power_data["x"])
    y = mm_to_kicad(power_data["y"])
    pwr_type = power_data["type"]

    return f"""  (symbol (lib_id "power:{pwr_type}") (at {x} {y} 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no)
    (uuid {uuid_str})
    (property "Reference" "#PWR?" (at {x} {y-5} 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Value" "{pwr_type}" (at {x} {y+3} 0)
      (effects (font (size 1.27 1.27)))
    )
  )
"""

def generate_schematic():
    """Generate complete KiCad schematic file."""

    timestamp = datetime.datetime.now().isoformat()

    header = f"""(kicad_sch (version 20230121) (generator generate_schematic.py)

  (uuid {generate_uuid()})

  (paper "A3")

  (title_block
    (title "WRX Power & CAN HAT")
    (date "{timestamp}")
    (rev "1.0")
    (company "Auto-generated by Python")
  )

"""

    # Generate all component instances
    components_section = ""
    for comp in COMPONENTS.values():
        components_section += create_symbol_instance(comp)

    # Generate power symbols
    power_section = ""
    for pwr in POWER_SYMBOLS:
        power_section += create_power_symbol(pwr)

    footer = """)
"""

    return header + components_section + power_section + footer

def main():
    """Main function to generate schematic."""
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-AUTO.kicad_sch"

    print("Generating KiCad schematic...")
    print(f"Output file: {output_file}")

    schematic_content = generate_schematic()

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(schematic_content)

    print(f"[OK] Generated {len(COMPONENTS)} components")
    print(f"[OK] Generated {len(POWER_SYMBOLS)} power symbols")
    print(f"[OK] Schematic saved to: {output_file}")
    print()
    print("Next steps:")
    print("1. Open KiCad")
    print("2. File > Open > wrx-power-can-hat-AUTO.kicad_sch")
    print("3. Components are pre-placed in logical groups")
    print("4. Wire them together using net labels (press 'L')")
    print("5. Assign footprints (Tools > Assign Footprints)")
    print()
    print("NOTE: Some symbols may need manual adjustment:")
    print("- PCM5142 uses placeholder (needs proper symbol)")
    print("- OBD-II connector uses generic 16-pin")
    print("- ISO connector uses generic 8-pin")

if __name__ == "__main__":
    main()
