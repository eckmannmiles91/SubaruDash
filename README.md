# SubaruDash

Digital dash project for 2013 Subaru WRX

## Overview

This project documents the development of a custom digital dashboard for a 2013 WRX, including cluster EEPROM backup/modification work.

## Documentation

- [CLUSTER_EEPROM_GUIDE.md](CLUSTER_EEPROM_GUIDE.md) - Guide for reading and writing the instrument cluster EEPROM using CH341A programmer
- [CAN_SNIFFING_GUIDE.md](CAN_SNIFFING_GUIDE.md) - Guide for CAN bus sniffing using Raspberry Pi 5 and MCP2515 module

## Tools

- [tools/AsProgrammer/](tools/AsProgrammer/) - AsProgrammer v2.1.2 for reading/writing EEPROM chips (Windows)

## Hardware

### Cluster EEPROM Work
- CH341A USB EEPROM Programmer - [Amazon Link](https://www.amazon.com/dp/B07VNVVXW6)
- 2013 WRX backup instrument cluster (eBay)

### CAN Bus Sniffing
- Raspberry Pi 5 with OpenDash installed
- 2x MCP2515 CAN Bus Module (TJA1050 transceiver)
- OBD-II Splitter Cable
- 12V to 5V buck converter
- Jumper wires

## Current Status

### Cluster EEPROM Work
- [ ] Backup cluster received (ordered from eBay)
- [x] EEPROM chip identified (S93C76)
- [x] Main MCU identified (MB90428GAV)
- [x] CH341A programmer purchased and set up
- [x] Documentation created for EEPROM reading/writing
- [ ] Backup cluster EEPROM read and backed up

### CAN Bus Sniffing
- [x] MCP2515 CAN modules available (2x)
- [x] Raspberry Pi 5 with OpenDash running
- [x] OBD-II splitter cable available
- [x] CAN sniffing documentation created
- [ ] MCP2515 connected to Pi5 GPIO
- [ ] SocketCAN configured on Pi5
- [ ] CAN bus data collection started
- [ ] CAN IDs mapped for WRX sensors

### Digital Dash Development
- [ ] Hardware platform selection
- [ ] Display selection
- [ ] Software architecture design
- [ ] Implementation
