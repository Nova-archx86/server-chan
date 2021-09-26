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
        embed.add_field(name='yt <url> ', value='Plays the given url from youtube', inline=True)
        embed.add_field(name='play <query>', value='Plays a music file from the local music folder', inline=True)
        embed.add_field(name='meme', value='sends a meme from the r/memes subreddit', inline=True)
        embed.add_field(name='ls', value='Lists all music files in the music folder', inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
