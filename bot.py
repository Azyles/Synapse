
import asyncio
import base64
import random
import time

import discord
from discord.ext import commands


description = '''The ultimate bot'''

bot = commands.Bot('X ', description=description)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='With Machine Learning Algorithms'))
    print(bot.user.name)
    print('status set to online')
    print(bot.user.id)
    print('------')


@bot.command()
async def ping(ctx):
    ping = round(bot.latency*1000)
    await ctx.send(f"The ping of this bot is {ping} ms")


@bot.command()
async def a(ctx, * message):
    channel = bot.get_channel(699328249154633768)
    text = ' '.join(message)
    await channel.send(text)

@bot.command()
async def logo(ctx):
    await ctx.send('https://i.imgur.com/Q66BhxI.png')


@bot.command()
async def about(ctx):
    embed = discord.Embed(
        title="Synapse", description='Hello Im synapse', color=0xBB0000)

    await ctx.send(embed=embed)

bot.run()
