"""
diagnosa_ispa_cute_v6_merged_final.py
Fungsionalitas v5 (Data ISPA, CF Math, Reset, Info Popup)
Tampilan v6 (Tema Pink, Font Comic Sans, Layout)
Perbaikan: Dropdown CF kini dapat dipilih.
DIHAPUS: Fungsionalitas "Simpan".
"""

import tkinter as tk
from tkinter import ttk, messagebox
# import datetime  # Tidak lagi diperlukan
# import filedialog # Tidak lagi diperlukan

# ---------------- DATA (dari v5) ----------------
RULES = [
    {"id": "R1",  "if": [("G1",0.6),("G2",0.8),("G4",0.8),("G7",0.4),("G11",0.6),("G12",0.6),("G17",0.6)], "desc":"Common cold"},
    {"id": "R2",  "if": [("G1",0.8),("G2",0.4),("G3",0.6),("G4",0.6),("G6",0.8),("G8",0.4)], "desc":"Bronkiolitis"},
    {"id": "R3",  "if": [("G1",0.8),("G3",0.8),("G4",0.4),("G6",0.6)], "desc":"Bronkitis"},
    {"id": "R4",  "if": [("G2",0.8),("G3",0.6),("G8",0.8),("G9",0.6)], "desc":"Bronkopneumonia"},
    {"id": "R5",  "if": [("G1",0.8),("G2",0.4),("G4",0.6),("G5",0.6),("G10",0.6),("G12",0.8),("G18",0.6)], "desc":"Laringitis"},
    {"id": "R6",  "if": [("G1",0.8),("G4",0.6),("G5",0.6),("G10",0.8),("G11",0.6)], "desc":"Pertusis Kataralis"},
    {"id": "R7",  "if": [("G1",0.8),("G6",0.8),("G21",0.4),("G23",0.8)], "desc":"Pertusis Spasmodik"},
    {"id": "R8",  "if": [("G2",0.8),("G3",0.6),("G5",0.4),("G7",0.6),("G8",0.8),("G14",0.4),("G19",0.4)], "desc":"Pneumonia"},
    {"id": "R9",  "if": [("G1",0.8),("G2",0.6),("G7",0.6),("G10",0.6),("G15",0.8),("G16",0.6)], "desc":"Sinusitis"},
    {"id": "R10", "if": [("G1",0.6),("G2",0.8),("G3",0.8),("G5",0.4),("G6",0.6),("G7",0.4),("G9",0.4),("G13",0.6),("G14",0.4),("G18",0.4),("G20",0.4)], "desc":"Flu Burung"},
    {"id": "R10b","if": [("G1",0.8),("G2",0.8),("G3",0.8),("G6",0.6),("G9",0.4),("G13",0.8),("G22",0.4)], "desc":"Tuberculosis"},
]

GEJALA_NAMES = {
    "G1":"Batuk","G2":"Demam","G3":"Sesak Nafas","G4":"Pilek","G5":"Sakit Tenggorokan",
    "G6":"Napas Cepat","G7":"Bersin","G8":"Suara Napas Abnormal","G9":"Napas Berat",
    "G10":"Mengi","G11":"Nyeri Dada","G12":"Dahak","G13":"Mual","G14":"Nyeri Otot",
    "G15":"Nyeri Kepala","G16":"Hidung Tersumbat","G17":"Kelelahan","G18":"Batuk Berdahak",
    "G19":"Batuk Kronis","G20":"Lemas","G21":"Kejang","G22":"Keringat Malam","G23":"Muntah"
}

ALL_GEJALA = [f"G{i}" for i in range(1, 24)]

CF_LABELS = ["Tidak", "Tidak tahu", "Sedikit yakin", "Cukup yakin", "Yakin", "Sangat yakin"]
CF_MAP = {"Tidak":0.0, "Tidak tahu":0.2, "Sedikit yakin":0.4, "Cukup yakin":0.6, "Yakin":0.8, "Sangat yakin":1.0}

DISEASE_INFO = {
    "Common cold":{"icon":"🤧","desc":"Infeksi saluran pernapasan atas, biasanya ringan.","tindakan":"Istirahat & cairan.","pencegahan":"Cuci tangan."},
    "Bronkiolitis":{"icon":"🫁","desc":"Infeksi bronkiolus pada anak.","tindakan":"Monitoring & hidrasi.","pencegahan":"Hindari asap rokok."},
    "Bronkitis":{"icon":"💨","desc":"Peradangan bronkus.","tindakan":"Istirahat & inhalasi bila perlu.","pencegahan":"Hindari polusi asap."},
    "Bronkopneumonia":{"icon":"⚕️","desc":"Infeksi paru; perlu evaluasi.","tindakan":"Periksa dokter; mungkin antibiotik.","pencegahan":"Vaksinasi & kebersihan."},
    "Laringitis":{"icon":"🗣️","desc":"Peradangan laring.","tindakan":"Istirahat suara & cairan hangat.","pencegahan":"Hindari berteriak."},
    "Pertusis Kataralis":{"icon":"🤒","desc":"Tahap awal batuk rejan.","tindakan":"Konsultasi dokter.","pencegahan":"Vaksin DTP."},
    "Pertusis Spasmodik":{"icon":"😮‍💨","desc":"Batuk rejan paroksismal.","tindakan":"Perawatan medis.","pencegahan":"Vaksinasi lengkap."},
    "Pneumonia":{"icon":"🩺","desc":"Infeksi paru; bisa serius.","tindakan":"Segera periksa dokter.","pencegahan":"Vaksinasi & cuci tangan."},
    "Sinusitis":{"icon":"🌡️","desc":"Peradangan sinus.","tindakan":"Dekongestan & evaluasi bila lama.","pencegahan":"Hindari alergen."},
    "Flu Burung":{"icon":"🐔","desc":"Infeksi influenza tipe tertentu.","tindakan":"Segera ke fasilitas kesehatan.","pencegahan":"Hindari kontak unggas sakit."},
    "Tuberculosis":{"icon":"🧾","desc":"Infeksi Mycobacterium tuberculosis.","tindakan":"Diagnosis & pengobatan jangka panjang.","pencegahan":"Vaksin BCG & ventilasi baik."}
}

# ---------------- CF math (dari v5) ----------------
def hitung_cf_sekuensial(cf_user, cf_pakar): return cf_user * cf_pakar
def cf_combine(a, b):
    if a >= 0 and b >= 0: return a + b * (1 - a)
    if a < 0 and b < 0: return a + b * (1 + a)
    denom = 1 - min(abs(a), abs(b))
    if denom == 0: return 0.0
    return (a + b) / denom

def forward_chaining(cf_user_input):
    hasil = {}
    for rule in RULES:
        nama = rule["desc"]
        cf_list = []
        for gejala, cf_pakar in rule["if"]:
            cf_user = cf_user_input.get(gejala, 0.0)
            if cf_user > 0:
                cf_seq = hitung_cf_sekuensial(cf_user, cf_pakar)
                cf_list.append(cf_seq)
        if cf_list:
            total = cf_list[0]
            for v in cf_list[1:]:
                total = cf_combine(total, v)
            hasil[nama] = total * 100
    return hasil

# ---------------- UI (Tema v6, Fungsionalitas v5) ----------------

class CuteCFv6(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cute CF v6 💕 Diagnosa ISPA Anak")
        self.geometry("900x650") # Sedikit lebih tinggi untuk tombol
        self.minsize(900, 600)
        self.configure(bg="#FFEAF4")

        self.row_vars = {}
        self._last_results = {}
        
        self._style_setup()
        self._build_ui()
        self._show_results({}) # Tampilkan placeholder awal

    def _style_setup(self):
        # Style dari v5, disesuaikan dengan warna v6
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        # Progressbar styles
        style.configure("Red.Horizontal.TProgressbar", troughcolor="#FFF0F0", background="#ff4d4d", thickness=12) # Merah v6
        style.configure("Pink.Horizontal.TProgressbar", troughcolor="#FFF0F4", background="#ffb6c1", thickness=12) # Pink v6
        style.configure("Blue.Horizontal.TProgressbar", troughcolor="#F0FCFF", background="#007bff", thickness=12) # Biru v6
        
        # Combobox style dari v5
        try:
            style.configure("Small.TCombobox", font=("Segoe UI", 9))
        except Exception:
            pass

    def _build_ui(self):
        # Frame utama (layout v6)
        left_frame = tk.Frame(self, bg="#FFF7FA")
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        right_frame = tk.Frame(self, bg="#FFF7FA")
        right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Judul (style v6, teks v5)
        tk.Label(
            left_frame, text="🩺 Pilih Gejala Pernafasan Anak",
            font=("Comic Sans MS", 14, "bold"), bg="#FFF7FA", fg="#ff5f9e"
        ).pack(pady=(10,5))
        
        tk.Label(
            left_frame, text="Centang gejala, lalu pilih tingkat keyakinan (CF). Minimal 3 gejala.",
            font=("Segoe UI", 9), bg="#FFF7FA", fg="#6b6b6b"
        ).pack(pady=(0,10))


        # Scroll area (layout v6)
        canvas = tk.Canvas(left_frame, bg="#FFF7FA", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#FFF7FA")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Gejala list (Data v5, Fungsionalitas row v5, Tampilan row v6)
        for g in ALL_GEJALA:
            nama = GEJALA_NAMES.get(g, '')
            
            # Wrapper frame untuk ganti bg (logika v5, warna v6)
            wrapper = tk.Frame(self.scrollable_frame, bg="#d8d8d8")
            wrapper.pack(fill="x", pady=4, padx=10)

            chk_var = tk.IntVar(value=0)
            sel_var = tk.StringVar(value=CF_LABELS[0]) # Default "Tidak"

            # 1. Definisikan widget dulu
            chk = tk.Checkbutton(
                wrapper, text=f"{g} — {nama}", variable=chk_var,
                onvalue=True, offvalue=False,
                bg="#d8d8d8", activebackground="#FFEAF4",
                font=("Segoe UI", 10), anchor="w"
            )
            
            cb = ttk.Combobox(
                wrapper, textvariable=sel_var,
                values=CF_LABELS,
                state="disabled", width=14, justify="center",
                style="Small.TCombobox"
            )

            # 2. Definisikan fungsi command
            def on_chk_change(var=chk_var, s_var=sel_var, c=cb, w=wrapper, c_btn=chk):
                enabled = var.get() 
                new_bg = "#ffffff" if enabled else "#d8d8d8"
                
                w.configure(bg=new_bg)
                c_btn.configure(bg=new_bg)
                
                if enabled:
                    c.configure(state="readonly")
                    if s_var.get() == CF_LABELS[0]: 
                        s_var.set(CF_LABELS[1]) 
                else:
                    c.configure(state="disabled")
                    s_var.set(CF_LABELS[0]) 

            # 3. Atur command untuk checkbutton
            chk.configure(command=on_chk_change)
            
            # 4. Tampilkan widget
            chk.pack(side="left", padx=5, pady=2, fill="x", expand=True)
            cb.pack(side="right", padx=10, pady=5)
            
            # 5. Inisialisasi status
            on_chk_change() 
            
            # Simpan referensi widget (logika v5)
            self.row_vars[g] = (chk_var, sel_var, cb, wrapper, chk)


        # Tombol (Fungsionalitas v5, Tampilan v6)
        btn_area = tk.Frame(left_frame, bg="#FFF7FA")
        btn_area.pack(fill="x", pady=15, padx=10)

        diagnose_btn = tk.Button(
            btn_area, text="💖 Diagnosa",
            font=("Comic Sans MS", 12, "bold"), bg="#ffb6c1", fg="white",
            relief="flat", padx=10, pady=5, command=self.on_diagnose
        )
        diagnose_btn.pack(side="left", fill="x", expand=True, padx=4)

        reset_btn = tk.Button(
            btn_area, text="♻️ Reset",
            font=("Comic Sans MS", 10), bg="#ffffff", fg="#ff5f9e",
            relief="flat", padx=10, pady=5, command=self.on_reset
        )
        reset_btn.pack(side="left", fill="x", expand=True, padx=4)

        # Tombol Simpan (💾) DIHAPUS
        
        info_btn = tk.Button(
            btn_area, text="❓ Info CF",
            font=("Comic Sans MS", 10), bg="#ffffff", fg="#6b6b6b",
            relief="flat", padx=10, pady=5, command=self._show_cf_info
        )
        info_btn.pack(side="left", fill="x", expand=True, padx=4)


        # Area hasil diagnosa (Judul v6)
        tk.Label(
            right_frame, text="📋 Hasil Diagnosa (Top 5)",
            font=("Comic Sans MS", 14, "bold"), bg="#FFF7FA", fg="#007bff"
        ).pack(pady=10)

        # Area scroll hasil (Logika v5, Tampilan v6)
        res_card = tk.Frame(right_frame, bg="#ffffff")
        res_card.pack(fill="both", expand=True, padx=6, pady=(8,6))
        
        res_canvas = tk.Canvas(res_card, bg="#ffffff", highlightthickness=0)
        res_canvas.pack(side="left", fill="both", expand=True)
        
        res_sb = ttk.Scrollbar(res_card, orient="vertical", command=res_canvas.yview)
        res_sb.pack(side="right", fill="y")
        
        res_canvas.configure(yscrollcommand=res_sb.set)
        self.res_inner = tk.Frame(res_canvas, bg="#ffffff") 
        res_canvas.create_window((0,0), window=self.res_inner, anchor="nw")
        self.res_inner.bind("<Configure>", lambda e: res_canvas.configure(scrollregion=res_canvas.bbox("all")))
        self.res_canvas = res_canvas 


        # Ringkasan diagnosa di kanan bawah (dari v6)
        summary_card = tk.Frame(right_frame, bg="#FFF7FA", bd=0)
        summary_card.pack(fill="x", pady=(10, 0), side="bottom", anchor="s")

        summary_text = (
            "Menampilkan 5 penyakit teratas berdasarkan tingkat keyakinan Anda.\n"
            "Klik ikon/nama penyakit untuk melihat informasi lebih lanjut."
        )
        self.summary_label = tk.Label(
            summary_card,
            text=summary_text,
            font=("Segoe UI", 9, "italic"),
            bg="#FFF7FA",
            fg="#6b6b6b",
            wraplength=360,
            justify="left"
        )
        self.summary_label.pack(anchor="w", padx=10, pady=5)

    # --- Fungsionalitas (Metode disalin dari v5) ---

    def _show_cf_info(self):
        messagebox.showinfo("Apa itu CF (Certainty Factor)?",
            "CF (Certainty Factor) mengukur tingkat keyakinan terhadap suatu gejala (0.00–1.00).\n\n"
            "Pilihan:\n - Tidak -> 0.00\n - Tidak tahu -> 0.20\n - Sedikit yakin -> 0.40\n - Cukup yakin -> 0.60\n - Yakin -> 0.80\n - Sangat yakin -> 1.00\n\n"
            "CF user dikalikan CF pakar, lalu digabung (MYCIN-like). Hasil ditampilkan persen.\n\n"
            "Catatan: ini alat bantu pembelajaran, bukan pengganti diagnosa medis."
        )

    def on_diagnose(self):
        user_cf = {}
        # Baca nilai dari row_vars (logika v5)
        for g, (chk_var, sel_var, cb, wrapper, chk) in self.row_vars.items():
            if chk_var.get():
                val = CF_MAP.get(sel_var.get(), 0.0)
                if val > 0:
                    user_cf[g] = val
        
        if len(user_cf) < 3: # Validasi v5
            messagebox.showwarning("Peringatan", "Centang minimal 3 gejala dan pilih tingkat keyakinan (CF) selain 'Tidak'.")
            return
            
        hasil = forward_chaining(user_cf)
        items = sorted(hasil.items(), key=lambda x: x[1], reverse=True)[:5]
        self._last_results = dict(items)
        self._show_results(self._last_results)

    def _show_results(self, hasil_dict):
        # Hapus hasil lama
        for c in self.res_inner.winfo_children():
            c.destroy()
            
        if not hasil_dict:
            # Tampilkan placeholder (style v6)
            ph = tk.Frame(self.res_inner, bg="#ffffff")
            ph.pack(fill="both", expand=True)
            tk.Label(ph, text="🧸 Silakan mulai diagnosa...", bg="#ffffff", font=("Comic Sans MS", 12), fg="#6b6b6b").pack(pady=40)
            return

        first = True
        # Tampilkan hasil (logika v5)
        for name, val in hasil_dict.items():
            info = DISEASE_INFO.get(name, {})
            icon = info.get("icon", "❓")
            
            # Card untuk setiap hasil (style v5, bg v6)
            card = tk.Frame(self.res_inner, bg="#ffffff", padx=6, pady=6)
            card.pack(fill="x", padx=10, pady=6)

            icon_lbl = tk.Label(card, text=icon, font=("Segoe UI Emoji", 20), bg="#ffffff", cursor="hand2")
            icon_lbl.pack(side="left", padx=(0,10))
            icon_lbl.bind("<Button-1>", lambda e, nm=name: self._open_info_popup(nm))

            # Frame untuk teks dan progress bar
            text_frame = tk.Frame(card, bg="#ffffff")
            text_frame.pack(fill="x", expand=True, side="left")

            lbl = tk.Label(text_frame, text=name, font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2b2b2b", cursor="hand2")
            lbl.pack(anchor="w")
            lbl.bind("<Button-1>", lambda e, nm=name: self._open_info_popup(nm))

            # Progress bar (style v5/v6)
            if first:
                pb = ttk.Progressbar(text_frame, style="Red.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
                lbl.configure(font=("Segoe UI", 12, "bold"), fg="#ff4d4d") # Top-1 merah
            else:
                pb = ttk.Progressbar(text_frame, style="Pink.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
            
            pb.pack(fill="x", pady=(4,0))
            pb['value'] = max(0, min(100, val))
            
            tk.Label(card, text=f"{val:.2f}%", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#444").pack(side="right", padx=(10,0))
            
            first = False
            
        self.res_canvas.yview_moveto(0) # Scroll ke atas

    def _open_info_popup(self, disease_name):
        # Popup detail (logika v5, style v6)
        info = DISEASE_INFO.get(disease_name)
        if not info:
            messagebox.showinfo(disease_name, "Informasi tidak tersedia.")
            return
            
        win = tk.Toplevel(self)
        win.title(f"ℹ️ Info: {disease_name}")
        win.geometry("450x300")
        win.configure(bg="#FFF7FA") # Latar belakang pink
        win.resizable(False, False)

        header = tk.Frame(win, bg="#FFF7FA")
        header.pack(fill="x", padx=16, pady=(16,8))
        
        tk.Label(header, text=info.get("icon","❓"), font=("Segoe UI Emoji", 32), bg="#FFF7FA").pack(side="left", padx=(0,12))
        tk.Label(header, text=disease_name, font=("Comic Sans MS", 16, "bold"), bg="#FFF7FA", fg="#ff5f9e").pack(side="left", anchor="s", pady=(0,4))

        body = tk.Text(win, wrap="word", bg="#ffffff", bd=0, font=("Segoe UI", 10), relief="flat", highlightthickness=0)
        body.pack(fill="both", expand=True, padx=16, pady=(0,16))
        
        text = f"Deskripsi:\n{info.get('desc','-')}\n\n"
        text += f"Tindakan / Tindak lanjut:\n{info.get('tindakan','-')}\n\n"
        text += f"Pencegahan:\n{info.get('pencegahan','-')}"
        
        body.insert("1.0", text)
        
        # Tambahkan tag untuk styling (opsional tapi bagus)
        body.tag_configure("bold", font=("Segoe UI", 10, "bold"), spacing1=5)
        body.tag_add("bold", "1.0", "1.9")      # "Deskripsi:"
        body.tag_add("bold", "3.0", "3.26")     # "Tindakan / Tindak lanjut:"
        body.tag_add("bold", "5.0", "5.10")     # "Pencegahan:"
        
        body.configure(state="disabled")

    def on_reset(self):
        # Reset semua input (logika v5)
        for (chk_var, sel_var, cb, wrapper, chk) in self.row_vars.values():
            
            if chk_var.get() == 1:
                chk_var.set(0) # Ini akan memicu command
            else:
                sel_var.set(CF_LABELS[0])
                cb.configure(state="disabled")
                wrapper.configure(bg="#d8d8d8")
                chk.configure(bg="#d8d8d8")

        # Hapus hasil (logika v5)
        for c in self.res_inner.winfo_children():
            c.destroy()
        self._last_results = {}
        self._show_results({}) # Tampilkan placeholder lagi

    # Fungsi on_save() DIHAPUS
    
if __name__ == "__main__":
    app = CuteCFv6()
    app.mainloop()