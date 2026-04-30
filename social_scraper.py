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
    {"casa": "Betsson", "usuario": "betssonbrasil"},
    {"casa": "Rei do Pitaco", "usuario": "reidopitaco"},
    {"casa": "Multi Bet", "usuario": "multibet"},
    {"casa": "Meridian Bet", "usuario": "meridianbet_br"},
    {"casa": "Versus", "usuario": "versusbet_br"},
]

PERFIS_TWITTER = [
    {"casa": "Betano", "usuario": "BetanoBrasil"},
    {"casa": "Superbet", "usuario": "SuperbetBrasil"},
    {"casa": "KTO", "usuario": "KTOBrasil"},
    {"casa": "Galera Bet", "usuario": "GaleraBet"},
    {"casa": "Sportingbet", "usuario": "Sportingbet_BR"},
    {"casa": "Hiper Bet", "usuario": "HiperBet_BR"},
    {"casa": "Betsul", "usuario": "betsul"},
    {"casa": "F12 Bet", "usuario": "f12bet"},
]

PALAVRAS_CASSINO = [
    "slot", "slots", "cassino", "casino", "roleta", "blackjack",
    "poker", "baccarat", "crash", "mines", "aviator", "fortune",
    "pragmatic", "pgsoft", "spribe", "evolution", "giros",
    "rodadas gratis", "rodadas grátis", "giro gratis", "giro grátis",
    "tigre", "gates", "sugar rush", "sweet bonanza", "big bass",
    "wild", "scatter", "book of", "fortune rabbit", "fortune snake",
    "fortune tiger", "superspin", "supercoins", "golden chips",
    "playtech", "evoplay", "popok",
]

PALAVRAS_LIXO = [
    "siga", "seguir", "compartilhe", "marque um amigo",
    "regulamento", "termos e condições", "saiba mais",
    "jogue com responsabilidade", "proibido para menores",
    "18+", "+18", "portaria", "spa/mf",
]

PALAVRAS_PROMO_VALIDAS = [
    "aposta gratis", "aposta grátis", "freebet", "free bet",
    "cashback futebol", "cashback esport", "cashback na champions",
    "cashback na libertadores", "cashback no brasileirao",
    "cashback da liberta", "empate premiado",
    "super odds", "superodds", "odds aumentadas", "golden boost",
    "super aposta turbinada", "turbinada", "super aumentada",
    "mega impulso", "ou anula", "marca ou anula",
    "ganhe r$", "ganhe ate r$", "aposte r$",
    "aposta sem risco", "reembolso",
    "bonus futebol", "bonus esport", "bonus apostas",
    "missao", "missão", "desafio", "liga da galera",
    "kings league", "champions league e ganhe",
    "libertadores e ganhe", "brasileirao e ganhe",
    "nba e ganhe", "nba playoffs",
    "utilize a ferramenta criar aposta",
    "garanta 100%", "garanta 50%",
    "50% cashback", "25% cashback", "20% cashback",
    "100% do valor", "chance extra",
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

def detectar_tipo(texto):
    t = texto.lower()
    if any(p in t for p in ["aposta gratis", "aposta grátis", "freebet", "free bet", "aposta sem risco", "chance extra"]):
        return "aposta_gratis"
    if any(p in t for p in ["cashback", "empate premiado", "reembolso"]):
        return "cashback"
    if any(p in t for p in ["super odds", "odds aumentadas", "golden boost", "turbinada", "mega impulso", "ou anula", "superodds", "super aumentada"]):
        return "super_odds"
    if any(p in t for p in ["missao", "missão", "desafio", "liga da galera"]):
        return "missao"
    if any(p in t for p in ["bonus", "bônus"]):
        return "bonus"
    return "outro"

def is_post_valido(texto):
    if not texto or len(texto) < 20:
        return False

    t = texto.lower()

    for cassino in PALAVRAS_CASSINO:
        if cassino in t:
            return False

    for lixo in PALAVRAS_LIXO:
        if lixo in t:
            return False

    if any(p in t for p in PALAVRAS_PROMO_VALIDAS):
        return True

    return False

def salvar_nova(con, promo):
    try:
        con.execute(
            "INSERT INTO promocoes VALUES (?,?,?,?,?,?,?,0)",
            (promo["id"], promo["casa"], promo["titulo"],
             promo["descricao"], promo["url"], promo["tipo"],
             promo["data_coleta"])
        )
        con.commit()
        return True
    except:
        return False

def scrape_instagram(perfil):
    print(f"Instagram: {perfil['usuario']}")
    try:
        resposta = requests.post(
            "https://api.apify.com/v2/acts/apify~instagram-post-scraper/run-sync-get-dataset-items",
            params={"token": APIFY_TOKEN, "timeout": 60},
            json={
                "directUrls": [f"https://www.instagram.com/{perfil['usuario']}/"],
                "resultsLimit": 12
            },
            timeout=90
        )
        if resposta.status_code == 200:
            return resposta.json()
        print(f"  Erro status: {resposta.status_code}")
        return []
    except Exception as e:
        print(f"  Erro: {e}")
        return []

def scrape_twitter(perfil):
    print(f"Twitter: {perfil['usuario']}")
    try:
        resposta = requests.post(
            "https://api.apify.com/v2/acts/apify~twitter-scraper/run-sync-get-dataset-items",
            params={"token": APIFY_TOKEN, "timeout": 60},
            json={
                "startUrls": [{"url": f"https://twitter.com/{perfil['usuario']}"}],
                "maxItems": 12
            },
            timeout=90
        )
        if resposta.status_code == 200:
            return resposta.json()
        print(f"  Erro status: {resposta.status_code}")
        return []
    except Exception as e:
        print(f"  Erro: {e}")
        return []

def processar_posts_instagram(con, posts, perfil):
    novas = 0
    url_perfil = f"https://www.instagram.com/{perfil['usuario']}/"

    for post in posts:
        texto = post.get("caption", "") or ""
        if not is_post_valido(texto):
            continue

        titulo = texto[:100].split("\n")[0].strip()
        descricao = texto[:400]
        uid = hashlib.md5(f"instagram_{perfil['casa']}_{titulo}".encode()).hexdigest()

        promo = {
            "id": uid,
            "casa": f"{perfil['casa']} (Instagram)",
            "titulo": titulo,
            "descricao": descricao,
            "url": post.get("url", url_perfil),
            "tipo": detectar_tipo(texto),
            "data_coleta": datetime.now().isoformat(),
        }

        if salvar_nova(con, promo):
            novas += 1
            print(f"  Nova: {titulo[:60]}")

    return novas

def processar_posts_twitter(con, posts, perfil):
    novas = 0
    url_perfil = f"https://twitter.com/{perfil['usuario']}"

    for post in posts:
        texto = post.get("text", "") or post.get("full_text", "") or ""
        if not is_post_valido(texto):
            continue

        titulo = texto[:100].split("\n")[0].strip()
        descricao = texto[:400]
        uid = hashlib.md5(f"twitter_{perfil['casa']}_{titulo}".encode()).hexdigest()

        promo = {
            "id": uid,
            "casa": f"{perfil['casa']} (Twitter)",
            "titulo": titulo,
            "descricao": descricao,
            "url": post.get("url", url_perfil),
            "tipo": detectar_tipo(texto),
            "data_coleta": datetime.now().isoformat(),
        }

        if salvar_nova(con, promo):
            novas += 1
            print(f"  Nova: {titulo[:60]}")

    return novas

def main():
    if not APIFY_TOKEN:
        print("APIFY_TOKEN não configurado, pulando redes sociais")
        return

    con = init_db()
    total = 0

    print("\n=== INSTAGRAM ===")
    for perfil in PERFIS_INSTAGRAM:
        posts = scrape_instagram(perfil)
        novas = processar_posts_instagram(con, posts, perfil)
        print(f"  {perfil['casa']}: {len(posts)} posts, {novas} novas promocoes")
        total += novas

    print("\n=== TWITTER ===")
    for perfil in PERFIS_TWITTER:
        posts = scrape_twitter(perfil)
        novas = processar_posts_twitter(con, posts, perfil)
        print(f"  {perfil['casa']}: {len(posts)} posts, {novas} novas promocoes")
        total += novas

    print(f"\nTotal redes sociais: {total} novas promocoes")

if __name__ == "__main__":
    main()
