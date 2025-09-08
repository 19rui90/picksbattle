import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import create_client
import json

# ----------------------
# Configurações Supabase
# ----------------------
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ----------------------
# Dicionário de continentes
# ----------------------
CONTINENTS = {
    "Europe": ["Portugal", "France", "Spain", "Germany", "Italy", "Netherlands", "Belgium", "Sweden", "Switzerland", "Denmark", "Ireland", "Greece", "Hungary", "Poland", "Romania", "Scotland", "Northern Ireland", "Wales"],
    "Asia": ["Japan", "China", "India", "South Korea", "Singapore"],
    "South America": ["Argentina", "Brazil", "Chile", "Colombia", "Bolivia", "Peru", "Paraguay", "Uruguay", "Venezuela", "Ecuador"],
    "North America": ["Canada", "United States", "Costa Rica", "Mexico"],
    "Africa": ["Nigeria", "South Africa", "Morocco", "Egypt"],
    "Oceania": ["Australia"]
}

# ----------------------
# Países e divisões
# ----------------------
COUNTRIES = ["Argentina","Australia","Austria","Belgium","Bolivia","Brazil","Bulgaria","Canada","Chile","China","Colombia","Costa Rica","Czech Republic","Denmark","Ecuador","Egypt","England","France","Germany","Greece","Hungary","India","Ireland","Italy","Japan","Mexico","Morocco","Netherlands","Nigeria","Northern Ireland","Norway","Paraguay","Peru","Poland","Portugal","Rest of World","Romania","Scotland","Singapore","Slovakia","South Africa","South Korea","Spain","Sweden","Switzerland","Turkey","United States","Uruguay","Venezuela","Wales"]

DIVISIONS = ["Top Series","Div 1.1","Div 1.2","Div 1.3","Div 2.1","Div 2.2","Div 2.3","Div 2.4","Div 2.5","Div 2.6","Div 2.7","Div 2.8","Div 2.9"]

# ----------------------
# Funções auxiliares
# ----------------------
def get_continent(country):
    for continent, countries in CONTINENTS.items():
        if country in countries:
            return continent
    return "Unknown"

def fetch_players(country, division):
    # API principal
    url = f"https://picksbattle.com/api/leagueTableData?country={country}&division={division}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao buscar {country} - {division}")
        return []

    data = response.json()
    players = []

    for p in data:
        player = {
            "id": p["USER_ID"],
            "name": p["PLAYER_NAME"],
            "multiplier": float(p["MULTIPLIER"]),
            "country": country,
            "continent": get_continent(country),
            "division": division,
            # Inicializa troféus vazios
            "trophies_total": 0,
            "national_league": [],
            "national_cup": [],
            "champions_cup": [],
            "challenge_cup": [],
            "conference_cup": [],
            "register_date": None,
            "register_season": None
        }
        # HTML scraping do player
        player_html_url = f"https://picksbattle.com/playercentre?userId={p['USER_ID']}"
        html_resp = requests.get(player_html_url)
        if html_resp.status_code == 200:
            soup = BeautifulSoup(html_resp.text, "html.parser")
            
            # Trophies
            trophies = soup.select(".playerCenter-trophies")
            for t in trophies:
                title = t.select_one(".trophy-title-block strong").text.strip()
                seasons = [s.text.strip() for s in t.select(".season-label")]
                if title == "National League":
                    player["national_league"] = seasons
                elif title == "National Cup":
                    player["national_cup"] = seasons
                elif title == "Champions Cup":
                    player["champions_cup"] = seasons
                elif title == "Challenge Cup":
                    player["challenge_cup"] = seasons
                elif title == "Conference Cup":
                    player["conference_cup"] = seasons
            player["trophies_total"] = sum(len(player[key]) for key in ["national_league","national_cup","champions_cup","challenge_cup","conference_cup"])
            
            # Register season e date
            # Aqui podemos pegar da primeira temporada visível ou do HTML de registro
            player["register_season"] = soup.select_one(".season-label").text.strip() if soup.select_one(".season-label") else None
            player["register_date"] = datetime.today().date()
        
        players.append(player)
    return players

def save_to_db(players):
    for p in players:
        supabase.table("players").upsert(p, on_conflict="id").execute()

# ----------------------
# Loop principal
# ----------------------
while True:
    for country in COUNTRIES:
        for division in DIVISIONS:
            print(f"Buscando jogadores: {country} - {division}")
            try:
                players = fetch_players(country, division)
                save_to_db(players)
                print(f"{len(players)} jogadores salvos.")
            except Exception as e:
                print(f"Erro: {e}")
    print("Aguardando 15 minutos para próxima atualização...")
    time.sleep(900)
