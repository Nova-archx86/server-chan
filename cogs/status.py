import discord
import os
import logging

from discord.ext import commands
from mcstatus import JavaServer


class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.server_address = os.environ['IP_ADDRESS']

    @commands.command()
    async def status(self, ctx):
        try:
            server = JavaServer.lookup(self.server_address)
            status = server.status()

            if status.players.sample is not None:
                player_names = [f"{player.name} " for player in status.players.sample]
                online_players = ", ".join(player_names[:])
            else:
                online_players = "No players online"

            online_embed = discord.Embed(title='Online', color=discord.Color.green())
            online_embed.add_field(name='Version', value=f'{status.version.name}')
            online_embed.add_field(name='Description', value=f'{status.description}')
            online_embed.add_field(name='Latency', value=f'{round(status.latency)}ms')
            online_embed.add_field(name='Players online',
                                   value=f'{status.players.online}/{status.players.max}: {online_players}')
            await ctx.send(embed=online_embed)
        except Exception as err:
            offline_embed = discord.Embed(title='Error', description='Could not connect to the server!',
                                          color=discord.Color.red())
            logging.error(f'{err}')
            await ctx.send(embed=offline_embed)


async def setup(client):
    await client.add_cog(Status(client))
