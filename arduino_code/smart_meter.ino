#include <WiFi.h>


// WiFi Configuration Profile
const char* ssid = "YOUR_HOME_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Pin Architecture Configuration
const int CURRENT_PIN = 34; // ACS712 Output connected to Analog PIN 34
const int RELAY_PIN = 26;   // Safety Relay Gate Pin
const int BUZZER_PIN = 27;  // Local Warning Siren Pin

// Calibration Constants
const float V_RMS = 230.0; 
const float SENSITIVITY = 0.185; // 185mV/A sensitivity layout
const float OVERLOAD_THRESHOLD = 2500.0;

unsigned long previousMillis = 0;
const long interval = 2000; // Telemetry cycle interval (2 seconds)

void setup() {
    Serial.begin(115200);
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, HIGH); // Complete breaker connection by default
    
    WiFi.begin(ssid, password);
    int wifiAttempts = 0;
    while (WiFi.status() != WL_CONNECTED && wifiAttempts < 20) {
        delay(500);
        Serial.print(".");
        wifiAttempts++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n📡 Node Matrix Connected to Local Access Point.");
    } else {
        Serial.println("\n⚠️ WiFi Connection Failed. Operating in Standalone Mode.");
    }
}

void loop() {
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;
        
        // Edge Sampling Conversion Logic
        float rawCurrentAnalog = analogRead(CURRENT_PIN);
        float measuredCurrent = (rawCurrentAnalog * (3.3 / 4095.0) - 1.65) / SENSITIVITY;
        if (measuredCurrent < 0.08) measuredCurrent = 0.0; // Dynamic current threshold noise filter

        float powerWatts = V_RMS * measuredCurrent;
        Serial.printf("⚡ Telemetry Core Node -> Current: %.2fA | Power: %.2fW\n", measuredCurrent, powerWatts);
        
        // Automation Interlock Core Safety Logic
        if (powerWatts > OVERLOAD_THRESHOLD) {
            digitalWrite(RELAY_PIN, LOW);   // Instantly trip the breaker open
            digitalWrite(BUZZER_PIN, HIGH); // Activate local audio alert warning
            Serial.println("🚨 AUTOMATION ALERT: BREAK LIMIT REACHED! CIRCUIT OVERLOAD SHUTDOWN EXECUTED.");
        } else {
            digitalWrite(BUZZER_PIN, LOW);
        }
    }
}
