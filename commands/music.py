import discord 
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL

class MusicPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ytdlp_options = {
                'format': 'bestaudio',
                'outtmpl': 'song',
                'quiet': True,
                'noplaylist': True,
                'source_address': '0.0.0.0'
        }
    
    os.chdir('./music')
    
    @commands.command()
    async def play(self, ctx, url:str):
        if ctx.message.author.voice: 
            voice_clients = discord.utils.get(self.client.voice_clients, guild=ctx.guild) 
            if voice_clients == None:
                channel = ctx.message.author.voice.channel 
                await channel.connect() 
            
            with YoutubeDL(self.ytdlp_options) as ytdl:
                try: 
                    await ctx.send('Downloading audio file...') 
                    ytdl.download([url])
                    source = FFmpegPCMAudio('./song')
                    ctx.voice_client.play(source, after=lambda x: os.remove('./song'))
                    await ctx.send(f'Now playing!')
                except DownloadError as de:
                    ctx.send("Failed to download audio!")
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

def setup(client):
    client.add_cog(MusicPlayer(client))
