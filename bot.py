import discord
import os
import asyncio
from discord.ext import commands

discord.utils.setup_logging()

async def load():
    for file in os.listdir('./commands'):
        if file.endswith('.py'): 
            await client.load_extension(f'commands.{file[:-3]}')

client = commands.Bot(command_prefix='$', help_command=None, intents=discord.Intents.all())
token = os.environ['TOKEN_1']

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Python 3.10'))
    print('online!')

async def main():
    await load() 
    await client.start(token)

asyncio.run(main())