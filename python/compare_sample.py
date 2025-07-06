import serial
import time

# Reference values for clean water (collected earlier)
ref_white = 600  # example analog value before drop
ref_uv = 680     # example analog value before drop

# Drops will be calculated from these — update if needed
sample_count = 1

ser = serial.Serial("COM3", 9600)  # Change COM port if needed
time.sleep(2)

print("📡 Waiting for sample from Arduino...")

for _ in range(sample_count):
    line = ser.readline().decode().strip()
    if "White" in line and "UV" in line:
        print(f"🧪 Raw Sample: {line}")
        w = int(line.split("White:")[1].split(",")[0].strip())
        u = int(line.split("UV:")[1].strip())

        # Drop calculation
        white_drop = 100 * (1 - (w / ref_white))
        uv_drop = 100 * (1 - (u / ref_uv))

        print(f"📉 White Drop: {white_drop:.2f}%, UV Drop: {uv_drop:.2f}%")

        # Calibration logic
        if white_drop >= 45 and uv_drop >= 30:
            result = "Safe"
            water_type = "Clean Water"
        elif 15 <= white_drop <= 35:
            result = "Unsafe"
            water_type = "Light Turbidity"
        elif white_drop < 10 and uv_drop < 25:
            result = "Unsafe"
            water_type = "High Turbidity"
        else:
            result = "Unsafe"
            water_type = "Unidentified Liquid"

        print(f"\n🔍 Type: {water_type}")
        print(f"✅ Final Result: {result}")

        ser.write((result + "\n").encode())
        break

ser.close()
