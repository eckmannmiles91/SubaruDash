#!/usr/bin/env python3
"""
Fix Power HAT: Upgrade J4 from 2-pin to 4-pin PWM fan connector

Standard 4-pin PWM fan pinout:
- Pin 1: GND
- Pin 2: +12V (power)
- Pin 3: TACH (speed feedback)
- Pin 4: PWM (speed control)
"""

import re
import shutil
from pathlib import Path

def main():
    schematic_path = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\boards\power-hat\power-hat.kicad_sch")

    # Create backup
    backup_path = schematic_path.parent / "power-hat-BACKUP-fan.kicad_sch"
    shutil.copy(schematic_path, backup_path)
    print(f"Backup created: {backup_path.name}")

    content = schematic_path.read_text(encoding='utf-8')

    # 1. Update the footprint from 1x02 to 1x04
    old_footprint = 'PinHeader_1x02_P2.54mm_Vertical'
    new_footprint = 'PinHeader_1x04_P2.54mm_Vertical'

    # Find and update J4's footprint property
    content = re.sub(
        r'(\(property "Reference" "J4".*?property "Footprint" "Connector_PinHeader_2\.54mm:)PinHeader_1x02_P2\.54mm_Vertical',
        r'\g<1>PinHeader_1x04_P2.54mm_Vertical',
        content,
        flags=re.DOTALL
    )
    print(f"Updated footprint: {old_footprint} -> {new_footprint}")

    # 2. Update the lib_id from Conn_01x02 to Conn_01x04
    # First find the J4 symbol block
    j4_pattern = r'(\(symbol\s*\n\s*\(lib_id ")Connector_Generic:Conn_01x02(".*?"Reference" "J4")'
    if re.search(j4_pattern, content, re.DOTALL):
        content = re.sub(j4_pattern, r'\1Connector_Generic:Conn_01x04\2', content, flags=re.DOTALL)
        print("Updated lib_id: Conn_01x02 -> Conn_01x04")

    # 3. Update the Value property
    content = re.sub(
        r'(\(property "Reference" "J4".*?\(property "Value" )"FAN"',
        r'\1"FAN_4PIN"',
        content,
        flags=re.DOTALL
    )
    print("Updated value: FAN -> FAN_4PIN")

    # 4. Make sure the Conn_01x04 symbol is in lib_symbols if not present
    # Check if Conn_01x04 exists
    if 'symbol "Connector_Generic:Conn_01x04"' not in content:
        # Find the Conn_01x02 symbol definition and duplicate it for 01x04
        conn_02_pattern = r'(\(symbol "Connector_Generic:Conn_01x02".*?\n\s*\(symbol "Conn_01x02_1_1".*?\n\s*\)\n\s*\(embedded_fonts no\)\n\s*\))'

        conn_02_match = re.search(conn_02_pattern, content, re.DOTALL)
        if conn_02_match:
            # Create a 4-pin version
            conn_04_symbol = '''(symbol "Connector_Generic:Conn_01x04"
			(pin_names
				(offset 1.016)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "J"
				(at 0 5.08 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "Conn_01x04"
				(at 0 -7.62 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Generic connector, single row, 01x04"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "ki_keywords" "connector"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "ki_fp_filters" "Connector*:*_1x??_*"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "Conn_01x04_1_1"
				(rectangle
					(start -1.27 3.81)
					(end 1.27 -6.35)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(pin passive line
					(at -5.08 2.54 0)
					(length 3.81)
					(name "Pin_1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at -5.08 0 0)
					(length 3.81)
					(name "Pin_2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at -5.08 -2.54 0)
					(length 3.81)
					(name "Pin_3"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "3"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at -5.08 -5.08 0)
					(length 3.81)
					(name "Pin_4"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "4"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)
'''
            # Insert after the Conn_01x02 symbol
            insert_pos = conn_02_match.end()
            content = content[:insert_pos] + '\n\t\t' + conn_04_symbol + content[insert_pos:]
            print("Added Conn_01x04 symbol to lib_symbols")

    # Write updated schematic
    schematic_path.write_text(content, encoding='utf-8')
    print(f"\nUpdated schematic: {schematic_path}")
    print("\nNote: You'll need to manually add wires for pins 3 (TACH) and 4 (PWM) in KiCad")
    print("Pin 1: GND, Pin 2: +12V/FAN+, Pin 3: FAN_TACH, Pin 4: FAN_PWM")

if __name__ == "__main__":
    main()
