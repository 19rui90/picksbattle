import time
import requests
from datetime import date
from supabase import create_client
from dotenv import load_dotenv
import os

# carregar variáveis de ambiente
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===== Função para salvar/atualizar jogador =====
def save_player(player):
    supabase.table("players").upsert(player).execute()
    print(f"Jogador {player['name']} guardado/atualizado!")

# ===== Função para buscar jogadores reais do PicksBattle =====
def fetch_players():
    url = "AQUI_VAI_O_ENDPOINT_DOS_JOGADORES"
    response = requests.get(url)
    data = response.json()

    players = []
    for p in data:  # depende da estrutura do JSON que a API devolver
        players.append({
            "id": p["id"],
            "name": p["name"],
            "multiplier": p.get("multiplier", 1.0),
            "country": p.get("country"),
            "continent": p.get("continent"),
            "division": p.get("division"),
            "trophies_total": p.get("trophies_total", 0),
            "national_league": p.get("national_league", []),
            "national_cup": p.get("national_cup", []),
            "champions_cup": p.get("champions_cup", []),
            "challenge_cup": p.get("challenge_cup", []),
            "conference_cup": p.get("conference_cup", []),
            "register_date": p.get("register_date", date.today().isoformat()),
            "register_season": p.get("register_season")
        })
    return players

# ===== Loop infinito =====
while True:
    jogadores = fetch_players()
    for j in jogadores:
        save_player(j)
    print("✅ Atualização completa, a dormir 60s...")
    time.sleep(60)
