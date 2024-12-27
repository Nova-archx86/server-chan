# Copyright © 2023 David Moor <moorcode66@yahoo.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import discord
import logging
import time
import asyncio
import os

from discord.ext import commands
from discord import FFmpegPCMAudio, Embed, Color, ClientException, PCMVolumeTransformer

from downloader import Downloader
from yt_dlp import DownloadError

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

"""
The actual queue data structure itself
resume() is called internally by MusicPlayer.play() after the inital audio file has finished playing.
"""
class MusicQueue:

    def __init__(self):
        self.items = []

    def __repr__(self):
        return f'{[x for x in self.items]}'

    def push(self, item:QueueItem):
        self.items.append(item)
        logging.info(f'Queue: {self.items}') # for debugging purposes (just the titles of the videos)

    def pop(self):
        self.items.pop(0)
        logging.info(f'Queue: {self.items}')


    def clear(self):
        self.items.clear()

    # Loop through the rest of the songs in queue
    async def resume(self, ctx, vc):
        while len(self.items) != 0:
            if not vc.is_playing() and not vc.is_paused():
                try:
                    vc.play(self.items[0].audio, after=lambda x: self.pop())
                except ClientException:
                    await ctx.send('An error occured while playing audio')

            await asyncio.sleep(1)

"""
The class that handles the end user facing discord commands,
e.g !play, !pause, !stop, etc.
"""
class MusicPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queue = MusicQueue()

    @commands.command()
    async def play(self, ctx, url=None):
        if ctx.message.author.voice:
            # Make sure that a url parameter was provided
            if url is None:
                await ctx.send('You must provide at least one url!')
                return

            await self.join(ctx)
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

            dl = Downloader(url)
            info = dl.get_info()
            video_id = info[0]

            try:
                # Check if the audio has already been downloaded
                if video_id in os.listdir('./music/'):
                    await ctx.send('audio already downloaded! skipping download...')
                else:
                    dl.download()

            except DownloadError as err:
                await ctx.send('Failed to download audio!')
                logging.error(f'{err}')
            source = QueueItem(info, PCMVolumeTransformer(FFmpegPCMAudio(f'./music/{video_id}'), 0.50))

            if voice.is_playing() or voice.is_paused():
                self.queue.push(source)
                await source.send_embed(ctx, info, 'Queued')

            else:
                self.queue.push(source)

                voice.play(source.audio, after=lambda x: asyncio.run(self.queue.resume(ctx, voice)))
                await source.send_embed(ctx, info, 'Now playing:')

        else:
            await ctx.send('you must be in a voice channel to use this command!')


    @commands.command()
    async def join(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice is None:
            channel = ctx.message.author.voice.channel
            await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.message.author.voice:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

            if voice.is_playing():
                voice.stop()
                await voice.disconnect()

            else:
                await voice.disconnect()
        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def skip(self, ctx):
        if ctx.message.author.voice:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice.is_playing():
                voice.stop()
                if len(self.queue.items) == 1:
                    self.queue.pop()
                else:
                    await ctx.send('skipped!')
                    await self.queue.resume(ctx, voice)

            else:
                await ctx.send('Nothing is playing in this channel')
        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def pause(self, ctx):
        if ctx.message.author.voice:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice.is_playing():
                voice.pause()
                await ctx.send('Paused!')

            else:
                await ctx.send('Nothing is playing in this channel!')

        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def resume(self, ctx):

        if ctx.message.author.voice:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice.is_paused():
                voice.resume()
                await ctx.send('Resuming...')

            else:
                await ctx.send('Nothing is paused.')
        else:
            await ctx.send('You must be in a voice channel to use this command')

    @commands.command()
    async def stop(self, ctx):
        if ctx.message.author.voice:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

            if voice.is_playing():
                self.queue.clear()
                voice.stop()
                await ctx.send('Stopped!')
                await ctx.send('Queue cleared!')

            else:
                await ctx.send('Nothing is currently playing!')

        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def vol(self, ctx, volume: float):
        if ctx.message.author.voice:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice.is_playing():
                if 0 <= volume <= 100:
                    new_vol = volume / 100
                    voice.source.volume = new_vol
                else:
                    await ctx.send('hey dummy! volume should be between 0 and 100!')

            else:
                await ctx.send('Nothing is playing in this channel')
        else:
            await ctx.send('You must be in a voice channel to use this command!')

async def setup(client):
    await client.add_cog(MusicPlayer(client))
