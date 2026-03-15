import requests
from bs4 import BeautifulSoup

def eczane_kazı(sehir="istanbul"):
    # Hata almamak için en stabil kaynaklardan birini kullanıyoruz
    url = "https://www.aeo.org.tr/NobetciEczaneler"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Eğer site cevap vermezse boş dönme, hata mesajı ver
        if response.status_code != 200:
            return [{"ad": "Kaynak siteye ulasilamadi"}]

        soup = BeautifulSoup(response.content, "lxml")
        liste = []
        
        # Basitçe tablo satırlarını tarıyoruz
        rows = soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                isim = cols[0].text.strip()
                if "ECZANE" in isim.upper():
                    liste.append({"ad": isim, "tel": cols[1].text.strip()})
        
        return liste if liste else [{"ad": "Bugun icin veri bulunamadi"}]
    except Exception as e:
        return [{"ad": f"Sistem Hatasi: {str(e)}"}]
