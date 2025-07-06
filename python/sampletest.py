import serial
import time

# Reference values for clean (safe) water
ref_white = 600 
ref_uv = 680  

# Classification ranges (drop %)
drop_ranges = [
    {
        "type": "RO Water",
        "white": (60.5, 61.6),  # Your exact observed white % drop
        "uv": (39.1, 41.0),
        "status": "Safe"
    },
    {
        "type": "Tap Water",
        "white": (62.3, 62.5),
        "uv": (39.26, 43.5),
        "status": "Unsafe" 
    },
    {
        "type": "Shampoo/Soap",
        "white": (44.1, 45.3),
        "uv": (31.6, 32.9),
        "status": "Unsafe"
    },
    {
        "type": "colored drinks",
        "white": (55.3, 56.1),
        "uv": (31.7, 35.2),
        "status": "safe"
    },
    {
        "type": "Visible Soil (Lightly Turbid)",
        "white": (50.5, 52.3),
        "uv": (28.9, 31.6),
        "status": "Unsafe"
    },
    {
        "type": "Alcohol",
        "white": (58.0, 58.8),
        "uv": (38.6, 39.7),
        "status": "Unsafe"
    }
]


# Start serial
ser = serial.Serial("COM3", 9600, timeout=5)
time.sleep(2)
print("📡 Waiting for sample from Arduino...")

try:
    line = ser.readline().decode().strip()
    print(f"🧪 Raw Reading → {line}")

    if "White:" in line and "UV:" in line:
        parts = line.replace("White:", "").replace("UV:", "").split(",")
        w = float(parts[0].strip())
        u = float(parts[1].strip())

        white_drop = 100 * (1 - (w / ref_white))
        uv_drop = 100 * (1 - (u / ref_uv))

        white_drop = round(white_drop, 2)
        uv_drop = round(uv_drop, 2)

        print(f"\n📉 White Drop: {white_drop}%, UV Drop: {uv_drop}%")

        matched = False
        for entry in drop_ranges:
            w_range = entry["white"]
            u_range = entry["uv"]
            if w_range[0] <= white_drop <= w_range[1] and u_range[0] <= uv_drop <= u_range[1]:
                print(f"🔍 Type: {entry['type']}")
                print(f"✅ Final Result: {entry['status']}")
                ser.write((entry['type'] + "\n").encode())
                time.sleep(0.1)
                ser.write((entry['status'] + "\n").encode())
                matched = True
                break

        if not matched:
            print("🔍 Type: Unknown")
            print("❌ Final Result: Unsafe")
            ser.write("Unknown Liquid\n".encode())
            time.sleep(0.1)
            ser.write("Unsafe\n".encode())

    else:
        print("⚠️ Invalid data received.")

except Exception as e:
    print("❌ Error:", e)

ser.close()
