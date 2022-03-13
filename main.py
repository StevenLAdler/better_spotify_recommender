from random import gauss
from config import Config

from spotipy import Spotify, util
from pylast import LastFMNetwork

from spotify_song import SpotifySong
from lastfm_song import LastFMSong


def convert_song(spotify_session: Spotify, 
                 lastfm_network: LastFMNetwork, 
                 spotify_song: SpotifySong = None, 
                 lastfm_song: LastFMSong = None):
    
    if spotify_song and lastfm_song:
        print("both spotify and lastfm song provided, no valid conversion")
        return

    if spotify_song:
        song = LastFMSong(lastfm_network=lastfm_network, 
                        artist=spotify_song.track['artists'][0]['name'], 
                        title=spotify_song.track['name'], 
                        album=spotify_song.track['album']['name'])
        song.set_track()
        return song

    elif lastfm_song:
        song = SpotifySong(spotify_session=spotify_session,
                         artist=lastfm_song.artist,
                         title=lastfm_song.title,
                         album=lastfm_song.album)
        song.set_track()
        return song

def get_lastfm_network(config):
    lastfm_network = LastFMNetwork(api_key = config.lastfm_key, 
                                   api_secret = config.lastfm_secret, 
                                   username = config.lastfm_username, 
                                   password_hash = config.lastfm_pass)
    return(lastfm_network)

def get_spotify_session(config, scope = 'playlist-read-private'):
    token = util.prompt_for_user_token(config.username,
                                       scope,
                                       config.client_id,
                                       config.client_secret,
                                       redirect_uri='http://localhost/')
    if token:    
        spotify_session = Spotify(auth=token)
    else: 
        raise Exception("Failed Spotify auth flow")

    return(spotify_session)

if __name__ == '__main__':
    config = Config('config.json')
    lastfm_network = get_lastfm_network(config)
    spotify_session = get_spotify_session(config)
    