import requests
from flask.cli import load_dotenv

from app.vinile import Vinile
import json
import os

load_dotenv()
DISCOGS_TOKEN = os.getenv('DISCOGS_TOKEN')
if not DISCOGS_TOKEN:
    raise ValueError("DISCOGS_TOKEN not set. Please add it to your .env file")

def cerca_per_barcode(barcode):
    url = f"https://api.discogs.com/database/search?q={barcode}&type=release&token={DISCOGS_TOKEN}"

    vinili_disponibili = []

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        risultato = data["results"][0]
        titolo_completo = risultato["title"]
        artista,album = titolo_completo.split(" - ",1)
        anno = risultato.get("year")
        country = risultato.get("country")
        master_url = risultato["master_url"]
        formato = risultato.get("format", [])
        barcode=risultato.get("barcode",[])

        vinile_input=Vinile(artista, album, anno, country,master_url, formato, None, None, barcode)
        vinile_risultato=estrai_da_master_url(vinile_input)
        vinili_disponibili.append(vinile_risultato)
        return vinili_disponibili
    else:
        return None


def cerca_per_album(album):
    url = f"https://api.discogs.com/database/search?q={album}&type=release&token={DISCOGS_TOKEN}"
    
    response = requests.get(url)

    if response.status_code == 200:

        vinili_disponibili = []
        nome_file='dump_vinili.json'

        percorso_cartella = "Database"
        percorso_sottocartella = "dump"
        percorso_file = os.path.join(percorso_cartella,percorso_sottocartella,nome_file)

        os.makedirs(os.path.dirname(percorso_file), exist_ok=True)

        data = response.json()
        with open(percorso_file, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(data, ensure_ascii=False, indent=4))

        if 'results' in data:
            for risultato in data['results']:
                titolo_completo = risultato["title"]
                artista,album = titolo_completo.split(" - ",1)
                country = risultato.get("country")
                anno = risultato.get("year")
                master_url = risultato["master_url"]
                formato = risultato.get("format",[])
                genres = risultato.get("genres",[])
                style=risultato.get("style",[])
                barcode=risultato.get("barcode",[])
                vinile = Vinile(artista, album,anno,country,master_url,formato,genres,style,barcode)
                vinili_disponibili.append(vinile)
        
        return vinili_disponibili
    else:
        return None

def estrai_da_master_url(vinile):
    url = vinile.master_url
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        genres=data.get("genres",[])
        style=data.get("styles",[])
        vinile2 = Vinile(vinile.artista, vinile.album, vinile.anno, vinile.country, vinile.master_url, vinile.formato, genres, style, vinile.barcode)
        return vinile2
    else:
        return None