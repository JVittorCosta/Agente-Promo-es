import requests
import sqlite3
import hashlib
import os
from datetime import datetime

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

PERFIS_INSTAGRAM = [
    {"casa": "Betano", "usuario": "betanobrasil"},
    {"casa": "Superbet", "usuario": "superbetbrasil"},
    {"casa": "Estrela Bet", "usuario": "estrelabet"},
    {"casa": "KTO", "usuario": "ktobrasil"},
    {"casa": "Galera Bet", "usuario": "galerabetoficial"},
    {"casa": "Sportingbet", "usuario": "sportingbetbrasil"},
    {"casa": "Hiper Bet", "usuario": "hiperbet"},
    {"casa": "F12 Bet", "usuario": "f12bet"},
    {"casa": "Betsul", "usuario": "betsul"},
    {"casa": "Vai de Bet", "usuario": "vaidebet"},
]

PERFIS_TWITTER = [
    {"casa": "Betano", "usuario": "BetanoBrasil"},
    {"casa": "Superbet", "usuario": "SuperbetBrasil"},
    {"casa": "KTO", "usuario": "KTOBrasil"},
    {"casa": "Galera Bet", "usuario": "GaleraBet"},
    {"casa": "Sportingbet", "usuario": "Sportingbet_BR"},
]

def init_db():
    con = sqlite3.connect("promocoes.db")
    con.execute("""
        CREATE TABLE IF NOT EXISTS promocoes (
            id TEXT PRIMARY KEY,
            casa TEXT,
            titulo TEXT,
            descricao TEXT,
            url TEXT,
            tipo TEXT,
            data_coleta TEXT,
            notificado INTEGER DEFAULT 0
        )
    """)
    con.commit()
    return con

def classificar_post(texto):
    texto_lower = texto.lower()

    palavras_cassino = [
        "slot", "cassino", "casino", "roleta", "crash", "mines",
        "aviator", "giros", "rodadas gratis", "fortune", "pragmatic"
    ]
    if any(p in texto_lower for p in palavras_cassino):
        return None

    if any(p in texto_lower for p in ["aposta grátis", "aposta gratis", "freebet", "free bet"]):
        return "aposta_gratis"
    if "cashback" in texto_lower:
        return "cashback"
    if any(p in texto_lower for p in ["super odds", "odds aumentadas", "golden boost", "turbinada"]):
        return "super_odds"
    if any(p in texto_lower for p in ["bônus", "bonus", "ganhe r$", "ganhe até r$"]):
        return "bonus"

    return None

def scrape_instagram(perfil):
    print(f"Scraping Instagram: {perfil['usuario']}")
    try:
        run = requests.post(
            "https://api.apify.com/v2/acts/apify~instagram-post-scraper/run-sync-get-dataset-items",
            params={"token": APIFY_TOKEN},
            json={
                "directUrls": [f"https://www.instagram.com/{perfil['usuario']}/"],
                "resultsLimit": 10
            },
            timeout=60
        )
        return run.json() if run.status_code == 200 else []
    except Exception as e:
        print(f"Erro Instagram {perfil['usuario']}: {e}")
        return []

def scrape_twitter(perfil):
    print(f"Scraping Twitter: {perfil['usuario']}")
    try:
        run = requests.post(
            "https://api.apify.com/v2/acts/apify~twitter-scraper/run-sync-get-dataset-items",
            params={"token": APIFY_TOKEN},
            json={
                "startUrls": [f"https://twitter.com/{perfil['usuario']}"],
                "maxItems": 10
            },
            timeout=60
        )
        return run.json() if run.status_code == 200 else []
    except Exception as e:
        print(f"Erro Twitter {perfil['usuario']}: {e}")
        return []

def processar_posts(con, posts, casa, rede, url_perfil):
    novas = 0
    for post in posts:
        texto = post.get("caption") or post.get("text") or post.get("full_text", "")
        if not texto or len(texto) < 10:
            continue

        tipo = classificar_post(texto)
        if not tipo:
            continue

        titulo = texto[:100].split("\n")[0].strip()
        uid = hashlib.md5(f"{rede}{casa}{titulo}".encode()).hexdigest()

        try:
            con.execute(
                "INSERT INTO promocoes VALUES (?,?,?,?,?,?,?,0)",
                (uid, f"{casa} ({rede})", titulo, texto[:500],
                 url_perfil, tipo, datetime.now().isoformat())
            )
            novas += 1
        except:
            pass

    con.commit()
    return novas

def main():
    con = init_db()
    total = 0

    for perfil in PERFIS_INSTAGRAM:
        posts = scrape_instagram(perfil)
        url = f"https://www.instagram.com/{perfil['usuario']}/"
        novas = processar_posts(con, posts, perfil["casa"], "Instagram", url)
        print(f"  {perfil['casa']} Instagram: {novas} novas")
        total += novas

    for perfil in PERFIS_TWITTER:
        posts = scrape_twitter(perfil)
        url = f"https://twitter.com/{perfil['usuario']}"
        novas = processar_posts(con, posts, perfil["casa"], "Twitter", url)
        print(f"  {perfil['casa']} Twitter: {novas} novas")
        total += novas

    print(f"\nTotal redes sociais: {total} novas promocoes")

if __name__ == "__main__":
    main()
