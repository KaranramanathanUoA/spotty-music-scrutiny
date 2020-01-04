import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import json

def loadSongDataIntoDataFrame():
    with open('songs.json') as jsonData:
        songData = json.load(jsonData)

    df = pd.DataFrame(songData)
    return df

def extractTopTenFavoriteArtistsFromLibrary(df):
    favoriteArtists = df['Artist'].value_counts()[:10]
    return dict(favoriteArtists)

def plotBarChartOfFavouriteArtists(favoriteArtists):
    index = np.arange(len(favoriteArtists))
    plt.bar(index, list(favoriteArtists.values()), align = 'center')
    plt.xlabel('Artists', fontsize=12)
    plt.ylabel('Total Songs in Playlist', fontsize=12)
    plt.xticks(index, list(favoriteArtists.keys()), fontsize=8, rotation=30)
    plt.title('Breakdown of Favorite Artists in Playlist')
    plt.tight_layout()
    plt.show()

def main():
    df = loadSongDataIntoDataFrame()
    favoriteArtists = extractTopTenFavoriteArtistsFromLibrary(df)
    print (favoriteArtists)
    plotBarChartOfFavouriteArtists(favoriteArtists)

if __name__ == "__main__":
    main()