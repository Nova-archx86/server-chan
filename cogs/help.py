import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title='List of commands')
        embed.add_field(name='Bot prefix', value='$', inline=True)
        embed.add_field(name='help', value='Sends this message', inline=True)
        embed.add_field(name='join', value='Joins vc (Must be used before playing audio!)', inline=True)
        embed.add_field(name='leave', value='Leaves the current voice channel', inline=True)
        embed.add_field(name='yt <url>', value='Plays the given url from youtube', inline=True)
        embed.add_field(name='play <query>', value='Plays a music file from the local music folder', inline=True)
        embed.add_field(name='ls', value='Lists all music files in the music folder', inline=True)
        embed.add_field(name='pause', value='Pauses the curently playing audio', inline=True)
        embed.add_field(name='resume', value='Plays audio that is currently paused', inline=True)
        embed.add_field(name='stop', value='stops playing audio', inline=True)
        embed.add_field(name='meme', value='sends a meme from the r/memes subreddit', inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
