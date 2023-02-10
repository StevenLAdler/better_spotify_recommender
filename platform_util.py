from config import Config

from spotipy import Spotify, util
from pylast import LastFMNetwork

from spotify_song import SpotifySong
from lastfm_song import LastFMSong


class PlatformUtil:
    def __init__(self, config_path):
        self.config = config_path
        self.lastfm_network = None
        self.spotify_session = None

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config_path):
        self.__config = Config(config_path)

    def set_lastfm_network(self):
        self.lastfm_network = LastFMNetwork(api_key = self.config.lastfm_key, 
                                            api_secret = self.config.lastfm_secret, 
                                            username = self.config.lastfm_username, 
                                            password_hash = self.config.lastfm_pass)

    def set_spotify_session(self, scope = 'playlist-read-private'):
        token = util.prompt_for_user_token(self.config.username,
                                           scope,
                                           self.config.client_id,
                                           self.config.client_secret,
                                           redirect_uri='http://localhost/')
        if token:    
            self.spotify_session = Spotify(auth=token)
        else: 
            raise Exception("Failed Spotify auth flow")

    def spotify_song(self, song_url=None, title=None, artist=None, album=None):
        song = SpotifySong(self.spotify_session, song_url, title, artist, album)
        song.set_track()
        song.set_features()
        return song

    def lastfm_song(self, title, artist, album=None):
        song = LastFMSong(self.lastfm_network, title, artist, album)
        song.set_track()
        song.set_song_tags()
        return song

    def spotify_playlist(self, playlist_url):
        playlist = self.spotify_session.playlist(playlist_url)
        return [self.spotify_song(song_url = song['track']['external_urls']['spotify']) for song in playlist['tracks']['items']]

    def convert_song(self, 
                     spotify_song: SpotifySong = None, 
                     lastfm_song: LastFMSong = None):
        
        if spotify_song and lastfm_song:
            raise Exception("both spotify and lastfm song provided, no valid conversion")

        if spotify_song:
            song = self.lastfm_song(title=spotify_song.track['name'],  
                                    artist=spotify_song.track['artists'][0]['name'], 
                                    album=spotify_song.track['album']['name'])
            return song

        elif lastfm_song:
            song = self.spotify_song(title=lastfm_song.title,
                                     artist=lastfm_song.artist,
                                     album=lastfm_song.album)
            return song

if __name__ == '__main__':
        path = 'config.json'
        pu = PlatformUtil(path)

        pu.set_lastfm_network()
        pu.set_spotify_session()

        #Revolution 909 - Daft Punk
        spotify_song = pu.spotify_song(song_url='https://open.spotify.com/track/5pgZpHqfv4TSomtkfGZGrG?si=a2ab9879ed114407')
        lastfm_song = pu.convert_song(spotify_song=spotify_song)

        print(spotify_song.features)
        print(lastfm_song.tags)
