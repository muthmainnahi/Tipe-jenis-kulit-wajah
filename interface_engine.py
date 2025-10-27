"""
Inference Engine Sistem Pakar Jenis Kulit Wajah
Metode: Forward Chaining + Certainty Factor (CF)
Versi: Hanya menampilkan tipe kulit (rule) dengan minimal 3 gejala cocok
"""

import json

# --- Fungsi CF ---
def cf_pararel(cf_user, cf_pakar):
    return cf_user * cf_pakar

def cf_combine(cf_list):
    if not cf_list:
        return 0
    result = cf_list[0]
    for cf in cf_list[1:]:
        result = result + cf * (1 - result)
    return result


# --- Baca file JSON (rules dari jurnal) ---
with open("rules_kulit_wajah_CF.json", "r") as f:
    rules = json.load(f)

# --- Kumpulkan semua kode gejala dari rules ---
all_symptoms = sorted({g for rule in rules for g in rule["Gejala"].keys()})

print("=== SISTEM PAKAR IDENTIFIKASI JENIS KULIT WAJAH ===")
print("Masukkan daftar gejala yang Anda alami, pisahkan dengan koma (,)")
print("Contoh: G5,G6,G11,G15")
print("Minimal 3 gejala agar sistem dapat memberikan hasil.\n")

# --- Input daftar gejala ---
input_str = input("Masukkan kode gejala: ").strip().upper()
selected_symptoms = [x.strip() for x in input_str.split(",") if x.strip()]

# Validasi jumlah gejala
if len(selected_symptoms) < 3:
    print("\n⚠️ Anda harus memasukkan minimal 3 gejala untuk melakukan diagnosa.")
    exit()

# Validasi apakah gejala terdaftar
invalid = [g for g in selected_symptoms if g not in all_symptoms]
if invalid:
    print(f"\n❌ Gejala berikut tidak ditemukan di basis pengetahuan: {', '.join(invalid)}")
    print("Periksa kembali kode gejala yang Anda masukkan.")
    exit()

# --- Input nilai CF untuk setiap gejala yang dimasukkan ---
print("\nMasukkan tingkat keyakinan Anda untuk masing-masing gejala (0–1)")
user_cf = {}
for g in selected_symptoms:
    try:
        val = float(input(f"Nilai CF untuk {g}: "))
        if 0 <= val <= 1:
            user_cf[g] = val
        else:
            print("⚠️ Nilai CF harus antara 0 dan 1, diabaikan.")
    except ValueError:
        print("⚠️ Input tidak valid, nilai CF dianggap 0.")
        user_cf[g] = 0

# --- Proses inferensi ---
results = []
for rule in rules:
    gejala_dict = rule["Gejala"]
    cocok = set(gejala_dict.keys()) & set(user_cf.keys())
    # Lewati rule yang gejala cocoknya kurang dari 3
    if len(cocok) < 3:
        continue

    cf_temp = []
    detail = []
    for g in cocok:
        cf_pakar = gejala_dict[g]
        cf_user = user_cf.get(g, 0)
        cf_p = cf_pararel(cf_user, cf_pakar)
        detail.append((g, cf_pakar, cf_user, cf_p))
        if cf_p > 0:
            cf_temp.append(cf_p)
    cf_final = cf_combine(cf_temp)
    results.append({
        "RuleID": rule["RuleID"],
        "Diagnosis": rule["JenisKulit"],
        "CF_Final": round(cf_final, 4),
        "CF_Percent": round(cf_final * 100, 2),
        "MatchedSymptoms": len(cocok),
        "Details": detail
    })

# --- Jika tidak ada rule dengan ≥3 gejala cocok ---
if not results:
    print("\n Tidak ada tipe kulit yang memiliki minimal 3 gejala cocok.")
    print("Silakan tambahkan lebih banyak gejala untuk hasil lebih akurat.")
    exit()

# --- Urutkan hasil berdasarkan CF tertinggi ---
results.sort(key=lambda x: x["CF_Final"], reverse=True)

# --- Tampilkan hasil ---
print("\n=== HASIL DIAGNOSA (Hanya Rule dengan ≥3 Gejala Cocok) ===\n")
for r in results:
    print(f"{r['RuleID']} → {r['Diagnosis']}")
    print(f"  CF Akhir: {r['CF_Final']} ({r['CF_Percent']}%) — "
          f"{r['MatchedSymptoms']} gejala cocok")
    for d in r["Details"]:
        print(f"   - {d[0]}: CF_pakar={d[1]}, CF_user={d[2]} → CF_pararel={d[3]}")
    print()

print(f" Diagnosis paling mungkin: {results[0]['Diagnosis']} "
      f"dengan tingkat keyakinan {results[0]['CF_Percent']}%")
