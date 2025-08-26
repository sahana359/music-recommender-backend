
from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import Recommender
from spotify_api import search_track


app = Flask(__name__)
CORS(app)
recommender = Recommender()
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    song_title = data.get("song_title")

    if not song_title:
        return jsonify({"error": "Missing input"}), 400

    try:
        recs = recommender.get_recommendations(song_title)

        import math
        results = []
        for rec in recs:
            song = rec.get("track_name")
            artist = rec.get("track_artist")
            # Replace NaN with None
            if isinstance(artist, float) and math.isnan(artist):
                artist = None
            if isinstance(song, float) and math.isnan(song):
                song = None
            metadata = search_track(song, artist)
            if metadata:
                results.append({
                    "song": song,
                    "artist": artist,
                    "metadata": metadata
                })
            else:
                results.append({
                    "song": song,
                    "artist": artist,
                    "metadata": None
                })

        return jsonify({"recommendations": results})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# New endpoint: /search_songs
import pandas as pd
import os

@app.route("/search_songs", methods=["POST"])
def search_songs():
    data = request.get_json()
    keyword = data.get("keyword", "").strip().lower()
    if not keyword:
        return jsonify({"error": "Missing keyword"}), 400

    # Load CSV
    csv_path = os.path.join(os.path.dirname(__file__), "model", "df.csv")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return jsonify({"error": f"Could not load songs: {str(e)}"}), 500

    # Filter songs starting with keyword (case-insensitive)
    matches = df[df["track_name"].str.lower().str.startswith(keyword)]
    track_names = matches["track_name"].head(10).tolist()
    return jsonify({"songs": track_names})

if __name__ == "__main__":
    app.run(debug=True)