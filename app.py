import requests
import json
from datetime import datetime

YOUTUBE_API_KEY = "TU_CLAVE_AQUI"

def obtener_canales_tv():
    try:
        r = requests.get("https://iptv-org.github.io/iptv/index.m3u", timeout=30)
        lineas = r.text.splitlines()
    except:
        return []
    canales = []
    i = 0
    while i < len(lineas):
        if lineas[i].startswith("#EXTINF"):
            nombre = lineas[i].split(',')[-1].strip() or "Canal"
            if i+1 < len(lineas) and lineas[i+1].strip().endswith(('.m3u8', '.ts')):
                canales.append({"nombre": nombre, "url": lineas[i+1].strip(), "tipo": "tv"})
            i += 2
        else:
            i += 1
    return canales

def buscar_youtube(query):
    if YOUTUBE_API_KEY == "TU_CLAVE_AQUI":
        return []
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": YOUTUBE_API_KEY,
            "q": query,
            "type": "video",
            "videoLicense": "creativeCommon",
            "maxResults": 5,
            "order": "date"
        }
        r = requests.get(url, params=params, timeout=20)
        items = r.json().get("items", [])
        return [{"nombre": f"🎥 {i['snippet']['title']}", "url": f"https://www.youtube.com/watch?v={i['id']['videoId']}", "tipo": "yt"} for i in items]
    except:
        return []

def main():
    tv = obtener_canales_tv()
    yt = []
    yt += buscar_youtube("película completa 2025")
    yt += buscar_youtube("documental 2025")
    yt += buscar_youtube("K-drama completo")
    yt += buscar_youtube("telenovela completa")

    todo = {}
    for item in tv + yt:
        cat = "peliculas"
        n = item["nombre"].lower()
        if "corea" in n or "k-drama" in n: cat = "series_coreanas"
        elif "novela" in n or "telenovela" in n: cat = "telenovelas"
        elif "2025" in n or "estreno" in n: cat = "estrenos_2025"
        elif item["tipo"] == "tv": cat = "otros"
        todo.setdefault(cat, []).append({"nombre": item["nombre"], "url": item["url"]})

    with open("canales.json", "w") as f:
        json.dump(todo, f, ensure_ascii=False, indent=2)
    print("✅ Actualizado:", datetime.now())

if __name__ == "__main__":
    main()