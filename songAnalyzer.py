import pandas as pd
import json

with open('songs.json') as jsonData:
    songData = json.load(jsonData)

df = pd.DataFrame(songData)
print (df)
