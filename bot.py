import discord
import os
import asyncio
import logging
import argparse
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
# token = os.environ['TOKEN_1']


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('python 3.10'))
    logging.info(f'Successfully logged in!')


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', metavar='<TOKEN_ENV_VARIABLE>', type=str, help='The token to login with (must be stored in an env variable!)', required=False) 
    args = parser.parse_args()
    
    if args.token == None:
        # Default token env to use 
        token = os.environ['TOKEN_1']
    else:
        token = os.environ[args.token]

    clean_dir()
    await load()
    await client.start(token)

try:
    asyncio.run(main())
except KeyError:
    print('Error! token is invalid!')
    exit(1)
