import json
import tkinter as tk
from tkinter import ttk, messagebox

# === Fungsi CF ===
def cf_pararel(cf_user, cf_pakar):
    return cf_user * cf_pakar

def cf_combine(cf_list):
    if not cf_list:
        return 0
    result = cf_list[0]
    for cf in cf_list[1:]:
        result = result + cf * (1 - result)
    return result

# === Load Rules dari JSON ===
with open("rules_kulit_wajah_CF_20rules.json", "r") as f:
    rules = json.load(f)

# === Ambil semua gejala unik ===
all_symptoms = sorted({g for r in rules for g in r["Gejala"].keys()})

# === GUI Setup ===
root = tk.Tk()
root.title("💆‍♀️ Sistem Pakar Jenis Kulit Wajah")
root.geometry("800x600")
root.configure(bg="#f9fafb")

title = tk.Label(root, text="Sistem Pakar Identifikasi Jenis Kulit Wajah",
                 font=("Segoe UI", 16, "bold"), bg="#f9fafb", fg="#111827")
title.pack(pady=15)

desc = tk.Label(root, text="Pilih minimal 3 gejala dan masukkan tingkat keyakinan (0–1):",
                font=("Segoe UI", 11), bg="#f9fafb", fg="#374151")
desc.pack(pady=5)

# === Scroll area untuk gejala ===
frame_canvas = tk.Frame(root, bg="#f9fafb")
frame_canvas.pack(fill="both", expand=True, padx=15, pady=10)

canvas = tk.Canvas(frame_canvas, bg="#f9fafb", highlightthickness=0)
scroll_y = ttk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg="#f9fafb")

scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)
canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# === Checkbox & Entry CF ===
check_vars = {}
entry_vars = {}

for g in all_symptoms:
    f = tk.Frame(scroll_frame, bg="#f9fafb")
    f.pack(fill="x", pady=3)
    var = tk.BooleanVar()
    check = ttk.Checkbutton(f, text=g, variable=var)
    check.pack(side="left", padx=10)
    check_vars[g] = var

    lbl = tk.Label(f, text="CF (0–1):", bg="#f9fafb", fg="#374151")
    lbl.pack(side="left")
    val = tk.DoubleVar(value=0.5)
    entry = ttk.Entry(f, textvariable=val, width=5)
    entry.pack(side="left", padx=5)
    entry_vars[g] = val

# === Hasil Diagnosa ===
result_frame = tk.LabelFrame(root, text="Hasil Diagnosa", font=("Segoe UI", 11, "bold"),
                             bg="#f9fafb", fg="#111827", padx=10, pady=10)
result_frame.pack(fill="x", padx=20, pady=10)

txt_result = tk.Text(result_frame, height=8, wrap="word", font=("Consolas", 10))
txt_result.pack(fill="x")

# === Tombol Diagnosa ===
def diagnosa():
    user_cf = {g: entry_vars[g].get() for g in all_symptoms if check_vars[g].get()}

    if len(user_cf) < 3:
        messagebox.showwarning("Peringatan", "Masukkan minimal 3 gejala untuk diagnosa.")
        return

    results = []
    for rule in rules:
        cocok = set(rule["Gejala"].keys()) & set(user_cf.keys())
        if len(cocok) < 3:
            continue
        cf_temp = []
        for g in cocok:
            cf_pakar = rule["Gejala"][g]
            cf_user = user_cf[g]
            cf_p = cf_pararel(cf_user, cf_pakar)
            cf_temp.append(cf_p)
        cf_final = cf_combine(cf_temp)
        results.append({
            "RuleID": rule["RuleID"],
            "JenisKulit": rule["JenisKulit"],
            "CF_Final": round(cf_final, 4),
            "CF_Percent": round(cf_final * 100, 2),
            "Cocok": len(cocok)
        })

    if not results:
        txt_result.delete(1.0, tk.END)
        txt_result.insert(tk.END, "⚠️ Tidak ada tipe kulit dengan minimal 3 gejala cocok.")
        return

    results.sort(key=lambda x: x["CF_Final"], reverse=True)
    txt_result.delete(1.0, tk.END)
    best = results[0]

    output = f"Tipe Kulit: {best['JenisKulit']}\n"
    output += f"Tingkat Keyakinan: {best['CF_Percent']}%\n"
    output += f"Jumlah Gejala Cocok: {best['Cocok']}\n\n"
    output += "Rincian Rule yang Cocok:\n"
    for r in results:
        output += f"{r['RuleID']} → {r['JenisKulit']} ({r['CF_Percent']}%)\n"
    txt_result.insert(tk.END, output)

btn = ttk.Button(root, text="🔍 Diagnosa Sekarang", command=diagnosa)
btn.pack(pady=10)

root.mainloop()
