# Server-Chan
A simple discord bot written in python originally for a friends discord server.

## Installation
Download the source code and make sure that you have a version of python >= 3.9

Install the required packages using pip:

    pip install -r requirements.txt

## Features
- Ability to play audio files from a url provided that its compatible
with the yt-dlp project

- Retrive the status of a minecraft server

## Usage
In order to run another instance of Server-Chan, you will need to create your own discord application and generate your own token
more information can be found here: https://discord.com/developers/docs/intro

    python3 bot.py --token <your generated token here> --prefix <your prefix of choice>

Optionally, you can also set a TOKEN_1 enviorment variable to the token that you generated via the discord dev portal to avoid having to constantly using the --token option.

### Disabling specific cogs
By default all files in the cogs/ directory will be loaded, however if there is a particular cog that you wish to disable then you can do so with the --disable flag
Ex:

    python3 bot.py [Other options] --disable <filename>.py

# Notice
As of now the bot has not been tested on windows and may not function correctly due to some of the file paths used (Might be changed in the future), will likely
work if running inside of WSL or git bash. For now, It is recomended that if you intend on hosting your own instance that you run it in a
unix like enviorment. (Linux, MacOS, BSD etc.)
