# dataset_preparation.py
# Use this to generate a synthetic CSV of ~100 songs. Replace entries with real data if desired.
import pandas as pd

# Expand by duplicating with small variations to reach 100 rows
rows = []
idc = 1
for i in range(10):
    for title, artist, genre, mood, lyrics in sample:
        rows.append((idc, f"{title} {i}", artist, genre, mood, lyrics))
        idc += 1

df = pd.DataFrame(rows, columns=['id','song_name','artist','genre','mood','lyrics'])
df.to_csv('data/songs.csv', index=False)
print('Generated data/songs.csv with', len(df), 'rows')




