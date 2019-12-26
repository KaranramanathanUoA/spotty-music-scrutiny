import sys
import spotipy
import spotipy.util as util
import credentialManager
from datetime import datetime
import json

scope = 'user-library-read'
# Secrets are retrieved from credentialManager.py, which is also added to the .gitignore file to ensure security
clientId = credentialManager.SPOTIPY_CLIENT_ID
clientSecret = credentialManager.SPOTIPY_CLIENT_SECRET
redirectURI = credentialManager.SPOTIPY_REDIRECT_URI

def extract_saved_songs_info_from_user_library(clientId, clientSecret, redirectURI):
    # Throw error if user name is not provided in the command line arguments
    if len(sys.argv) > 1:
        userName = sys.argv[1]
    else:
        print ("Usage: {0} userName".format(sys.argv[0]))
        sys.exit()
    
    # User Authorization
    token = util.prompt_for_user_token(userName, scope, client_id = clientId, client_secret = clientSecret, redirect_uri= redirectURI)

    if token:
        sp = spotipy.Spotify(auth = token)
        # First run through only returns 20 songs by default, but it also retrieves total no of songs in library
        response = sp.current_user_saved_tracks()
        savedSongsInfo = response['items']
        
        # Subsequently runs until it has read all songs in the library
        while (len(savedSongsInfo) < response["total"]):
            response = sp.current_user_saved_tracks(offset = len(savedSongsInfo))
            savedSongsInfo.extend(response['items'])
        return savedSongsInfo
    
    else:
        print ("Can't get token for {0}".format(userName))
        sys.exit()

def extract_song_details(savedSongsInfo):
    # Extract the song name, artist name and the artist Id using the spotify API and save them in the detailsOfAllSongs 
    # dictionary
    detailsOfAllSongs = []
    for item in savedSongsInfo:
        songDetails = {}
        track = item['track']
        trackName = track['name']
        artistName = track['artists'][0]['name']
        artistId = track['artists'][0]['id']
        songDetails['Track Name'] = trackName
        songDetails['Artist'] = artistName
        songDetails['Artist Id'] = artistId
        detailsOfAllSongs.append(songDetails)
    return detailsOfAllSongs

def extract_genre_of_every_song_in_user_library(savedSongsInfo, detailsOfAllSongs):
    # Since genre information is not retrieved with the songs information, we have to make a seperate call to the 'artist'
    # endpoint to get the genre.
    listOfArtistIds = extract_artist_ids(savedSongsInfo)
    artistInfo = extract_genres_of_all_artists(listOfArtistIds)
    matchGenreToArtist(detailsOfAllSongs, artistInfo)

def extract_artist_ids(savedSongsInfo):
    # Set is used here to retrieve all distinct artists in the user library and only get genre information for them.
    listOfArtistIds = set()
    for item in savedSongsInfo:
        track = item['track']
        artistId = track['artists'][0]['id']
        listOfArtistIds.add(artistId)
    return listOfArtistIds

def extract_genres_of_all_artists(listOfArtistIds):
    artistInfo = {}
    userName = sys.argv[1]
    token = util.prompt_for_user_token(userName, scope, client_id = clientId, client_secret = clientSecret, redirect_uri= redirectURI)
    sp = spotipy.Spotify(auth = token)
    for artistId in listOfArtistIds:
        artist = sp.artist(artistId)
        # Get genre information of all distinct artists in the users library
        genres = artist['genres']
        # Store this in a dictionary with the artist uri as the key and the genre as the values.
        artistInfo[artistId] = genres
    return artistInfo

def matchGenreToArtist(detailsOfAllSongs, artistInfo):
    for song in detailsOfAllSongs:
        artistId = song['Artist Id']
        # Lookup artistId in the artistInfo dictionary
        genres = artistInfo[artistId]
        # Update genre for every song in a loop
        song.update({"Genre": genres})

def printJsonContentsToFile(detailsOfAllSongs):
    pass

def main():
    startTime = datetime.now()
    savedSongsInfo = extract_saved_songs_info_from_user_library(clientId, clientSecret, redirectURI)
    detailsOfAllSongs = extract_song_details(savedSongsInfo)
    extract_genre_of_every_song_in_user_library(savedSongsInfo, detailsOfAllSongs)
    print (datetime.now() - startTime)
    #print (detailsOfAllSongs)

if __name__ == "__main__":
    main()   