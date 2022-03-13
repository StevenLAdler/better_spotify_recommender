import json
from pylast import LastFMNetwork
        
class LastFMSong:
    def __init__(self, lastfm_network: LastFMNetwork, title, artist, album=None):
        self.lastfm_network = lastfm_network
        self.title = title
        self.artist = artist
        self.album = album
        self.track = None

    def set_track(self):
        try:
            self.track = self.lastfm_network.search_for_track(artist_name=self.artist,
                                                              track_name=self.title).get_next_page()[0]
        except IndexError:
                print(f"Failed to find track {self.artist} - {self.title}")

    def get_song_genres(self):
        tags = [tag.item.get_name() for tag in self.track.get_top_tags() if float(tag.weight)>90]
        return tags
