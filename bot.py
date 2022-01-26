import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from main_cog import main_cog
from music_cog import music_cog


load_dotenv()


bot = commands.Bot(command_prefix='R!', description='Music bot manager with better features')

bot.remove_command('help')

bot.add_cog(main_cog(bot))
bot.add_cog(music_cog(bot))

bot.run(os.getenv('DISCORD_TOKEN'))