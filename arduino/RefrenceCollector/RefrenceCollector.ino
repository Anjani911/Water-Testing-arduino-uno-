const int whiteLED = 6;
const int uvLED = 7;
const int sensorPin = A0;

void setup() {
  Serial.begin(9600);
  pinMode(whiteLED, OUTPUT);
  pinMode(uvLED, OUTPUT);
  Serial.println("📡 Sending Sample Reading...");
}

int readAverageSensor(int ledPin) {
  int sum = 0;
  digitalWrite(ledPin, HIGH);
  delay(500);  // LED warm-up
  for (int i = 0; i < 5; i++) {
    sum += analogRead(sensorPin);
    delay(200);  // Time between reads
  }
  digitalWrite(ledPin, LOW);
  return sum / 5;
}

void loop() {
  int whiteReading = readAverageSensor(whiteLED);
  delay(300);
  int uvReading = readAverageSensor(uvLED);

  Serial.print(whiteReading);
  Serial.print(",");
  Serial.println(uvReading);

  // Prevent sending more readings automatically
  while (true);
}
