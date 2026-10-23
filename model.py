# model.py

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from textblob import TextBlob
import re


class MusicMoodRecommender:
    def __init__(self, csv_path='data/spotify_songs.csv'):
        self.df = pd.read_csv(csv_path)
        
        # Map Spotify column names to our expected names
        if 'track_name' in self.df.columns:
            # Spotify dataset
            self.df['song_name'] = self.df['track_name']
            self.df['artist'] = self.df['track_artist']
            self.df['genre'] = self.df['playlist_genre']
            # Infer mood from audio features
            self.df['mood'] = self.df.apply(self._infer_mood_from_features, axis=1)
        else:
            # Original dataset format
            if 'lyrics' in self.df.columns:
                self.df['lyrics'] = self.df['lyrics'].fillna(self.df['song_name'] + ' ' + self.df['artist'])
        
        # Create combined text for TF-IDF (no lyrics in Spotify dataset)
        if 'lyrics' in self.df.columns:
            self.df['combined'] = (self.df['song_name'] + ' ' + self.df['artist'] + ' ' + self.df['genre'] + ' ' + self.df['lyrics']).astype(str)
        else:
            self.df['combined'] = (self.df['song_name'] + ' ' + self.df['artist'] + ' ' + self.df['genre']).astype(str)
        
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['combined'])
        # Don't precompute full similarity matrix - compute on-demand to save memory
        # Map indices
        self.indices = pd.Series(self.df.index, index=self.df['song_name']).drop_duplicates()
    
    def _infer_mood_from_features(self, row):
        """Infer mood from Spotify audio features"""
        valence = row.get('valence', 0.5)  # 0-1, higher = more positive/happy
        energy = row.get('energy', 0.5)     # 0-1, higher = more energetic
        danceability = row.get('danceability', 0.5)
        acousticness = row.get('acousticness', 0.5)
        
        # Energetic: high energy and high danceability
        if energy > 0.7 and danceability > 0.6:
            return 'energetic'
        # Happy: high valence and moderate-high energy
        elif valence > 0.5 and energy > 0.5:
            return 'happy'
        # Calm: low energy and high acousticness
        elif energy < 0.4 and acousticness > 0.5:
            return 'calm'
        # Sad: low valence and low energy
        elif valence < 0.4 and energy < 0.5:
            return 'sad'
        # Default based on valence
        elif valence > 0.5:
            return 'happy'
        else:
            return 'calm'

    def detect_mood(self, text):
        """Return one of: happy, sad, energetic, calm"""
        # Basic preprocessing
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        # heuristics combining polarity and presence of energetic keywords
        energetic_words = ['excited', 'energetic', 'hyped', 'pumped', 'amazing', 'thrilled']
        calm_words = ['calm', 'relaxed', 'peaceful', 'chill', 'serene']
        text_words = set(text.split())
        if any(w in text_words for w in energetic_words):
            return 'energetic'
        if any(w in text_words for w in calm_words):
            return 'calm'
        # polarity thresholds
        if polarity >= 0.35:
            return 'happy'
        elif polarity <= -0.2:
            return 'sad'
        else:
            # neutral mapped to calm
            return 'calm'

    def recommend_by_mood(self, mood, topn=10):
        # Filter dataset by mood first
        mood_df = self.df[self.df['mood'] == mood]
        if len(mood_df) == 0:
            # fallback to global top songs
            return self._topn_global(topn)
        
        # Sample a subset of mood-matched songs for efficiency (max 100 seed songs)
        sample_size = min(100, len(mood_df))
        mood_indices = mood_df.sample(n=sample_size, random_state=42).index.tolist()
        
        # Compute similarities on-demand using sparse operations
        recs = {}
        for idx in mood_indices:
            # Compute similarity for this song against all songs
            sim_scores = linear_kernel(self.tfidf_matrix[idx:idx+1], self.tfidf_matrix).flatten()
            # Get top similar songs (excluding itself)
            top_indices = np.argsort(sim_scores)[::-1][1:6]  # Top 5 similar
            for i in top_indices:
                recs[i] = recs.get(i, 0) + sim_scores[i]
        
        # Rank by aggregated score
        ranked = sorted(recs.items(), key=lambda x: x[1], reverse=True)
        results = [self._row_to_dict(self.df.loc[i]) for i, _ in ranked[:topn]]
        return results

    def recommend_similar_song(self, song_name, topn=10):
        if song_name not in self.indices:
            return []
        idx = self.indices[song_name]
        # Compute similarity on-demand
        sim_scores = linear_kernel(self.tfidf_matrix[idx:idx+1], self.tfidf_matrix).flatten()
        # Get top similar songs (excluding itself)
        top_indices = np.argsort(sim_scores)[::-1][1:topn+1]
        recs = [self._row_to_dict(self.df.loc[i]) for i in top_indices]
        return recs

    def _topn_global(self, topn=10):
        # simple heuristic: by index order
        return [self._row_to_dict(row) for _, row in self.df.head(topn).iterrows()]

    def _row_to_dict(self, row):
        result = {
            'song_name': row['song_name'],
            'artist': row['artist'],
            'genre': row['genre'],
            'mood': row['mood']
        }
        # Add lyrics if available
        if 'lyrics' in row:
            result['lyrics'] = row['lyrics']
        # Add audio features if available (Spotify dataset)
        if 'valence' in row:
            result['valence'] = round(row['valence'], 3)
            result['energy'] = round(row['energy'], 3)
            result['danceability'] = round(row['danceability'], 3)
        return result


if __name__ == '__main__':
    rec = MusicMoodRecommender('data/spotify_songs.csv')
    print('Loaded', len(rec.df), 'songs')
    print('Detect mood for "I am feeling very happy today!":', rec.detect_mood('I am feeling very happy today!'))
    print('Top recommendations for happy:')
    for r in rec.recommend_by_mood('happy', 5):
        print(r['song_name'], '-', r['artist'])


