# Copyright © 2023 David Moor <moorcode66@yahoo.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import discord
import os
import asyncio
import logging
import argparse
import subprocess

from discord.ext import commands

# For the the bot status... not required
python_version = str(subprocess.run(['python3', '--version'], capture_output=True).stdout, 'utf-8')

discord.utils.setup_logging()

parser = argparse.ArgumentParser()

parser.add_argument('--token', metavar='<TOKEN>', 
                        type=str, help='The token to login with',
                        required=False)

parser.add_argument('--prefix', metavar='<PREFIX_CHAR>', 
                        type=str, help='the command prefix to use ex: !,%, <', 
                        required=False)
parser.add_argument('--disable', metavar='<COG>',
                    type=str, help='disable a particular cog',
                    required=False)

args = parser.parse_args()
    
if args.token == None:
    # Default token env to use 
    token = os.environ['TOKEN_1']
else:
    token = args.token

if args.prefix == None:
   client = commands.Bot(
           command_prefix='$',
           help_command=None,
           intents=discord.Intents.all())
else:
    client = commands.Bot(
            command_prefix=args.prefix, 
            help_command=None, 
            intents=discord.Intents.all())



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
            if args.disable == file:
                logging.info(f'Skipping the loading of {file}')
                continue
            await client.load_extension(f'cogs.{file[:-3]}')
            logging.info(f'Loaded cogs.{file[:-3]}')


# client = commands.Bot(command_prefix='$', help_command=None, intents=discord.Intents.all())


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{python_version[:-3]}'))
    logging.info(f'Successfully logged in!')

# entry point
async def main():
    clean_dir()
    await load()
    await client.start(token)

try:
    asyncio.run(main())
except KeyError:
    print('Error! token is invalid!')
    exit(1)
