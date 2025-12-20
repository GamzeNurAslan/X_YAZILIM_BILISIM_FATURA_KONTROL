from tkinter import filedialog, messagebox
from datetime import datetime

class ReportExporter:

    @staticmethod
    def txt_kaydet(icerik):
        dosya = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Dosyası", "*.txt")],
            initialfile=f"netsim_rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if dosya:
            try:
                with open(dosya, "w", encoding="utf-8") as f:
                    f.write(icerik)
                messagebox.showinfo("Başarılı", "Rapor kaydedildi.")
            except Exception as e:
                messagebox.showerror("Hata", str(e))

