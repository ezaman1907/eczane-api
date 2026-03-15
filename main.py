from fastapi import FastAPI
from scraper import eczane_kazı
import json
import os
from datetime import datetime

app = FastAPI()

# Verilerin saklanacağı dosya adı
DATA_FILE = "eczaneler_cache.json"

def veriyi_yukle():
    # Eğer dosya varsa ve tarih bugüne aitse veriyi dosyadan oku
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
            if cache.get("tarih") == str(datetime.now().date()):
                return cache.get("data")
    return None

def veriyi_kaydet(data):
    # Çekilen veriyi tarihle birlikte dosyaya kaydet
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"tarih": str(datetime.now().date()), "data": data}, f, ensure_ascii=False)

@app.get("/")
def home():
    return {"mesaj": "Erdinç Zaman Akıllı API Sistemi Aktif"}

@app.get("/nobetci")
def verileri_ver(sehir: str = "istanbul"):
    # 1. Önce hafızaya (cache) bak
    onbellekteki_veri = veriyi_yukle()
    
    if onbellekteki_veri:
        return {"kaynak": "yerel_hafıza", "sehir": sehir, "data": onbellekteki_veri}
    
    # 2. Hafızada yoksa veya eskiyse robotu çalıştır
    yeni_veri = eczane_kazı(sehir)
    
    # 3. Yeni veriyi hafızaya kaydet
    if yeni_veri and "Hata" not in yeni_veri[0].get("ad", ""):
        veriyi_kaydet(yeni_veri)
        
    return {"kaynak": "canli_robot", "sehir": sehir, "data": yeni
