import discord 
import os
import yt_dlp
import logging
from discord.ext import commands
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL

class MusicPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ytdlp_options = {
                'format': 'bestaudio',
                'outtmpl': '%(title)s',
                'quiet': True,
                'noplaylist': True,
                'source_address': '0.0.0.0'
        }
        self.queue = []

    # os.chdir('./music') 
    
    def clean_up(self, title=None):
        if title: 
            os.remove(f'./music/{title}')

        if len(self.queue) > 0: 
            self.queue.pop(0) 

    async def queue_player(self, ctx, title, player:FFmpegPCMAudio): 
        self.queue.append(player)
        await ctx.send(f'Added: {title} to queue')
    
    def get_title(self, ctx, url):
        with YoutubeDL(self.ytdlp_options) as yt:
                info = yt.extract_info(url, download=False)
                return info.get('title')
              
    async def download(self, ctx, url):
        with YoutubeDL(self.ytdlp_options) as ytdl:
            try: 
                os.chdir('./music') 
                await ctx.send('Downloading audio...') 
                ytdl.download([url])
                os.chdir('../')
            except yt_dlp.DownloadError:
                await ctx.send('Failed to download audio!')
                
    @commands.command()
    async def play(self, ctx, url:str):
        if ctx.message.author.voice: 
                logging.info(f'Current queue: {self.queue}') 
                await self.join(ctx)
                
                if ctx.voice_client.is_playing(): 
                    await self.download(ctx, url) 
                    title = self.get_title(ctx, url) 
                    await self.queue_player(ctx, title, FFmpegPCMAudio(f'./music/{title}'))
                else:
                    await self.download(ctx, url)
                    title = self.get_title(ctx, url)
                    await self.queue_player(ctx, title, FFmpegPCMAudio(f'./music/{title}'))
                    await ctx.voice_client.play(self.queue[0], after=lambda x: self.clean_up(title))
                    await ctx.send(f'Now playing: {title}')
        else:
            await ctx.send('you must be in a voice channel to use this command!')

    @commands.command()
    async def join(self, ctx):
        voice_clients = discord.utils.get(self.client.voice_clients, guild=ctx.guild) 
        if voice_clients == None:
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
                self.clean_up()
                await ctx.send('Skipping song!') 
                await ctx.voice_client.play(self.queue[0], after=lambda x: self.clean_up())
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
                await ctx.voice_client.disconnect()
            else:
                await ctx.send('Nothing is currently playing!')
        else:
            await ctx.send('You must be in a voice channel to use this command!')
    
async def setup(client):
    await client.add_cog(MusicPlayer(client))
