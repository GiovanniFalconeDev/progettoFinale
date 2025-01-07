import requests
import os

officialPlaylist = {
    'Top 50 - Italia' : '37i9dQZEVXbIQnj7RRhdSX',
    'Viral 50 - Italia' : '37i9dQZEVXbKbvcwe5owJ1',
    "Italia's Top Hits" : '37i9dQZF1DX6wfQutivYYr',
    'Pop Italia' : '065NSxcopkTPYnSSDaLYif',
    'Rap Italiano' : '37i9dQZF1DWSxF6XNtQ9Rg'
}

class AuthenticationError(Exception):
    """Eccezione personalizzata per errori di autenticazione."""
    def __init__(self, message="Errore di autenticazione: accesso negato (401)."):
        super().__init__(message)

def getBearerToken():
    url = "https://accounts.spotify.com/api/token"

    payload = 'grant_type=client_credentials&client_id=e2829fb6a07945b18bc9f3a5fdaaac98&client_secret=7c4fa8a96cef40ed933fea6a466a6720'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()
    
    os.environ['access_token_spotify'] = response['access_token']
    #print(os.environ['access_token_spotify'])

def makeCallToSpotify(url):
    flag = True
    response = None

    while(flag):

        try:
            payload = {}
            headers = {
            'Authorization': 'Bearer ' + os.environ['access_token_spotify']
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 401:
                raise AuthenticationError()
            else:
                response = response.json()
                flag = False
            
        except AuthenticationError as auth_err:
            getBearerToken()
        except KeyError:
            getBearerToken()
    
    return response

def getArtisTopTracks():
    url = 'https://api.spotify.com/v1/playlists/'
    result = []

    for item in officialPlaylist:
        completeUrl = str(url) + officialPlaylist[item]
        result.append(makeCallToSpotify(completeUrl))
        print((str(url) + officialPlaylist[item]))

    print(result[0])

def getPlaylists(region='italia', limit=5, offset=0):
    url = 'https://api.spotify.com/v1/search?q=' + region + '&type=playlist&limit=' + str(limit) + '&offset=' + str(offset)

    # Supponiamo che makeCallToSpotify ritorni una risposta valida in formato JSON
    result = makeCallToSpotify(url)

    data = {}
    
    # Recupera next e previous
    data['next'] = result['playlists']['next']
    data['previous'] = result['playlists']['previous']
    
    # Inizializza la lista delle playlist
    data['items'] = []

    # Itera sugli items (ignorando i nulli)
    for item in result['playlists']['items']:
        if item is not None:  # Verifica che l'elemento non sia null
            playlist_info = {
                'description': item['description'],
                'name': item['name'],
                'external_url': item['external_urls']['spotify'],
                'id': item['id'],
                'image_url': item['images'][0]['url'] if item['images'] else None
            }
            data['items'].append(playlist_info)

    return data
