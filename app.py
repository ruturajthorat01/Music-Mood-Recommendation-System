# app.py

import streamlit as st
from model import MusicMoodRecommender


st.set_page_config(page_title='Music Mood Recommender', layout='centered')
st.title('🎵 Music Mood Recommender')


rec = MusicMoodRecommender('data/spotify_songs.csv')


st.markdown('Tell me how you are feeling and I will suggest songs for your mood.')
user_input = st.text_area('How are you feeling right now?', height=100)

if st.button('Get Mood Recommendations'):
    if user_input.strip() == '':
        st.warning('Please type how you are feeling (e.g., "I am feeling very happy")')
    else:
        mood = rec.detect_mood(user_input)
        st.success(f'Detected mood: **{mood}**')
        songs = rec.recommend_by_mood(mood, topn=10)
        st.subheader('Recommended songs')
        for s in songs:
            st.write(f"**{s['song_name']}** — {s['artist']} ({s['genre']})")


