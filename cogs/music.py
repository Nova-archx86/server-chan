import discord 
import subprocess
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL

class MusicPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client

    os.chdir('./music')

    def remove_file(self, file):
        subprocess.run(['rm', f'{file}'])

    @commands.command()
    async def play(self, ctx, url:str):
        if ctx.author.voice: 
            
            ytdlp_options = {
                'format': 'bestaudio',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                'quiet': True,
                'noplaylist': True,
                'source_address': '0.0.0.0'
            }

            with YoutubeDL(ytdlp_options) as ytdl:
                ytdl.download([url])

            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            music_file = os.listdir()
            source = FFmpegPCMAudio(f'{music_file[0]}')
            
            vc.play(source, after=lambda x: self.remove_file(music_file[0]))
        else:
            await ctx.send('you must be in a voice channel to use this command!')

    @commands.command()
    async def pause(self, ctx):
        if ctx.author.voice:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
            else:
                await ctx.send('Nothing is playing in this channel!')
        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def resume(self, ctx):
        if ctx.author.voice:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
            else:
                await ctx.send('Nothing is paused.')
        else:
            await ctx.send('You must be in a voice channel to use this command')

    @commands.command()
    async def stop(self, ctx):
        if ctx.author.voice:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.voice_client.disconnect()
            else:
                ctx.send('Nothing is currently playing!')
        else:
            await ctx.send('You must be in a voice channel to use this command!')

def setup(client):
    client.add_cog(MusicPlayer(client))