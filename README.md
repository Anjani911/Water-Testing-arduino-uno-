*Water Contamination Detector

A smart system that detects water contamination using light-based sensors and classifies the water as Safe or Unsafe, while identifying the type of impurity (e.g., turbidity, soap, alcohol).

🚀 Features
Uses photodiode (LDR) with white and UV LEDs to detect light absorption in water.

Calculates light drop percentages relative to reference (safe) readings.

Classifies water into types like:

✅ Clear (Safe)

⚠️ Turbid (Unsafe)

🧼 Soap/Reflective (Unsafe)

🍷 Alcohol (Unsafe)

   Coloured (unsafe)

Displays result on a 16x2 I2C LCD and also prints through Python serial interface.

Can be easily extended to train with more samples or turn into an ML-based classifier.



*Components Used

Arduino UNO
White LED
UV LED	
LM393/LDR Photodiode	
16x2 I2C LCD Module
Jumper Wires	
Breadboard
Test Tube/Cuvette


*How It Works

Reference Collection:

Run reference_collector.ino on Arduino with clean (safe) water.

Run collect_reference.py on Python.

It collects 5–10 readings and calculates average white and UV intensity.

Sample Testing:

Run sample_test.ino on Arduino.

Run compare_sample.py in Python terminal.

Arduino sends new readings → Python compares them to reference → Result sent back to Arduino → Shown on LCD.


*Sample Classification Logic

In Python (compare_sample.py):

python

white_drop = 100 * (1 - (w / ref_white))
uv_drop = 100 * (1 - (u / ref_uv))

*Requirements

Python 3.x

Arduino IDE


*How to Run

Upload Arduino code (sample_test.ino) via Arduino IDE.

Open Terminal:

python sampletest.py
Wait for LCD to display the result.


* Notes
Ensure Arduino COM port is correctly set in Python file.

Test tube should remain in the same position during testing for accuracy.

USB power stability matters (use powered port or external source if needed).






Water Contamination Detector/
├── arduino/
│   ├── sample_test.ino
│   └── reference_collector.ino
├── python/
│   ├── collect_reference.py
│   └── compare_sample.py
├── reference_readings.txt
└── README.md
