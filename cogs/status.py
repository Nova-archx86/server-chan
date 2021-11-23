import discord 
import os
from discord.ext import commands
from mcstatus import MinecraftServer


class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.server_address = os.environ['IP_ADDRESS']

    @commands.command()
    async def status(self, ctx):
        try: 
            server =  MinecraftServer.lookup(self.server_address)
            status = server.status()
            online_embed = discord.Embed(title='Online', color=discord.Color.green())
            online_embed.add_field(name='Latency', value=f'{status.latency}ms')
            online_embed.add_field(name='Players online', value=f'{status.players.online}')
            await ctx.send(embed=online_embed)
        except Exception as err:
            offline_embed = discord.Embed(title='Error', description='Could not connect to the server!', color=discord.Color.red())
            print(f'{err}') 
            await ctx.send(embed=offline_embed)


def setup(client):
    client.add_cog(Status(client))
