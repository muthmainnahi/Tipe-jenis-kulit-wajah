import json

class InferenceEngineCF:
    def __init__(self, rule_file="Rules.json"):
        """Load basis pengetahuan (rules) dari file JSON"""
        with open(rule_file, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)

    # ===============================
    # === FUNGSI PERHITUNGAN CF ===
    # ===============================

    def hitung_cf_sekuensial(self, cf_user, cf_pakar):
        """Rumus dasar CF sekuensial"""
        return cf_user * cf_pakar

    def cf_combine(self, cf1, cf2):
        """Gabungkan dua CF sesuai rumus MYCIN"""
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))

    # ===============================
    # === MESIN INFERENSI CF ===
    # ===============================

    def forward_chaining(self, cf_user_input):
        """Proses pencocokan rule dengan input user"""
        hasil_diagnosa = {}

        for rule in self.rules:
            nama_penyakit = rule["desc"]
            cf_rule = []

            for kondisi in rule["if"]:
                g = kondisi["gejala"]
                cf_pakar = kondisi["cf"]
                cf_user = cf_user_input.get(g, 0.0)

                if cf_user > 0:  # hanya gejala yang diisi user
                    cf_seq = self.hitung_cf_sekuensial(cf_user, cf_pakar)
                    cf_rule.append(cf_seq)

            if cf_rule:
                # Gabungkan semua CF dalam satu rule
                cf_total = cf_rule[0]
                for i in range(1, len(cf_rule)):
                    cf_total = self.cf_combine(cf_total, cf_rule[i])
                hasil_diagnosa[nama_penyakit] = cf_total * 100  # jadi persen

        return hasil_diagnosa

    # ===============================
    # === INPUT DARI USER ===
    # ===============================

    def input_gejala_user(self):
        """
        User memasukkan gejala dengan format:
        G1=0.8,G2=0.6,G4=1
        """
        print("=== SISTEM PAKAR DIAGNOSA ISPA ANAK ===")
        print("Masukkan minimal 3 gejala dan nilai CF user (0–1).")
        print("Contoh: G1=0.8,G2=0.6,G4=1")
        print("------------------------------------------------------")

        semua_gejala = sorted({g["gejala"] for r in self.rules for g in r["if"]})
        print("Daftar gejala yang tersedia:")
        print(", ".join(semua_gejala))
        print("------------------------------------------------------")

        while True:
            masukan = input("Masukkan gejala dan nilai CF: ").strip().upper()
            pasangan = [p.strip() for p in masukan.split(",") if "=" in p]

            cf_user_input = {}
            for item in pasangan:
                try:
                    kode, nilai = item.split("=")
                    kode = kode.strip()
                    nilai = float(nilai.strip())
                    if kode in semua_gejala and 0 <= nilai <= 1:
                        cf_user_input[kode] = nilai
                except ValueError:
                    continue

            if len(cf_user_input) < 3:
                print("❗ Masukkan minimal 3 gejala dengan nilai CF valid (0–1)\n")
            else:
                break

        return cf_user_input

    # ===============================
    # === PROSES DIAGNOSA ===
    # ===============================

    def diagnosa(self):
        cf_user_input = self.input_gejala_user()
        hasil = self.forward_chaining(cf_user_input)

        if not hasil:
            print("\n⚠️ Tidak ada penyakit yang cocok dengan gejala yang dimasukkan.")
            return

        print("\n=== HASIL DIAGNOSA ===")
        for p, cf in sorted(hasil.items(), key=lambda x: x[1], reverse=True):
            print(f"{p:<25} : {cf:.2f}%")

        penyakit_tertinggi = max(hasil, key=hasil.get)
        print(f"\n>> Diagnosis paling mungkin: {penyakit_tertinggi} ({hasil[penyakit_tertinggi]:.2f}%)")


# ===============================
# === EKSEKUSI LANGSUNG ===
# ===============================

if __name__ == "__main__":
    engine = InferenceEngineCF("Rules.json")
    engine.diagnosa()

