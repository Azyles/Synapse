
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
from datetime import datetime, timedelta

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import quandl
#Specific
import pyfolio as pf
from yahoo_fin import stock_info as si
import stocker

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
async def Graph(ctx, * stocksymbol):
    df = web.DataReader(stocksymbol, 'yahoo')
    df['Adj Close'].plot(color=random.choice(graphcolor), linewidth=1,figsize=(10, 7))
    plt.title("Adjusted Close Price of %s" % stocksymbol, fontsize=16)
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.3)
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    await ctx.send(file=file)
    os.remove("Images/Stock.png")

@bot.command()
async def Predict(ctx, stocksymbol:str):
    await ctx.send('Coming Soon')



@bot.command()
async def Analysis(ctx, stocksymbol: str):
    stock = si.get_live_price(stocksymbol)
    livevalue = format(round(stock, 2))
    embed = discord.Embed(
        title=stocksymbol, description="Current Value: " + livevalue +"\nChange: " + "X" , color=0x00FFCD)
    await asyncio.sleep(1)
    await ctx.send(embed=embed)

@bot.command()
async def stonks(ctx):
    stock = si.get_live_price('TSLA')
    if stock < 850:
        await ctx.send('https://i.kym-cdn.com/photos/images/newsfeed/001/499/826/2f0.png')
    else:
        await ctx.send('https://vmsseaglescall.org/wp-content/uploads/2019/10/Screen-Shot-2019-10-25-at-11.23.07-AM-475x260.png')

@bot.command()
async def Stock(ctx, stocksymbol: str):
    stock = si.get_live_price(stocksymbol)
    await ctx.send(format(round(stock, 2)))
    

@bot.command()
async def Data(ctx, stocksymbol,days = 0): 
    if days == 0:
        yesterday = datetime.now() - timedelta(days=7)
        df = web.DataReader(stocksymbol, 'yahoo',yesterday,dt.datetime.now())
        style.use('ggplot')
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        await ctx.send(df.head())
    else:
        yesterday = datetime.now() - timedelta(days=days)
        df = web.DataReader(stocksymbol, 'yahoo',yesterday,dt.datetime.now())
        style.use('ggplot')
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        await ctx.send(df.head())

@bot.command()
async def logo(ctx):
    await ctx.send('https://i.imgur.com/Q66BhxI.png')


@bot.command()
async def about(ctx):
    embed = discord.Embed(
        title="Synapse", description='Hello Im synapse', color=0xBB0000)

    await ctx.send(embed=embed)

