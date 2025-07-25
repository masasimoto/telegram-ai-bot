import httpx

def search_web(query: str) -> str:
    try:
        url = f"https://ddg-api.herokuapp.com/search?q={query}"
        r = httpx.get(url, timeout=10)
        data = r.json()
        result = data.get("results", [])
        if result:
            return f"{result[0].get('title')}: {result[0].get('url')}"
        return "Gak nemu info di web, coba tanya yang lain~"
    except Exception as e:
        return f"Error web search: {e}"
