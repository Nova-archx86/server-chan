import discord
import logging
import os
import asyncio
from discord.ext import commands

async def load():
    for file in os.listdir('./commands'):
        if file.endswith('.py'): 
            await client.load_extension(f'commands.{file[:-3]}')

# Loads all of the command cogs from the commands folder
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
client = commands.Bot(command_prefix='$', help_command=None, intents=discord.Intents.all())
token = os.environ['TOKEN_1']

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity('Looking for bugs'))
    print('online!')

async def main():
    await load() 
    await client.start(token)

asyncio.run(main())