import serial # type: ignore
import time

# Set your correct port and baudrate
PORT = "COM3"   # ← Change if needed
BAUD = 9600

# Open serial connection
ser = serial.Serial(PORT, BAUD)
time.sleep(2)  # Allow Arduino to reset

print("📥 Collecting 5 readings from Arduino...")

readings = []

while len(readings) < 5:
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        if ',' in line:
            try:
                white, uv = map(int, line.split(','))
                readings.append((white, uv))
                print(f"Reading {len(readings)}: White={white}, UV={uv}")
            except ValueError:
                continue

ser.close()

# Save readings to file
with open("reference_readings.txt", "w") as f:
    for w, u in readings:
        f.write(f"{w},{u}\n")

# Calculate average
avg_white = sum(w for w, _ in readings) / len(readings)
avg_uv = sum(u for _, u in readings) / len(readings)

print(f"\n✅ Saved to reference_readings.txt")
print(f"📌 Reference → White Avg: {avg_white:.1f} UV Avg: {avg_uv:.1f}")
