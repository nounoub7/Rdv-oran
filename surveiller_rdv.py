import requests
import time
from datetime import datetime

TOKEN = "8726284365:AAFjP9rZInV6w0ClwKUdtovQ0z05WXfcgws"
CHAT_ID = "5841992286"

URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/2da8fb6f4ac7361929959598a1e5b1e45/#services"
CHECK_INTERVAL = 30

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9,fr;q=0.8",
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})
    print("✅ Message Telegram envoyé !")

def check_availability():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        html = response.text.lower()
        negative_keywords = ["no hay citas disponibles", "no existen citas", "no disponible", "sin citas"]
        positive_keywords = ["cita disponible", "seleccione", "fecha disponible", "disponible"]
        for kw in negative_keywords:
            if kw in html:
                return False, f"Pas de créneau : '{kw}'"
        for kw in positive_keywords:
            if kw in html:
                return True, f"Disponible : '{kw}'"
        return False, "Aucun indicateur clair"
    except Exception as e:
        return False, f"Erreur : {e}"

def main():
    print("Surveillance RDV — Consulat d'Oran")
    print(f"Vérification toutes les {CHECK_INTERVAL} secondes...\n")
    send_telegram("🟢 Bot démarré ! Je surveille les RDV du Consulat d'Oran...")
    alerte_envoyee = False
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        disponible, message = check_availability()
        if disponible:
            print(f"[{now}] 🟢 DISPONIBLE ! {message}")
            if not alerte_envoyee:
                send_telegram(f"🚨 CRÉNEAU DISPONIBLE !\n\nConsulat d'Oran — Légalisation\n\n👉 Va vite sur le site :\n{URL}\n\nDétecté à {now}")
                alerte_envoyee = True
        else:
            print(f"[{now}] 🔴 Pas de créneau. {message}")
            alerte_envoyee = False
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
