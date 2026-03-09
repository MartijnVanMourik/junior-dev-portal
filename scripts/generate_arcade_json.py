import json
import re
import os
import csv
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
        if os.path.isdir(folder_path) and re.match(r'^[0-9]{4}-[0-9]{4}$', folder_name):
            years.append(folder_name)
            
    # Bepaal het laatste jaar voor inkomende CSV data
    latest_year = years[-1] if years else None

    # Lees CSV bestand indien aanwezig in datasources map
    csv_file = os.path.join(datasources_dir, 'ingeleverde_games.csv')
    csv_games = []
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8', errors='replace') as f:
            dialect = csv.excel
            try:
                sample = f.read(1024)
                f.seek(0)
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample, delimiters=',;')
            except Exception:
                pass
                
            reader = list(csv.reader(f, dialect=dialect))
            if reader:
                headers = reader[0]
                name_idx, author_idx, url_idx = -1, -1, -1
                for i, h in enumerate(headers):
                    hl = h.lower()
                    if any(kw in hl for kw in ['naam', 'titel', 'name', 'game']):
                        if name_idx == -1: name_idx = i
                    if any(kw in hl for kw in ['maker', 'auteur', 'leerling', 'author', 'wie']):
                        if author_idx == -1: author_idx = i
                    if any(kw in hl for kw in ['link', 'url', 'makecode', 'deel']):
                        if url_idx == -1: url_idx = i
                
                for row in reader[1:]:
                    url = row[url_idx] if url_idx != -1 and url_idx < len(row) else ''
                    name = row[name_idx] if name_idx != -1 and name_idx < len(row) else ''
                    author = row[author_idx] if author_idx != -1 and author_idx < len(row) else ''
                    
                    if url_idx == -1:
                        # Als we geen geldige unieke kolom vinden, zoek door row cells heen
                        for cell in row:
                            if extract_id(cell):
                                url = cell
                                break
                    
                    share_id = extract_id(url)
                    if share_id:
                        if not name: name = f"Project {share_id[:5]}"
                        if not author: author = "MakeCode Arcade"
                        game_obj = {
                            "name": name.strip(),
                            "author": author.strip(),
                            "shareId": share_id,
                            "customImage": "assets/backup.jpg" # Pad vanuit kiosk.html referentie
                        }
                        csv_games.append(game_obj)
        print(f"CSV Ingelezen: {len(csv_games)} games gevonden in CSV.")

    for folder_name in years:
        folder_path = os.path.join(datasources_dir, folder_name)
        input_file = os.path.join(folder_path, 'links.txt')
        json_file = os.path.join(folder_path, 'games.json')
        
        games_dict = {} # Deduplicatie via een interne dict
        
        if os.path.exists(input_file):
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
                            "customImage": "assets/backup.jpg"
                        }
                        
                        games_dict[share_id] = game_obj

        # Voeg games uit de CSV toe aan de huidige (laatste) jaargang
        if folder_name == latest_year:
            for game in csv_games:
                games_dict[game["shareId"]] = game # Overschrijft eventuele oude data/links

        games_list = list(games_dict.values())
        
        # Sorteer games op titel (ascending), head-on case insensitive
        games_list.sort(key=lambda x: x['name'].lower())

        # Push to all_games list deduplicator
        for game in games_list:
            all_games[game["shareId"]] = game

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(games_list, f, indent=2)
        print(f"Jaar {folder_name}: {len(games_list)} games (Gesorteerd).")
            
    # Genereer de 'all' folder
    all_folder = os.path.join(datasources_dir, 'all')
    os.makedirs(all_folder, exist_ok=True)
    all_games_list = list(all_games.values())
    all_games_list.sort(key=lambda x: x['name'].lower())
    
    with open(os.path.join(all_folder, 'games.json'), 'w', encoding='utf-8') as f:
        json.dump(all_games_list, f, indent=2)
    print(f"Totaal unieke games verzameld in 'all/games.json': {len(all_games_list)}")

    # Maak de globale index aan
    index_data = {
        "years": years,
        "latest": latest_year
    }
    
    with open(os.path.join(datasources_dir, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2)
    print(f"Index.json gegenereerd. Meest recente jaar ingesteld op: {latest_year}.")

if __name__ == "__main__":
    generate_fresh_json()