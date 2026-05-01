import requests
import sqlite3
import hashlib
import os
from datetime import datetime

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

PERFIS_INSTAGRAM = [
    {"casa": "1 Pra 1", "usuario": "1pra1.bet"},
    {"casa": "1xbet", "usuario": "1xbet_brasil"},
    {"casa": "4play", "usuario": "4playbet"},
    {"casa": "4win", "usuario": "4win.bet.oficial"},
    {"casa": "55W", "usuario": "55w.bet"},
    {"casa": "5G", "usuario": "5gbet_"},
    {"casa": "6R", "usuario": "6r.bet.br"},
    {"casa": "6Z", "usuario": "6zbet"},
    {"casa": "7Games", "usuario": "7games.bet"},
    {"casa": "9D", "usuario": "9d.bet"},
    {"casa": "9F", "usuario": "9f.bet"},
    {"casa": "A247", "usuario": "a247bet"},
    {"casa": "Afun", "usuario": "afunbet"},
    {"casa": "AI", "usuario": "aibet.brasil"},
    {"casa": "Alfabet", "usuario": "alfabetoficial"},
    {"casa": "Aposta Ganha", "usuario": "apostaganha"},
    {"casa": "Aposta1", "usuario": "aposta1br"},
    {"casa": "ApostaBet", "usuario": "apostabet"},
    {"casa": "ApostaMax", "usuario": "apostamax"},
    {"casa": "Apostar", "usuario": "apostar.bet.br"},
    {"casa": "ApostaTudo", "usuario": "apostatudo.bet.br"},
    {"casa": "Apostou", "usuario": "apostou.bet.br"},
    {"casa": "ArenaPlus", "usuario": "arenabetplus"},
    {"casa": "AviãoBet", "usuario": "aviaobet"},
    {"casa": "B1 Bet", "usuario": "b1.bet"},
    {"casa": "B2xBet", "usuario": "b2xbet"},
    {"casa": "Bacana Play", "usuario": "bacanaplay"},
    {"casa": "BandBet", "usuario": "bandbet.br"},
    {"casa": "BateuBet", "usuario": "bateubet"},
    {"casa": "Baubingo", "usuario": "baubingo"},
    {"casa": "Bet Buffalos", "usuario": "betbuffalos"},
    {"casa": "Bet dá Sorte", "usuario": "betdasorte"},
    {"casa": "Bet do Milhão", "usuario": "betdomilhaooficial"},
    {"casa": "Bet Falcons", "usuario": "betfalcons"},
    {"casa": "Bet Gorillas", "usuario": "betgorillas"},
    {"casa": "Bet.App", "usuario": "betapp.br"},
    {"casa": "Bet365", "usuario": "bet365brasil"},
    {"casa": "Bet4", "usuario": "bet4brasil"},
    {"casa": "Bet7K", "usuario": "bet7k"},
    {"casa": "Betaki", "usuario": "betakioficial"},
    {"casa": "Betano", "usuario": "betano.brasil"},
    {"casa": "Betão", "usuario": "betaobr"},
    {"casa": "Betboo", "usuario": "betboo_br"},
    {"casa": "Betboom", "usuario": "betboombr"},
    {"casa": "Betbra", "usuario": "betbra.oficial"},
    {"casa": "Betcaixa", "usuario": "betcaixa"},
    {"casa": "BetCopa", "usuario": "betcopaoficial"},
    {"casa": "Betespecial", "usuario": "betespecial"},
    {"casa": "BETesporte", "usuario": "betesporte"},
    {"casa": "Betfair", "usuario": "betfairbrasil"},
    {"casa": "BetFast", "usuario": "betfast.oficial"},
    {"casa": "Betfusion", "usuario": "betfusion_br"},
    {"casa": "BetMGM", "usuario": "betmgmbrasil"},
    {"casa": "Betnacional", "usuario": "betnacional"},
    {"casa": "Betou", "usuario": "betou.bet.br"},
    {"casa": "BetPix365", "usuario": "betpix365"},
    {"casa": "Betsson", "usuario": "betssonbrasil"},
    {"casa": "Betsul", "usuario": "betsul"},
    {"casa": "BetVip", "usuario": "betvip.oficial"},
    {"casa": "BetWarrior", "usuario": "betwarriorbrasil"},
    {"casa": "Bigbet", "usuario": "bigbetsportsbrasil"},
    {"casa": "Bolsa de Aposta", "usuario": "bolsadeaposta"},
    {"casa": "Br4bet", "usuario": "br4bet"},
    {"casa": "BraBet", "usuario": "brabet_official"},
    {"casa": "Brasil Bet", "usuario": "brasilbet"},
    {"casa": "Brasil da Sorte", "usuario": "brasildasorte"},
    {"casa": "Bravo", "usuario": "bravobet.br"},
    {"casa": "Brazino777", "usuario": "brazino777"},
    {"casa": "BrBet", "usuario": "brbetoficial"},
    {"casa": "Brxbet", "usuario": "brxbetoficial"},
    {"casa": "Bullsbet", "usuario": "bullsbet"},
    {"casa": "Casa de Apostas", "usuario": "casadeapostas"},
    {"casa": "CBEsportes", "usuario": "cbesportes"},
    {"casa": "Donald Bet", "usuario": "donaldbetoficial"},
    {"casa": "Donos da Bola", "usuario": "donosdabola"},
    {"casa": "Energia", "usuario": "energiabet"},
    {"casa": "Esporte 365", "usuario": "esporte365"},
    {"casa": "Esportes da Sorte", "usuario": "esportesdasorte"},
    {"casa": "Esportiva Bet", "usuario": "esportivabt"},
    {"casa": "EstrelaBet", "usuario": "estrelabt"},
    {"casa": "F12 Bet", "usuario": "f12bet"},
    {"casa": "Fanbit", "usuario": "fanbitoficial"},
    {"casa": "Faz1Bet", "usuario": "faz1bet"},
    {"casa": "FazoBet", "usuario": "fazobet"},
    {"casa": "Galerabet", "usuario": "galerabet"},
    {"casa": "Ganhei Bet", "usuario": "ganheibet"},
    {"casa": "Geral Bet", "usuario": "geralbet"},
    {"casa": "Ginga Bet", "usuario": "gingabetofc"},
    {"casa": "Gol de Bet", "usuario": "goldebet"},
    {"casa": "H2bet", "usuario": "h2bet"},
    {"casa": "Hiperbet", "usuario": "hiperbetoficial"},
    {"casa": "Ice", "usuario": "icebet.br"},
    {"casa": "iJogo", "usuario": "ijogobet"},
    {"casa": "Joga Junto", "usuario": "jogajunto.bet"},
    {"casa": "Jogo de Ouro", "usuario": "jogodeouro"},
    {"casa": "Jonbet", "usuario": "jonbetoficial"},
    {"casa": "KTO", "usuario": "ktobrasil"},
    {"casa": "Lance da Sorte", "usuario": "lancedasorte"},
    {"casa": "Lotogreen", "usuario": "lotogreen"},
    {"casa": "Lottoland", "usuario": "lottolandbrasil"},
    {"casa": "Lottu", "usuario": "lottubet"},
    {"casa": "Luvabet", "usuario": "luvabet"},
    {"casa": "Maxima Bet", "usuario": "maximabet.br"},
    {"casa": "MC Games", "usuario": "mcgamesbet"},
    {"casa": "Meridian", "usuario": "meridianbet_br"},
    {"casa": "Multibet", "usuario": "multibet.bet"},
    {"casa": "Novibet", "usuario": "novibetbrasil"},
    {"casa": "Pagolbet", "usuario": "pagolbet"},
    {"casa": "Pinnacle", "usuario": "pinnacleoficial"},
    {"casa": "PixBet", "usuario": "pixbet"},
    {"casa": "Play", "usuario": "playbet.br"},
    {"casa": "Rei do Pitaco", "usuario": "reidopitaco"},
    {"casa": "Rivalo", "usuario": "rivalo_br"},
    {"casa": "Sorte Online", "usuario": "sorteonlinebr"},
    {"casa": "Spin", "usuario": "spinbet.br"},
    {"casa": "Sportingbet", "usuario": "sportingbetbrasil"},
    {"casa": "SportyBet", "usuario": "sportybetbrasil"},
    {"casa": "Stake", "usuario": "stakebrasil"},
    {"casa": "Startbet", "usuario": "startbet.brasil"},
    {"casa": "Superbet", "usuario": "superbet.brasil"},
    {"casa": "Vai de Bet", "usuario": "vaidebet"},
    {"casa": "Vbet", "usuario": "vbet_brasil"},
    {"casa": "Versusbet", "usuario": "versusbet.br"},
    {"casa": "Viva Sorte", "usuario": "vivasorte"},
    {"casa": "Vupi", "usuario": "vupibet"},
]

PERFIS_TWITTER = [
    {"casa": "1xbet", "usuario": "1xbet_br"},
    {"casa": "A247", "usuario": "a247bet"},
    {"casa": "Aposta Ganha", "usuario": "ApostaGanha"},
    {"casa": "ApostaTudo", "usuario": "apostatudo"},
    {"casa": "BandBet", "usuario": "bandbet_br"},
    {"casa": "Bet dá Sorte", "usuario": "betdasorte"},
    {"casa": "Bet365", "usuario": "bet365_br"},
    {"casa": "Bet7K", "usuario": "bet7k_br"},
    {"casa": "Betano", "usuario": "BetanoBrasil"},
    {"casa": "Betboom", "usuario": "BetBoomBrasil"},
    {"casa": "Betfair", "usuario": "BetfairBrasil"},
    {"casa": "BetMGM", "usuario": "BetMGMBrasil"},
    {"casa": "Betnacional", "usuario": "betnacional"},
    {"casa": "Betsson", "usuario": "Betsson_Brasil"},
    {"casa": "Betsul", "usuario": "betsulbet"},
    {"casa": "Blaze", "usuario": "blaze"},
    {"casa": "Br4bet", "usuario": "br4bet"},
    {"casa": "Brasil Bet", "usuario": "brasilbet_br"},
    {"casa": "Brazino777", "usuario": "brazino777br"},
    {"casa": "Esportes da Sorte", "usuario": "EsportesdaSorte"},
    {"casa": "EstrelaBet", "usuario": "EstrelaBet"},
    {"casa": "Galerabet", "usuario": "galerabet"},
    {"casa": "Gol de Bet", "usuario": "goldebet"},
    {"casa": "Hiperbet", "usuario": "hiperbetoficial"},
    {"casa": "KTO", "usuario": "KTOBrasil"},
    {"casa": "Luvabet", "usuario": "luva_bet"},
    {"casa": "Matchbook", "usuario": "matchbook"},
    {"casa": "Meridian", "usuario": "meridianbet_br"},
    {"casa": "Novibet", "usuario": "NovibetBrasil"},
    {"casa": "Pinnacle", "usuario": "Pinnacle"},
    {"casa": "PixBet", "usuario": "PixBet"},
    {"casa": "Realsbet", "usuario": "realsbetoficial"},
    {"casa": "Rivalo", "usuario": "RivaloBrasil"},
    {"casa": "Sportingbet", "usuario": "SportingBetBR"},
    {"casa": "Stake", "usuario": "Stake"},
    {"casa": "Superbet", "usuario": "SuperbetBrasil"},
    {"casa": "Vai de Bet", "usuario": "vaidebet"},
    {"casa": "Vbet", "usuario": "VBet_Brasil"},
]

PALAVRAS_CASSINO = [
    "slot", "slots", "cassino", "casino", "roleta", "blackjack",
    "poker", "baccarat", "crash", "mines", "aviator", "fortune",
    "pragmatic", "pgsoft", "spribe", "evolution", "giros",
    "rodadas gratis", "rodadas grátis", "giro gratis", "giro grátis",
    "tigre", "gates", "sugar rush", "sweet bonanza", "big bass",
    "wild", "scatter", "book of", "fortune rabbit", "fortune snake",
    "fortune tiger", "superspin", "supercoins", "golden chips",
    "playtech", "evoplay", "popok", "jackpot", "raspadinha",
]

PALAVRAS_LIXO = [
    "siga", "seguir", "compartilhe", "marque um amigo",
    "regulamento", "termos e condições", "jogue com responsabilidade",
    "proibido para menores", "18+", "+18", "portaria", "spa/mf",
    "link na bio", "acesse o site", "baixe o app",
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
    "em apostas gratis", "em freebet", "em creditos",
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
    if any(p in t for p in ["aposta gratis", "aposta grátis", "freebet", "free bet", "aposta sem risco", "chance extra", "em apostas gratis", "em freebet"]):
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
    try:
        resposta = requests.post(
            "https://api.apify.com/v2/acts/apify~instagram-post-scraper/run-sync-get-dataset-items",
            params={"token": APIFY_TOKEN, "timeout": 60},
            json={
                "directUrls": [f"https://www.instagram.com/{perfil['usuario']}/"],
                "resultsLimit": 10
            },
            timeout=90
        )
        if resposta.status_code == 200:
            return resposta.json()
        return []
    except Exception as e:
        print(f"  Erro Instagram {perfil['usuario']}: {e}")
        return []

def scrape_twitter(perfil):
    try:
        resposta = requests.post(
            "https://api.apify.com/v2/acts/apify~twitter-scraper/run-sync-get-dataset-items",
            params={"token": APIFY_TOKEN, "timeout": 60},
            json={
                "startUrls": [{"url": f"https://twitter.com/{perfil['usuario']}"}],
                "maxItems": 10
            },
            timeout=90
        )
        if resposta.status_code == 200:
            return resposta.json()
        return []
    except Exception as e:
        print(f"  Erro Twitter {perfil['usuario']}: {e}")
        return []

def processar_posts(con, posts, perfil, rede):
    url_perfil = f"https://www.instagram.com/{perfil['usuario']}/" if rede == "Instagram" else f"https://twitter.com/{perfil['usuario']}"
    novas = 0

    for post in posts:
        if rede == "Instagram":
            texto = post.get("caption", "") or ""
        else:
            texto = post.get("text", "") or post.get("full_text", "") or ""

        if not is_post_valido(texto):
            continue

        titulo = texto[:100].split("\n")[0].strip()
        descricao = texto[:400]
        uid = hashlib.md5(f"{rede}_{perfil['casa']}_{titulo}".encode()).hexdigest()

        promo = {
            "id": uid,
            "casa": f"{perfil['casa']} ({rede})",
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
        print("APIFY_TOKEN nao configurado, pulando redes sociais")
        return

    con = init_db()
    total = 0

    print(f"\n=== INSTAGRAM ({len(PERFIS_INSTAGRAM)} casas) ===")
    for perfil in PERFIS_INSTAGRAM:
        print(f"Scraping: {perfil['casa']}")
        posts = scrape_instagram(perfil)
        novas = processar_posts(con, posts, perfil, "Instagram")
        print(f"  {len(posts)} posts, {novas} novas promocoes")
        total += novas

    print(f"\n=== TWITTER ({len(PERFIS_TWITTER)} casas) ===")
    for perfil in PERFIS_TWITTER:
        print(f"Scraping: {perfil['casa']}")
        posts = scrape_twitter(perfil)
        novas = processar_posts(con, posts, perfil, "Twitter")
        print(f"  {len(posts)} posts, {novas} novas promocoes")
        total += novas

    print(f"\nTotal redes sociais: {total} novas promocoes")

if __name__ == "__main__":
    main()
