import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title='List of commands')
        embed.add_field(name='prefix', value='$', inline=True)
        embed.add_field(name='help', value='Sends this message', inline=True)
        embed.add_field(name='meme', value='sends a meme from the r/memes subreddit', inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
