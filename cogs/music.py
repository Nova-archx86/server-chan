import discord
from discord import channel
from discord.ext.commands.core import command
from discord.player import FFmpegPCMAudio
import youtube_dl
import os
from discord.ext import commands


class MusicPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queue = {}

    @commands.command()
    async def play(self, ctx, url: str):

        if (ctx.message.author.voice):

            ytdl_options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio', 
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
                ytdl.download([url])

            for file in os.listdir('./'):
                if file.endswith('.mp3'):
                    os.rename(file, 'music.mp3')


            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            source = FFmpegPCMAudio('music.mp3')
            vc.play(source)

        else:
            await ctx.send('You must be in a voice channel to use this command!')


def setup(client):
    client.add_cog(MusicPlayer(client))
