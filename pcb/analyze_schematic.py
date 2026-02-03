#!/usr/bin/env python3
"""
Comprehensive KiCad Schematic Analyzer
Analyzes wrx-power-can-hat-MANUAL.kicad_sch and creates component inventory
"""

import re
import json
from pathlib import Path
from collections import defaultdict

def parse_kicad_schematic(filepath):
    """Parse KiCad schematic and extract all components"""

    components = []
    labels = []
    global_labels = []
    wires = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract all symbol instances (components)
    symbol_pattern = r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+\(at\s+([\d.]+)\s+([\d.]+)'
    for match in re.finditer(symbol_pattern, content):
        lib_id = match.group(1)
        x = match.group(2)
        y = match.group(3)

        # Find the reference and value for this symbol
        start_pos = match.start()
        # Search forward from symbol start to find reference
        ref_match = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', content[start_pos:start_pos+2000])
        val_match = re.search(r'\(property\s+"Value"\s+"([^"]+)"', content[start_pos:start_pos+2000])

        reference = ref_match.group(1) if ref_match else "?"
        value = val_match.group(1) if val_match else "?"

        components.append({
            'reference': reference,
            'value': value,
            'lib_id': lib_id,
            'position': (float(x), float(y))
        })

    # Extract local labels
    label_pattern = r'\(label\s+"([^"]+)"\s+\(at\s+([\d.]+)\s+([\d.]+)'
    for match in re.finditer(label_pattern, content):
        labels.append({
            'name': match.group(1),
            'position': (float(match.group(2)), float(match.group(3)))
        })

    # Extract global labels
    global_label_pattern = r'\(global_label\s+"([^"]+)"'
    for match in re.finditer(global_label_pattern, content):
        global_labels.append(match.group(1))

    return {
        'components': components,
        'labels': labels,
        'global_labels': list(set(global_labels))  # Unique global labels
    }

def categorize_components(components):
    """Categorize components by type"""

    categories = defaultdict(list)

    for comp in components:
        ref = comp['reference']

        # Categorize by reference designator prefix
        if ref.startswith('U'):
            categories['ICs'].append(comp)
        elif ref.startswith('Q'):
            categories['Transistors'].append(comp)
        elif ref.startswith('D'):
            categories['Diodes'].append(comp)
        elif ref.startswith('LED'):
            categories['LEDs'].append(comp)
        elif ref.startswith('R'):
            categories['Resistors'].append(comp)
        elif ref.startswith('C'):
            categories['Capacitors'].append(comp)
        elif ref.startswith('L'):
            categories['Inductors'].append(comp)
        elif ref.startswith('F'):
            categories['Fuses'].append(comp)
        elif ref.startswith('J'):
            categories['Connectors'].append(comp)
        elif ref.startswith('JP'):
            categories['Jumpers'].append(comp)
        elif ref.startswith('Y'):
            categories['Crystals'].append(comp)
        else:
            categories['Other'].append(comp)

    return dict(categories)

def check_design_requirements(data):
    """Check against design requirements from SCHEMATIC_DESIGN.md"""

    required_components = {
        'Input Protection': {
            'F1': {'type': 'Fuse', 'value': '5A', 'required': True},
            'D1': {'type': 'Diode', 'value': 'SMBJ18A', 'required': True},
            'D2': {'type': 'Diode', 'value': 'SS34', 'required': True},
            'LED1': {'type': 'LED', 'value': 'Green', 'required': True},
            'R1': {'type': 'Resistor', 'value': '1k', 'required': True},
        },
        'Power Supply': {
            'U1': {'type': 'IC', 'value': 'TPS54560', 'required': True},
            'U6': {'type': 'IC', 'value': 'AMS1117-3.3', 'required': True},
            'L1': {'type': 'Inductor', 'value': '33µH', 'required': True},
        },
        'Power Management': {
            'U3': {'type': 'IC', 'value': 'ATtiny85', 'required': True},
            'Q1': {'type': 'MOSFET', 'value': 'IRLB8721', 'required': True},
            'Q2': {'type': 'MOSFET', 'value': '2N7002', 'required': True},
            'Q3': {'type': 'MOSFET', 'value': '2N7002', 'required': True},
        },
        'CAN Bus Interface': {
            'U4': {'type': 'IC', 'value': 'MCP2515', 'required': True},
            'U5': {'type': 'IC', 'value': 'SN65HVD230', 'required': True},
            'Y1': {'type': 'Crystal', 'value': '16MHz', 'required': True},
            'R8': {'type': 'Resistor', 'value': '120', 'required': True},
        },
        'Ignition Detection': {
            'U2': {'type': 'IC', 'value': 'LTV-817S', 'required': True},
            'R6': {'type': 'Resistor', 'value': '10k', 'required': True},
            'R7': {'type': 'Resistor', 'value': '10k', 'required': True},
        },
        'Connectors': {
            'J1': {'type': 'Connector', 'pins': 8, 'desc': 'ISO-A Power', 'required': True},
            'J2': {'type': 'Connector', 'pins': 40, 'desc': 'Raspberry Pi GPIO', 'required': True},
            'J3': {'type': 'Connector', 'pins': 16, 'desc': 'OBD-II', 'required': True},
        }
    }

    components = data['components']
    comp_dict = {c['reference']: c for c in components}

    results = {}
    missing = []
    found = []
    value_mismatch = []

    for category, items in required_components.items():
        results[category] = {}
        for ref, spec in items.items():
            if ref in comp_dict:
                comp = comp_dict[ref]
                status = 'FOUND'

                # Check value match
                expected_val = spec.get('value', '')
                actual_val = comp['value']

                if expected_val and expected_val.lower() not in actual_val.lower():
                    status = 'VALUE_MISMATCH'
                    value_mismatch.append({
                        'ref': ref,
                        'expected': expected_val,
                        'actual': actual_val
                    })

                results[category][ref] = {
                    'status': status,
                    'value': actual_val,
                    'position': comp['position']
                }
                found.append(ref)
            else:
                results[category][ref] = {
                    'status': 'MISSING',
                    'expected': spec.get('value', '?')
                }
                if spec.get('required', False):
                    missing.append(ref)

    return results, missing, found, value_mismatch

def generate_report(data, design_check):
    """Generate comprehensive analysis report"""

    categories = categorize_components(data['components'])
    results, missing, found, value_mismatch = design_check

    report = []
    report.append("=" * 80)
    report.append("COMPREHENSIVE SCHEMATIC ANALYSIS REPORT")
    report.append("File: wrx-power-can-hat-MANUAL.kicad_sch")
    report.append("=" * 80)
    report.append("")

    # Summary
    report.append("SUMMARY:")
    report.append(f"  Total Components: {len(data['components'])}")
    report.append(f"  Total Labels: {len(data['labels'])}")
    report.append(f"  Global Labels: {len(data['global_labels'])}")
    report.append("")

    # Component breakdown by category
    report.append("COMPONENT INVENTORY BY CATEGORY:")
    report.append("-" * 80)
    for category, items in sorted(categories.items()):
        report.append(f"\n{category} ({len(items)}):")
        for comp in sorted(items, key=lambda x: x['reference']):
            report.append(f"  {comp['reference']:8} = {comp['value']:20} @ ({comp['position'][0]:.1f}, {comp['position'][1]:.1f})")
    report.append("")

    # Design requirements check
    report.append("=" * 80)
    report.append("DESIGN REQUIREMENTS VERIFICATION")
    report.append("=" * 80)
    report.append("")

    for category, items in results.items():
        report.append(f"\n{category}:")
        report.append("-" * 80)
        for ref, info in items.items():
            status = info['status']
            if status == 'FOUND':
                marker = '✓'
            elif status == 'VALUE_MISMATCH':
                marker = '⚠'
            else:
                marker = '✗'

            if status == 'MISSING':
                report.append(f"  {marker} {ref:8} MISSING - Expected: {info.get('expected', '?')}")
            elif status == 'VALUE_MISMATCH':
                # Find expected value from value_mismatch list
                expected = next((item['expected'] for item in value_mismatch if item['ref'] == ref), '?')
                report.append(f"  {marker} {ref:8} VALUE MISMATCH - Expected: {expected}, Got: {info['value']}")
            else:
                report.append(f"  {marker} {ref:8} OK - {info['value']}")

    report.append("")
    report.append("=" * 80)
    report.append("ISSUES SUMMARY")
    report.append("=" * 80)
    report.append("")

    if missing:
        report.append(f"✗ MISSING COMPONENTS ({len(missing)}):")
        for ref in missing:
            report.append(f"  - {ref}")
        report.append("")

    if value_mismatch:
        report.append(f"⚠ VALUE MISMATCHES ({len(value_mismatch)}):")
        for item in value_mismatch:
            report.append(f"  - {item['ref']}: Expected '{item['expected']}', Got '{item['actual']}'")
        report.append("")

    # Critical signals check
    report.append("=" * 80)
    report.append("CRITICAL SIGNAL NETS")
    report.append("=" * 80)
    report.append("")

    critical_signals = [
        '12V_IN', '12V_FUSED', '12V_IGN', '12V_SWITCHED', 'GND',
        '+5V', '+3.3V',
        'IGN_DETECT', 'GATE_CTRL', 'SHUTDOWN_REQ',
        'SPI_MISO', 'SPI_MOSI', 'SPI_SCLK', 'SPI_CE0',
        'CAN_INT', 'CAN_TX', 'CAN_RX', 'CANH', 'CANL'
    ]

    found_signals = [s for s in critical_signals if s in data['global_labels']]
    missing_signals = [s for s in critical_signals if s not in data['global_labels']]

    report.append(f"Found Critical Signals ({len(found_signals)}):")
    for sig in found_signals:
        report.append(f"  ✓ {sig}")
    report.append("")

    if missing_signals:
        report.append(f"Missing Critical Signals ({len(missing_signals)}):")
        for sig in missing_signals:
            report.append(f"  ✗ {sig}")
        report.append("")

    # Connector analysis
    report.append("=" * 80)
    report.append("CONNECTOR ANALYSIS")
    report.append("=" * 80)
    report.append("")

    connectors = categories.get('Connectors', [])
    for conn in sorted(connectors, key=lambda x: x['reference']):
        report.append(f"{conn['reference']} ({conn['value']}):")
        # Try to determine pin count from lib_id
        if 'Conn_01x' in conn['lib_id']:
            pins = conn['lib_id'].split('x')[1] if 'x' in conn['lib_id'] else '?'
            report.append(f"  Pins: {pins}")
        report.append(f"  Location: ({conn['position'][0]:.1f}, {conn['position'][1]:.1f})")
        report.append("")

    return "\n".join(report)

def generate_checklist(missing, value_mismatch, data):
    """Generate actionable checklist"""

    checklist = []
    checklist.append("=" * 80)
    checklist.append("ACTION CHECKLIST - TODO ITEMS")
    checklist.append("=" * 80)
    checklist.append("")

    priority = 1

    # Critical missing components
    if missing:
        checklist.append(f"PRIORITY {priority}: ADD MISSING COMPONENTS")
        checklist.append("-" * 80)
        for ref in missing:
            checklist.append(f"  [ ] Add {ref} to schematic")
        checklist.append("")
        priority += 1

    # Value mismatches
    if value_mismatch:
        checklist.append(f"PRIORITY {priority}: FIX COMPONENT VALUES")
        checklist.append("-" * 80)
        for item in value_mismatch:
            checklist.append(f"  [ ] Change {item['ref']} from '{item['actual']}' to '{item['expected']}'")
        checklist.append("")
        priority += 1

    # J1 connector issues (known from previous analysis)
    checklist.append(f"PRIORITY {priority}: FIX J1 (ISO-A CONNECTOR) WIRING")
    checklist.append("-" * 80)
    checklist.append("  [ ] Remove SPI_CE0 from J1 pins")
    checklist.append("  [ ] Remove SPI_MISO from J1 pins")
    checklist.append("  [ ] Remove SPI_MOSI from J1 pins")
    checklist.append("  [ ] Remove SPI_SCLK from J1 pins")
    checklist.append("  [ ] Change J1 Pin 7 from '+3.3V' to '12V_ACC'")
    checklist.append("  [ ] Connect J1 Pin 8 to 'GND'")
    checklist.append("  [ ] Leave J1 Pins 1,2,3,5,6 unconnected (not used)")
    checklist.append("")
    priority += 1

    # Verify all other components are properly connected
    checklist.append(f"PRIORITY {priority}: VERIFY ALL COMPONENT CONNECTIONS")
    checklist.append("-" * 80)
    checklist.append("  [ ] Verify U1 (TPS54560) feedback network")
    checklist.append("  [ ] Verify U2 (LTV-817S) optoisolator connections")
    checklist.append("  [ ] Verify U3 (ATtiny85) all GPIO pins assigned")
    checklist.append("  [ ] Verify U4 (MCP2515) SPI connections to J2 (Pi GPIO)")
    checklist.append("  [ ] Verify U5 (SN65HVD230) CAN connections to J3 (OBD-II)")
    checklist.append("  [ ] Verify U6 (3.3V LDO) input from 5V, output to 3.3V")
    checklist.append("  [ ] Verify Q1 gate drive circuit (R_Q1_GATE, R_Q1_PULLDOWN)")
    checklist.append("  [ ] Verify Q2, Q3 LED driver circuits")
    checklist.append("")
    priority += 1

    # Final verification
    checklist.append(f"PRIORITY {priority}: FINAL VERIFICATION")
    checklist.append("-" * 80)
    checklist.append("  [ ] Run ERC and verify <60 errors remaining")
    checklist.append("  [ ] Review all power nets (12V_IGN, +5V, +3.3V, GND)")
    checklist.append("  [ ] Review all signal nets for correct routing")
    checklist.append("  [ ] Verify no net conflicts (like previous CAN_INT/SPI_CE0)")
    checklist.append("  [ ] Create backup before PCB layout")
    checklist.append("  [ ] Commit to git with detailed message")
    checklist.append("")

    return "\n".join(checklist)

def main():
    schematic_file = Path(r"C:\Users\eckma\projects\SubaruDash\pcb\wrx-power-can-hat-MANUAL.kicad_sch")

    print("Parsing KiCad schematic...")
    data = parse_kicad_schematic(schematic_file)

    print("Checking design requirements...")
    design_check = check_design_requirements(data)

    print("Generating report...")
    report = generate_report(data, design_check)

    print("Generating checklist...")
    checklist = generate_checklist(design_check[1], design_check[3], data)

    # Save report
    report_file = schematic_file.parent / "SCHEMATIC_ANALYSIS_REPORT.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n[OK] Report saved to: {report_file}")

    # Save checklist
    checklist_file = schematic_file.parent / "ACTION_CHECKLIST.txt"
    with open(checklist_file, 'w', encoding='utf-8') as f:
        f.write(checklist)
    print(f"[OK] Checklist saved to: {checklist_file}")

    # Save component data as JSON
    json_file = schematic_file.parent / "schematic_data.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"[OK] Component data saved to: {json_file}")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nTotal Components Found: {len(data['components'])}")
    print(f"Missing Required Components: {len(design_check[1])}")
    print(f"Value Mismatches: {len(design_check[3])}")
    print(f"\nReview the files above for detailed analysis and action items.")

if __name__ == "__main__":
    main()
