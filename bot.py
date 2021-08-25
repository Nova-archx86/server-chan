import discord
import random
import os
import praw
from discord.ext import commands
from discord import FFmpegPCMAudio

client = commands.Bot(command_prefix = '$')
token = os.environ['TOKEN']
client_secret = os.environ['CLIENT_SECRET']
client_id = os.environ['CLIENT_ID']
reddit_pass = os.environ['PASS']

reddit = praw.Reddit (
    
    check_for_async = False,  
    client_id = client_id,
    client_secret = client_secret, 
    username = 'Novax86', 
    password = reddit_pass, 
    user_agent = "Server_Chan"

)

@client.event
async def on_ready():
    print('online')

@client.command()
async def meme(ctx):
    sub = reddit.subreddit('dankmemes')
    hot = sub.hot(limit=50)
    random_post = []
    
    for submission in hot:
        random_post.append(submission)

    random_pick = random.choice(random_post)
    url = random_pick.url
    name = random_pick.title
    embed = discord.Embed(title = name)
    embed.set_image(url=url)
    await ctx.send(embed = embed)

@client.command(pass_context = True)
async def rickroll(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        vc = await channel.connect()
        source = FFmpegPCMAudio('/Users/nova/rickroll.mp3')
        vc.play(source)
    else:
        ctx.send('You need to be in a voice channel to use this command')

client.run(token)