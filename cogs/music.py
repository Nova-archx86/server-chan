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
        # self.queue = {}

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

    @commands.command()
    async def leave(self, ctx):
        if (ctx.author.voice):
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send('I am not in a voice channel!')

    @commands.command()
    async def pause(self, ctx):
        current_vc = discord.utils.get(
            self.client.voice_clients, guild=ctx.guild)
        if (current_vc.is_playing):
            current_vc.pause()
        else:
            await ctx.send('Nothing is playing')

    @commands.command()
    async def resume(self, ctx):
        current_vc = discord.utils.get(
            self.client.voice_clients, guild=ctx.guild)
        if (current_vc.is_paused()):
            current_vc.resume()
        else:
            await ctx.send('Nothing is paused at the moment.')

    @commands.command()
    async def stop(self, ctx):
       current_vc = discord.utils.get(
            self.client.voice_clients, guild=ctx.guild)
       current_vc.stop()

def setup(client):
    client.add_cog(MusicPlayer(client))
