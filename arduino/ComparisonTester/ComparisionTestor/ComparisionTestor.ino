#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int whiteLED = 6;
const int uvLED = 7;
const int sensorPin = A0;

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  pinMode(whiteLED, OUTPUT);
  pinMode(uvLED, OUTPUT);
  lcd.init();
  lcd.backlight();
  
  lcd.setCursor(0, 0);
  lcd.print("Waiting...");
}

void loop() {
  int white = 0;
  int uv = 0;

  // White LED reading
  digitalWrite(whiteLED, HIGH);
  delay(500); // LED warm-up
  white = analogRead(sensorPin);
  delay(5000);
  digitalWrite(whiteLED, LOW);
  delay(500);

  // UV LED reading
  digitalWrite(uvLED, HIGH);
  delay(500); // LED warm-up
  uv = analogRead(sensorPin);
  delay(5000);
  digitalWrite(uvLED, LOW);
  delay(500);

  // Send reading to Python
  Serial.print("White: ");
  Serial.print(white);
  Serial.print(", UV: ");
  Serial.println(uv);

  // Show interim message
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Waiting Result...");

  // Wait for Python result
  String result = "";
  unsigned long start = millis();
  while (millis() - start < 10000) {
    if (Serial.available()) {
      result = Serial.readStringUntil('\n');
      result.trim();
      break;
    }
  }

  // Display final result
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Water Status:");
  lcd.setCursor(0, 1);
  if (result.length() > 0) {
    lcd.print(result);
  } else {
    lcd.print("No response");
  }

  delay(10000);  // Keep result for 10 seconds

  // Reset screen for next reading
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Waiting...");
}
