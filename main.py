import os
from datetime import date
from supabase import create_client

# ===== Conexão com Supabase =====
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não encontradas!")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===== Função para salvar/atualizar jogador =====
def save_player(player):
    # Garantir que register_date é string ISO
    if "register_date" in player and isinstance(player["register_date"], date):
        player["register_date"] = player["register_date"].isoformat()

    response = supabase.table("players").select("*").eq("id", player["id"]).execute()
    existing = response.data

    if existing:
        # Atualiza os campos que possam ter mudado
        supabase.table("players").update({
            "name": player["name"],
            "multiplier": player.get("multiplier"),
            "country": player.get("country"),
            "continent": player.get("continent"),
            "division": player.get("division"),
            "trophies_total": player.get("trophies_total", 0),
            "national_league": player.get("national_league", []),
            "national_cup": player.get("national_cup", []),
            "champions_cup": player.get("champions_cup", []),
            "challenge_cup": player.get("challenge_cup", []),
            "conference_cup": player.get("conference_cup", []),
            "register_date": player.get("register_date"),
            "register_season": player.get("register_season")
        }).eq("id", player["id"]).execute()
        print(f"Jogador {player['name']} atualizado!")
    else:
        # Inserir novo jogador
        supabase.table("players").insert({
            "id": player["id"],
            "name": player["name"],
            "multiplier": player.get("multiplier"),
            "country": player.get("country"),
            "continent": player.get("continent"),
            "division": player.get("division"),
            "trophies_total": player.get("trophies_total", 0),
            "national_league": player.get("national_league", []),
            "national_cup": player.get("national_cup", []),
            "champions_cup": player.get("champions_cup", []),
            "challenge_cup": player.get("challenge_cup", []),
            "conference_cup": player.get("conference_cup", []),
            "register_date": player.get("register_date", date.today().isoformat()),
            "register_season": player.get("register_season")
        }).execute()
        print(f"Novo jogador {player['name']} inserido!")

# ===== Simulação de jogadores =====
players_to_add = [
    {
        "id": "101",
        "name": "Rui Simões",
        "multiplier": 1.0,
        "country": "Portugal",
        "continent": "Europe",
        "division": "S1",
        "trophies_total": 3,
        "national_league": ["S1"],
        "national_cup": ["S0"],
        "champions_cup": [],
        "challenge_cup": ["S0"],
        "conference_cup": [],
        "register_date": date.today(),
        "register_season": "Season 1"
    }
]

# ===== Loop para salvar jogadores =====
for player in players_to_add:
    save_player(player)

print("Script a correr no Render! ✅")
