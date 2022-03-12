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
        ls = LastFMSong(lastfm_network=lastfm_network, 
                        artist=spotify_song.track['artists'][0]['name'], 
                        title=spotify_song.track['name'], 
                        album=spotify_song.track['album']['name'])
        ls.set_track()
        return ls

    elif lastfm_song:
        ss = SpotifySong(spotify_session=spotify_session,
                         artist=lastfm_song.artist,
                         title=lastfm_song.title,
                         album=lastfm_song.album)
        ss.set_track()
        return ss


scope = 'playlist-read-private'
config = Config('config.json')

base_songs_pl = 'https://open.spotify.com/playlist/4cU6aKcZOTMK8rVNJvkz7r?si=6c097cde821f4a9e'

token = util.prompt_for_user_token(config.username,
                                   scope,
                                   config.client_id,
                                   config.client_secret,
                                   redirect_uri='http://localhost/')

if token:    
    sp = Spotify(auth=token)
else: 
    raise Exception("Failed Spotify auth flow")

lastfm_network = LastFMNetwork(api_key = config.lastfm_key, 
                               api_secret = config.lastfm_secret, 
                               username = config.lastfm_username, 
                               password_hash = config.lastfm_pass)
    