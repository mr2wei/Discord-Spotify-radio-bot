# The better discord music bot
A Discord music bot that utilises spotify's API to create recommendations based on music played.

This bot also has sponsorblock integration to skip non music segments when the source is from music videos.

# How to use it?
These are the additional python packages i used:

- tekore
- discord.py
- youtube-dl
- beautifulsoup4
- lyrics-extractor
- dotenv
- colorthief
- sponsorblock.py


I stored my discord and spotify keys in a .env file like this:
```
#.env
DISCORD_TOKEN = <your discord bot token>
SPOTIFY_CLIENT_ID = <your spotify application client id>
SPOTIFY_CLIENT_SECRET = <your spotify application client secret>
GOOGLE_ENGINE_ID = <google custom search engine id>
GOOGLE_CUSTOM_SEARCH_API = <google custom search api key>
```

For the google keys, follow this link https://pypi.org/project/lyrics-extractor/
the instructions can be found in the requirements segment of the linked page

To start the bot, run this command where the bot is located (just run it like any python program)
```
python3 bot.py
```

# What can the bot do?
The bot uses the prefix R!

you can:

- R!play <\song name> to add a song to queue
- R!radio to use Spotify's algorithms to suggest and add music to queue
- R!pause R!resume to pause and resume
- R!skip to skip the curent song (it is a little finnicky)
- R!loop loops the whole queue including songs that have already played
- R!loopcurrent loops the current song
- R!shuffle shuffles the whole queue
- R!queue displays upcoming music or the whole queue if loop is on
- R!lyrics to get lyrics for the current song

# What can't the bot do?
Alot of things...

- It can't play in more than one vc or server
- Cannot skip non music segments that are in between the music segments

# Issues
- audio output can be inconsistent with random speeding up and slowing down. I cannot find a solution for this.


