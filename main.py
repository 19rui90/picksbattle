import os
from datetime import datetime
from supabase import create_client

# ===== Conexão com Supabase =====
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não encontradas!")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===== Função para salvar/atualizar jogador =====
def save_player(player):
    # Verifica se o jogador já existe
    response = supabase.table("players").select("*").eq("player_id", player["id"]).execute()
    existing = response.data

    if existing:
        # Se atributos mudaram, atualiza
        if existing[0]["stats"] != player["stats"]:
            supabase.table("players").update({
                "stats": player["stats"],
                "updated_at": datetime.utcnow().isoformat()
            }).eq("player_id", player["id"]).execute()
            print(f"Jogador {player['name']} atualizado!")
        else:
            print(f"Jogador {player['name']} sem alterações.")
    else:
        # Inserir novo jogador
        supabase.table("players").insert({
            "player_id": player["id"],
            "name": player["name"],
            "age": player["age"],
            "nationality": player["nationality"],
            "stats": player["stats"],
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        print(f"Novo jogador {player['name']} inserido!")

# ===== Simulação de extração de jogadores =====
# Substitui esta lista pelo teu scraping ou API real
players_to_add = [
    {
        "id": 101,
        "name": "Rui Simões",
        "age": 18,
        "nationality": "Portugal",
        "stats": {"attack": 75, "defense": 60, "speed": 80}
    },
    {
        "id": 102,
        "name": "João Silva",
        "age": 19,
        "nationality": "Portugal",
        "stats": {"attack": 65, "defense": 70, "speed": 75}
    }
]

# ===== Loop para salvar jogadores =====
for player in players_to_add:
    save_player(player)

print("Script a correr no Render! ✅")
