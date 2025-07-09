import tkinter as tk
from tkinter import ttk, messagebox
import serial
import time
import matplotlib.pyplot as plt

# --- Config ---
COM_PORT = "COM3"
BAUD_RATE = 9600
REF_WHITE = 600
REF_UV = 680

drop_ranges = [
    {"type": "RO Water", "white": (60.5, 61.6), "uv": (39.1, 41.0), "status": "Safe"},
    {"type": "Tap Water", "white": (62.3, 62.5), "uv": (39.26, 43.5), "status": "Unsafe"},
    {"type": "Soap/reflective surface", "white": (44.1, 45.3), "uv": (31.6, 32.9), "status": "Unsafe"},
    {"type": "Colored Drinks", "white": (55.3, 56.1), "uv": (31.7, 35.2), "status": "Safe (Should test)"},
    {"type": "Visible Soil", "white": (50.5, 52.3), "uv": (28.9, 31.6), "status": "Unsafe"},
    {"type": "organic contaminants", "white": (58.0, 58.8), "uv": (38.6, 39.7), "status": "Unsafe"},
]

def get_sample():
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=5)
        time.sleep(2)
        line = ser.readline().decode().strip()
        if "White:" in line and "UV:" in line:
            parts = line.replace("White:", "").replace("UV:", "").split(",")
            w = float(parts[0].strip())
            u = float(parts[1].strip())
            wd = round(100 * (1 - (w / REF_WHITE)), 2)
            ud = round(100 * (1 - (u / REF_UV)), 2)
            return w, u, wd, ud, ser
        messagebox.showerror("Error", "Invalid data from Arduino")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    return None, None, None, None, None

def classify_sample(wd, ud):
    for entry in drop_ranges:
        if entry["white"][0] <= wd <= entry["white"][1] and entry["uv"][0] <= ud <= entry["uv"][1]:
            return entry["type"], entry["status"]
    return "Unknown", "Unsafe"

def plot_graph(wd, ud):
    labels = ['White Drop %', 'UV Drop %']
    values = [wd, ud]
    plt.style.use("dark_background")
    plt.bar(labels, values, color=['#4FC3F7', '#CE93D8'])
    plt.ylim(0, 100)
    plt.title("Light Drop % Comparison")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

def run_real_test():
    result_label.config(text="Reading sample...")
    w, u, wd, ud, ser = get_sample()
    if w is None: return
    w_type, status = classify_sample(wd, ud)
    result_label.config(text=f"Result: {status}")
    type_label.config(text=f"Type: {w_type}")
    drop_label.config(text=f"White Drop: {wd:.2f}%, UV Drop: {ud:.2f}%")
    if ser:
        ser.write((w_type + "\n").encode())
        time.sleep(0.1)
        ser.write((status + "\n").encode())
        ser.close()
    plot_graph(wd, ud)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Water Contamination Detector")
root.geometry("440x350")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use('default')
style.configure('.', background="#1e1e1e", foreground="white", font=('Arial', 10))
style.configure('TButton', padding=6, relief="flat", background="#333", foreground="white")
style.map('TButton', background=[('active', '#444')])

frame = ttk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

ttk.Label(frame, text="💧 Water Contamination Test", font=('Arial', 16)).pack(pady=10)
result_label = ttk.Label(frame, text="Result:", font=('Arial', 12))
result_label.pack(pady=5)
type_label = ttk.Label(frame, text="Type:", font=('Arial', 12))
type_label.pack(pady=5)
drop_label = ttk.Label(frame, text="Drop Info:", font=('Arial', 10))
drop_label.pack(pady=5)

ttk.Button(frame, text="Run Real Test", command=run_real_test).pack(pady=20)

root.mainloop()
