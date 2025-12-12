# 📚 LGS Türkçe Soru Bankası

<div align="center">

![Turkish](https://img.shields.io/badge/Language-Turkish-red)
![Questions](https://img.shields.io/badge/Questions-371-blue)
![Years](https://img.shields.io/badge/Years-2018--2025-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

**MEB LGS Türkçe Örnek Soruları - NLP ve Eğitim Araştırmaları İçin**

</div>

---

## 🎯 Proje Hakkında

Bu proje, **T.C. Millî Eğitim Bakanlığı (MEB)** tarafından yayınlanan **Liselere Geçiş Sınavı (LGS)** Türkçe örnek sorularını içeren kapsamlı bir veri seti oluşturur.

### ✨ Özellikler

- 📝 **371 geçerli soru** (kalite filtreli)
- 📅 **7 akademik yıl** kapsamı (2018-2025)
- 📄 **47 resmi PDF** kaynağından otomatik çıkarım
- 🎯 **4 seçenekli** çoktan seçmeli format
- ✅ **%100 cevap anahtarı** mevcut
- 📊 CSV ve JSON formatlarında çıktı

---

## 📁 Proje Yapısı

```
lgs-question-generator/
├── data/
│   ├── kaggle/                    # 📊 Hazır veri seti
│   │   ├── lgs_turkce_sorulari.csv
│   │   ├── lgs_turkce_gecerli.csv
│   │   ├── lgs_turkce_sorulari.json
│   │   ├── dataset-metadata.json
│   │   └── README.md
│   └── raw/                       # 📄 PDF kaynakları
│       ├── 2018-2019/
│       ├── 2019-2020/
│       ├── ...
│       └── 2024-2025/
├── scripts/
│   └── kaggle_ultimate.py         # 🔧 Ana çıkarım scripti
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚀 Kurulum

```bash
# Repo'yu klonla
git clone https://github.com/RAhsencicek/lgs-turkce-soru-bankasi.git
cd lgs-turkce-soru-bankasi

# Virtual environment oluştur
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

---

## 💻 Kullanım

### Veri Setini Kullanma

```python
import pandas as pd

# CSV'den yükle
df = pd.read_csv('data/kaggle/lgs_turkce_gecerli.csv')
print(f"Toplam soru: {len(df)}")

# Rastgele bir soru göster
sample = df.sample(1).iloc[0]
print(f"Soru: {sample['soru_metni'][:200]}...")
print(f"Doğru Cevap: {sample['dogru_cevap']}")
```

### Veri Setini Yeniden Oluşturma

```bash
# PDF'lerden veri setini oluştur
python scripts/kaggle_ultimate.py
```

---

## 📊 Veri Seti İstatistikleri

| Metrik | Değer |
|--------|-------|
| Toplam Soru | 431 |
| Geçerli Soru | 371 |
| Geçerlilik Oranı | %86 |
| Yıl Aralığı | 2018-2025 |
| PDF Kaynak | 47 adet |

### Yıllara Göre Dağılım

| Yıl | Soru |
|-----|------|
| 2018-2019 | 60 |
| 2019-2020 | 92 |
| 2020-2021 | 47 |
| 2021-2022 | 64 |
| 2022-2023 | 59 |
| 2023-2024 | 26 |
| 2024-2025 | 23 |

---

## 🎓 Kullanım Alanları

- 🤖 **Soru-Cevap Sistemleri**: Türkçe QA model eğitimi
- 📊 **Metin Sınıflandırma**: Konu/zorluk tahmin modelleri
- 📖 **Eğitim Araçları**: LGS hazırlık uygulamaları
- 🧠 **Dil Modelleri**: Türkçe anlama benchmarkları

---

## 📜 Kaynak

- **Kurum**: T.C. Millî Eğitim Bakanlığı
- **Birim**: Ölçme, Değerlendirme ve Sınav Hizmetleri Genel Müdürlüğü
- **URL**: [odsgm.meb.gov.tr](https://odsgm.meb.gov.tr)

---

## 📄 Lisans

Bu proje eğitim ve araştırma amaçlı kullanım için hazırlanmıştır.

---

## 🔗 Bağlantılar

- [Kaggle Dataset](https://kaggle.com/datasets/) *(yakında)*
- [Hugging Face](https://huggingface.co/datasets/) *(yakında)*

---

<div align="center">

**Anahtar Kelimeler**: `LGS` `Türkçe` `NLP` `Soru-Cevap` `Eğitim` `MEB` `Dataset`

</div>
