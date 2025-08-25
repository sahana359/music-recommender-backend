import pandas as pd
import pickle
import os

class Recommender:
    def __init__(self, base_path="model"):
        df_path = os.path.join(base_path, "df.csv")
        embeddings_path = os.path.join(base_path, "embeddings.pkl")
        model_path = os.path.join(base_path, "nn_model.pkl")

        self.df = pd.read_csv(df_path, on_bad_lines='skip')
        self.df['track_name'] = self.df['track_name'].str.lower()

        with open(embeddings_path, "rb") as f:
            self.embeddings = pickle.load(f)
        with open(model_path, "rb") as f:
            self.nn_model = pickle.load(f)

    def get_recommendations(self, song_title, top_n=10):
        song_title = song_title.lower()
        if song_title not in self.df['track_name'].values:
            return {"error": "Song not found in dataset."}

        idx = self.df[self.df['track_name'] == song_title].index[0]
        query_embedding = self.embeddings[idx].reshape(1, -1)

        distances, indices = self.nn_model.kneighbors(query_embedding, n_neighbors=top_n+1)

        recommendations = []
        for index, distance in zip(indices[0][1:], distances[0][1:]):
            track = self.df.iloc[index]
            similarity = 1 - distance
            recommendations.append({
                "track_name": track['track_name'],
                "track_artist": track['track_artist'],
                "similarity": round(similarity, 4),
                "genre": track['playlist_genre']
            })

        return recommendations
