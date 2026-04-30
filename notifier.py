import requests
import sqlite3
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

EMOJIS = {
    "aposta_gratis": "🎁",
    "cashback": "💰",
    "super_odds": "🚀",
    "bonus": "🎯",
    "missao": "🏆",
    "outro": "📢",
}

def enviar(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    )

def notificar():
    con = sqlite3.connect("promocoes.db")
    pendentes = con.execute(
        "SELECT id, casa, titulo, descricao, url, tipo FROM promocoes WHERE notificado=0"
    ).fetchall()

    for id_, casa, titulo, desc, url, tipo in pendentes:
        emoji = EMOJIS.get(tipo, "📢")
        msg = (
            f"{emoji} <b>{casa}</b>\n"
            f"<b>{titulo}</b>\n"
            f"{desc[:200]}\n"
            f"🔗 {url}"
        )
        enviar(msg)
        con.execute("UPDATE promocoes SET notificado=1 WHERE id=?", (id_,))
        con.commit()

    print(f"{len(pendentes)} notificacoes enviadas")

if __name__ == "__main__":
    notificar()
