import tkinter as tk
from tkinter import ttk, messagebox
import serial
import time
import matplotlib.pyplot as plt

# --------------- CONFIG ----------------
COM_PORT = "COM3"
BAUD_RATE = 9600
REF_WHITE = 600
REF_UV = 680

# Predefined calibration ranges (based on % drop)
drop_ranges = [
    {
        "type": "RO Water",
        "white": (60.5, 61.6),
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
        "type": "Colored Drinks",
        "white": (55.3, 56.1),
        "uv": (31.7, 35.2),
        "status": "Safe (Should test)"
    },
    {
        "type": "Visible Soil",
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

# --------------- FUNCTIONS ----------------
def get_sample():
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=5)
        time.sleep(2)
        ser.flushInput()
        line = ser.readline().decode().strip()
        print("Raw Reading:", line)

        if "White:" in line and "UV:" in line:
            parts = line.replace("White:", "").replace("UV:", "").split(",")
            w = float(parts[0].strip())
            u = float(parts[1].strip())
            white_drop = round(100 * (1 - (w / REF_WHITE)), 2)
            uv_drop = round(100 * (1 - (u / REF_UV)), 2)
            return w, u, white_drop, uv_drop, ser
        else:
            messagebox.showerror("Error", "Invalid data format from Arduino")
            return None, None, None, None, None
    except Exception as e:
        messagebox.showerror("Serial Error", str(e))
        return None, None, None, None, None

def classify_sample(white_drop, uv_drop):
    for entry in drop_ranges:
        if (entry["white"][0] <= white_drop <= entry["white"][1] and
            entry["uv"][0] <= uv_drop <= entry["uv"][1]):
            return entry["type"], entry["status"]
    return "Unknown", "Unsafe"

def plot_graph(white_drop, uv_drop):
    labels = ['White Drop %', 'UV Drop %']
    values = [white_drop, uv_drop]
    colors = ['#4FC3F7', '#CE93D8']

    plt.style.use("dark_background")
    plt.bar(labels, values, color=colors)
    plt.ylim(0, 100)
    plt.title("Light Drop % Comparison")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.ylabel("% Drop")
    plt.show()

def run_real_test():
    result_label.config(text="Reading sample...")
    w, u, w_drop, u_drop, ser = get_sample()
    if w is None:
        return

    water_type, status = classify_sample(w_drop, u_drop)
    result_label.config(text=f"Result: {status}")
    type_label.config(text=f"Type: {water_type}")
    drop_label.config(text=f"White Drop: {w_drop:.2f}%, UV Drop: {u_drop:.2f}%")

    if ser:
        ser.write((water_type + "\n").encode())
        time.sleep(0.1)
        ser.write((status + "\n").encode())
        ser.close()

    plot_graph(w_drop, u_drop)

# --------------- GUI ----------------
root = tk.Tk()
root.title("Water Contamination Detector")
root.geometry("420x340")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use('default')
style.configure('.', background="#1e1e1e", foreground="white", font=('Arial', 10))
style.configure('TButton', padding=6, relief="flat", background="#333333", foreground="white")
style.map('TButton', background=[('active', '#555555')])

frame = ttk.Frame(root, padding=10)
frame.pack(fill='both', expand=True)

title = ttk.Label(frame, text="💧 Water Contamination Test", font=('Arial', 16, 'bold'))
title.pack(pady=10)

result_label = ttk.Label(frame, text="Result: ", font=('Arial', 12))
result_label.pack(pady=5)

type_label = ttk.Label(frame, text="Type: ", font=('Arial', 12))
type_label.pack(pady=5)

drop_label = ttk.Label(frame, text="Drop% Info:", font=('Arial', 10))
drop_label.pack(pady=5)

run_button = ttk.Button(frame, text="Run Real Test", command=run_real_test)
run_button.pack(pady=15)

root.mainloop()
