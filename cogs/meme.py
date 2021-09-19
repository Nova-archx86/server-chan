import discord
import os
import praw
import random
from discord.ext import commands
from discord import FFmpegPCMAudio

client_secret = os.environ['CLIENT_SECRET']
client_id = os.environ['CLIENT_ID']
reddit_pass = os.environ['PASS']

reddit = praw.Reddit(

    check_for_async=False,
    client_id=client_id,
    client_secret=client_secret,
    username='Novax86',
    password=reddit_pass,
    user_agent="Server_Chan"

)


class MemeSender(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):

        sub = reddit.subreddit('dankmemes')
        hot = sub.hot(limit=50)
        random_post = []

        for submission in hot:
            random_post.append(submission)

        random_pick = random.choice(random_post)
        url = random_pick.url
        name = random_pick.title
        embed = discord.Embed(title=name)
        embed.set_image(url=url)

        # catching any sneaky exceptions and
        # writing them to a log file
        # mainly for future debugging purposes

        try:
            await ctx.send(embed=embed)
        except Exception as ex:
            with open('./logs/log.txt', 'w') as f:
                f.write(ex)
                f.close()

    @commands.command()
    async def rickroll(self, ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            source = FFmpegPCMAudio('/home/pi/rickroll.mp3')
            vc.play(source)
        else:
            await ctx.send('You need to be in a voice channel to use this command')


def setup(client):
    client.add_cog(MemeSender(client))
