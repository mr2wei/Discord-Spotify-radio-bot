import discord
from discord.ext import commands

class main_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = discord.Embed(title = "Available commands 🎉", description = """
`R!play <song name>` to add a song to queue
`R!radio` to use Spotify's algorithms to suggest and add music to queue
`R!pause` `R!resume` to pause and resume
`R!skip` to skip the curent song (it is a little finnicky)
`R!loop` loops the whole queue including songs that have already played
`R!loopcurrent` loops the current song
`R!queue` displays upcoming music or the whole queue if loop is on
`R!lyrics` to get lyrics for the current song
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
R!radio is really scary because idk how stable it will be if you type a command while it's still adding songs
R!radio seems fine for now though
R!lyrics have formatting issues cause by <a> tags which is so annoying
play_music() sometimes doesn't play certain songs... i think this is an FFMPEG issue
```        
""")