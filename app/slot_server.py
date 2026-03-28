import os
import json
import random
import socketserver
from datetime import datetime

DATA_DIR = "/data"
STATS_FILE = os.path.join(DATA_DIR, "stats.json")
SYMBOLS = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]

os.makedirs(DATA_DIR, exist_ok=True)

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"plays": 0, "jackpots": 0}

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

def spin_once(stats):
    spin = [random.choice(SYMBOLS) for _ in range(3)]
    stats["plays"] += 1
    jackpot = (spin[0] == spin[1] == spin[2])
    if jackpot:
        stats["jackpots"] += 1

    lines = [
        "🎰 SLOT MACHINE 🎰",
        f"[ {spin[0]} | {spin[1]} | {spin[2]} ]",
        "💰 JACKPOT!!!" if jackpot else "❌ Ritenta!",
        f"Giocate totali: {stats['plays']}",
        f"Jackpot: {stats['jackpots']}",
        f"Ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    return "\n".join(lines)

class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(
            ("Benvenuto nella Slot Machine!\n"
             "Comandi: spin | stats | help | quit\n\n").encode("utf-8")
        )

        while True:
            self.wfile.write(b"> ")
            line = self.rfile.readline()
            if not line:
                break

            cmd = line.decode("utf-8", errors="ignore").strip().lower()

            if cmd in ("quit", "exit"):
                self.wfile.write(b"Ciao!\n")
                break

            if cmd in ("help", "?"):
                self.wfile.write(b"Comandi: spin | stats | help | quit\n\n")
                continue

            if cmd == "stats":
                stats = load_stats()
                self.wfile.write(
                    (f"Giocate totali: {stats['plays']}\n"
                     f"Jackpot: {stats['jackpots']}\n\n").encode("utf-8")
                )
                continue

            if cmd == "spin":
                stats = load_stats()
                out = spin_once(stats)
                save_stats(stats)
                self.wfile.write((out + "\n").encode("utf-8"))
                continue

            self.wfile.write(b"Comando non valido. Usa: spin | stats | help | quit\n\n")

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == "__main__":
    print("Slot server in ascolto su 0.0.0.0:7777", flush=True)
    with ThreadingTCPServer(("0.0.0.0", 7777), Handler) as server:
        server.serve_forever()