# WRX Power & CAN HAT - Detailed Bill of Materials

Complete component list with Digi-Key part numbers for ordering.

**Board:** Raspberry Pi HAT (with 4-channel audio DAC)
**Estimated Cost:** $40-48 per board (single quantity, Digi-Key pricing)

---

## Power Components

| Ref | Qty | Value | Description | Part Number | Package | Digi-Key | Unit Price | Ext Price |
|-----|-----|-------|-------------|-------------|---------|----------|-----------|-----------|
| U1 | 1 | LM2596S-5.0 | Buck regulator 12V→5V | LM2596S-5.0 | TO-263-5 | LM2596S-5.0/NOPB-ND | $3.50 | $3.50 |
| Q1 | 1 | IRF9540N | P-FET -100V -23A | IRF9540NPBF | TO-220 | IRF9540NPBF-ND | $2.10 | $2.10 |
| U6 | 1 | AMS1117-3.3 | LDO 3.3V 1A | AMS1117-3.3 | SOT-223 | 1470-AMS1117-3.3TR-ND | $0.42 | $0.42 |
| L1 | 1 | 33µH | Power inductor | SRN6045-330M | 6045 | SRN6045-330MCT-ND | $1.20 | $1.20 |
| D1 | 1 | SMBJ18A | TVS diode 18V | SMBJ18A | SMB | SMBJ18ALFCT-ND | $0.58 | $0.58 |
| D2 | 1 | SS34 | Schottky 3A 40V | SS34 | SMA | SS34FDICT-ND | $0.40 | $0.40 |
| D3 | 1 | SS54 | Schottky 5A 40V | SS54 | SMA | SS54FDICT-ND | $0.50 | $0.50 |
| F1 | 1 | 5A | Polyfuse resettable | 0154005.DR | 1206 | WK5505CT-ND | $0.70 | $0.70 |
| C1 | 1 | 100µF 25V | Electrolytic | EEE-FK1E101P | Radial | P122094-ND | $0.35 | $0.35 |
| C2 | 1 | 100µF 25V | Electrolytic | EEE-FK1E101P | Radial | P122094-ND | $0.35 | $0.35 |
| C3 | 1 | 220µF 16V | Electrolytic | EEE-FK1E221P | Radial | P122095-ND | $0.40 | $0.40 |
| C11 | 1 | 10µF | Ceramic 0805 | GRM21BR61E106KA73L | 0805 | 490-3886-1-ND | $0.20 | $0.20 |
| C12 | 1 | 10µF | Ceramic 0805 | GRM21BR61E106KA73L | 0805 | 490-3886-1-ND | $0.20 | $0.20 |
| R2 | 1 | 10kΩ | Resistor 0805 | RC0805FR-0710KL | 0805 | 311-10.0KCRCT-ND | $0.10 | $0.10 |
| R3 | 1 | 100Ω | Resistor 0805 | RC0805FR-07100RL | 0805 | 311-100CRCT-ND | $0.10 | $0.10 |
| R4 | 1 | 1.5kΩ | Resistor 0805 | RC0805FR-071K5L | 0805 | 311-1.50KCRCT-ND | $0.10 | $0.10 |
| R5 | 1 | 1kΩ | Resistor 0805 | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| | | | | | | **Subtotal** | | **$14.20** |

---

## Control & Timer Components

| Ref | Qty | Value | Description | Part Number | Package | Digi-Key | Unit Price | Ext Price |
|-----|-----|-------|-------------|-------------|---------|----------|-----------|-----------|
| U3 | 3 | ATtiny85-20PU | Microcontroller DIP-8 | ATTINY85-20PU | DIP-8 | ATTINY85-20PU-ND | $1.50 | $4.50 |
| - | 1 | DIP-8 Socket | IC socket | 4808-3000-CP | DIP-8 | AE10012-ND | $0.18 | $0.18 |
| Q2 | 1 | 2N7002 | N-FET SOT-23 | 2N7002 | SOT-23 | 2N7002NCT-ND | $0.35 | $0.35 |
| Q3 | 1 | 2N7002 | N-FET SOT-23 (fan) | 2N7002 | SOT-23 | 2N7002NCT-ND | $0.35 | $0.35 |
| C6 | 1 | 100nF | Ceramic 0805 | C0805C104K5RACTU | 0805 | 399-1170-1-ND | $0.10 | $0.10 |
| R8 | 1 | 10kΩ | Resistor 0805 | RC0805FR-0710KL | 0805 | 311-10.0KCRCT-ND | $0.10 | $0.10 |
| R9 | 1 | 470Ω | Resistor 0805 | RC0805FR-07470RL | 0805 | 311-470CRCT-ND | $0.10 | $0.10 |
| R10 | 1 | 470Ω | Resistor 0805 | RC0805FR-07470RL | 0805 | 311-470CRCT-ND | $0.10 | $0.10 |
| R11 | 1 | 10kΩ | Resistor 0805 | RC0805FR-0710KL | 0805 | 311-10.0KCRCT-ND | $0.10 | $0.10 |
| R14 | 1 | 470Ω | Resistor 0805 | RC0805FR-07470RL | 0805 | 311-470CRCT-ND | $0.10 | $0.10 |
| R15 | 1 | 1kΩ | Resistor 0805 (fan) | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| D7 | 1 | 1N4148 | Diode SOD-323 (flyback) | 1N4148 | SOD-323 | 1N4148W-FDICT-ND | $0.15 | $0.15 |
| LED2 | 1 | Red | LED 0805 (timer) | LTST-C150CKT | 0805 | 160-1405-1-ND | $0.20 | $0.20 |
| LED3 | 1 | Yellow | LED 0805 (heartbeat) | LTST-C150YKT | 0805 | 160-1130-1-ND | $0.20 | $0.20 |
| | | | | | | **Subtotal** | | **$6.63** |

---

## CAN Bus Components

| Ref | Qty | Value | Description | Part Number | Package | Digi-Key | Unit Price | Ext Price |
|-----|-----|-------|-------------|-------------|---------|----------|-----------|-----------|
| U4 | 1 | MCP2515-I/SO | CAN controller | MCP2515-I/SO | SOIC-18 | MCP2515-I/SO-ND | $3.20 | $3.20 |
| U5 | 1 | SN65HVD230 | CAN transceiver 3.3V | SN65HVD230DR | SOIC-8 | 296-42876-1-ND | $1.10 | $1.10 |
| Y1 | 1 | 8MHz | Crystal | ABM3-8.000MHZ-B2-T | 5032 SMD | 535-9122-1-ND | $0.60 | $0.60 |
| C7 | 1 | 100nF | Ceramic 0805 | C0805C104K5RACTU | 0805 | 399-1170-1-ND | $0.10 | $0.10 |
| C8 | 1 | 100nF | Ceramic 0805 | C0805C104K5RACTU | 0805 | 399-1170-1-ND | $0.10 | $0.10 |
| C9 | 1 | 22pF | Ceramic 0805 | C0805C220J5GACTU | 0805 | 399-1118-1-ND | $0.10 | $0.10 |
| C10 | 1 | 22pF | Ceramic 0805 | C0805C220J5GACTU | 0805 | 399-1118-1-ND | $0.10 | $0.10 |
| R12 | 1 | 10kΩ | Resistor 0805 | RC0805FR-0710KL | 0805 | 311-10.0KCRCT-ND | $0.10 | $0.10 |
| R13 | 1 | 120Ω | Resistor 0805 (termination) | RC0805FR-07120RL | 0805 | 311-120CRCT-ND | $0.10 | $0.10 |
| JP1 | 1 | 2-pin | Header 0.1" (termination jumper) | PEC02SAAN | 2-pin | S1011EC-02-ND | $0.10 | $0.10 |
| | | | | | | **Subtotal** | | **$5.70** |

---

## Audio Components (4-Channel DAC)

| Ref | Qty | Value | Description | Part Number | Package | Digi-Key | Unit Price | Ext Price |
|-----|-----|-------|-------------|-------------|---------|----------|-----------|-----------|
| U7 | 1 | PCM5142 | Quad I2S DAC | PCM5142RGZR | VQFN-48 | 296-38727-1-ND | $5.20 | $5.20 |
| C13 | 1 | 1µF | Ceramic 0805 | C0805C105K5RACTU | 0805 | 399-1284-1-ND | $0.12 | $0.12 |
| C14 | 1 | 1µF | Ceramic 0805 | C0805C105K5RACTU | 0805 | 399-1284-1-ND | $0.12 | $0.12 |
| C15 | 1 | 2.2µF | Ceramic 0805 (FL) | GRM21BR61E225KA12L | 0805 | 490-3897-1-ND | $0.15 | $0.15 |
| C16 | 1 | 2.2µF | Ceramic 0805 (FR) | GRM21BR61E225KA12L | 0805 | 490-3897-1-ND | $0.15 | $0.15 |
| C17 | 1 | 2.2µF | Ceramic 0805 (RL) | GRM21BR61E225KA12L | 0805 | 490-3897-1-ND | $0.15 | $0.15 |
| C18 | 1 | 2.2µF | Ceramic 0805 (RR) | GRM21BR61E225KA12L | 0805 | 490-3897-1-ND | $0.15 | $0.15 |
| R16 | 1 | 1kΩ | Resistor 0805 (FL) | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| R17 | 1 | 1kΩ | Resistor 0805 (FR) | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| R18 | 1 | 1kΩ | Resistor 0805 (RL) | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| R19 | 1 | 1kΩ | Resistor 0805 (RR) | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| | | | | | | **Subtotal** | | **$6.54** |

---

## Ignition Detection Components

| Ref | Qty | Value | Description | Part Number | Package | Digi-Key | Unit Price | Ext Price |
|-----|-----|-------|-------------|-------------|---------|----------|-----------|-----------|
| U2 | 1 | LTV-817S | Optoisolator | LTV-817S | SOP-4 | 160-1366-1-ND | $0.40 | $0.40 |
| C4 | 1 | 100nF | Ceramic 0805 | C0805C104K5RACTU | 0805 | 399-1170-1-ND | $0.10 | $0.10 |
| C5 | 1 | 10µF | Ceramic 0805 | GRM21BR61E106KA73L | 0805 | 490-3886-1-ND | $0.20 | $0.20 |
| R6 | 1 | 1kΩ | Resistor 0805 | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| R7 | 1 | 10kΩ | Resistor 0805 | RC0805FR-0710KL | 0805 | 311-10.0KCRCT-ND | $0.10 | $0.10 |
| | | | | | | **Subtotal** | | **$0.90** |

---

## Status LEDs

| Ref | Qty | Value | Description | Part Number | Package | Digi-Key | Unit Price | Ext Price |
|-----|-----|-------|-------------|-------------|---------|----------|-----------|-----------|
| LED1 | 1 | Green | LED 0805 (power) | LTST-C150GKT | 0805 | 160-1427-1-ND | $0.20 | $0.20 |
| LED4 | 1 | Blue | LED 0805 (CAN) | LTST-C150TBKT | 0805 | 160-1579-1-ND | $0.20 | $0.20 |
| R1 | 1 | 1kΩ | Resistor 0805 | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| R20 | 1 | 1kΩ | Resistor 0805 (CAN LED) | RC0805FR-071KL | 0805 | 311-1.00KCRCT-ND | $0.10 | $0.10 |
| | | | | | | **Subtotal** | | **$0.60** |

---

## Connectors

| Ref | Qty | Value | Description | Part Number | Package | Digi-Key | Unit Price | Ext Price |
|-----|-----|-------|-------------|-------------|---------|----------|-----------|-----------|
| **J1** | 1 | ISO A | ISO 10487-A Power (8-pin) | Molex 171822-0008 | 8-pin ISO | WM18753-ND | $1.40 | $1.40 |
| **J2** | 1 | GPIO | 40-pin stacking header | SSW-120-02-T-D | 2x20 female | SAM1206-20-ND | $2.50 | $2.50 |
| **J3** | 1 | ISP | Programming header 2x3 | 3220-06-0100-00 | 2x3 0.1" | 609-3234-ND | $0.40 | $0.40 |
| **J4** | 1 | OBD-II | OBD-II J1962 Female 16-pin | TE 1-1718644-1 | 16-pin OBD | A115904-ND | $3.50 | $3.50 |
| **J5** | 1 | CAN Term | Screw terminal 2-pos (optional) | ED555/2DS | 5mm pitch | ED2635-ND | $0.50 | $0.50 |
| **J6** | 1 | Fan | JST-XH 2-pin | JST B2B-XH-A | 2-pin JST | 455-2248-ND | $0.15 | $0.15 |
| **J7** | 1 | Audio | JST-XH 6-pin (to amp module) | JST B6B-XH-A | 6-pin JST | 455-2249-ND | $0.30 | $0.30 |
| **JP2** | 1 | Fan V Sel | Header 3-pin 0.1" | PEC03SAAN | 3-pin | S1011EC-03-ND | $0.12 | $0.12 |
| | | | | | | **Subtotal** | | **$8.87** |

---

## PCB & Manufacturing

| Item | Qty | Description | Supplier | Unit Price | Ext Price |
|------|-----|-------------|----------|-----------|-----------|
| PCB | 1 | 85×56mm 2-layer HAT | JLCPCB | $2.00 | $2.00 |
| Assembly | - | Hand solder | DIY | $0.00 | $0.00 |
| | | | **Subtotal** | | **$2.00** |

---

## Cost Summary

| Category | Cost |
|----------|------|
| Power Components | $14.20 |
| Control & Timer | $6.63 |
| CAN Bus | $5.70 |
| Audio DAC | $6.54 |
| Ignition Detection | $0.90 |
| Status LEDs | $0.60 |
| Connectors | $8.87 |
| PCB Fabrication | $2.00 |
| **TOTAL PER BOARD** | **$45.44** |

**Estimated total with shipping/tax:** ~$50-55 per board

---

## Ordering Notes

### Digi-Key Cart

1. All part numbers above are Digi-Key part numbers
2. Order 2-3x quantity for spare resistors/capacitors (cheap insurance)
3. Order 3x ATtiny85-20PU (extras for firmware iteration)
4. Minimum order usually $0 (no minimum at Digi-Key)

### JLCPCB PCB Order

1. Upload Gerber files (when design is complete)
2. Specifications:
   - Qty: 5 boards (minimum)
   - Layers: 2
   - Thickness: 1.6mm
   - Color: Green (or your preference)
   - Surface Finish: HASL or ENIG
   - Remove order number: Yes (+$1.50)
3. Total: ~$10-15 for 5 boards + shipping

### Total Project Cost (5 Boards)

- Components: 5 × $45 = $225
- PCBs: 5 boards = $12
- Shipping (Digi-Key): ~$8
- Shipping (JLCPCB): ~$15
- **Grand Total: ~$260 for 5 complete boards**
- **Cost per board: ~$52**

---

## Assembly Order

Recommended soldering sequence:

1. **SMD components first (0805):**
   - Resistors
   - Capacitors (ceramic)
   - LEDs
2. **IC chips (SOIC/SOT-23):**
   - U1-U7, Q2, Q3
3. **Through-hole:**
   - Electrolytic capacitors
   - DIP-8 socket (not the ATtiny85 yet!)
   - Crystal Y1
4. **Connectors:**
   - J1 (ISO A)
   - J4 (OBD-II)
   - J6, J7 (JST)
   - J2 (GPIO header - last!)
5. **Final:**
   - Program ATtiny85 using Arduino Mega ISP
   - Insert ATtiny85 into socket
   - Test before connecting to Pi

---

## Optional Upgrades

**Add to cart if desired:**
- Extra ATtiny85 chips (already 3x in BOM)
- Jumper shunts for JP1, JP2 (Digi-Key: S9000-ND, $0.10 each)
- Heatsink for LM2596 if needed (Digi-Key: HS145-ND, $0.50)

**Not included (user supplies):**
- Raspberry Pi 4/5
- MicroSD card
- Car-specific ISO harness adapter (~$15 on Amazon)
- OBD-II Y-splitter cable (~$10 on Amazon)
- Soldering equipment

---

## Next: Order Components

Once KiCad schematic is complete and verified:
1. Copy Digi-Key part numbers to Digi-Key BOM tool
2. Order components
3. Order PCBs from JLCPCB
4. Wait 5-7 days for delivery
5. Assemble and test!
