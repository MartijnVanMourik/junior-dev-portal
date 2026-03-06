import json
import re
import os
import glob

def extract_id(url):
    match = re.search(r'([S_][0-9]{5}-[0-9]{5}-[0-9]{5}-[0-9]{5}|[S_][0-9]{5}-[0-9]{5})', url)
    return match.group(1) if match else None

def generate_fresh_json():
    # Bepaal de paden relatief aan de locatie van dit script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    datasources_dir = os.path.join(project_root, 'datasources')
    
    if not os.path.exists(datasources_dir):
        print(f"Fout: Mapping '{datasources_dir}' niet gevonden.")
        return

    all_games = {} # Voor deduplicatie over alle jaren heen
    years = []
    
    # Loop over alle mappen in datasources heen
    for folder_name in sorted(os.listdir(datasources_dir)):
        folder_path = os.path.join(datasources_dir, folder_name)
        
        # Check of het een jaartal-formaat is (bijv. 2024-2025)
        if os.path.isdir(folder_path) and re.match(r'^[0-9]{4}-[0-9]{4}$', folder_name):
            years.append(folder_name)
            
            input_file = os.path.join(folder_path, 'links.txt')
            json_file = os.path.join(folder_path, 'games.json')
            
            # Waarschuwing als er geen bronbestand is
            if not os.path.exists(input_file):
                print(f"Waarschuwing: '{input_file}' ontbreekt in jaarmap.")
                continue
                
            games_list = []
            with open(input_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('//'): continue
                    
                    parts = line.split('#')
                    url_part = parts[0].strip()
                    
                    share_id = extract_id(url_part)
                    if share_id:
                        display_info = parts[1].strip() if len(parts) > 1 else f"Project {share_id[:5]}"
                        
                        name = display_info
                        author = "MakeCode Arcade"
                        if " - " in display_info:
                            name, author = display_info.split(" - ", 1)
                        elif " door " in display_info:
                            name, author = display_info.split(" door ", 1)

                        game_obj = {
                            "name": name.strip(),
                            "author": author.strip(),
                            "shareId": share_id,
                            "customImage": "assets/backup.jpg" # Pad vanuit kiosk.html referentie
                        }
                        
                        games_list.append(game_obj)
                        all_games[share_id] = game_obj # Voor de 'all' lijst (overschrijft dubbelen met unieke ID)
                        
            # Bewaar de specifieke jaar-lijst
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(games_list, f, indent=2)
            print(f"Jaar {folder_name}: {len(games_list)} games.")
            
    # Genereer de 'all' folder met alle samengevoegde, unieke games
    all_folder = os.path.join(datasources_dir, 'all')
    os.makedirs(all_folder, exist_ok=True)
    all_games_list = list(all_games.values())
    
    with open(os.path.join(all_folder, 'games.json'), 'w', encoding='utf-8') as f:
        json.dump(all_games_list, f, indent=2)
    print(f"Totaal unieke games verzameld in 'all/games.json': {len(all_games_list)}")

    # Maak de globale index aan
    years.sort()
    index_data = {
        "years": years,
        "latest": years[-1] if years else None
    }
    
    with open(os.path.join(datasources_dir, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2)
    print(f"Index.json gegenereerd. Meest recente jaar ingesteld op: {index_data['latest']}.")

if __name__ == "__main__":
    generate_fresh_json()