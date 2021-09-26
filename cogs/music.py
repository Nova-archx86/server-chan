import discord
import youtube_dl
import os
from discord.ext import commands
from discord import channel
from discord.player import FFmpegPCMAudio

class MusicPlayer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music_path = '/Users/nova/Music/bot/'
        self.script_path = '/Users/nova/Workspace/Nova-archx86/Projects/ServerChan'

    @commands.command()
    async def join(self, ctx):
        if (ctx.message.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send('You are not in a voice channel!')

    # Plays song url's from youtube
    @commands.command()
    async def yt(self, ctx, url: str):
        if (ctx.message.author.voice):
            ytdl_options = {
                'format': 'bestaudio/best',
                'no-playlist': True,
                'quiet': True,
                'source_address': '0.0.0.0',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
                ytdl.download([url])

            for file in os.listdir(self.script_path):
                if file.endswith('.mp3'):
                    os.rename(file, 'music.mp3')

            source = FFmpegPCMAudio('music.mp3')
            ctx.voice_client.play(source)

        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    # Play's a song from the local file system
    async def play(self, ctx, query:str):
            os.chdir(self.music_path)
            try:
                source = FFmpegPCMAudio(f'{query}.mp3')
                ctx.voice_client.play(source)
            except FileNotFoundError as err:
                await ctx.send(f'These are not the files that you are looking for! (i couldnt find {query}, try using the $lsdb command to get a list of all music files)')
                with open('../logs/fnf.txt', 'w') as f:
                    f.write(f'{err}')
                    f.close()
            os.chdir(f'{self.script_path}/cogs')

    # List all .mp3 files in the music folder
    @commands.command()
    async def ls(self, ctx):
        list_of_music_files = []
        for file in os.listdir(self.music_path):
            if file.endswith('.mp3'):
                list_of_music_files.append(file)
        formatted_text = '\n'.join(list_of_music_files)
        await ctx.send(f'Available music:\n{formatted_text}')

    @commands.command()
    async def leave(self, ctx):
        if (ctx.author.voice):
            await ctx.voice_client.disconnect()
        else:
            await ctx.send('I am not in a voice channel!')

    @commands.command()
    async def pause(self, ctx):
        current_vc = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (current_vc.is_playing):
            current_vc.pause()
        else:
            await ctx.send('Nothing is playing')

    @commands.command()
    async def resume(self, ctx):
        current_vc = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (current_vc.is_paused()):
            current_vc.resume()
        else:
            await ctx.send('Nothing is paused at the moment.')

    @commands.command()
    async def stop(self, ctx):
       current_vc = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
       current_vc.stop()

def setup(client):
    client.add_cog(MusicPlayer(client))
