# Bill of Materials - SubaruDash WRX Power CAN HAT

## Summary
- **Total Unique Parts:** 35
- **Total Components:** 64
- **Estimated Cost:** ~$25-35 USD (excluding PCB)

---

## Capacitors (20 pcs)

| Value | Package | Qty | Part Number | Notes |
|-------|---------|-----|-------------|-------|
| 100nF | 0805 | 5 | CL21B104KBCNNNC | C1,C3,C7,C8 - Decoupling |
| 22pF | 0805 | 4 | CL21C220JBANNNC | C5,C6,C16,C17 - Crystal load |
| 1uF | 0805 | 2 | CL21B105KAFNNNE | C11,C13 |
| 2.2uF | 0805 | 4 | CL21B225KAFNNNE | C9,C12,C14,C15 |
| 10uF | 1206 | 4 | CL31A106KAHNNNE | C2,C4,C10,C18 - 25V rated |
| 22uF | 1206 | 2 | CL31A226MPHNNNE | C19,C20 - 25V rated |

## Resistors (18 pcs)

| Value | Package | Qty | Part Number | Notes |
|-------|---------|-----|-------------|-------|
| 120Ω | 0805 | 1 | RC0805FR-07120RL | R8 - CAN termination |
| 470Ω | 0805 | 3 | RC0805FR-07470RL | R13,R16,R20 - LED/Gate |
| 1kΩ | 0805 | 7 | RC0805FR-071KL | R1,R10,R14,R15,R17,R18,R19 |
| 10kΩ | 0805 | 5 | RC0805FR-0710KL | R6,R9,R11,R12,R21 |
| 10kΩ 1% | 0805 | 1 | RC0805FR-0710KL | R4 - Feedback |
| 51kΩ 1% | 0805 | 1 | RC0805FR-0751KL | R5 - Feedback |

## Inductors (3 pcs)

| Value | Package | Qty | Part Number | Notes |
|-------|---------|-----|-------------|-------|
| 33µH | 6045 | 1 | SRN6045TA-330M | L1 - Power inductor 5A+ |
| Ferrite | 0805 | 2 | BLM21PG121SN1D | L2,L3 - CAN EMI filter |

## Semiconductors (12 pcs)

| Part | Package | Qty | Part Number | Notes |
|------|---------|-----|-------------|-------|
| TPS54560BDDA | HTSSOP-8 | 1 | TPS54560BDDAR | 5A buck converter |
| AMS1117-3.3 | SOT-223 | 1 | AMS1117-3.3 | 3.3V LDO |
| MCP2515 | SOIC-18 | 1 | MCP2515-I/SO | CAN controller |
| SN65HVD230 | SOIC-8 | 1 | SN65HVD230DR | CAN transceiver |
| ATtiny85 | DIP-8 | 1 | ATTINY85-20PU | Timer MCU |
| LTV-817S | DIP-4 | 1 | LTV-817S | Optoisolator |
| IRLB8721PBF | TO-220 | 1 | IRLB8721PBF | Power MOSFET |
| 2N7002 | SOT-23 | 2 | 2N7002 | Small signal MOSFET |
| SMBJ18A | SMB | 1 | SMBJ18A | TVS diode |
| SS34 | SMA | 1 | SS34 | Schottky diode |

## LEDs (3 pcs)

| Color | Package | Qty | Part Number | Notes |
|-------|---------|-----|-------------|-------|
| Green | 0805 | 1 | LTST-C171GKT | LED1 - Power |
| Red | 0805 | 1 | LTST-C171KRKT | LED2 - Timer |
| Yellow | 0805 | 1 | LTST-C171KSKT | LED3 - Heartbeat |

## Connectors (9 pcs)

| Type | Qty | Part Number | Notes |
|------|-----|-------------|-------|
| Molex Mini-Fit Jr 8-pin | 1 | 39-30-1080 | J1 - Automotive power |
| 2x20 Header | 1 | PPPC202LFBN-RC | J2 - Raspberry Pi |
| DB9 Male | 1 | Generic | J3 - OBD-II |
| 2-pos Screw Terminal | 1 | 1935161 | J4 - CAN termination |
| 2x3 Header | 1 | PPPC032LFBN-RC | J5 - ISP |
| 1x2 Header | 2 | PPPC021LFBN-RC | J6, JP1 |
| 1x3 Header | 2 | PPPC031LFBN-RC | J7, JP2 |

## Misc (3 pcs)

| Part | Qty | Part Number | Notes |
|------|-----|-------------|-------|
| 16MHz Crystal HC49 | 2 | ABLS-16.000MHZ-B4-T | Y1, Y2 |
| Mini Blade Fuse Holder | 1 | Keystone 3568 | F1 |
| 5A Mini Blade Fuse | 1 | Generic | For F1 |

---

## Supplier Links

### DigiKey Order
Most parts available from DigiKey. Search by part number.

### LCSC (Budget Option)
For basic passives (resistors, capacitors), LCSC offers lower prices.

### Amazon/eBay
- Raspberry Pi 2x20 headers
- Generic blade fuse holders
- DB9 connectors

---

## Notes

1. **Voltage Ratings:** All capacitors should be rated 25V+ for 12V automotive use
2. **1% Resistors:** R4, R5 critical for voltage regulation accuracy
3. **Power Inductor:** L1 must handle 5A continuous, check DCR < 50mΩ
4. **Automotive Grade:** Consider AEC-Q qualified parts for harsh environments
