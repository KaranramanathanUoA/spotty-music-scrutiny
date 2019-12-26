import sys
import spotipy
import spotipy.util as util
import credentialManager

scope = 'user-library-read'
# Secrets are retrieved from credentialManager.py, which is also added to the .gitignore file to ensure security
clientId = credentialManager.SPOTIPY_CLIENT_ID
clientSecret = credentialManager.SPOTIPY_CLIENT_SECRET
redirectURI = credentialManager.SPOTIPY_REDIRECT_URI

def extract_saved_songs_info_of_user_from_spotify(clientId, clientSecret, redirectURI):
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
        results = response['items']
        
        # subsequently runs until it has read all songs in the library
        while (len(results) < response["total"]):
            response = sp.current_user_saved_tracks(offset = len(results))
            results.extend(response['items'])
        return results
    
    else:
        print ("Can't get token for {0}".format(userName))
        sys.exit()

def extract_song_details_from_saved_song_info(results):
    detailsOfAllSongs = []
    for item in results:
        songDetails = {}
        track = item['track']
        trackName = track['name']
        artistName = track['artists'][0]['name']
        artistId = track['artists'][0]['id']
        songDetails['Track Name'] = trackName
        songDetails['Artist'] = artistName
        songDetails['Artist Id'] = artistId
        songDetails['genres'] = extract_genres_of_artist(artistId)
        detailsOfAllSongs.append(songDetails)
    return detailsOfAllSongs

def extract_genres_of_artist(artistId):
    userName = sys.argv[1]
    token = util.prompt_for_user_token(userName, scope, client_id = clientId, client_secret = clientSecret, redirect_uri= redirectURI)
    sp = spotipy.Spotify(auth = token)
    artist = sp.artist(artistId)
    genres = artist['genres']
    return genres

def main():
    result = extract_saved_songs_info_of_user_from_spotify(clientId, clientSecret, redirectURI)
    #print (result)
    detailsOfAllSongs = extract_song_details_from_saved_song_info(result)
    print (detailsOfAllSongs)

if __name__ == "__main__":
    main()   