import os
from supabase import create_client, Client

# Configurações Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    print("Script a correr no Render!")
    # Aqui vais colocar o teu código para extrair dados do PicksBattle
    # e gravar na base de dados Supabase
    # Por exemplo: consulta jogadores, guarda no supabase, etc.

if __name__ == "__main__":
    main()
