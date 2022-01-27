# Discord-Spotify-radio-bot
A Discord music bot built on python that utilises Spotify's get recommendation API

# How to use it?
I'm not really sure the proper ways of doing it...

Anyway, these are the additional python packages i used:

- tekore
- discord.py
- youtube-dl
- beautifulsoup


I stored my discord and spotify keys in a .env file like this:
```
#.env
DISCORD_TOKEN = <your discord bot token>
SPOTIFY_CLIENT_ID = <your spotify application client id>
SPOTIFY_CLIENT_SECRET = <your spotify application client secret>
```

bot.py is the main program so hopefully just running that would work

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

It can't play in more than one vc or server

# Issues
- R!lyrics have formatting issues cause by <a> tags which is so annoying
- play_music() sometimes doesn't play certain songs... i think this is an FFMPEG issue

