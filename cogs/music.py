import discord
import logging
import time
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from downloader import Downloader
from yt_dlp import DownloadError

class MusicPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queue = []

    def queue_player(self, player: FFmpegPCMAudio):
        self.queue.append(player)

    async def continue_p(self, ctx):
        while len(self.queue) >= 1:     
            if not ctx.voice_client.is_playing(): 
                self.queue.pop(0)
                try: 
                    ctx.voice_client.play(self.queue[0])
                except Exception:
                    await ctx.send('An error occured while playing audio')
            
            await asyncio.sleep(1)


    @commands.command()
    async def play(self, ctx, url: str=None):
        if ctx.message.author.voice:
            if url is None: 
                await ctx.send('You must provide at least one url!')
                return

            await self.join(ctx)
            dl = Downloader(url)

            try: 
                info = dl.get_info()
                dl.download()
            except DownloadError as err:
                await ctx.send('Failed to download audio!')

            id = info[0] 
            title = info[1]
            source = FFmpegPCMAudio(f'./music/{id}')

            if ctx.voice_client.is_playing():
                self.queue_player(source)
                embed = dl.create_embed('Queued', info)
                await ctx.send(embed=embed)
            else:
                self.queue_player(source)
                
                try: 
                    ctx.voice_client.play(source, after=lambda x: asyncio.run(self.continue_p(ctx)))
                except Exception:
                    await ctxt.send('An error occured while playing audio!')

                embed = dl.create_embed(f'Now playing: {title}', info)
                await ctx.send(embed=embed)

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
                
                if len(self.queue) == 1:
                    self.queue.pop(0)
                else:
                    await ctx.send('skipped!')
                    await self.continue_p(ctx)
            else:
                await ctx.send('Nothing is playing in this channel')
        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def pause(self, ctx):
        if ctx.message.author.voice:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                await ctx.send('Paused!')
            else:
                await ctx.send('Nothing is playing in this channel!')
        else:
            await ctx.send('You must be in a voice channel to use this command!')

    @commands.command()
    async def resume(self, ctx):
        if ctx.message.author.voice:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                await ctx.send('Resuming...')
            else:
                await ctx.send('Nothing is paused.')
        else:
            await ctx.send('You must be in a voice channel to use this command')

    # Halts all audio players and clears the queue
    @commands.command()
    async def stop(self, ctx):
        if ctx.message.author.voice:
            if ctx.voice_client.is_playing():
                self.queue.clear()
                ctx.voice_client.stop()
                await ctx.send('Stopped!')
                await ctx.send('Queue cleared!')
            else:
                await ctx.send('Nothing is currently playing!')
        else:
            await ctx.send('You must be in a voice channel to use this command!')


async def setup(client):
    await client.add_cog(MusicPlayer(client))
