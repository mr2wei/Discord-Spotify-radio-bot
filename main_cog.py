import discord
from discord.ext import commands

class main_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = discord.Embed(title = "Available commands 🎉", description = """
`R!play <song name> or <spotify song link> or <youtube link>` to add a song to queue
**Youtube songs cannot be used for the Radio feature**
`R!radio` to use Spotify's algorithms to automagically add similar songs to the queue
`R!pause` `R!resume` to pause and resume
`R!skip` to skip the curent song
`R!jump <index of song to jump to>` to skip to the desired song
`R!loop` loops the whole queue including songs that have already played
`R!loopcurrent` loops the current song
`R!shuffle` shuffles the whole queue
`R!queue` displays upcoming music or the whole queue if loop is on
`R!move <index of song to move> <index of destination>` moves the song in the queue
`R!remove <queue number> to remove the song
`R!clear` clears the queue
`R!lyrics` to get lyrics for the current song
`R!dc` 
""")
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Connected')
    
    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(embed = self.help_message)
    
    @commands.command(name = "issues", help = "Displays known issues")
    async def issues(self, ctx):
        await ctx.send("""
```
R!lyrics have formatting issues cause by <a> tags which is so annoying
play_music() sometimes doesn't play certain songs... i think this is an FFMPEG issue
the player will occasionally speed up or slow down songs at certain parts. (out of my control)
```        
""")