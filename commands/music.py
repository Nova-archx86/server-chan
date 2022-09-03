from logging import exception
import discord 
import os
import yt_dlp
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
    def clean_up(self, song):
        os.remove(f'./music/{song}')
        self.queue.pop(0) 

    def queue_player(self, player:FFmpegPCMAudio):
        self.queue.append(player)

    async def get_video_info(self, ctx, url):
        with YoutubeDL(self.ytdlp_options) as yt:
            try:
                info = yt.extract_info()
                return info.get('title')
            except exception:
                await ctx.send('Failed to get video info!')
                
    async def download(self, ctx, url):
        os.chdir('./music') 
        with YoutubeDL(self.ytdlp_options) as ytdl:
            try: 
                ytdl.download([url])
            except yt_dlp.DownloadError:
                await ctx.send('Failed to download audio!')
                
    @commands.command()
    async def play(self, ctx, url:str):
        if ctx.message.author.voice: 
            voice_clients = discord.utils.get(self.client.voice_clients, guild=ctx.guild) 
            
            if voice_clients == None:
                channel = ctx.message.author.voice.channel 
                await channel.connect()

                if self.queue is None:
                    await ctx.send('Downloading audio file...')
                    title = self.get_video_info(url) 
                    self.download(url)
                    self.queue_player(FFmpegPCMAudio(f'./music/{title}'))
                    ctx.voice_client.play(self.queue[0], after=lambda x: os.remove(f'./music/{title}'))
                else:
                    ctx.voice_client.play(self.queue[0], after=lambda x: self.queue.pop(0))
        else:
            await ctx.send('you must be in a voice channel to use this command!')

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
