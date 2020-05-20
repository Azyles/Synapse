
import asyncio
import base64
import random
import time
import os
import discord
from discord.ext import commands



#StockPrice Imports
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style

description = '''The ultimate bot'''

bot = commands.Bot('X ', description=description)

activeactivity = ['Watching Stock Prices Fall', 'Analyzing Market...', 'Calculating Stock Prices']

graphcolor = ['Red','Blue','Green','Orange','Pink']

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(activeactivity)))
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
async def stock(ctx, * stocksymbol):
    df = web.DataReader(stocksymbol, 'yahoo')
    df['Adj Close'].plot(color=random.choice(graphcolor), linewidth=1)
    plt.savefig("Stock.png")
    file = discord.File("Stock.png", filename="Stock.png")
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    await ctx.send(file=file)
    os.remove("Stock.png")

@bot.command()
async def stockp(ctx, * stocksymbol):
    df = web.DataReader(stocksymbol, 'yahoo')

@bot.command()
async def logo(ctx):
    await ctx.send('https://i.imgur.com/Q66BhxI.png')


@bot.command()
async def about(ctx):
    embed = discord.Embed(
        title="Synapse", description='Hello Im synapse', color=0xBB0000)

    await ctx.send(embed=embed)
