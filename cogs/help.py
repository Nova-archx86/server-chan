# Copyright © 2023 David Moor <moorcode66@yahoo.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.


import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title='List of commands', color=discord.Color.random())
        embed.add_field(name='prefix', value=ctx.prefix, inline=False)
        embed.add_field(name='help', value='Sends this message', inline=False)
        embed.add_field(name='status', value='Gets the current status from the minecraft server (online players and '
                                             'latency)', inline=False)
        embed.add_field(name='pm', value='Randomly picks a map and difficulty for phasmophobia')
        embed.add_field(name='play <url>', value='Downloads and plays audio from a valid  url using the yt-dlp project', inline=False)
        embed.add_field(name='pause', value='Pauses the current audio player', inline=False)
        embed.add_field(name='resume', value='Resumes a paused audio player', inline=False)
        embed.add_field(name='skip', value='Skips the current song in the queue', inline=False)
        embed.add_field(name='stop', value='Stops the current audio player and leaves the voice channel', inline=False)
        embed.add_field(name='leave', value='Disconnects from the current voice channel', inline=False)
        embed.add_field(name='vol', value='Sets a volume (between 0 and 100) for the current voice channel', inline=False)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Help(client))
