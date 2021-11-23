import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='$', help_command=None)
token = os.environ['TOKEN_1']


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Python 3.9.6'))
    print('online')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for file in os.listdir('./cogs'):

    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

client.run(token)
