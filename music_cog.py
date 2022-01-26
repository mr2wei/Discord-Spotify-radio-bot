import discord
from discord.ext import commands
from matplotlib.image import thumbnail
from Spotify import Spotify
from random import randint, shuffle
import asyncio
from threading import Thread, Timer


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.goodbye_quotes = ["“It is hard to say goodbye to someone with whom you spend so many years”", "“It is hard but you have to say goodbye because to start a new chapter in life you have to end the previous chapter”", "“Farewell doesn't mean that you will not see each other but it means that you will meet again and create more memories”", "“It doesn’t matter if today we are going on a different journey but I promise you that I will meet you again no matter how far you are”", "“It is not ending it is the beginning so smile and say goodbye”", "“To move forward in life you have to say goodbye if you can’t say goodbye you will never able to move forward”", "“Goodbye, but you will always be in my memories and I will always treasure the memories that I created with you”", "“In every goodbye, there is a secret message that is we will miss you until you come back”"]

        self.spotify = Spotify()

        #according to a guide https://www.youtube.com/watch?v=i0nNPidYQ2w&t=6s 2d array with song and channel
        self.history = [] 
        self.music_queue = []
        self.current_song = {}
        self.is_loop = False
        self.is_loop_current = False
        self.is_shuffle = False
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        #current voice channel
        self.vc = ""

    async def search(self, query):
        track = await self.spotify.search(query)
        if not track:
            return False
        #i chose to search song title and artist name to eliminate possibility of the bot playing a random youtube video
        youtube_link = self.spotify.search_youtube(f"{track.name} {track.artists[0].name}")
        seconds, milliseconds = divmod(track.duration_ms, 1000)
        minutes, seconds = divmod(seconds, 60)
        return {
            'source': youtube_link, 
            'title': f"{track.name} by {track.artists[0].name}", 
            'thumbnail': track.album.images[0].url, 
            'duration': f'{int(minutes):02d}:{int(seconds):02d}', 
            'duration_ms': track.duration_ms, 
            'trackname': track.name, 
            'artist': track.artists[0].name, 
            'spotify_id': track.uri.split(':')[-1]
        }        

    async def add_from_playlist(self, ctx, playlist, voice_channel):
        await self.bot.wait_until_ready()
        embed = discord.Embed(title = f"Adding from playlist: {playlist.name}", description = "playlist.owner.display_name\n[----------]")
        embed.set_thumbnail(url = playlist.images[0].url)
        embed.set_footer(text = "Requested by " + ctx.author.display_name)
        message = await ctx.send(embed = embed)
        await ctx.send("If music doesn't start after 5 seconds type R!play to force it to play")
        for index, track in enumerate(playlist.tracks.items):
            youtube_link = self.spotify.search_youtube(f"{track.track.name} {track.track.artists[0].name}")
            seconds, milliseconds = divmod(track.track.duration_ms, 1000)
            minutes, seconds = divmod(seconds, 60)
            song = {
                'source': youtube_link, 
                'title': f"{track.track.name} by {track.track.artists[0].name}", 
                'thumbnail': track.track.album.images[0].url, 
                'duration': f'{int(minutes):02d}:{int(seconds):02d}', 
                'duration_ms': track.track.duration_ms, 
                'trackname':track.track.name, 
                'artist': track.track.artists[0].name, 
                'spotify_id': track.track.uri.split(':')[-1]
            }
                   
            self.music_queue.append([song, voice_channel])
            self.history.append([song, voice_channel])
            progress = int((index + 1)/(len(playlist.tracks.items)/100))
            embed = discord.Embed(title = f"Adding from playlist: {playlist.name}", description = f"playlist.owner.display_name\n[{'#' * int(progress/10)}{'-'* (10 - int(progress/10))}] {progress}%")
            embed.set_thumbnail(url = playlist.images[0].url)
            embed.set_footer(text = "Requested by " + ctx.author.display_name)  
            await message.edit(embed = embed)

    def play_next(self, ctx): #https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-pass-a-coroutine-to-the-player-s-after-function
        coro = self.play_music(ctx)
        fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        try:
            fut.result()
        except:
            print("error")

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            song = self.music_queue[0][0]
            m_url = song['source']
            
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None or ctx.voice_client is None:
                self.vc = await self.music_queue[0][1].connect()
            elif self.vc == self.music_queue[0][1]:
                pass
            else:
                await self.vc.move_to(self.music_queue[0][1])
            source = discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS)
            print(self.music_queue)
            #remove the first element as you are currently playing it and assign it to current song
            self.current_song = self.music_queue.pop(0)
            #if the user set it to loop current song, it will just reinsert the current song to the front of the queue
            if self.is_loop_current:
                self.music_queue.insert(0, self.current_song)
            #if the user chose to loop the queue, once the queue is complete, it will copy the previously played songs back into queue
            if len(self.music_queue) == 0 and self.is_loop:
                self.music_queue = self.history.copy()
                if self.is_shuffle:
                    shuffle(self.music_queue)
            self.vc.play(source, after= lambda e: self.play_next(ctx))
            #Now playing embed
            embed = discord.Embed(title = f"Now playing: {song['title']}", description = f"duration: {song['duration']}")
            embed.set_thumbnail(url = song['thumbnail'])
            await ctx.send(embed = embed)

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args, internal = False):
        query = " ".join(args)
        if query == "" and len(self.music_queue) > 0:
            await self.play_music(ctx)
        elif query == "":
            await ctx.send("Enter the song name after R!play to add the song to queue")
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        else:
            if "open.spotify.com/playlist" in query:
                playlist_id = query.split('/')[-1].split('?')[0]
                playlist = await self.spotify.get_playlist(playlist_id)
                
                #i have to use another Thread because doing it on the main thread or whatever thread it uses causes timeouterror
                #Thread(target = self.add_from_playlist_buffer, args = (ctx, playlist, voice_channel, message,)).start()
                self.bot.loop.create_task(self.add_from_playlist(ctx, playlist, voice_channel))
                await asyncio.sleep(5)
                if self.vc == "":
                    await self.play_music(ctx)
                elif not self.vc.is_playing():
                    await self.play_music(ctx)
            else:
                song = await self.search(query)
                if type(song) == type(True):
                    await ctx.send(f"Could not find any songs matching {query}")
                else:
                    if not internal:
                        #create the embed message (add to queue message)
                        embed = discord.Embed(title = f"Added to queue: {song['title']}", description = f"duration: {song['duration']}")
                        embed.set_thumbnail(url = song['thumbnail'])
                        embed.set_footer(text= "Requested by " + ctx.author.display_name)
                        await ctx.send(embed = embed)
                        await ctx.message.add_reaction(["👍", "⏯", "😏", "😀", "😍", "😲", "🥶"][randint(0,6)])
                    self.music_queue.append([song, voice_channel])
                    self.history.append([song, voice_channel])
                    if self.vc == "":
                        await self.play_music(ctx)
                    elif not self.vc.is_playing():
                        await self.play_music(ctx)
    
    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        playtime = 0
        #if the user chose to loop, the bot will show the whole queue instead of up next
        if self.is_loop or self.is_loop_current:
            for i in range(0, len(self.history)):
                retval +=f"`{i+1}:` {self.history[i][0]['title']} - **{self.history[i][0]['duration']}**\n"
                playtime += int(self.history[i][0]['duration_ms'])
        else:
            for i in range(0, len(self.music_queue)):
                retval +=f"`{i+1}:` {self.music_queue[i][0]['title']} - **{self.music_queue[i][0]['duration']}**\n"
                playtime += int(self.music_queue[i][0]['duration_ms'])
        seconds, milliseconds = divmod(playtime, 1000)
        minutes, seconds = divmod(seconds, 60)    
        embed = discord.Embed(title = "Queue" if self.is_loop or self.is_loop_current else "Up next", description = retval)
        embed.set_footer(text = f'total play time: {int(minutes):02d}:{int(seconds):02d} loop is {"on" if self.is_loop or self.is_loop_current else "off"}')
        print(retval)
        if retval != "":
            await ctx.send(embed = embed)
            await ctx.message.add_reaction("📜")
        else:
            await ctx.send("No music in queue")

    
    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_channel.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)
            await ctx.message.add_reaction("⏩")
        except AttributeError:
            await ctx.send("Are you in the voice channel? 🧐")

            
    @commands.command(name="disconnect", help="Disconnecting bot from VC")
    async def dc(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        await ctx.send(self.goodbye_quotes[randint(0,len(self.goodbye_quotes)-1)])
        voice_channel.stop()
        #resets variables
        self.vc = ""
        self.history = []
        self.music_queue = []
        self.is_loop_current = False
        self.is_loop = False
        self.current_song = {}
        await voice_channel.disconnect()
        await ctx.message.add_reaction("⏹")
        
        

    @commands.command(name="pause", help="Pausing the song")
    async def pause(self, ctx):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            #if the bot is playing and is not paused
            if voice_channel.is_playing() and not voice_channel.is_paused():
                voice_channel.pause()
                await ctx.send("Paused")
                await ctx.message.add_reaction("⏸")
            else:
                await ctx.send("Already paused... or am i even there 🤔")
        except AttributeError:
            await ctx.send("Are you in the voice channel? 🧐")

    @commands.command(name="resume", help="Resuming the song")
    async def resume(self, ctx):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            if voice_channel.is_paused():
                voice_channel.resume()
                await ctx.send("Resuming")
                await ctx.message.add_reaction("▶")
            else:
                await ctx.send("Still playing... or am i even there 🤔")
        except AttributeError:
            await ctx.send("Are you in the voice channel? 🧐")
    
    @commands.command(name = 'radio', help = "Uses spotify's recommendation API to auto add similar songs based on current songs")
    async def radio(self, ctx):
        if len(self.history) > 0:
            spotify_id_history = []
            #copy the spotify ids of the songs in self.history
            for song in self.history:
                spotify_id_history.append(song[0]['spotify_id'])
            #get the last 5 song's spotify id
            last_five = spotify_id_history[-5:]
            if len(self.history) < 3:
                await ctx.send("For better recommendations, try adding 5 songs")
            recommendations = await self.spotify.get_recommendations(last_five) #this is an object (well that's what i'd describe it as) it returns a list? dictionary? of recommended tracks from spotify
            track_names = []
            for track in recommendations.tracks:
                track_names.append(track.name)
            await ctx.send("Turning on the radio 📻🎵")
            for trackname in track_names:
                #calls self.p to add these songs to queue
                await self.p(ctx, trackname, internal = True)
        else:
            await ctx.send("Add some songs to start the radio! (it is recommended to add atleast 3 songs)")

    @commands.command(name = 'lyrics', help = "Get lyrics for the current song")
    async def lyrics(self, ctx):
        if bool(self.current_song):
            lyrics = self.spotify.get_lyrics(self.current_song[0])
            if lyrics is None:
                await ctx.send("Could not find lyrics for the current song")
            else:
                embed = discord.Embed(title = f"Lyrics: {self.current_song[0]['title']}", description = lyrics)
                embed.set_footer(text = "lyrics by genius.com (the format is screwed but I can't be bothered)")
                await ctx.send(embed = embed)
                await ctx.message.add_reation("🎤")
        else:
            await ctx.send("There is no song playing at the moment")

    @commands.command(name= 'loop', help = 'Loop the songs you have fed the bot')
    async def loop(self, ctx):
        if len(self.history) > 0:
            self.is_loop = True
            await ctx.send("Loop is on")
            await ctx.message.add_reaction("🔁")
        else:
            await ctx.send("You haven't added any songs to queue")

    @commands.command(name = 'loopcurrent', help = 'Loop current song')
    async def loop_current(self, ctx):
        if bool(self.current_song):
            self.is_loop_current = True
            if self.current_song not in self.music_queue:
                self.music_queue.insert(0, self.current_song)
            await ctx.send("Looping current song")
            await ctx.message.add_reaction("🔂")
        else:
            await ctx.send("There is no song playing")

    @commands.command(name = "shuffle", help = "shuffles the queue")
    async def shuffle_queue(self, ctx):
        if len(self.music_queue) > 0 or len(self.history) > 0:
            self.is_shuffle = True
            shuffle(self.music_queue)
            await ctx.send("Shuffling")
            await ctx.message.add_reaction("🔀")
        else:
            await ctx.send("Theres no songs in the queue!")
    

    