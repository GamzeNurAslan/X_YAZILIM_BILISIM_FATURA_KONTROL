from tkinter import filedialog, messagebox
from datetime import datetime

class ReportExporter:

    @staticmethod
    def txt_kaydet(metin):
        dosya_adi = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Dosyası", "*.txt")],
            initialfile="rapor_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        if dosya_adi:
            try:
                with open(dosya_adi, "w", encoding="utf-8") as dosya:
                    dosya.write(metin)
                messagebox.showinfo("Bilgi", "Rapor kaydedildi")
            except Exception as hata:
                messagebox.showerror("Hata", str(hata))

