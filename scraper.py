import requests
from bs4 import BeautifulSoup

def eczane_kazı():
    url = "https://www.istanbuleczaciodasi.org.tr/nobetci-ezaneler"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    liste = []
    # Not: Site yapısı değişirse burayı güncelleriz
    for eczane in soup.find_all("div", class_="nobetci-eczane-adi"):
        liste.append({"ad": eczane.text.strip()})

    return liste
