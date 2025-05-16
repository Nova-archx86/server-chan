import discord
import logging
import time
import asyncio
import os

from yt_dlp import YoutubeDL
from discord.ext import commands
from discord import FFmpegPCMAudio, Embed, Color, ClientException, PCMVolumeTransformer

"""
Wrapper class for PCMVolumeTransformer objects
allows you to easily retrive information about a song currently in queue.
"""
class QueueItem:

    def __init__(self, info:tuple, audio:PCMVolumeTransformer):
        self.info = info
        self.audio = audio

    def __repr__(self):
        title = self.info[1]
        return title

    async def send_embed(self, ctx, info,  embed_title):
        # video info from yt_dlp
        video_id, title, duration, thumbnail, author = info

        em = Embed(title=embed_title, color=Color.random())
        em.set_thumbnail(url=thumbnail)
        em.add_field(name='Song', value=title, inline=False)
        em.add_field(name='Channel', value=author, inline=False)
        em.add_field(name='Duration', value=duration, inline=False)
        await ctx.send(embed=em)

class Downloader:

    def __init__(self, url):

        self.url = url

        # the output filename is the video id due to some
        # youtube video titles having names that don't play nice
        # with bash or any shell for that matter

        self.options = {
            'format': 'bestaudio',
            'outtmpl': '%(id)s',
            'quiet': True,
            'noplaylist': True,
            'source_address': '0.0.0.0'
        }

    def get_info(self) -> tuple:
        video_info = None

        with YoutubeDL(self.options) as yt:
            info = yt.extract_info(self.url, download=False)

            video_id = info.get('id')
            title = info.get('title')
            author = info.get('uploader')
            thumbnail = info.get('thumbnail')

            # Formats duration in mm:ss
            duration_secs = info.get('duration')
            mins, secs = divmod(duration_secs, 60)
            duration = f'{mins}:{secs}'
            video_info = (video_id, title, duration, thumbnail, author)

            return video_info

    def download(self):
        with YoutubeDL(self.options) as yt:
            os.chdir('./music')
            yt.download([self.url])
            os.chdir('../')
