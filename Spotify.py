import requests
from bs4 import BeautifulSoup
import tekore as tk
from youtube_dl import YoutubeDL
import re

class Spotify:
    def __init__(self):
        self.conf = tk.config_from_environment()
        self.token_spotify = tk.request_client_token(*self.conf[:2])
        self.spotify = tk.Spotify(self.token_spotify, asynchronous=True)
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

    
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
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                if link:
                    info = ydl.extract_info(query, download = False)
                else:
                    info = ydl.extract_info("ytsearch:%s" % query, download=False)['entries'][0]
            except Exception: 
                return False

        return info
    
    async def get_recommendations(self, spotify_ids: list): #spotify ids max length 5
        recommendations = await self.spotify.recommendations(track_ids= spotify_ids, limit = 20)
        return recommendations
    
    def get_lyrics(self, track): #returns None if no lyrics
        track_name = track['trackname'].split(' ')
        artist_name = track['artist'].split(' ')
        #filters the words to ensure there are no specil characters
        for word in track_name:
            track_name[track_name.index(word)] = re.sub('[^A-Za-z0-9]+', '', word)
        for word in artist_name:
            artist_name[artist_name.index(word)] = re.sub('[^A-Za-z0-9]+', '', word)
        #joins them back with '-' for the url ex: 'The-weeknd'
        track_name = '-'.join(track_name)
        artist_name = '-'.join(artist_name)
        print(track_name)

        print(artist_name)
        #ex: https://genius.com/The-weeknd-less-than-zero
        page = requests.get(f'https://genius.com/{artist_name}-{track_name}-lyrics')
        html = BeautifulSoup(page.text, 'html.parser')
        #this could cause problems in the future but my bot scrapes the genius website. I should find alternatives :|
        lyrics = html.find_all("div", {'data-lyrics-container' : "true"})
        full_lyrics = []
        if lyrics:
            for lyric_parts in lyrics:
                full_lyrics.append(lyric_parts.get_text(separator= '\n'))
            return '\n'.join(full_lyrics)
        else:
            return None
    
    async def get_playlist(self, playlist_id):
        return await self.spotify.playlist(playlist_id)

        
        


if __name__ == "__main__":
    #this is just for me to test the functions
    import asyncio
    spotify = Spotify()
    print(spotify.search_youtube("https://www.youtube.com/watch?v=_nQMRuVwzhY", True))
    