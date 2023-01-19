import discord
import os
import asyncio
import logging
from discord.ext import commands

discord.utils.setup_logging()


def clean_dir():
    logging.info('Cleaning music directory...')
    try:
        if os.listdir('music'):
            for file in os.listdir('music'):
                logging.info(f'removing {file}')
                os.remove(f'music/{file}')
        else:
            logging.info('Nothing to be cleaned!')
    except FileNotFoundError:
        logging.info("No music direcotry found!, creating a new one...")
        os.mkdir(f'{os.getcwd()}/music')


async def load():
    files = os.listdir('cogs')

    for file in files:
        if file.endswith('.py'):
            await client.load_extension(f'cogs.{file[:-3]}')
            logging.info(f'Loaded cogs.{file[:-3]}')


client = commands.Bot(command_prefix='$', help_command=None, intents=discord.Intents.all())
token = os.environ['TOKEN_1']


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('python 3.10'))
    logging.info(f'Successfully logged in!')


async def main():
    clean_dir()
    await load()
    await client.start(token)


asyncio.run(main())
