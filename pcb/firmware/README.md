# ATtiny85 Timer Controller Firmware

This folder contains the firmware for the ATtiny85 microcontroller that handles the 45-second shutdown delay timer on the WRX Power & CAN HAT.

## Files

- **timer_controller.ino** - Main firmware code for ATtiny85

## Hardware Requirements

- ATtiny85-20PU (DIP-8 package) - 3x recommended for testing/spares
- Arduino Mega 2560 (as ISP programmer)
- Jumper wires
- Breadboard (optional, for testing)
- 10µF capacitor (for Arduino Mega RESET pin)

## Programming Setup

### Step 1: Prepare Arduino Mega as ISP Programmer

1. Open Arduino IDE
2. Go to **File → Examples → 11.ArduinoISP → ArduinoISP**
3. Select **Tools → Board → Arduino Mega 2560**
4. Select the correct **Port** for your Mega
5. Upload the ArduinoISP sketch to the Mega
6. **Important:** Place a 10µF capacitor between RESET and GND on the Mega (this prevents it from resetting during programming)

### Step 2: Wire ATtiny85 to Arduino Mega

Connect the ATtiny85 DIP-8 chip to the Arduino Mega using these connections:

| ATtiny85 Pin | Pin Name | Arduino Mega Pin | Notes |
|--------------|----------|------------------|-------|
| 1 | PB5 (RESET) | Pin 10 | ISP RESET signal |
| 2 | PB3 (XTAL1) | Not connected | Timer status LED (on PCB) |
| 3 | PB4 (XTAL2) | Not connected | Debug LED (on PCB) |
| 4 | GND | GND | Ground |
| 5 | PB0 (MOSI) | Pin 51 (MOSI) | ISP data in |
| 6 | PB1 (MISO) | Pin 50 (MISO) | ISP data out |
| 7 | PB2 (SCK) | Pin 52 (SCK) | ISP clock |
| 8 | VCC | 5V | Power (5V) |

**Visual Wiring Diagram:**
```
Arduino Mega                    ATtiny85 DIP-8
============                    ==============

                                 ┌────────┐
Pin 10 (RESET) ─────────────────┤1 RST  8├──── 5V
                                 │        │
Pin 51 (MOSI)  ─────────────────┤5 PB0  7├──── Pin 52 (SCK)
                                 │        │
Pin 50 (MISO)  ─────────────────┤6 PB1  6├──── Not connected (LED on PCB)
                                 │        │
GND ────────────────────────────┤4 GND  5├──── Not connected (LED on PCB)
                                 └────────┘

5V ──────────────────────────────────────── Pin 8 (VCC)
GND ─────────────────────────────────────── Pin 4 (GND)

RESET ───[10µF Cap]─── GND  (on Arduino Mega, prevents auto-reset)
```

### Step 3: Configure Arduino IDE for ATtiny85

1. Install ATtiny board support:
   - Go to **File → Preferences**
   - Add this URL to "Additional Boards Manager URLs":
     ```
     https://raw.githubusercontent.com/damellis/attiny/ide-1.6.x-boards-manager/package_damellis_attiny_index.json
     ```
   - Go to **Tools → Board → Boards Manager**
   - Search for "attiny" and install **"attiny by David A. Mellis"**

2. Configure board settings:
   - **Tools → Board → ATtiny Microcontrollers → ATtiny25/45/85**
   - **Tools → Processor → ATtiny85**
   - **Tools → Clock → Internal 8 MHz**
   - **Tools → Programmer → Arduino as ISP**
   - **Tools → Port →** (select your Arduino Mega's port)

### Step 4: Upload Firmware

1. Open **timer_controller.ino** in Arduino IDE
2. Verify the wiring is correct (see Step 2)
3. **Burn Bootloader** (only needed once per chip):
   - Go to **Tools → Burn Bootloader**
   - This sets the fuses to use the internal 8MHz oscillator
   - Wait for "Done burning bootloader" message
4. **Upload the sketch**:
   - Click **Sketch → Upload Using Programmer** (NOT the regular Upload button!)
   - Wait for "Done uploading" message

**Important:** Always use **"Upload Using Programmer"**, NOT the regular Upload button!

### Step 5: Verify Programming

After uploading, the ATtiny85 should:
- Output HIGH on PB2 when powered (power control active)
- Blink the heartbeat LED on PB4 every 2 seconds (if connected)

You can test this by:
1. Removing the ATtiny85 from the programming setup
2. Powering it with 5V and GND
3. Checking PB2 with a multimeter (should read ~5V)

## Firmware Operation

The firmware implements a state machine with three states:

1. **POWER_ON** - Normal operation when ignition is ON
   - Keeps power enabled (PB2 = HIGH)
   - Monitors ignition signal on PB0

2. **TIMER_RUNNING** - Ignition OFF, 45-second countdown active
   - Keeps power enabled during countdown
   - Blinks timer LED on PB3
   - Cancels timer if ignition comes back ON
   - Proceeds to shutdown if timer expires or Pi signals ready

3. **SHUTDOWN** - Power off
   - Cuts power (PB2 = LOW)
   - Waits for ignition to come back ON

## Pin Assignments (on PCB)

| ATtiny85 Pin | Function | Direction | Connected To |
|--------------|----------|-----------|--------------|
| PB0 (Pin 5) | Ignition Detect | Input | PC817 output (LOW = ON) |
| PB1 (Pin 6) | Shutdown Signal | Input | Pi GPIO (HIGH = shutdown) |
| PB2 (Pin 7) | Power Control | Output | P-FET gate driver (HIGH = on) |
| PB3 (Pin 2) | Timer LED | Output | Red LED (blinks during timer) |
| PB4 (Pin 3) | Heartbeat LED | Output | Optional debug LED |

## Troubleshooting

**"avrdude: stk500_getsync() not in sync"**
- Check that you uploaded ArduinoISP to the Mega first
- Verify the 10µF cap is between RESET and GND on Mega
- Check all wiring connections

**"avrdude: Yikes! Invalid device signature"**
- Wrong board selected, should be ATtiny85
- Check VCC and GND connections
- Try different ATtiny85 chip (might be damaged)

**Firmware uploads but doesn't work:**
- Make sure you burned the bootloader first (sets fuses)
- Verify clock is set to "Internal 8MHz"
- Check that you're using "Upload Using Programmer"

**LEDs don't blink on PCB:**
- ATtiny85 might not be powered (check 3.3V rail)
- Check LED polarity and resistor values
- Verify firmware uploaded successfully

## Reprogramming on PCB

With the DIP-8 socket on the PCB:
1. Power off the PCB completely
2. Use a small flathead screwdriver to gently pry the ATtiny85 out of the socket
3. Insert it into your programming setup (Arduino Mega ISP)
4. Upload new firmware
5. Remove from programmer and insert back into PCB socket
6. Power on and test

**Time required:** 2-3 minutes per iteration

## Firmware Modifications

If you need to adjust the timer duration, edit this line in `timer_controller.ino`:

```cpp
const uint32_t SHUTDOWN_DELAY_MS = 45000; // 45 seconds
```

Change 45000 to your desired delay in milliseconds (e.g., 30000 for 30 seconds, 60000 for 60 seconds).

After making changes, re-upload using "Upload Using Programmer".

## Testing Without PCB

You can test the firmware logic on a breadboard with just the ATtiny85 and a couple LEDs:

**Test Circuit:**
```
ATtiny85 Pin 5 (PB0) ──┬── Button to GND (simulates ignition OFF)
                       └── 10kΩ to 5V (pull-up)

ATtiny85 Pin 6 (PB1) ──┬── Button to 5V (simulates Pi shutdown signal)
                       └── 10kΩ to GND (pull-down)

ATtiny85 Pin 7 (PB2) ──── LED ──── 470Ω ──── GND (power status)

ATtiny85 Pin 2 (PB3) ──── LED ──── 470Ω ──── GND (timer status)

ATtiny85 Pin 8 ──── 5V
ATtiny85 Pin 4 ──── GND
```

**Test Scenarios:**
1. Power on → PB2 LED should light (power active)
2. Press ignition button → PB3 LED should blink (timer running)
3. Wait 45s → PB2 LED should turn off (power cut)
4. Release ignition button → PB2 LED should turn on (power restored)

## Additional Resources

- [ATtiny85 Datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2586-AVR-8-bit-Microcontroller-ATtiny25-ATtiny45-ATtiny85_Datasheet.pdf)
- [Arduino as ISP Tutorial](https://docs.arduino.cc/built-in-examples/arduino-isp/ArduinoISP/)
- [Programming ATtiny with Arduino IDE](https://create.arduino.cc/projecthub/arjun/programming-attiny85-with-arduino-uno-afb829)
