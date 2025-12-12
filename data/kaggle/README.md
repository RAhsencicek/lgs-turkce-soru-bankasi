# 📚 LGS Türkçe Soru Bankası (2018-2025)

<div align="center">

![Turkish](https://img.shields.io/badge/Language-Turkish-red)
![Questions](https://img.shields.io/badge/Questions-371-blue)
![Years](https://img.shields.io/badge/Years-2018--2025-green)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)

</div>

## 🎯 Veri Seti Hakkında

Bu veri seti, **T.C. Millî Eğitim Bakanlığı (MEB)** tarafından yayınlanan **Liselere Geçiş Sınavı (LGS)** Türkçe örnek sorularını içermektedir.

7 akademik yılı (2018-2025) kapsayan bu koleksiyon, **doğal dil işleme (NLP)**, **soru-cevap sistemleri** ve **eğitim teknolojileri** araştırmaları için değerli bir kaynaktır.

### ✨ Özellikler

- 📝 **371 geçerli soru** (kalite filtreli)
- 📅 **7 akademik yıl** kapsamı
- 📄 **47 resmi PDF** kaynağından derlenmiş
- 🎯 **4 seçenekli** çoktan seçmeli format
- ✅ **%100 cevap anahtarı** mevcut

---

## 📊 İstatistikler

| Metrik | Değer |
|--------|-------|
| **Toplam Soru** | 431 |
| **Geçerli Soru** | 371 |
| **Geçerlilik Oranı** | %86 |
| **Yıl Aralığı** | 2018-2025 |
| **PDF Kaynak** | 47 adet |

### 📅 Yıllara Göre Dağılım

| Akademik Yıl | Soru Sayısı |
|--------------|-------------|
| 2018-2019 | 60 |
| 2019-2020 | 92 |
| 2020-2021 | 47 |
| 2021-2022 | 64 |
| 2022-2023 | 59 |
| 2023-2024 | 26 |
| 2024-2025 | 23 |

### 📊 Cevap Dağılımı

| Şık | Sayı | Oran |
|-----|------|------|
| A | 81 | %22 |
| B | 104 | %28 |
| C | 90 | %24 |
| D | 96 | %26 |

---

## 📁 Dosya Yapısı

```
📦 lgs-turkce-soru-bankasi
├── 📄 lgs_turkce_sorulari.csv      # Tüm sorular (CSV)
├── 📄 lgs_turkce_gecerli.csv       # Kalite filtreli sorular
├── 📄 lgs_turkce_sorulari.json     # Tüm sorular (JSON)
├── 📄 dataset-metadata.json        # Kaggle metadata
└── 📄 README.md                    # Bu dosya
```

---

## 🔤 Sütun Açıklamaları

| Sütun | Tip | Açıklama | Örnek |
|-------|-----|----------|-------|
| `soru_id` | string | Benzersiz soru kimliği | `2022_2023_S01_SOZEL_ORNEK` |
| `yil` | string | Akademik yıl | `2022-2023` |
| `ay` | string | Yayın ayı | `Kasım` |
| `soru_no` | int | Soru numarası | `1-10` |
| `soru_metni` | string | Paragraf + soru cümlesi | *Metin...* |
| `secenek_A` | string | A şıkkı | *Seçenek metni* |
| `secenek_B` | string | B şıkkı | *Seçenek metni* |
| `secenek_C` | string | C şıkkı | *Seçenek metni* |
| `secenek_D` | string | D şıkkı | *Seçenek metni* |
| `dogru_cevap` | string | Doğru cevap | `A`, `B`, `C`, `D` |
| `kaynak` | string | PDF dosya adı | `SOZEL_ORNEK_126498` |

---

## 🎓 Kullanım Alanları

### 🤖 Makine Öğrenmesi & NLP

- **Soru-Cevap Sistemleri**: Türkçe QA model eğitimi
- **Metin Sınıflandırma**: Konu/zorluk tahmin modelleri
- **Dil Modelleri**: Türkçe anlama benchmarkları
- **Reading Comprehension**: Okuma anlama değerlendirmesi

### 📖 Eğitim Teknolojileri

- **Uyarlanabilir Öğrenme**: Öğrenci seviyesine göre soru seçimi
- **Otomatik Soru Üretimi**: Mevcut sorulardan yeni sorular türetme
- **Sınav Hazırlık Araçları**: LGS hazırlık uygulamaları
- **Eğitim Analitiği**: Öğrenci performans analizi

### 📊 Veri Analizi

- **Soru Analizi**: Zorluk derecesi, konu dağılımı
- **Trend Analizi**: Yıllar arası değişim
- **Metin Madenciliği**: Soru kalıpları keşfi

---

## 💻 Örnek Kullanım

### Python (Pandas)

```python
import pandas as pd

# Veri setini yükle
df = pd.read_csv('lgs_turkce_gecerli.csv')

# Temel istatistikler
print(f"Toplam soru: {len(df)}")
print(f"Yıl dağılımı:\n{df['yil'].value_counts()}")

# 2023-2024 sorularını filtrele
df_2024 = df[df['yil'] == '2023-2024']
print(f"\n2023-2024 soruları: {len(df_2024)}")

# Rastgele bir soru göster
sample = df.sample(1).iloc[0]
print(f"\n📝 Örnek Soru ({sample['yil']}):")
print(f"Soru: {sample['soru_metni'][:200]}...")
print(f"A) {sample['secenek_A']}")
print(f"B) {sample['secenek_B']}")
print(f"C) {sample['secenek_C']}")
print(f"D) {sample['secenek_D']}")
print(f"✅ Doğru Cevap: {sample['dogru_cevap']}")
```

### Python (JSON)

```python
import json

with open('lgs_turkce_sorulari.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Metadata: {data['metadata']}")
print(f"İstatistikler: {data['statistics']}")
print(f"Soru sayısı: {len(data['questions'])}")
```

---

## 📜 Kaynak & Lisans

### Kaynak
- **Kurum**: T.C. Millî Eğitim Bakanlığı
- **Birim**: Ölçme, Değerlendirme ve Sınav Hizmetleri Genel Müdürlüğü
- **URL**: [odsgm.meb.gov.tr](https://odsgm.meb.gov.tr)

### Lisans
Bu veri seti **eğitim ve araştırma amaçlı** kullanım için hazırlanmıştır.

- Ticari olmayan kullanım serbesttir
- Kaynak gösterilmesi gerekmektedir
- Türev çalışmalar aynı lisansla paylaşılmalıdır

---

## 📌 Notlar

1. **Görsel İçerikli Sorular**: Bazı sorular grafik, tablo veya resim içermektedir. Bu sorularda görsel içerik metin olarak yansıtılmış olabilir.

2. **Metin Kalitesi**: PDF'lerden otomatik çıkarım yapıldığından bazı sorularda format bozuklukları olabilir.

3. **Eksik Veriler**: Görsel ağırlıklı sorularda seçenek metinleri eksik olabilir.

---

## 🔗 İlgili Bağlantılar

- [MEB Örnek Sorular](https://odsgm.meb.gov.tr)
- [LGS Hakkında](https://www.meb.gov.tr)

---

<div align="center">

**Anahtar Kelimeler**: `LGS` `Türkçe` `NLP` `Soru-Cevap` `Eğitim` `MEB` `Türkiye` `Turkish` `QA` `Education` `Reading Comprehension`

*Bu veri seti akademik araştırma amacıyla oluşturulmuştur.*

</div>
