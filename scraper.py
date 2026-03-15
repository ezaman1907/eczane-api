import requests

def eczane_kazı(sehir="istanbul"):
    # Buraya CollectAPI veya seçtiğin bir belediye linkini koyabilirsin
    # Test için şimdilik bir örnek yapı kuruyoruz
    url = "https://openapi.izmir.bel.tr/api/ibb/nobetcieczaneler"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            liste = []
            for eczane in data:
                liste.append({
                    "ad": eczane.get("Adi"),
                    "ilce": eczane.get("Ilce"),
                    "tel": eczane.get("Telefon"),
                    "adres": eczane.get("Adres")
                })
            return liste
    except:
        return [{"ad": "Hata: Veri çekilemedi"}]
