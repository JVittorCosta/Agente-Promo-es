import asyncio
from playwright.async_api import async_playwright
import sqlite3
import hashlib
from datetime import datetime

CASAS = [
    {"nome": "Bolsa de Aposta", "url": "https://bolsadeaposta.bet.br/b/exchange/custom-markets"},
    {"nome": "Lottu", "url": "https://www.lottu.bet.br/sports"},
    {"nome": "Sporty", "url": "https://www.sporty.bet.br/br/promotions/"},
    {"nome": "Betsson", "url": "https://www.betsson.bet.br/promocoes?filter=sportsbook"},
    {"nome": "Esportes da Sorte", "url": "https://esportesdasorte.bet.br/ptb/bet/main"},
    {"nome": "Jogo de Ouro", "url": "https://jogodeouro.bet.br/pt/promotions/sports"},
    {"nome": "Betsul", "url": "https://betsul.bet.br/beneficios"},
    {"nome": "MCGames", "url": "https://blog.mcgames.bet.br/novidades/"},
    {"nome": "Betano", "url": "https://www.betano.bet.br/"},
    {"nome": "Sportingbet", "url": "https://www.sportingbet.bet.br/pt-br/promo/offers/p/sportsbook"},
    {"nome": "KTO", "url": "https://www.kto.bet.br/promo/sports"},
    {"nome": "F12 Bet", "url": "https://f12.bet.br/promocao/"},
    {"nome": "Lottoland", "url": "https://www.lottoland.bet.br/ofertas#esportes"},
    {"nome": "Sorteo Online", "url": "https://www.sorteonline.bet.br/ofertas#Aposta-Esportiva"},
    {"nome": "BetMGM", "url": "https://www.betmgm.bet.br/promocoes"},
    {"nome": "Vbet", "url": "https://www.vbet.bet.br/pb/promotions/sport"},
    {"nome": "Bet Esporte", "url": "https://betesporte.bet.br/sports/desktop/promotions"},
    {"nome": "Betfair", "url": "https://www.betfair.bet.br/apostas/"},
    {"nome": "Viva Sorte", "url": "https://vivasorte.bet.br/promocoes"},
    {"nome": "Novibet", "url": "https://www.novibet.bet.br/apostas-esportivas"},
    {"nome": "Versus", "url": "https://www.versus.bet.br/promos"},
    {"nome": "Rivalo", "url": "https://www.rivalo.bet.br/pt/promotions"},
    {"nome": "Rei do Pitaco", "url": "https://reidopitaco.bet.br/promocoes?tab=all"},
    {"nome": "Meridian Bet", "url": "https://meridianbet.bet.br/promo/ca/category/1413"},
    {"nome": "7K Bet", "url": "https://7k.bet.br/promotions"},
    {"nome": "Vera Bet", "url": "https://vera.bet.br/promotions"},
    {"nome": "Bet Nacional", "url": "https://betnacional.bet.br/"},
    {"nome": "Pix Bet", "url": "https://pix.bet.br/sports"},
    {"nome": "Galera Bet", "url": "https://www.galera.bet.br/promocoes"},
    {"nome": "Betwarrior", "url": "https://apostas.betwarrior.bet.br/pt-br/sports/home"},
    {"nome": "Esportiva", "url": "https://esportiva.bet.br/sports"},
    {"nome": "Superbet", "url": "https://superbet.bet.br/promocoes-e-bonus"},
    {"nome": "Bateu Bet", "url": "https://bateu.bet.br/promotions"},
    {"nome": "Seu Bet", "url": "https://www.seu.bet.br/promocoes"},
    {"nome": "Faz1 Bet", "url": "https://faz1.bet.br/br/sportsbook/prematch"},
    {"nome": "Betfast", "url": "https://betfast.bet.br/br/static/promos"},
    {"nome": "Bet da Sorte", "url": "https://www.betdasorte.bet.br/sports"},
    {"nome": "Betao", "url": "https://betao.bet.br/pb/promotions/sport"},
    {"nome": "Casa de Apostas", "url": "https://casadeapostas.bet.br/br/promo"},
    {"nome": "H2 Bet", "url": "https://www.h2.bet.br/promocoes"},
    {"nome": "Brasil da Sorte", "url": "https://www.brasildasorte.bet.br/"},
    {"nome": "Seguro Bet", "url": "https://www.seguro.bet.br/promocoes"},
    {"nome": "BR4 Bet", "url": "https://br4.bet.br/sports#/overview"},
    {"nome": "Lotogreen", "url": "https://lotogreen.bet.br/sports#/overview"},
    {"nome": "Golde Bet", "url": "https://goldebet.bet.br/sports#/overview"},
    {"nome": "Alfa Bet", "url": "https://alfa.bet.br/promocoes"},
    {"nome": "Luva Bet", "url": "https://luva.bet.br/promotions?category=1000290"},
    {"nome": "Hiper Bet", "url": "https://hiper.bet.br/ptb/contents/promotions"},
    {"nome": "Estrela Bet", "url": "https://www.estrelabet.bet.br/ofertas"},
    {"nome": "Aposta Ganha", "url": "https://apostaganha.bet.br/?open_promo_modal=true"},
    {"nome": "Stake", "url": "https://stake.bet.br/esportes/home"},
    {"nome": "4Play Bet", "url": "https://4play.bet.br/promocoes"},
    {"nome": "Pagol", "url": "https://pagol.bet.br/br/promocoes/promo"},
    {"nome": "BRX Bet", "url": "https://brx.bet.br/promotions"},
    {"nome": "Bulls Bet", "url": "https://bullsbet.bet.br/sports?eventlistTab=Early"},
    {"nome": "Lance de Sorte", "url": "https://lancedesorte.bet.br/sports/desktop/promotions"},
    {"nome": "Apostou", "url": "https://www.apostou.bet.br/promotions"},
    {"nome": "Bravo Bet", "url": "https://bravo.bet.br/promocoes"},
    {"nome": "BR Bet", "url": "https://www.brbet.bet.br/sports#/overview"},
    {"nome": "MMA Bet", "url": "https://mmabet.bet.br/sports/"},
    {"nome": "Multi Bet", "url": "https://multi.bet.br/pb/promotions/sports"},
    {"nome": "Bet VIP", "url": "https://betvip.bet.br/promotions"},
    {"nome": "Aposta Tudo", "url": "https://apostatudo.bet.br/sports"},
    {"nome": "Ganhei Bet", "url": "https://ganhei.bet.br/promotions"},
    {"nome": "Play Bet", "url": "https://play.bet.br/sports"},
    {"nome": "Up Bet", "url": "https://up.bet.br/pt-BR/pages/promocoes#/overview"},
    {"nome": "Start Bet", "url": "https://start.bet.br/promotions"},
    {"nome": "Band Bet", "url": "https://www.bandbet.bet.br/promocoes"},
]

KEYWORDS = {
    "aposta_gratis": ["aposta gratis", "aposta grátis", "free bet", "freebet", "aposta sem risco", "aposte e ganhe", "freebet", "superodds", "comboboost"],
    "cashback": ["cashback esport", "cashback futebol", "cashback aposta", "cashback semanal esport"],
    "super_odds": ["super odds", "odds aumentadas", "odds turbinadas", "boost", "superodds", "super aposta turbinada", "turbinada", "mega impulso", "ou anula", "odds melhoradas"],
    "bonus": ["bonus boas-vindas", "bonus primeiro deposito", "bonus esport"],
}

PALAVRAS_PROMO_ESPORTE = [
    "aposta gratis", "aposta grátis", "freebet", "free bet",
    "super odds", "superodds", "odds aumentadas", "odds turbinadas",
    "odds melhoradas", "boost", "turbinada", "turbinado",
    "mega impulso", "ou anula", "aposte e ganhe",
    "cashback futebol", "cashback esport", "cashback aposta",
    "cashback champions", "cashback libertadores", "cashback brasileirao",
    "bonus futebol", "bonus esport", "bonus aposta",
    "acumulador", "combo boost", "comboboost",
    "aposta sem risco", "reembolso futebol", "reembolso esport",
    "kings league", "champions league", "libertadores", "brasileirao",
    "copa do brasil", "europa league", "premier league",
    "freebet todos os dias", "liga da galera",
    "super aposta turbinada", "super odds bds",
]

PALAVRAS_CASSINO = [
    "cassino", "casino", "slot", "slots", "roleta", "blackjack",
    "poker", "pôquer", "baccarat", "caça-niquel", "jackpot",
    "crash", "mines", "aviator", "fortune", "pragmatic", "pgsoft",
    "spribe", "evolution", "bacbo", "dragon tiger", "giros",
    "giro gratis", "giro grátis", "rodadas gratis", "rodadas grátis",
    "tigre", "gates", "sugar rush", "sweet bonanza", "big bass",
    "wild", "scatter", "fruit", "book of", "diamond",
    "bonus buy", "ante bet", "hold and win", "sortudo",
    "raspadinha", "popok", "evoplay", "aviatrix", "fortune rabbit",
    "fortune snake", "fortune tiger", "fortune ox", "rico gorila",
    "jaguar dojo", "rico rabbit", "rico dj", "yo dragon",
    "torneio evoplay", "superspin", "supercoins", "supercoins",
]

PALAVRAS_LIXO = [
    "cookie", "privacidade", "termos e condicoes", "você concorda",
    "saiba mais sobre", "política de privacidade",
    "é seguro apostar", "como funciona", "o que é",
    "format", "decimal", "americanas", "hongkong",
    "minha conta", "notificacoes", "chat social", "depositar",
    "retirada", "historico", "detalhes da conta", "verificacao",
    "jogo responsavel", "configuracoes", "ajuda", "suporte",
    "você está sendo bloqueado", "unable to access", "sorry",
    "você foi bloqueado", "blocked",
    "onde assistir", "horario e odds", "ao vivo:",
    "1º tempo", "2º tempo", "ambos os tempos",
    "ganhador", "empate", "suspenso",
    "esportes ativos", "ao vivo",
    "não é permitido apostar com recursos",
]

PALAVRAS_ESPECIAIS = {
    "Lottu": ["super aposta turbinada"],
    "Esportes da Sorte": ["super aposta turbinada"],
    "Brasil da Sorte": ["super odds bds", "odds aumentadas", "freebet", "bonus acumulador"],
    "Bulls Bet": ["mega impulso"],
    "Bet VIP": ["odds aumentadas"],
    "Aposta Tudo": ["superodds"],
    "Play Bet": ["turbinada da play"],
    "Bolsa de Aposta": ["ou anula"],
    "Stake": ["aposte e ganhe"],
    "Ganhei Bet": ["superodds", "comboboost", "quiz", "bolao europeu"],
}

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

def detectar_tipo(titulo, descricao):
    texto = (titulo + " " + descricao).lower()
    for tipo, palavras in KEYWORDS.items():
        if any(p in texto for p in palavras):
            return tipo
    return "outro"

def is_valido(titulo, casa_nome):
    t = titulo.lower().strip()

    if len(t) < 10 or len(t) > 150:
        return False

    for lixo in PALAVRAS_LIXO:
        if lixo in t:
            return False

    for cassino in PALAVRAS_CASSINO:
        if cassino in t:
            return False

    palavras_especiais = PALAVRAS_ESPECIAIS.get(casa_nome, [])
    if any(p in t for p in palavras_especiais):
        return True

    if any(p in t for p in PALAVRAS_PROMO_ESPORTE):
        return True

    return False

def salvar_novas(con, promos):
    novas = []
    for p in promos:
        try:
            con.execute(
                "INSERT INTO promocoes VALUES (?,?,?,?,?,?,?,0)",
                (p["id"], p["casa"], p["titulo"], p["descricao"],
                 p["url"], p["tipo"], p["data_coleta"])
            )
            novas.append(p)
        except sqlite3.IntegrityError:
            pass
    con.commit()
    return novas

async def scrape_casa(browser, casa):
    page = await browser.new_page()
    try:
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        await page.goto(casa["url"], timeout=25000, wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)

        elementos = await page.query_selector_all(
            "h1, h2, h3, h4, "
            "[class*='promo'], [class*='offer'], [class*='banner'], "
            "[class*='promotion'], [class*='boost'], "
            "[class*='turbin'], [class*='impulso'], [class*='odds']"
        )

        promos = []
        titulos_vistos = set()

        for el in elementos[:50]:
            try:
                titulo = (await el.inner_text()).strip()
                titulo = titulo.split("\n")[0].strip()
            except:
                continue

            if titulo in titulos_vistos:
                continue

            if not is_valido(titulo, casa["nome"]):
                continue

            titulos_vistos.add(titulo)

            desc = ""
            try:
                parent = await el.evaluate_handle(
                    "el => el.closest('article, section, li') || el.parentElement"
                )
                desc_full = (await parent.as_element().inner_text()).strip()
                desc = desc_full[:300]
            except:
                pass

            uid = hashlib.md5(f"{casa['nome']}{titulo}".encode()).hexdigest()
            promos.append({
                "id": uid,
                "casa": casa["nome"],
                "titulo": titulo,
                "descricao": desc,
                "url": casa["url"],
                "tipo": detectar_tipo(titulo, desc),
                "data_coleta": datetime.now().isoformat(),
            })

        print(f"{casa['nome']}: {len(promos)} promocoes validas")
        return promos

    except Exception as e:
        print(f"Erro em {casa['nome']}: {e}")
        return []
    finally:
        await page.close()

async def main():
    con = init_db()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for casa in CASAS:
            promos = await scrape_casa(browser, casa)
            novas = salvar_novas(con, promos)
            print(f"  -> {len(novas)} novas salvas")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
