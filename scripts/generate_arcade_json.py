import json
import re
import os

def extract_id(url):
    match = re.search(r'([S_][0-9]{5}-[0-9]{5}-[0-9]{5}-[0-9]{5}|[S_][0-9]{5}-[0-9]{5})', url)
    return match.group(1) if match else None

def generate_fresh_json():
    # Bepaal de paden relatief aan de locatie van dit script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    input_file = os.path.join(project_root, 'assets', 'links.txt')
    json_file = os.path.join(project_root, 'assets', 'games.json')
    
    if not os.path.exists(input_file):
        print(f"Fout: '{input_file}' niet gevonden.")
        return

    games_list = []
    
    with open(input_file, 'r') as f:
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

                games_list.append({
                    "name": name.strip(),
                    "author": author.strip(),
                    "shareId": share_id,
                    "customImage": "assets/backup.png" # Pad vanaf de index.html gezien
                })

    with open(json_file, 'w') as f:
        json.dump(games_list, f, indent=2)
    
    print(f"Succes! {len(games_list)} games verwerkt naar assets/games.json.")

if __name__ == "__main__":
    generate_fresh_json()