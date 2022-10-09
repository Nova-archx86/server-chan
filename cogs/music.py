import discord
import logging
import os
import yt_dlp
from discord.ext import commands
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL


class MusicPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.options = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s',
            'quiet': True,
            'noplaylist': True,
            'source_address': '0.0.0.0'
        }
        self.queue = []

    def queue_player(self, player: FFmpegPCMAudio):
        self.queue.append(player)

    # Checks if the queue is empty
    # removes the previously played song and plays the next one
    # Loop recursively until the queue is empty
    # Note: a while loop can't be used in place of recursion, due to the flow of execution
    def check_queue(self, ctx):
        if self.queue:
            self.queue.pop(0)
            ctx.voice_client.play(self.queue[0], after=lambda x: self.check_queue(ctx))

    @staticmethod
    async def send_embed(ctx, name, title, duration, thumbnail, author):
        em = discord.Embed(title=name, color=discord.Color.random())
        em.set_thumbnail(url=thumbnail)
        em.add_field(name='Song', value=title, inline=False)
        em.add_field(name='Channel', value=author, inline=False)
        em.add_field(name='duration', value=duration, inline=False)
        await ctx.send(embed=em)

    def download(self, url):
        with YoutubeDL(self.options) as ytdl:
            # get video info
            info = ytdl.extract_info(url, download=False)
            title = info.get('title')
            author = info.get('uploader')
            thumbnail = info.get('thumbnail')

            # Formats the duration as mm:ss
            duration = list(str(info.get('duration')))
            duration.insert(1, ':')
            duration = ''.join(duration)
            video_info = (title, duration, thumbnail, author)
            os.chdir('./music')
            ytdl.download([url])
            os.chdir('../')
            return video_info

    @commands.command()
    async def play(self, ctx, url: str):
        if ctx.message.author.voice:
            await self.join(ctx)

            if ctx.voice_client.is_playing():
                try:
                    await ctx.send('Downloading audio...')
                    title, duration, thumbnail, author = self.download(url)
                    source = FFmpegPCMAudio(f'./music/{title}')
                    self.queue_player(source)
                    await self.send_embed(ctx, 'Queued', title, duration, thumbnail, author)
                except yt_dlp.DownloadError as err:
                    logging.error(f'{err}')
                    await ctx.send('Failed to download audio')
                    return
            else:
                try:
                    await ctx.send('Downloading audio...')
                    title, duration, thumbnail, author = self.download(url)
                    source = FFmpegPCMAudio(f'./music/{title}')
                    self.queue_player(source)
                    ctx.voice_client.play(source, after=lambda x: self.check_queue(ctx))
                    await self.send_embed(ctx, 'Now playing', title, duration, thumbnail, author)
                except yt_dlp.DownloadError as err:
                    logging.error(f'{err}')
                    await ctx.send('Failed to download audio')
        else:
            await ctx.send('you must be in a voice channel to use this command!')

    @commands.command()
    async def join(self, ctx):
        voice_clients = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice_clients is None:
            channel = ctx.message.author.voice.channel
            await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.message.author.voice:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.voice_client.disconnect()
            else:
                await ctx.voice_client.disconnect()
        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def skip(self, ctx):
        if ctx.message.author.voice:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                # await ctx.send('Skipping song!')
                self.check_queue(ctx)
            else:
                await ctx.send('Nothing is playing in this channel')
        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def pause(self, ctx):
        if ctx.message.author.voice:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
            else:
                await ctx.send('Nothing is playing in this channel!')
        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def resume(self, ctx):
        if ctx.message.author.voice:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
            else:
                await ctx.send('Nothing is paused.')
        else:
            await ctx.send('You must be in a voice channel to use this command')

    @commands.command()
    async def stop(self, ctx):
        if ctx.message.author.voice:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            else:
                await ctx.send('Nothing is currently playing!')
        else:
            await ctx.send('You must be in a voice channel to use this command!')


async def setup(client):
    await client.add_cog(MusicPlayer(client))
