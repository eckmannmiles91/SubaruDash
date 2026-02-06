# Footprint Assignment Plan

## Components Already Assigned
| Ref | Value | Current Footprint | Status |
|-----|-------|-------------------|--------|
| Q1 | IRLB8721PBF | TO-220-3_Vertical | OK |
| Q2 | 2N7002 | SOT-23 | OK |
| Q3 | 2N7002 | SOT-23 | OK |
| U1 | TPS54560BDDA | Texas_R-PDSO-G8 | OK |
| U2 | LTV-817S | DIP-4_W7.62mm | OK |
| U3 | ATtiny85 | DIP-8_W7.62mm | OK |
| U4 | MCP2515 | SOIC-18W | OK |
| U5 | SN65HVD230 | SOIC-8 | OK |
| U6 | AMS1117-3.3 | SOT-223-3 | OK |

## Capacitors - Recommended: 0805 (most), 1206 (bulk)
| Ref | Value | Suggested Footprint | Notes |
|-----|-------|---------------------|-------|
| C1 | 100nF | Capacitor_SMD:C_0805_2012Metric | Decoupling |
| C2 | 10uF | Capacitor_SMD:C_1206_3216Metric | Bulk |
| C3 | 100nF | Capacitor_SMD:C_0805_2012Metric | Decoupling |
| C4 | 10uF | Capacitor_SMD:C_1206_3216Metric | Bulk |
| C5 | 22pF | Capacitor_SMD:C_0805_2012Metric | Crystal load |
| C6 | 22pF | Capacitor_SMD:C_0805_2012Metric | Crystal load |
| C7 | 100nF | Capacitor_SMD:C_0805_2012Metric | Decoupling |
| C8 | 100nF | Capacitor_SMD:C_0805_2012Metric | Decoupling |
| C9 | 2.2uF | Capacitor_SMD:C_0805_2012Metric | Filter |
| C10 | 10uF | Capacitor_SMD:C_1206_3216Metric | Input bulk |
| C11 | 1uF | Capacitor_SMD:C_0805_2012Metric | Output |
| C12 | 2.2uF | Capacitor_SMD:C_0805_2012Metric | Output |
| C13 | 1uF | Capacitor_SMD:C_0805_2012Metric | Output |
| C14 | 2.2uF | Capacitor_SMD:C_0805_2012Metric | Output |
| C15 | 2.2uF | Capacitor_SMD:C_0805_2012Metric | Output |
| C16 | 22pF | Capacitor_SMD:C_0805_2012Metric | Crystal load |
| C17 | 22pF | Capacitor_SMD:C_0805_2012Metric | Crystal load |
| C18 | 10uF | Capacitor_SMD:C_1206_3216Metric | Bulk |
| C19 | 22uF | Capacitor_SMD:C_1206_3216Metric | Bulk |
| C20 | 22uF | Capacitor_SMD:C_1206_3216Metric | Input bulk |

## Resistors - Recommended: 0805
| Ref | Value | Suggested Footprint | Notes |
|-----|-------|---------------------|-------|
| R1 | 1k | Resistor_SMD:R_0805_2012Metric | LED current limit |
| R4 | 10k 1% | Resistor_SMD:R_0805_2012Metric | Feedback divider |
| R5 | 51k 1% | Resistor_SMD:R_0805_2012Metric | Feedback divider |
| R6 | 10k | Resistor_SMD:R_0805_2012Metric | Optoisolator |
| R8 | 120 | Resistor_SMD:R_0805_2012Metric | CAN termination |
| R9 | 10k | Resistor_SMD:R_0805_2012Metric | Pull-up |
| R10 | 1k | Resistor_SMD:R_0805_2012Metric | Gate resistor |
| R11 | 10k | Resistor_SMD:R_0805_2012Metric | Pull-down |
| R12 | 10k | Resistor_SMD:R_0805_2012Metric | LED current |
| R13 | 470 | Resistor_SMD:R_0805_2012Metric | LED current |
| R14 | 1k | Resistor_SMD:R_0805_2012Metric | |
| R15 | 1k | Resistor_SMD:R_0805_2012Metric | |
| R16 | 470 | Resistor_SMD:R_0805_2012Metric | LED current |
| R17 | 1k | Resistor_SMD:R_0805_2012Metric | |
| R18 | 1k | Resistor_SMD:R_0805_2012Metric | |
| R19 | 1k | Resistor_SMD:R_0805_2012Metric | |
| R20 | 470 | Resistor_SMD:R_0805_2012Metric | Gate drive |
| R21 | 10k | Resistor_SMD:R_0805_2012Metric | Pull-up |

## Inductors
| Ref | Value | Suggested Footprint | Notes |
|-----|-------|---------------------|-------|
| L1 | 33uH | Inductor_SMD:L_Bourns_SRN6045TA | Power inductor 5A+ |
| L2 | Ferrite | Inductor_SMD:L_0805_2012Metric | EMI filter |
| L3 | Ferrite | Inductor_SMD:L_0805_2012Metric | EMI filter |

## Diodes
| Ref | Value | Suggested Footprint | Notes |
|-----|-------|---------------------|-------|
| D1 | SMBJ18A | Diode_SMD:D_SMB | TVS diode |
| D2 | SS34 | Diode_SMD:D_SMA | Schottky 3A |

## Fuse
| Ref | Value | Suggested Footprint | Notes |
|-----|-------|---------------------|-------|
| F1 | 5A | Fuse:Fuseholder_Blade_Mini_Keystone_3568 | Automotive blade fuse |

## LEDs
| Ref | Value | Suggested Footprint | Notes |
|-----|-------|---------------------|-------|
| LED1 | Green | LED_SMD:LED_0805_2012Metric | Power indicator |
| LED2 | Red | LED_SMD:LED_0805_2012Metric | Timer LED |
| LED3 | Yellow | LED_SMD:LED_0805_2012Metric | Heartbeat LED |

## Connectors
| Ref | Value | Suggested Footprint | Notes |
|-----|-------|---------------------|-------|
| J1 | ISO_A | Connector_Molex:Molex_Mini-Fit_Jr_5566-08A | 8-pin automotive power |
| J2 | Pi_GPIO | Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical | Raspberry Pi header |
| J3 | OBD-II | Connector_Dsub:DSUB-9_Male_Horizontal_P2.77x2.84mm | OBD-II (DB9 subset) |
| J4 | CAN_Term | TerminalBlock:TerminalBlock_bornier-2_P5.08mm | Screw terminal |
| J5 | ISP | Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical | AVR ISP header |
| J6 | FAN | Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical | Fan connector |
| J7 | Audio | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Audio output |
| JP1 | Jumper | Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical | Config jumper |
| JP2 | 5V/12V | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Voltage select |

## Crystals
| Ref | Value | Suggested Footprint | Notes |
|-----|-------|---------------------|-------|
| Y1 | 16MHz | Crystal:Crystal_HC49-4H_Vertical | Through-hole crystal |
| Y2 | 16MHz | Crystal:Crystal_HC49-4H_Vertical | Through-hole crystal |

---

## Summary
- **Total components:** 64
- **Already assigned:** 9
- **Need assignment:** 55

## Design Notes
- Using 0805 for most passives (good balance of size and hand-solderability)
- 1206 for bulk capacitors (10uF+) due to voltage rating
- Power inductor needs current rating for 5A TPS54560
- Automotive blade fuse for easy replacement
