import pandas as pd

class FaturaAnalizi:
    GEREKLI_SUTUNLAR = ["Fatura No", "Tutar", "Tarih", "Fabrika Adı"]

    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu
        self.df = None

    def yukle(self):
        self.df = pd.read_excel(self.dosya_yolu)
        self.sutun_kontrol()

    def sutun_kontrol(self):
        eksikler = [s for s in self.GEREKLI_SUTUNLAR if s not in self.df.columns]
        if eksikler:
            raise ValueError(f"Eksik sütunlar: {', '.join(eksikler)}")

    def tekrar_kayitlar(self):
        return self.df[self.df.duplicated(subset=["Fatura No"], keep=False)]

    def eksik_veriler(self):
        return self.df[self.df.isnull().any(axis=1)]

    def hatali_tutarlar(self):
        return self.df[(self.df["Tutar"] <= 0) | (self.df["Tutar"].isnull())]



