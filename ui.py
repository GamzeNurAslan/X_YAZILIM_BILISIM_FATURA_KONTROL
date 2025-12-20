import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from analyzer import FaturaAnalyzer
from exporter import ReportExporter


class NetsimFaturaKontrolUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.parent = parent
        self.parent.title("X YAZILIM & BİLİŞİM FATURA KONTROL SİSTEMİ")
        self.parent.geometry("1100x700")

        self.dosya_yolu = None
        self.analyzer = None

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ust_cerceve = tk.Frame(self, bg="#2c3e50", height=60)
        ust_cerceve.pack(fill=tk.X)

        baslik = tk.Label(ust_cerceve, text="X YAZILIM & BİLİŞİM FATURA KONTROL SİSTEMİ",
                          fg="white", bg="#2c3e50",
                          font=("Segoe UI", 16, "bold"))
        baslik.pack(pady=15)

        alt_baslik = tk.Label(ust_cerceve, text="Muhasebe Veri Doğrulama ve Kontrol Platformu",
                              fg="white", bg="#2c3e50", font=("Segoe UI", 9))
        alt_baslik.pack()

        veri_kaynagi_frame = ttk.LabelFrame(self, text="Veri Kaynağı", padding=(15,10))
        veri_kaynagi_frame.pack(fill=tk.X, padx=20, pady=(15, 5))

        self.dosya_sec_btn = ttk.Button(veri_kaynagi_frame, text="Dosya Seç", command=self.dosya_sec)
        self.dosya_sec_btn.pack(side=tk.LEFT)

        self.secilen_dosya_label = tk.Label(veri_kaynagi_frame, text="", fg="green", font=("Segoe UI", 9, "bold"))
        self.secilen_dosya_label.pack(side=tk.LEFT, padx=10)

        self.analiz_baslat_btn = ttk.Button(veri_kaynagi_frame, text="Analizi Başlat", command=self.analiz_et, state=tk.DISABLED)
        self.analiz_baslat_btn.pack(side=tk.LEFT, padx=20)

        self.toplam_kayit_label = tk.Label(veri_kaynagi_frame, text="Toplam Kayıt: 0", font=("Segoe UI", 9))
        self.toplam_kayit_label.pack(side=tk.RIGHT)

        self.hata_label = tk.Label(veri_kaynagi_frame, text="Hata: 0", fg="green", font=("Segoe UI", 9))
        self.hata_label.pack(side=tk.RIGHT, padx=20)

        analiz_raporu_frame = ttk.LabelFrame(self, text="Analiz Raporu", padding=(15,10))
        analiz_raporu_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))

        self.rapor_text = tk.Text(analiz_raporu_frame, font=("Consolas", 11))
        self.rapor_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(analiz_raporu_frame, orient=tk.VERTICAL, command=self.rapor_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.rapor_text.config(yscrollcommand=scrollbar.set)

        self.rapor_disa_aktar_btn = ttk.Button(self, text="Rapor Dışa Aktar", command=self.rapor_kaydet, state=tk.DISABLED)
        self.rapor_disa_aktar_btn.pack(anchor=tk.NE, padx=30)

    def dosya_sec(self):
        self.dosya_yolu = filedialog.askopenfilename(
            filetypes=[("Excel Dosyaları", "*.xlsx *.xls")]
        )
        if self.dosya_yolu:
            dosya_adi = self.dosya_yolu.split("/")[-1].split("\\")[-1]
            self.secilen_dosya_label.config(text=dosya_adi)
            self.analiz_baslat_btn.config(state=tk.NORMAL)
            self.rapor_text.delete("1.0", tk.END)
            self.toplam_kayit_label.config(text="Toplam Kayıt: 0")
            self.hata_label.config(text="Hata: 0", fg="green")
            self.rapor_disa_aktar_btn.config(state=tk.DISABLED)

    def analiz_et(self):
        try:
            self.analyzer = FaturaAnalyzer(self.dosya_yolu)
            self.analyzer.yukle()

            tekrarlar = self.analyzer.tekrar_kayitlar()
            eksikler = self.analyzer.eksik_veriler()
            hatalilar = self.analyzer.hatali_tutarlar()

            toplam_kayit = len(self.analyzer.df)
            toplam_hata = len(tekrarlar) + len(eksikler) + len(hatalilar)

            self.toplam_kayit_label.config(text=f"Toplam Kayıt: {toplam_kayit}")

            self.rapor_text.delete("1.0", tk.END)
            self.rapor_text.insert(tk.END, "NETSİM VERİ DOĞRULAMA RAPORU\n")
            self.rapor_text.insert(tk.END, f"Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")

            self.rapor_text.insert(tk.END, "GENEL BİLGİLER\n")
            self.rapor_text.insert(tk.END, f"Toplam Kayıt: {toplam_kayit}\n")
            self.rapor_text.insert(tk.END, f"Kaynak Dosya: {self.secilen_dosya_label.cget('text')}\n\n")

            self.rapor_text.insert(tk.END, "ANALİZ ÖZETİ\n")

            if toplam_hata == 0:
                self.rapor_text.insert(tk.END, "Veri doğrulaması başarılı\n", "basarili")
                self.hata_label.config(text="Hata: 0", fg="green")
            else:
                self.rapor_text.insert(tk.END, f"{toplam_hata} hata tespit edildi\n", "hata")
                self.hata_label.config(text=f"Hata: {toplam_hata}", fg="red")

            self.rapor_text.tag_config("basarili", foreground="green", font=("Segoe UI", 11, "bold"))
            self.rapor_text.tag_config("hata", foreground="red", font=("Segoe UI", 11, "bold"))

            self.rapor_disa_aktar_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def rapor_kaydet(self):
        icerik = self.rapor_text.get("1.0", tk.END)
        ReportExporter.txt_kaydet(icerik)


