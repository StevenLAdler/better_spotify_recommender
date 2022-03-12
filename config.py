import json
import pylast
        
class Config:
    def __init__(self, config_path):
        self.config = config_path

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config_path):
        with open(config_path) as config_file:
            self._config = json.load(config_file)
        config_file.close()

    @property
    def client_id(self):
        if self.config:
            return self.config['SPOTIFY']['CLIENT_ID']

    @property
    def client_secret(self):
        if self.config:
            return self.config['SPOTIFY']['CLIENT_SECRET']

    @property
    def username(self):
        if self.config:
            return self.config['SPOTIFY']['USERNAME']
    
    @property
    def lastfm_key(self):
        if self.config:
            return self.config['LASTFM']['API_KEY']
    
    @property
    def lastfm_secret(self):
        if self.config:
            return self.config['LASTFM']['SHARED_SECRET']
    
    @property
    def lastfm_username(self):
        if self.config:
            return self.config['LASTFM']['USERNAME']
    
    @property
    def lastfm_pass(self):
        if self.config:
            return self.config['LASTFM']['PASS_HASH']

    @property
    def lastfm_network(self):
        if self.config:
            return pylast.LastFMNetwork(api_key = self.config.lastfm_key, 
                                        api_secret = self.config.lastfm_secret, 
                                        username = self.config.lastfm_username, 
                                        password_hash = self.config.lastfm_pass)
