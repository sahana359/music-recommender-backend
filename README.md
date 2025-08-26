# Music Recommender Backend

This is the backend for the Music Recommender app.

## Demo Video
- [Watch the demo](https://www.youtube.com/watch?v=j7ncdhlwny4)

## Related Repositories
- [Frontend](https://github.com/sahana359/music-recommender-frontend)
- [Model-Training] (https://github.com/sahana359/music-recommender-ml)

## Features
- Song recommendations based on input track
- Spotify API for metadata
- Search for songs by keyword

## Setup
1. Install dependencies:
   pip install -r requirements.txt

2. Run the backend server:
   python app.py

## Endpoints
- `/recommend` (POST): Get recommendations for a song title
- `/search_songs` (POST): Search for songs suggestions by keyword

## Environment
- Python 3.8+
- Flask
- pandas

## Model files
- Model and dataset files in the `model/` directory

