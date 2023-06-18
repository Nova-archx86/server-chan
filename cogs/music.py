import discord
import logging
import time
import asyncio
import os

from discord.ext import commands
from discord import FFmpegPCMAudio, Embed, Color, ClientException

from downloader import Downloader
from yt_dlp import DownloadError

class QueueItem:
    
    def __init__(self, info:tuple, audio:FFmpegPCMAudio):
        self.info = info
        self.audio = audio
    
    def __repr__(self):
        title = self.info[1]
        return title
    
    async def send_embed(self, ctx, info,  embed_title):
        # video info from yt_dlp 
        id, title, duration, thumbnail, author = info
        
        em = Embed(title=embed_title, color=Color.random())
        em.set_thumbnail(url=thumbnail)
        em.add_field(name='Song', value=title, inline=False)
        em.add_field(name='Channel', value=author, inline=False)
        em.add_field(name='Duration', value=duration, inline=False)
        
        await ctx.send(embed=em)
        


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
    async def loop(self, ctx):
        
        while len(self.items) >= 1:     
            
            if not ctx.voice_client.is_playing(): 
                self.pop()
                
                try: 
                    ctx.voice_client.play(self.items[0].audio)
                except ClientException:
                    await ctx.send('An error occured while playing audio')

            await asyncio.sleep(1)


class MusicPlayer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queue = MusicQueue()

        
    @commands.command()
    async def play(self, ctx, url: str=None):
        
        if ctx.message.author.voice:
            
            # Make sure that a url parameter was provided 
            if url is None: 
                await ctx.send('You must provide at least one url!')
                return

            await self.join(ctx)
            
            dl = Downloader(url)
            info = dl.get_info()
            id = info[0]

            try: 
                
                # Check if the audio has already been downloaded 
                if id in os.listdir('./music/'):
                    await ctx.send('audio already downloaded! skipping download...')
                else:
                    dl.download()

            except DownloadError as err:
                
                await ctx.send('Failed to download audio!')
                logging.error(f'{err}')
            
            source = QueueItem(info, FFmpegPCMAudio(f'./music/{id}'))

            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                
                self.queue.push(source)
                await source.send_embed(ctx, info, 'Queued')

            else:
                self.queue.push(source)

                ctx.voice_client.play(source.audio, after=lambda x: asyncio.run(self.queue.loop(ctx)))
                await source.send_embed(ctx, info, 'Now playing:')

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
                
                if len(self.queue.items) == 1:
                    self.queue.pop()
                else:
                    await ctx.send('skipped!')
                    await self.queue.loop(ctx)

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
