import requests
from bs4 import BeautifulSoup

def search_web(query):
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("div", class_="BNeawe").text
        return f"Hasil cepat (Google): {result}"
    except:
        return "Aku gak bisa cari di web sekarang 😢"
