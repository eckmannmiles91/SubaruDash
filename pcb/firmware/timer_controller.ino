/*
 * ATtiny85 Timer Controller for WRX Power & CAN HAT
 *
 * Purpose: Provides 45-second shutdown delay when ignition turns off
 * to allow Raspberry Pi to complete safe shutdown sequence.
 *
 * Pin Assignments (ATtiny85 DIP-8):
 * - PB0 (Pin 5): Ignition Detect Input (from PC817, LOW = ignition ON, HIGH = ignition OFF)
 * - PB1 (Pin 6): Shutdown Signal Input (from Pi GPIO, HIGH = Pi requesting shutdown)
 * - PB2 (Pin 7): Power Control Output (to P-FET gate, HIGH = keep power on)
 * - PB3 (Pin 2): Timer Status LED (HIGH = timer counting, blinks during countdown)
 * - PB4 (Pin 3): Debug/Heartbeat LED (optional, blinks every 2s when powered)
 *
 * State Machine:
 * - POWER_ON: Ignition is on, power flows to Pi
 * - TIMER_RUNNING: Ignition off, 45s countdown active, power still on
 * - SHUTDOWN: Timer expired or Pi signaled shutdown, power off
 *
 * Behavior:
 * 1. When ignition ON → power ON immediately
 * 2. When ignition OFF → start 45-second timer, keep power ON
 * 3. During timer → if ignition comes back ON, cancel timer and return to POWER_ON
 * 4. After 45s OR if Pi signals shutdown → cut power (P-FET off)
 *
 * Hardware Notes:
 * - Uses internal 8MHz oscillator (no external crystal needed)
 * - Watchdog timer NOT used (we want predictable timing)
 * - Timer uses millis() for accurate 45-second countdown
 *
 * Compile Settings (Arduino IDE):
 * - Board: ATtiny25/45/85
 * - Processor: ATtiny85
 * - Clock: Internal 8MHz
 * - Programmer: Arduino as ISP
 */

// Pin definitions
const uint8_t PIN_IGNITION_IN = PB0;   // Input: Ignition detect (LOW = ON, HIGH = OFF)
const uint8_t PIN_SHUTDOWN_IN = PB1;   // Input: Pi shutdown signal (HIGH = Pi wants shutdown)
const uint8_t PIN_POWER_OUT = PB2;     // Output: P-FET gate control (HIGH = power ON)
const uint8_t PIN_TIMER_LED = PB3;     // Output: Timer status LED
const uint8_t PIN_HEARTBEAT_LED = PB4; // Output: Heartbeat LED (optional debug)

// Timer configuration
const uint32_t SHUTDOWN_DELAY_MS = 45000; // 45 seconds
const uint16_t DEBOUNCE_DELAY_MS = 100;   // 100ms debounce for ignition signal
const uint16_t LED_BLINK_RATE_MS = 500;   // Blink timer LED every 500ms during countdown

// State machine states
enum State {
  POWER_ON,       // Normal operation, ignition ON
  TIMER_RUNNING,  // Ignition OFF, countdown active
  SHUTDOWN        // Power off
};

// Global state
State currentState = POWER_ON;
uint32_t timerStartTime = 0;
uint32_t lastIgnitionChangeTime = 0;
uint32_t lastLedToggleTime = 0;
bool ignitionState = false;      // true = ON, false = OFF
bool lastIgnitionReading = false;
bool timerLedState = false;
bool heartbeatLedState = false;
uint32_t lastHeartbeatTime = 0;

void setup() {
  // Configure pins
  pinMode(PIN_IGNITION_IN, INPUT);      // PC817 output (pulled up externally)
  pinMode(PIN_SHUTDOWN_IN, INPUT);      // Pi shutdown signal (pulled down externally)
  pinMode(PIN_POWER_OUT, OUTPUT);       // P-FET gate control
  pinMode(PIN_TIMER_LED, OUTPUT);       // Timer status LED
  pinMode(PIN_HEARTBEAT_LED, OUTPUT);   // Heartbeat LED

  // Initial state: power ON (assume ignition is ON at boot)
  digitalWrite(PIN_POWER_OUT, HIGH);    // Turn power ON
  digitalWrite(PIN_TIMER_LED, LOW);     // Timer LED off
  digitalWrite(PIN_HEARTBEAT_LED, LOW); // Heartbeat LED off

  currentState = POWER_ON;

  // Read initial ignition state
  ignitionState = !digitalRead(PIN_IGNITION_IN); // LOW = ON, so invert
  lastIgnitionReading = ignitionState;
}

void loop() {
  uint32_t currentTime = millis();

  // Read inputs with debouncing
  bool ignitionReading = !digitalRead(PIN_IGNITION_IN); // LOW = ON, invert to true
  bool shutdownRequested = digitalRead(PIN_SHUTDOWN_IN); // HIGH = shutdown requested

  // Debounce ignition signal (100ms)
  if (ignitionReading != lastIgnitionReading) {
    lastIgnitionChangeTime = currentTime;
  }

  if ((currentTime - lastIgnitionChangeTime) > DEBOUNCE_DELAY_MS) {
    if (ignitionReading != ignitionState) {
      ignitionState = ignitionReading;
      // Ignition state changed after debounce
    }
  }
  lastIgnitionReading = ignitionReading;

  // Heartbeat LED (blink every 2 seconds to show we're alive)
  if (currentTime - lastHeartbeatTime > 2000) {
    heartbeatLedState = !heartbeatLedState;
    digitalWrite(PIN_HEARTBEAT_LED, heartbeatLedState);
    lastHeartbeatTime = currentTime;
  }

  // State machine
  switch (currentState) {
    case POWER_ON:
      // Normal operation: ignition is ON, power flows to Pi
      digitalWrite(PIN_POWER_OUT, HIGH);  // Keep power ON
      digitalWrite(PIN_TIMER_LED, LOW);   // Timer LED off

      if (!ignitionState) {
        // Ignition turned OFF → start timer
        currentState = TIMER_RUNNING;
        timerStartTime = currentTime;
        lastLedToggleTime = currentTime;
        timerLedState = true;
        digitalWrite(PIN_TIMER_LED, HIGH); // Turn on timer LED
      }
      break;

    case TIMER_RUNNING:
      // Timer countdown: ignition is OFF, but keeping power ON for Pi shutdown
      digitalWrite(PIN_POWER_OUT, HIGH);  // Keep power ON during countdown

      // Blink timer LED during countdown
      if (currentTime - lastLedToggleTime > LED_BLINK_RATE_MS) {
        timerLedState = !timerLedState;
        digitalWrite(PIN_TIMER_LED, timerLedState);
        lastLedToggleTime = currentTime;
      }

      // Check if ignition came back ON (user restarted car during countdown)
      if (ignitionState) {
        // Cancel timer, return to normal operation
        currentState = POWER_ON;
        digitalWrite(PIN_TIMER_LED, LOW);
        break;
      }

      // Check if Pi signaled shutdown complete
      if (shutdownRequested) {
        // Pi has shut down, cut power immediately
        currentState = SHUTDOWN;
        break;
      }

      // Check if timer expired
      if (currentTime - timerStartTime >= SHUTDOWN_DELAY_MS) {
        // 45 seconds elapsed, cut power
        currentState = SHUTDOWN;
      }
      break;

    case SHUTDOWN:
      // Power off: cut power to Pi
      digitalWrite(PIN_POWER_OUT, LOW);    // Turn P-FET OFF → no power to Pi
      digitalWrite(PIN_TIMER_LED, LOW);    // Timer LED off
      digitalWrite(PIN_HEARTBEAT_LED, LOW); // Heartbeat LED off

      // Check if ignition came back ON (user restarted car)
      if (ignitionState) {
        // Restore power and return to normal operation
        currentState = POWER_ON;
        digitalWrite(PIN_POWER_OUT, HIGH);
      }

      // Stay in SHUTDOWN state until ignition comes back ON
      break;
  }

  // Small delay to reduce CPU load (not critical for timing)
  delay(10);
}
