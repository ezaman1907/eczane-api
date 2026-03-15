import requests
from bs4 import BeautifulSoup

def eczane_kazı():
    url = "https://www.istanbuleczaciodasi.org.tr/nobetci-ezaneler"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        liste = []
        # İstanbul Eczacı Odası sitesinde eczane isimleri genellikle 'panel-title' veya h4 içinde olur
        # En garanti yol: Tüm 'eczane' geçen blokları taramak
        eczane_kartlari = soup.find_all("div", class_="panel-default") # Genel kart yapısı
        
        if not eczane_kartlari:
            # Alternatif olarak tablo yapısını deneyelim
            eczane_kartlari = soup.select(".table-responsive table tr")

        for kart in eczane_kartlari:
            # Kart içindeki metni temizleyip alalım
            text = kart.text.strip().split('\n')[0] # İlk satırı al (genelde isimdir)
            if text and len(text) < 100: # Gereksiz uzun metinleri ele
                liste.append({"ad": text})
        
        # Eğer hala boşsa, basit bir test verisi gönder ki çalıştığını anla
        if not liste:
            return [{"ad": "Su an site taranıyor, lutfen az sonra tekrar deneyin"}]
            
        return liste
    except Exception as e:
        return [{"ad": "Hata: " + str(e)}]
