#!/usr/bin/env python3
"""
Fix the remaining 11 errors from ERC_4
"""

import re
import uuid

def generate_uuid():
    return str(uuid.uuid4())

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

def delete_power_symbol(content, pwr_ref):
    """Delete a power symbol by reference"""
    # Find and remove the specific power symbol
    pattern = rf'\t\(symbol.*?property "Reference" "{pwr_ref}".*?\n\t\)\n'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content

def main():
    input_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-AUGMENTED.kicad_sch"
    output_file = "C:/Users/eckma/projects/SubaruDash/pcb/wrx-power-can-hat-FIXED.kicad_sch"

    print("Fixing remaining ERC errors...")
    print()

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    additions = "\n"
    fixes = []

    # Fix 1: Delete #PWR05 orphaned power symbol
    print("Fix 1: Deleting orphaned #PWR05...")
    content = delete_power_symbol(content, "#PWR05")
    fixes.append("Deleted #PWR05")

    # Fix 2-4: Add missing labels for disconnected pins
    # These pins had errors but weren't in our ERC report initially
    missing_connections = [
        # (x_mils, y_mils, net_name, description)
        (7350, 5000, "12V_FUSED", "D1 Pin 1"),
        (7350, 22500, "XTAL1", "Y1 Pin 1"),
        (22500, 7650, "+3.3V", "C8 Pin 2"),
        (22350, 12500, "LED3_ANODE", "LED3 Pin 1"),
    ]

    print("\nFix 2-5: Adding missing global labels...")
    for x_mils, y_mils, net_name, desc in missing_connections:
        additions += create_global_label(net_name, x_mils, y_mils)
        fixes.append(f"Added {net_name} label at {desc}")
        print(f"  - {desc}: {net_name}")

    # Insert additions
    marker = "\t(sheet_instances"
    insertion_point = content.find(marker)
    if insertion_point == -1:
        insertion_point = content.rfind(')')

    new_content = content[:insertion_point] + additions + content[insertion_point:]

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n{'='*60}")
    print("FIXES APPLIED")
    print(f"{'='*60}")
    print(f"Output: {output_file}")
    print()
    print("Automated fixes:")
    for i, fix in enumerate(fixes, 1):
        print(f"  {i}. {fix}")

    print("\n" + "="*60)
    print("MANUAL FIXES STILL NEEDED")
    print("="*60)
    print("""
The following errors require manual fixes in KiCad:

1. Pin-to-pin conflicts (Output-to-Output connections):
   - U1 Pin 2 (OUT) connected to U3 Pin 4 (R, Output)
   - U3 Pin 5 (Vref) connected to U2 Pin 2 (VO, Power output)

   These need to be traced in the schematic to see if:
   a) Wrong components were used
   b) Wrong pins were wired together
   c) The component pin types are incorrectly defined

2. Power pins not driven:
   - U3 Pin 3 (VCC) - needs power symbol or connection
   - U3 Pin 2 (GND) - needs GND connection
   - U2 Pin 1 (GND) - needs GND connection

   Solution: Add power symbols (GND, +3.3V) near these pins

After applying these fixes, run ERC again.
Expected result: ~4-6 errors remaining (mostly the pin-to-pin conflicts)
""")

if __name__ == "__main__":
    main()
