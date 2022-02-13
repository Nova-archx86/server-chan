import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title='List of commands')
        embed.add_field(name='prefix', value='$', inline=False)
        embed.add_field(name='help', value='Sends this message', inline=False)
        embed.add_field(name='meme', value='sends a meme from the r/memes subreddit', inline=False)
        embed.add_field(name='status', value='Gets the current status from the minecraft server (online players and latency)', inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
