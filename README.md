# Music Mood Recommendation System

A lightweight music recommendation system that suggests songs based on user's current mood using sentiment analysis and content-based filtering.

## Features

- 🎵 Mood-based song recommendations (Happy, Sad, Energetic, Calm)
- 💬 Text-based mood detection using sentiment analysis
- 🔍 Similar song search functionality
- 🌐 Interactive Streamlit web interface
- 📊 TF-IDF + Cosine Similarity for content-based recommendations

## Project Structure

```
music-mood-recommender/
├── data/
│   └── songs.csv          # Main dataset (100 songs)
├── model.py               # Mood detection & recommender functions
├── app.py                 # Streamlit web application
├── dataset_preparation.py # Optional: generate/expand dataset
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── report.md             # Project report
```

## Installation

### 1. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download TextBlob Corpora

```bash
python -m textblob.download_corpora
```

This step is required for sentiment analysis to work properly.

## Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Model Directly

```python
from model import MusicMoodRecommender

# Initialize recommender
rec = MusicMoodRecommender('data/songs.csv')

# Detect mood from text
mood = rec.detect_mood("I am feeling very happy today!")
print(f"Detected mood: {mood}")

# Get recommendations by mood
songs = rec.recommend_by_mood('happy', topn=10)
for song in songs:
    print(f"{song['song_name']} - {song['artist']}")

# Find similar songs
similar = rec.recommend_similar_song('Shape of You', topn=5)
for song in similar:
    print(f"{song['song_name']} - {song['artist']}")
```

### Generating/Expanding Dataset

If you want to generate or expand the dataset:

```bash
python dataset_preparation.py
```

This will create/overwrite `data/songs.csv` with synthetic data. You can modify `dataset_preparation.py` to add your own songs.

## How It Works

1. **Mood Detection**: 
   - User provides text describing their mood
   - TextBlob analyzes sentiment polarity
   - Keyword matching identifies energetic/calm moods
   - Returns one of: happy, sad, energetic, calm

2. **Recommendation**:
   - Filters songs by detected mood
   - Computes TF-IDF vectors for song metadata + lyrics
   - Uses cosine similarity to find similar songs
   - Returns top-N recommendations

## Dataset Format

The `songs.csv` file should have the following columns:

- `id`: Unique identifier (integer)
- `song_name`: Song title (string)
- `artist`: Artist name (string)
- `genre`: Musical genre (string)
- `mood`: Mood label - one of: happy, sad, energetic, calm
- `lyrics`: Song lyrics or text snippet (string)

## Requirements

- Python 3.7+
- streamlit
- pandas
- scikit-learn
- textblob
- numpy

## Limitations

- Small dataset (100 songs) limits diversity
- Simple keyword-based mood detection
- No user personalization
- No audio features (only text-based)

## Future Improvements

- Integrate Spotify API for audio features
- Use transformer models for better mood detection
- Add collaborative filtering
- Expand dataset to 1000+ songs
- Add user profiles and listening history

## Project Report

See `report.md` for a detailed 8-10 page project report covering:
- Abstract and Introduction
- Related Work
- Methodology
- Implementation Details
- Evaluation and Results
- Limitations and Future Work

## PPT Outline

For presentation, use the following slide structure:

1. **Title Slide**: Project name, your name, course details
2. **Objective**: Goal of the project
3. **Dataset**: Dataset description and sample
4. **System Architecture**: Flow diagram
5. **Mood Detection**: How mood is detected from text
6. **Recommender**: TF-IDF and similarity computation
7. **Demo**: Screenshots of the app
8. **Results**: Example inputs and outputs
9. **Limitations & Future Work**: Current limitations and improvements
10. **Conclusion**: Summary and learnings
11. **Q&A**: Thank you slide

## License

This project is for educational purposes.

## Contact

For questions or issues, please refer to the project documentation or contact the project author.




