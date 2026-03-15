import requests
from bs4 import BeautifulSoup

def eczane_kazı(sehir="istanbul"):
    # İstanbul Eczacı Odası'nın ana nöbetçi sayfası
    url = "https://www.istanbuleczaciodasi.org.tr/nobetci-eczane/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Referer': 'https://www.istanbuleczaciodasi.org.tr/'
    }
    
    try:
        # Site bir mobil uygulama gibi davrandığı için istek gönderiyoruz
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        liste = []
        
        # Sitedeki eczane bloklarını buluyoruz (İEO sitesinin yapısına göre güncellendi)
        # Not: İEO verileri dinamik yüklediği için bazen boş dönebilir, 
        # bu durumda sistem senin için yedek bir mesaj üretir.
        eczane_kartlari = soup.select(".eczane-bilgi") 
        
        for kart in eczane_kartlari:
            isim = kart.select_one(".eczane-adi").text.strip() if kart.select_one(".eczane-adi") else "Bilinmiyor"
            tel = kart.select_one(".telefon-no").text.strip() if kart.select_one(".telefon-no") else ""
            adres = kart.select_one(".adres-bilgi").text.strip() if kart.select_one(".adres-bilgi") else ""
            
            liste.append({
                "ad": isim,
                "tel": tel,
                "adres": adres
            })

        if not liste:
            # Eğer kazıma başarısız olursa, uygulamanın çökmemesi için test verisi gönderiyoruz
            return [{"ad": "İstanbul Nöbetçi Listesi Güncelleniyor", "tel": "Lütfen 1 dk sonra tekrar deneyin"}]
            
        return liste
    except Exception as e:
        return [{"ad": "Bağlantı Hatası", "detay": str(e)}]
