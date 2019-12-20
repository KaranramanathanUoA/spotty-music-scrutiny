import sys
import spotipy
import spotipy.util as util
import credentialManager

scope = 'user-library-read'
clientId = credentialManager.SPOTIPY_CLIENT_ID
clientSecret = credentialManager.SPOTIPY_CLIENT_SECRET
redirectURI = credentialManager.SPOTIPY_REDIRECT_URI

def extract_saved_songs_of_user(clientId, clientSecret, redirectURI):
    if len(sys.argv) > 1:
        userName = sys.argv[1]
    else:
        print ("Usage: {0} userName".format(sys.argv[0]))
        sys.exit()
    
    token = util.prompt_for_user_token(userName, scope, client_id = clientId, client_secret = clientSecret, redirect_uri= redirectURI)

    if token:
        sp = spotipy.Spotify(auth=token)
        #results only returns 20 songs from the library.
        #TO DO: Iteratively obtain all songs saved in 'My library'
        results = sp.current_user_saved_tracks()
        print (results)
        for item in results['items']:
            track = item['track']
            print (track['name'] + ' - ' + track['artists'][0]['name'])
    else:
        print ("Can't get token for {0}".format(userName))

if __name__ == "__main__":
    extract_saved_songs_of_user(clientId, clientSecret, redirectURI)