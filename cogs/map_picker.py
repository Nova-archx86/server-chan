# Copyright © 2023 David Moor <moorcode66@yahoo.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.


import discord
import random
import logging
from discord.ext import commands


class MapPicker(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.difficulties = ['Amateur', 'Intermediate', 'Professional', 'Nightmare']
        self.maps = [
            'Grafton Farmhouse',
            'Prison',
            'Brownstone High School',
            'Bleasdale Farmhouse',
            'Willow Street house',
            'Ridgeview Roadhouse',
            'Tanglewood Street house',
            'Edgefield',
            'Sunny meadows',
            'Campsite'
        ]

    @commands.command()
    async def pm(self, ctx):
        selected_map = random.choice(self.maps)
        difficulty = random.choice(self.difficulties)
        file = discord.File(f'./maps/{selected_map}.webp', filename=f'{selected_map}.webp')
        embed = discord.Embed(color=discord.Color.random())
        embed.add_field(name='Selected map', value=selected_map)
        embed.add_field(name='Difficulty', value=difficulty)
        embed.set_thumbnail(url=f'attachment://{selected_map}.png')

        await ctx.send(file=file, embed=embed)


async def setup(client):
    await client.add_cog(MapPicker(client))
