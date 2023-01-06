import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from main_cog import main_cog
from music_cog import music_cog


load_dotenv()

#the discord bot needs to be able to read messages and send messages
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=['R!', 'r!'], description='Music bot manager with better features', intents = intents)

bot.remove_command('help')

async def setup(bot):
    print("setting up bot")
    await bot.add_cog(main_cog(bot))
    await bot.add_cog(music_cog(bot))

@bot.event
async def on_ready():
    try:
        await setup(bot)
    except discord.ClientException:
        print("bot already setup")
    print('Connected')

bot.run(os.getenv('DISCORD_TOKEN'))