#!/usr/bin/env python3
"""
LGS-Türkçe-QA Kaggle Dataset Creator - ULTIMATE VERSION
========================================================
Tüm PDF formatlarını tam destekleyen final versiyon.
"""

import json
import os
import re
import csv
import fitz
from datetime import datetime
from typing import Dict, List, Tuple

DATA_DIR = "/Users/mac/lgs-question-generator/data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
OUTPUT_DIR = os.path.join(DATA_DIR, "kaggle")

YEARS = ["2018-2019", "2019-2020", "2020-2021", "2021-2022", 
         "2022-2023", "2023-2024", "2024-2025"]


def clean_text(text: str) -> str:
    """Metni temizle"""
    if not text:
        return ""
    text = re.sub(r'-\s*\n\s*', '', text)  # Tire ile bölünmüş kelimeleri birleştir
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_month(filename: str) -> str:
    """Dosya adından ayı çıkar"""
    f = filename.lower()
    months = {
        'ocak': 'Ocak', 'subat': 'Şubat', 'şubat': 'Şubat', 'mart': 'Mart',
        'nisan': 'Nisan', 'mayis': 'Mayıs', 'mayıs': 'Mayıs',
        'haziran': 'Haziran', 'ekim': 'Ekim', 'kasim': 'Kasım', 'kasım': 'Kasım',
        'aralik': 'Aralık', 'aralık': 'Aralık'
    }
    for k, v in months.items():
        if k in f:
            return v
    return "Bilinmiyor"


def get_turkce_section(full_text: str) -> str:
    """Türkçe bölümünü izole et"""
    # Bölüm başlangıçlarını bul (sırayla)
    section_markers = [
        (r'T\.?\s*C\.?\s*İnkılap\s*Tarihi', 'inkılap'),
        (r'İnkılap\s*Tarihi\s*ve\s*Atatürkçülük\s*\n\s*Örnek', 'inkılap'),
        (r'Din\s*Kültürü\s*ve\s*Ahlak\s*Bilgisi\s*\n?\s*Örnek', 'din'),
        (r'İNGİLİZCE\s*\n?\s*Örnek', 'ingilizce'),
        (r'YABANCI\s*DİL\s*\n?\s*Örnek', 'ingilizce'),
    ]
    
    # İçindekiler listesinden sonrasını ara (en az 2000 karakter)
    start_pos = 0
    
    # Türkçe bölümünün bitişini bul
    end_pos = len(full_text)
    
    for pattern, marker in section_markers:
        for match in re.finditer(pattern, full_text, re.IGNORECASE):
            # En az 2000 karakter sonrasında olmalı (içindekiler listesi değil)
            if match.start() > 2000:
                end_pos = min(end_pos, match.start())
                break
    
    turkce_text = full_text[start_pos:end_pos]
    return turkce_text


def extract_questions(turkce_text: str) -> List[Dict]:
    """Türkçe metninden soruları çıkar"""
    questions = []
    
    # Soru numaralarının konumlarını bul
    # Format: "1.\n" veya "1.  " (satır başı)
    positions = []
    
    for match in re.finditer(r'(?:^|\n)\s*(\d{1,2})\.\s*(?:\n|[A-ZÇĞİÖŞÜa-zçğıöşü])', turkce_text):
        num = int(match.group(1))
        if 1 <= num <= 10:
            positions.append((num, match.start()))
    
    # Sıralama ve duplicate temizleme
    positions.sort(key=lambda x: (x[0], x[1]))
    unique_positions = []
    seen = set()
    for num, pos in positions:
        if num not in seen:
            seen.add(num)
            unique_positions.append((num, pos))
    positions = sorted(unique_positions, key=lambda x: x[1])
    
    # Her soru için içeriği çıkar
    for i, (num, start) in enumerate(positions):
        # Sonraki sorunun başlangıcını bul
        if i + 1 < len(positions):
            end = positions[i + 1][1]
        else:
            end = len(turkce_text)
        
        block = turkce_text[start:end]
        
        # Soru numarasını temizle
        block = re.sub(r'^\s*\d+\.\s*\n?', '', block)
        
        # Seçenekleri parse et
        question = parse_options(block, num)
        
        if len(question["soru_metni"]) >= 30:
            questions.append(question)
    
    return questions


def parse_options(block: str, soru_no: int) -> Dict:
    """Soru bloğundan seçenekleri ayır"""
    question = {
        "soru_no": soru_no,
        "soru_metni": "",
        "secenek_A": "",
        "secenek_B": "",
        "secenek_C": "",
        "secenek_D": ""
    }
    
    # Seçenek pozisyonlarını bul
    # Formatlar: "A)", "A)  ", newline + "A)"
    option_positions = []
    for match in re.finditer(r'(?:^|\n)\s*([ABCD])\)\s*', block):
        option_positions.append((match.group(1), match.start(), match.end()))
    
    if option_positions:
        # Soru metni ilk seçenekten önce
        question["soru_metni"] = clean_text(block[:option_positions[0][1]])
        
        # Seçenekleri çıkar
        for i, (letter, start, content_start) in enumerate(option_positions):
            if i + 1 < len(option_positions):
                end = option_positions[i + 1][1]
            else:
                end = len(block)
            
            option_text = block[content_start:end]
            # Sayfa numaralarını ve footer'ları temizle
            option_text = re.sub(r'\n\d+\s*$', '', option_text)
            option_text = re.sub(r'Türkçe\s*Örnek\s*Soru.*$', '', option_text, flags=re.IGNORECASE)
            question[f"secenek_{letter}"] = clean_text(option_text)
    else:
        question["soru_metni"] = clean_text(block)
    
    return question


def extract_answers(full_text: str) -> Dict[int, str]:
    """Cevap anahtarını çıkar"""
    answers = {}
    
    # Son bölümde TÜRKÇE cevaplarını bul
    # Cevap anahtarı formatları:
    # "TÜRKÇE\n1. A  2. B ..."
    # "TÜRKÇE\n1-A\n2-B..."
    
    # Son 3000 karakterde ara
    last_section = full_text[-3000:]
    
    # TÜRKÇE başlığından sonraki cevapları bul
    turkce_match = re.search(r'TÜRKÇE\s*\n?([^\n]*(?:\n[^\n]*){0,5})', last_section, re.IGNORECASE)
    if turkce_match:
        answer_section = turkce_match.group(0)
        
        for match in re.finditer(r'(\d+)\s*[\.\-:\s]\s*([ABCD])', answer_section):
            num = int(match.group(1))
            ans = match.group(2)
            if 1 <= num <= 10:
                answers[num] = ans
    
    # Eğer yeterli cevap bulunamadıysa, tüm son bölümde ara
    if len(answers) < 5:
        for match in re.finditer(r'(\d+)\s*[\.\-:]\s*([ABCD])', last_section):
            num = int(match.group(1))
            ans = match.group(2)
            if 1 <= num <= 10 and num not in answers:
                answers[num] = ans
    
    return answers


def process_pdf(pdf_path: str, year: str, filename: str) -> List[Dict]:
    """PDF'yi işle"""
    try:
        doc = fitz.open(pdf_path)
        
        # Tüm metni birleştir
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n"
        
        # Türkçe bölümünü al
        turkce_text = get_turkce_section(full_text)
        
        # Soruları çıkar
        questions = extract_questions(turkce_text)
        
        # Cevapları çıkar
        answers = extract_answers(full_text)
        
        # Meta verileri ekle
        month = extract_month(filename)
        source_id = filename.replace('.pdf', '')
        
        for q in questions:
            q["yil"] = year
            q["ay"] = month
            q["dogru_cevap"] = answers.get(q["soru_no"], "")
            q["kaynak"] = source_id
            q["soru_id"] = f"{year.replace('-', '_')}_S{q['soru_no']:02d}_{source_id[:12]}"
        
        doc.close()
        return questions
        
    except Exception as e:
        print(f"  HATA: {e}")
        return []


def validate_question(q: Dict) -> bool:
    """Soru kalite kontrolü"""
    if len(q.get("soru_metni", "")) < 40:
        return False
    
    filled = sum(1 for opt in ["secenek_A", "secenek_B", "secenek_C", "secenek_D"] 
                 if len(q.get(opt, "")) > 5)
    if filled < 2:
        return False
    
    if q.get("dogru_cevap", "") not in ["A", "B", "C", "D"]:
        return False
    
    return True


def create_kaggle_readme(stats: Dict) -> str:
    """Kaggle README"""
    year_rows = '\n'.join(f"| {year} | {count} |" for year, count in stats.get('by_year', {}).items())
    
    return f"""# 📚 LGS Türkçe Soru Bankası (2018-2025)

## 🎯 Hakkında

T.C. Millî Eğitim Bakanlığı (MEB) tarafından yayınlanan LGS Türkçe örnek soruları.
7 akademik yıl, 47 PDF kaynağından derlenmiştir.

## 📊 İstatistikler

| Metrik | Değer |
|--------|-------|
| Toplam Soru | {stats['total']} |
| Geçerli Soru | {stats['valid']} |
| Geçerlilik | %{stats['valid']*100//max(1,stats['total'])} |
| Yıl Aralığı | 2018-2025 |
| PDF Sayısı | {stats['pdf_count']} |

### Yıl Dağılımı

| Yıl | Soru |
|-----|------|
{year_rows}

## 📁 Dosyalar

- `lgs_turkce_sorulari.csv` - Tüm sorular
- `lgs_turkce_gecerli.csv` - Kalite filtreli sorular
- `lgs_turkce_sorulari.json` - JSON format

## 🔤 Kolonlar

| Kolon | Açıklama |
|-------|----------|
| soru_id | Benzersiz ID |
| yil | Akademik yıl |
| ay | Yayın ayı |
| soru_no | Soru numarası (1-10) |
| soru_metni | Soru metni |
| secenek_A/B/C/D | Şıklar |
| dogru_cevap | Doğru şık |
| kaynak | PDF dosya adı |

## 🎓 Kullanım

```python
import pandas as pd
df = pd.read_csv('lgs_turkce_sorulari.csv')
print(df.head())
```

## 📜 Kaynak

T.C. Millî Eğitim Bakanlığı - [odsgm.meb.gov.tr](https://odsgm.meb.gov.tr)

---
*Eğitim ve araştırma amaçlı.*
"""


def main():
    print("=" * 60)
    print("LGS-Türkçe-QA Kaggle Dataset (Ultimate)")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_questions = []
    pdf_count = 0
    by_year = {}
    
    for year in YEARS:
        year_dir = os.path.join(RAW_DIR, year)
        if not os.path.exists(year_dir):
            continue
        
        print(f"\n📁 {year}")
        year_questions = []
        
        for filename in sorted(os.listdir(year_dir)):
            if not filename.endswith('.pdf'):
                continue
            
            pdf_path = os.path.join(year_dir, filename)
            questions = process_pdf(pdf_path, year, filename)
            
            year_questions.extend(questions)
            pdf_count += 1
            
            valid = sum(1 for q in questions if validate_question(q))
            sym = "✓" if valid >= 8 else "⚠" if valid >= 5 else "✗"
            print(f"  {sym} {filename[:42]}: {len(questions)} ({valid} geçerli)")
        
        all_questions.extend(year_questions)
        by_year[year] = len(year_questions)
    
    valid_questions = [q for q in all_questions if validate_question(q)]
    
    stats = {
        "total": len(all_questions),
        "valid": len(valid_questions),
        "pdf_count": pdf_count,
        "by_year": by_year
    }
    
    fields = ["soru_id", "yil", "ay", "soru_no", "soru_metni", 
              "secenek_A", "secenek_B", "secenek_C", "secenek_D",
              "dogru_cevap", "kaynak"]
    
    # CSV - tüm
    with open(os.path.join(OUTPUT_DIR, "lgs_turkce_sorulari.csv"), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(all_questions)
    
    # CSV - geçerli
    with open(os.path.join(OUTPUT_DIR, "lgs_turkce_gecerli.csv"), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(valid_questions)
    
    # JSON
    with open(os.path.join(OUTPUT_DIR, "lgs_turkce_sorulari.json"), 'w', encoding='utf-8') as f:
        json.dump({
            "metadata": {
                "title": "LGS Türkçe Soru Bankası",
                "version": "4.0",
                "created": datetime.now().isoformat(),
                "source": "MEB"
            },
            "statistics": stats,
            "questions": all_questions
        }, f, ensure_ascii=False, indent=2)
    
    # README
    with open(os.path.join(OUTPUT_DIR, "README.md"), 'w', encoding='utf-8') as f:
        f.write(create_kaggle_readme(stats))
    
    print("\n" + "=" * 60)
    print("✅ KAGGLE VERİ SETİ TAMAMLANDI")
    print("=" * 60)
    print(f"📊 Toplam: {stats['total']} | Geçerli: {stats['valid']} (%{stats['valid']*100//max(1,stats['total'])})")
    
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith(('.csv', '.json', '.md')):
            size = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
            print(f"   📄 {f}: {size:.1f} KB")


if __name__ == "__main__":
    main()
