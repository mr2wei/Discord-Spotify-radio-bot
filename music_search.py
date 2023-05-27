import requests
from bs4 import BeautifulSoup
import tekore as tk
from yt_dlp import YoutubeDL
import re
import os
from lyrics_extractor import SongLyrics
from lyrics_extractor import LyricScraperException

class music_search:
    def __init__(self):
        self.conf = tk.config_from_environment()
        self.token_spotify = tk.request_client_token(*self.conf[:2])
        self.spotify = tk.Spotify(self.token_spotify, asynchronous=True)
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.lyric_finder = SongLyrics(os.getenv('GOOGLE_CUSTOM_SEARCH_API'), os.getenv('GOOGLE_ENGINE_ID'))
        self.ydl = YoutubeDL(self.YDL_OPTIONS)
    
    #returns the first result
    async def search(self, query, id = False):
        if not id:
            tracks, = await self.spotify.search(query, limit=1)
            try: 
                return tracks.items[0]
            except IndexError:
                return False
        else:
            try:
                return await self.spotify.track(query)
            except tk.BadRequest:
                return False

    def search_youtube(self, query, link = False): #i copied to guide for this
        
        try: 
            if link:
                info = self.ydl.extract_info(query, download = False)
            else:
                info = self.ydl.extract_info("ytsearch:%s" % query, download=False)['entries'][0]
        except Exception: 
            return False

        return info
    
    async def get_recommendations(self, spotify_ids: list): #spotify ids max length 5
        recommendations = await self.spotify.recommendations(track_ids= spotify_ids, limit = 20)
        return recommendations
    
    def get_lyrics(self, track): #returns None if no lyrics
        track_name = track['trackname']
        artist_name = track['artist']
        try:
            return self.lyric_finder.get_lyrics(f'{track_name} {artist_name}')['lyrics']
        except LyricScraperException:
            return None
    
    async def get_playlist(self, playlist_id):
        return await self.spotify.playlist(playlist_id)

        
        
