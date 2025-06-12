# Music Library
This app allows you to search for albums and artists in a database of vinyl, CD and cassette powered by Discogs and save them in 
your local library. The app uses the Discogs API to fetch data from the database.

## Requirements
- Python 3.11
``` bash
pip install -r requirements.txt
```
## Docker
``` bash
docker build -t music_library .
docker run -it -p 5002:5002 music_library
```
## Usage
``` bash
python main.py
```

## Credits
This app uses the [Discogs API](https://www.discogs.com/developers/) to fetch album and artist information.
All data retrieved is licensed under [CC0 1.0 Universal (Public Domain Dedication)](https://creativecommons.org/public-domain/cc0/).
Data provided by Discogs.
