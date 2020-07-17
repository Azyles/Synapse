import asyncio
import random
import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

from datetime import datetime
#SynapseInvestor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('SynapseBot-02ec52c4b1b0.json')
firebase_admin.initialize_app(cred, {
  'projectId': "synapsebot-fb65a",
})

db = firestore.client()


#StockPrice Imports
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.ticker as ticker

#Specific
from yahoo_fin import stock_info as si
import stocker
#Covid
from covid import Covid
import requests, json

covid = Covid(source="worldometers")

city_name = 'Monterey'
api_key = ""
base_url = "http://api.openweathermap.org/data/2.5/weather?"

description = '''Advanced Stock Analysis Bot'''

bot = commands.Bot('Xe ', description=description)

activeactivity = [
    'Predicting Stock Prices'
]

graphcolor = ['Cyan']

plt.style.use('dark_background')


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=random.choice(activeactivity)))
    print(bot.user.name)
    print('status set to online')
    print(bot.user.id)
    print('--------------------')
    br = str(600)
    global massPing
    if br == "break":
        massPing= False
    else:
        massPing = True
        while massPing:
            x=0
            y= int(100) 
            i = int(600)
            while x < y:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time)
                await asyncio.sleep(i)
                x = x+1
                if massPing == False:
                    x=y + 1


@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)
    print(ping)
    await ctx.send(f"The ping of this bot is {ping} ms")


@bot.command()
async def a(ctx, *message):
    channel = bot.get_channel(699328249154633768)
    text = ' '.join(message)
    await channel.send(text)


@bot.command()
async def pinger(ctx, interval, times):
    br = str(interval)
    global massPing
    if br == "break":
        massPing= False
        await ctx.send("Mass ping broken")
    else:
        massPing = True
        while massPing:
            x=0
            y= int(times) 
            i = int(interval)
            while x < y:
                channel = bot.get_channel(728315394040791061)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                await channel.send(current_time)
                print(current_time)
                await asyncio.sleep(i)
                x = x+1
                if massPing == False:
                    x=y + 1


@bot.command()
async def Graph(ctx, *stocksymbol):
    df = web.DataReader(stocksymbol, 'yahoo')
    df['Adj Close'].plot(
        color=random.choice(graphcolor), linewidth=1, figsize=(10, 7))
    plt.title("Adjusted Close Price of %s" % stocksymbol, fontsize=16)
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.grid(which="major", color='grey', linestyle='-.', linewidth=0.3)
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    await ctx.send(file=file)
    os.remove("Images/Stock.png")


@bot.command()
async def CGraph(ctx, stocksymbol, range: int):
    week = datetime.now() - timedelta(days=range)
    df = web.DataReader(stocksymbol, 'yahoo', week, dt.datetime.now())
    df['Adj Close'].plot(
        color=random.choice(graphcolor), linewidth=1, figsize=(10, 7))
    plt.title("Adjusted Close Price of %s" % stocksymbol, fontsize=16)
    plt.ylabel('Price', fontsize=14)
    plt.xlabel('Days', fontsize=14)
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.3)
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    await ctx.send(file=file)
    os.remove("Images/Stock.png")


@bot.command()
async def AdvancedData(ctx, stocksymbol: str):
    r = requests.get('https://finnhub.io/api/v1/stock/metric?symbol='+stocksymbol+'&metric=all&token=bre3nkfrh5rckh454te0')
    e=r.json()
    j = e['metric']

    embed=discord.Embed(title=e['symbol'], description="Stock Analysis",color=0x5C5D7F)
    embed.set_author(name="Synapse", url="https://github.com/KingRegera", icon_url="https://avatars0.githubusercontent.com/u/56901151?s=460&u=b73775bdb91fcc2c59cb28b066404f3b6b348262&v=4")
    embed.set_thumbnail(url="https://i.imgur.com/WkqngoQ.png")
    embed.add_field(name="10DayAverageTradingVolume", value=j["10DayAverageTradingVolume"], inline=False)
    embed.add_field(name="26WeekPriceReturnDaily", value=j["26WeekPriceReturnDaily"], inline=False)
    embed.add_field(name="3MonthAverageTradingVolume", value=j["3MonthAverageTradingVolume"], inline=False)
    embed.add_field(name="52WeekHigh", value=j["52WeekHigh"], inline=False)
    embed.add_field(name="52WeekHighDate", value=j["52WeekHighDate"], inline=False)
    
    embed.add_field(name="52WeekPriceReturnDaily", value=j["52WeekPriceReturnDaily"], inline=False)
    
    embed.add_field(name="assetTurnoverAnnual", value=j["assetTurnoverAnnual"], inline=False)
    
    embed.add_field(name="beta", value=j["beta"], inline=False)
    
    embed.add_field(name="bookValuePerShareAnnual", value=j["bookValuePerShareAnnual"], inline=False)
    
    embed.add_field(name="bookValuePerShareQuarterly", value=j["bookValuePerShareQuarterly"], inline=False)
    
    embed.add_field(name="cashFlowPerShareAnnual", value=j["cashFlowPerShareAnnual"], inline=False)
    
    embed.add_field(name="cashPerSharePerShareAnnual", value=j["cashPerSharePerShareAnnual"], inline=False)

    
    embed.add_field(name="currentEv/freeCashFlowAnnual", value=j["currentEv/freeCashFlowAnnual"], inline=False)
    
    embed.add_field(name="currentRatioAnnual", value=j["currentRatioAnnual"], inline=False)
    
    embed.add_field(name="dilutedEpsExclExtraTTM", value=j["dilutedEpsExclExtraTTM"], inline=False)
    
    embed.add_field(name="dividendPerShareAnnual", value=j["dividendPerShareAnnual"], inline=False)
    
    embed.add_field(name="dividendYield5Y", value=j["dividendYield5Y"], inline=False)
    
    embed.add_field(name="freeCashFlowAnnual", value=j["freeCashFlowAnnual"], inline=False)
    
    embed.add_field(name="grossMargin5Y", value=j["grossMargin5Y"], inline=False)
    
    embed.add_field(name="inventoryTurnoverAnnual", value=j["inventoryTurnoverAnnual"], inline=False)
    
    embed.add_field(name="netDebtAnnual", value=j["netDebtAnnual"], inline=False)
    
    embed.add_field(name="netIncomeCommonAnnual", value=j["netIncomeCommonAnnual"], inline=False)
    
    embed.add_field(name="netIncomeCommonNormalizedAnnual", value=j["netIncomeCommonNormalizedAnnual"], inline=False)
    
    embed.add_field(name="netInterestCoverageAnnual", value=j["netInterestCoverageAnnual"], inline=False)
    
    embed.add_field(name="netMarginGrowth5Y", value=j["netMarginGrowth5Y"], inline=False)
    
    embed.add_field(name="operatingMarginAnnual", value=j["operatingMarginAnnual"], inline=False)
    
    embed.add_field(name="revenueAnnual", value=j["revenueAnnual"], inline=False)
    
    embed.add_field(name="revenueEmployeeAnnual", value=j["revenueEmployeeAnnual"], inline=False)
    
    embed.add_field(name="revenueGrowth3Y", value=j["revenueGrowth3Y"], inline=False)
    
    embed.add_field(name="revenueGrowth5Y", value=j["revenueGrowth5Y"], inline=False)
    
    embed.add_field(name="revenueGrowthQuarterlyYoy", value=j["revenueGrowthQuarterlyYoy"], inline=False)
    
    embed.add_field(name="totalDebt/totalEquityAnnual", value=j["totalDebt/totalEquityAnnual"], inline=False)
    
    embed.add_field(name="yearToDatePriceReturnDaily", value=j["yearToDatePriceReturnDaily"], inline=False)
    embed.set_footer(text="Synapse https://github.com/KingRegera/Synapse")
    await ctx.send(embed=embed)


@bot.command()
async def AnylastData(ctx, stocksymbol: str):
    r = requests.get('https://finnhub.io/api/v1/stock/recommendation?symbol='+stocksymbol+'&token=bre3nkfrh5rckh454te0')
    e=r.json()
    j = e[0]
    embed=discord.Embed(title=j["symbol"], description="Analyst Recommendation",color=0x5C5D7F)
    embed.set_author(name="Synapse", url="https://github.com/KingRegera", icon_url="https://avatars0.githubusercontent.com/u/56901151?s=460&u=b73775bdb91fcc2c59cb28b066404f3b6b348262&v=4")
    embed.set_thumbnail(url="https://i.imgur.com/WkqngoQ.png")
    embed.add_field(name="Buy", value=j["buy"], inline=False)
    embed.add_field(name="Hold", value=j["hold"], inline=False)
    embed.add_field(name="Period", value=j["period"], inline=False)
    embed.add_field(name="Sell", value=j["sell"], inline=False)
    embed.add_field(name="Strong Buy", value=j["strongBuy"], inline=False)
    embed.add_field(name="Strong Sell", value=j["strongSell"], inline=False)
    embed.set_footer(text="Synapse https://github.com/KingRegera/Synapse")
    await ctx.send(embed=embed)



@bot.command()
async def Analysis(ctx, stocksymbol: str):
    r = requests.get('https://finnhub.io/api/v1/quote?symbol='+stocksymbol+'&token=bre3nkfrh5rckh454te0')
    j=r.json()
    embed=discord.Embed(title="About", description="Stock Analysis",color=0x5C5D7F)
    embed.set_author(name="Synapse", url="https://github.com/KingRegera", icon_url="https://avatars0.githubusercontent.com/u/56901151?s=460&u=b73775bdb91fcc2c59cb28b066404f3b6b348262&v=4")
    embed.set_thumbnail(url="https://i.imgur.com/WkqngoQ.png")
    embed.add_field(name="Current Price", value=j["c"], inline=False)
    embed.add_field(name="Open Price", value=j["o"], inline=False)
    embed.add_field(name="High Price", value=j["h"], inline=False)
    embed.add_field(name="Low Price", value=j["l"], inline=False)
    embed.add_field(name="Previous Close Price", value=j["pc"], inline=False)
    embed.set_footer(text="Synapse https://github.com/KingRegera/Synapse")
    await ctx.send(embed=embed)


@bot.command()
async def Stock(ctx, stocksymbol: str):
    r = requests.get('https://finnhub.io/api/v1/quote?symbol='+stocksymbol+'&token=bre3nkfrh5rckh454te0')
    j=r.json()
    embed=discord.Embed(title="About", description="Stock Analysis",color=0x5C5D7F)
    embed.set_author(name="Synapse", url="https://github.com/KingRegera", icon_url="https://avatars0.githubusercontent.com/u/56901151?s=460&u=b73775bdb91fcc2c59cb28b066404f3b6b348262&v=4")
    embed.set_thumbnail(url="https://i.imgur.com/WkqngoQ.png")
    embed.add_field(name="Current Price", value=j["c"], inline=False)
    embed.add_field(name="Open Price", value=j["o"], inline=False)
    embed.add_field(name="High Price", value=j["h"], inline=False)
    embed.add_field(name="Low Price", value=j["l"], inline=False)
    embed.add_field(name="Previous Close Price", value=j["pc"], inline=False)
    embed.set_footer(text="Synapse https://github.com/KingRegera/Synapse")
    await ctx.send(embed=embed)


@bot.command()
async def Company(ctx, stocksymbol: str):
    r = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol='+stocksymbol+'&token=bre3nkfrh5rckh454te0')
    j=r.json()
    embed=discord.Embed(title=j["name"], description="Stock Analysis",color=0x5C5D7F)
    embed.set_author(name="SynapseBot", url="https://github.com/KingRegera", icon_url="https://i.imgur.com/WkqngoQ.png")
    embed.set_thumbnail(url=j["logo"])
    embed.add_field(name="Country", value=j["country"], inline=False)
    embed.add_field(name="exchange", value=j["exchange"], inline=False)
    embed.add_field(name="Name", value=j["name"], inline=False)
    embed.add_field(name="marketCapitalization", value=j["marketCapitalization"], inline=False)
    embed.add_field(name="Industry", value=j["finnhubIndustry"], inline=False)
    embed.set_footer(text=j["weburl"])
    await ctx.send(embed=embed)


@bot.command()
async def Crypto(ctx, stocksymbol: str):
    r = requests.get('https://www.alphavantage.co/query?function=CRYPTO_RATING&symbol='+stocksymbol+'&apikey=QWOU4B1BS6VHRKOF')
    f=r.json()
    j = f['Crypto Rating (FCAS)']
    a = requests.get('https://api.nomics.com/v1/currencies/ticker?key=9cfc5a1350155356f898ab4ecca3764e&ids=BTC')
    b=a.json()
    embed=discord.Embed(title=j["2. name"], description="Crypto Rating",color=0x5C5D7F)
    embed.set_author(name="SynapseBot", url="https://github.com/KingRegera", icon_url="https://i.imgur.com/WkqngoQ.png")
    embed.set_thumbnail(url="https://i.imgur.com/SYIs6VF.jpg")
    embed.add_field(name="Symbol", value=j["1. symbol"], inline=False)
    embed.add_field(name="Value", value=str(b["price"]), inline=False)
    embed.add_field(name="Rank", value=str(b["rank"]), inline=False)
    embed.add_field(name="Circulating Supply", value=str(b["circulating_supply"]), inline=False)
    embed.add_field(name="Max Supply", value=str(b["max_supply"]), inline=False)
    embed.add_field(name="Market Cap", value=str(b["market_cap"]), inline=False)
    embed.add_field(name="Fcas Rating", value=j["3. fcas rating"], inline=False)
    embed.add_field(name="Fcas score", value=j["4. fcas score"], inline=False)
    embed.add_field(name="Developer Score", value=j["5. developer score"], inline=False)
    embed.add_field(name="Market Maturity Score", value=j["6. market maturity score"], inline=False)
    embed.add_field(name="Utility Score", value=j["7. utility score"], inline=False)
    embed.add_field(name="Last Refreshed", value=j["8. last refreshed"], inline=False)
    embed.add_field(name="Timezone", value=j["9. timezone"], inline=False)
    embed.set_footer(text=j["2. name"])
    await ctx.send(embed=embed)


@bot.command()
async def Stonks(ctx):
    stock = si.get_live_price('DJI')
    if stock < 24000:
        await ctx.send(
            'https://i.kym-cdn.com/photos/images/newsfeed/001/499/826/2f0.png')
    else:
        await ctx.send(
            'https://vmsseaglescall.org/wp-content/uploads/2019/10/Screen-Shot-2019-10-25-at-11.23.07-AM-475x260.png'
        )


@bot.command()
async def RiskReturn(
        ctx,
        stocksymbol: str,
):
    dfcomp = web.DataReader(stocksymbol, 'yahoo')
    retscomp = dfcomp.pct_change()
    plt.scatter(retscomp.mean(), retscomp.std())
    plt.xlabel('Expected returns')
    plt.ylabel('Risk')
    for label, x, y in zip(retscomp.columns, retscomp.mean(), retscomp.std()):
        plt.annotate(
            label,
            xy=(x, y),
            xytext=(20, -20),
            textcoords='offset points',
            ha='right',
            va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    await ctx.send(file=file)
    os.remove("Images/Stock.png")


@bot.command()
async def XRiskReturn(
        ctx,
        stocksymbol: str,
        stocksymbol2: str,
        stocksymbol3: str,
):
    dfcomp = web.DataReader([stocksymbol, stocksymbol2, stocksymbol3], 'yahoo')
    retscomp = dfcomp.pct_change()
    plt.scatter(retscomp.mean(), retscomp.std())
    plt.xlabel('Expected returns')
    plt.ylabel('Risk')
    for label, x, y in zip(retscomp.columns, retscomp.mean(), retscomp.std()):
        plt.annotate(
            label,
            xy=(x, y),
            xytext=(20, -20),
            textcoords='offset points',
            ha='right',
            va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    await ctx.send(file=file)
    os.remove("Images/Stock.png")


@bot.command()
async def Return(ctx, stocksymbol: str):
    df = web.DataReader(stocksymbol, 'yahoo')
    df_daily_returns = df['Adj Close'].pct_change()
    df_monthly_returns = df['Adj Close'].resample('M').ffill().pct_change()
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.plot(df_daily_returns)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Percent")
    ax1.set_title("daily returns data")
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    await ctx.send(file=file)
    os.remove("Images/Stock.png")
    #monthly
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.plot(df_monthly_returns)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Percent")
    ax1.set_title("Monthly returns data")
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    await ctx.send(file=file)
    os.remove("Images/Stock.png")
    #HISTOGRAM
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    df_daily_returns.plot.hist(bins=60)
    ax1.set_xlabel("Daily returns %")
    ax1.set_ylabel("Percent")
    ax1.set_title("daily returns data")
    ax1.text(-0.35, 200, "Extreme Low\nreturns")
    ax1.text(0.25, 200, "Extreme High\nreturns")
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    await ctx.send(file=file)
    os.remove("Images/Stock.png")


@bot.command()
async def Predict(ctx, stocksymbol: str):
    await ctx.send(stocker.predict.tomorrow(stocksymbol))


@bot.command()
async def Data(ctx, stocksymbol, days=0):
    if days == 0:
        yesterday = datetime.now() - timedelta(days=7)
        df = web.DataReader(stocksymbol, 'yahoo', yesterday, dt.datetime.now())
        style.use('ggplot')
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        await ctx.send(df.head())
    else:
        yesterday = datetime.now() - timedelta(days=days)
        df = web.DataReader(stocksymbol, 'yahoo', yesterday, dt.datetime.now())
        style.use('ggplot')
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        await ctx.send(df.head())


@bot.command()
async def Start(ctx):
    doc_ref = db.collection(str(ctx.author.id)).document(u'UserData') 
    doc_ref.set({
        u'Name': ctx.author.name,
        u'Tier': 1,
        u'Cash': 10000,
    })

@bot.command()
async def Portfolio(ctx):
    users_ref = db.collection(str(ctx.author.id))
    docs = users_ref.stream()
    for doc in docs:
        if doc == "UserData":
            print("Ignore")
        else:
            stock = doc.id
            r = requests.get('https://finnhub.io/api/v1/quote?symbol='+str(stock)+'&token=bre3nkfrh5rckh454te0')
            j=r.json()
            sharevalue = j['c']
            refrence = db.collection(str(ctx.author.id)).document(str(stock)) 
            cash = refrence.get({u'Shares'})
            value = u'{}'.format(cash.to_dict()['Shares'])
            sharecashvalue = float(sharevalue) * float(value)
            await ctx.send(f'{doc.id}: {str(sharecashvalue)}')



@bot.command()
async def Sell(ctx, stocksymbol, amount: int):
    doc_ref = db.collection(str(ctx.author.id)).document(u'UserData') 
    doc = doc_ref.get()
    docs = doc_ref.get({u'Cash'})
    bal = u'{}'.format(docs.to_dict()['Cash'])
    if doc.exists:
        doc_refren = db.collection(str(ctx.author.id)).document(str(stocksymbol)) 
        stockown = doc_refren.get()
        if stockown.exists:
            r = requests.get('https://finnhub.io/api/v1/quote?symbol='+stocksymbol+'&token=bre3nkfrh5rckh454te0')
            j=r.json()
            sharevalue = j['c']
            shareown = doc_refren.get({u'Shares'})
            shareowned = u'{}'.format(shareown.to_dict()['Shares'])
            print(float(shareowned))
            sharestocash = float(shareowned)*sharevalue
            print(sharestocash)
            if int(sharestocash) >= amount:
                sharesselling = amount/sharevalue
                print(sharesselling)
                newownedshares = float(shareowned) - sharesselling
                print(newownedshares)
                newbalance = int(bal) + amount
                print(newbalance)
                doc_refr = db.collection(str(ctx.author.id)).document(str(stocksymbol))
                doc_refr.set({
                    u'Shares': newownedshares,
                })
                doc_refm = db.collection(str(ctx.author.id)).document("UserData")
                doc_refm.set({
                    u'Cash': newbalance,
                }, merge=True)
                embed=discord.Embed(title="Sell Successful", description="Successfully sold stocks",color=0x5C5D7F)
                embed.set_author(name="Synapse Xsim", url="https://github.com/KingRegera", icon_url="https://avatars0.githubusercontent.com/u/56901151?s=460&u=b73775bdb91fcc2c59cb28b066404f3b6b348262&v=4")
                embed.set_thumbnail(url="https://i.imgur.com/WkqngoQ.png")
                embed.add_field(name="Sell Price", value=j["c"], inline=False)
                embed.set_footer(text="Synapse https://github.com/KingRegera/Synapse")
                await ctx.send(embed=embed) 
            else:
                await ctx.send("`Sell excedes owned value`")
        else:
            await ctx.send("`No shares to sell`")
    else:
        await ctx.send("User not found, please do the following command `X Start`")

@bot.command()
async def Buy(ctx, stocksymbol, amount: int):
    doc_ref = db.collection(str(ctx.author.id)).document(u'UserData') 
    doc = doc_ref.get()
    if doc.exists:
        docs = doc_ref.get({u'Cash'})
        bal = u'{}'.format(docs.to_dict()['Cash'])
        if int(bal) < amount:
            await ctx.send("Purchase exceds balance")
        else:
            check_share = db.collection(str(ctx.author.id)).document(str(stocksymbol))
            share_check = check_share.get()
            if share_check.exists:
                r = requests.get('https://finnhub.io/api/v1/quote?symbol='+stocksymbol+'&token=bre3nkfrh5rckh454te0')
                j=r.json()
                sharevalue = j['c']
                getsharesc = db.collection(str(ctx.author.id)).document(str(stocksymbol)) 
                docs = getsharesc.get({u'Shares'})
                ownshares = u'{}'.format(docs.to_dict()['Shares'])
                sharesbought = amount/sharevalue
                ownshares = int(float(ownshares)) + sharesbought
                newbalance = int(bal) - amount
                doc_refr = db.collection(str(ctx.author.id)).document(str(stocksymbol))
                doc_refr.set({
                    u'Shares': ownshares,
                })
                doc_refm = db.collection(str(ctx.author.id)).document("UserData")
                doc_refm.set({
                    u'Cash': newbalance,
                }, merge=True)
                embed=discord.Embed(title="Purchase Successful", description="Successfully purchased stocks",color=0x5C5D7F)
                embed.set_author(name="Synapse Xsim", url="https://github.com/KingRegera", icon_url="https://avatars0.githubusercontent.com/u/56901151?s=460&u=b73775bdb91fcc2c59cb28b066404f3b6b348262&v=4")
                embed.set_thumbnail(url="https://i.imgur.com/WkqngoQ.png")
                embed.add_field(name="Shares Bought", value=sharesbought, inline=False)
                embed.add_field(name="Buy Price", value=j["c"], inline=False)
                embed.set_footer(text="Synapse https://github.com/KingRegera/Synapse")
                await ctx.send(embed=embed)   
            else:
                r = requests.get('https://finnhub.io/api/v1/quote?symbol='+stocksymbol+'&token=bre3nkfrh5rckh454te0')
                j=r.json()
                sharevalue = j['c']
                sharesbought = amount/sharevalue
                newbalance = int(bal) - amount
                doc_refr = db.collection(str(ctx.author.id)).document(str(stocksymbol))
                doc_refr.set({
                    u'Shares': sharesbought,
                })
                doc_refm = db.collection(str(ctx.author.id)).document("UserData")
                doc_refm.set({
                    u'Cash': newbalance,
                }, merge=True)
                embed=discord.Embed(title="Purchase Successful", description="Successfully purchased stocks",color=0x5C5D7F)
                embed.set_author(name="Synapse Xsim", url="https://github.com/KingRegera", icon_url="https://avatars0.githubusercontent.com/u/56901151?s=460&u=b73775bdb91fcc2c59cb28b066404f3b6b348262&v=4")
                embed.set_thumbnail(url="https://i.imgur.com/WkqngoQ.png")
                embed.add_field(name="Buy Price", value=j["c"], inline=False)
                embed.set_footer(text="Synapse https://github.com/KingRegera/Synapse")
                await ctx.send(embed=embed)   
    else:
        ctx.send("User not found, please do the following command `X Start`")

@bot.command()
async def Weather(ctx, *, City):
    complete_url = base_url + "appid=" + api_key + "&q=" + City
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        embed = discord.Embed(
            title=City,
            description=
            "Synapse Weather gets information with the help of openweathermap.org",
            color=0x5C5D7F)
        embed.set_author(
            name='Synapse', url="https://github.com/KingRegera/Synapse")
        embed.set_thumbnail(url="https://i.imgur.com/Q66BhxI.png")
        embed.add_field(
            name="Temperature",
            value=str(format(round(current_temperature - 273.15, 2))) + "°C",
            inline=False)
        faren = (current_temperature - 273.15) * 9 / 5 + 32
        embed.add_field(
            name="Temperature",
            value=str(format(round(faren, 2))) + "°F",
            inline=False)
        embed.add_field(
            name="atmospheric pressure",
            value=str(current_pressure) + " hPa",
            inline=False)
        embed.add_field(
            name="humidity", value=str(current_humidiy) + "%", inline=False)
        embed.add_field(
            name="Synapse+ Description",
            value=str(weather_description),
            inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error", description="City Not Found", color=0xFF8080)
        await ctx.send(embed=embed)


@bot.command()
async def CovidGraph(ctx):
    df = pd.read_csv(
        'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
        parse_dates=['Date'])
    countries = [
        'Canada', 'Germany', 'United Kingdom', 'US', 'France', 'China'
    ]
    df = df[df['Country'].isin(countries)]

    # Section 3 - Creating a Summary Column
    df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
    df = df.pivot(index='Date', columns='Country', values='Cases')
    countries = list(df.columns)
    covid = df.reset_index('Date')
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries

    # Section 5 - Calculating Rates per 100,000
    populations = {
        'Canada': 37664517,
        'Germany': 83721496,
        'United Kingdom': 67802690,
        'US': 330548815,
        'France': 65239883,
        'China': 1438027228
    }
    percapita = covid.copy()
    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 100000
    colors = {
        'Canada': '#045275',
        'China': '#089099',
        'France': '#7CCBA2',
        'Germany': '#FCDE9C',
        'US': '#DC3977',
        'United Kingdom': '#7C1D6F'
    }
    plt.style.use('fivethirtyeight')

    # Section 7 - Creating the Visualization
    plot = covid.plot(
        figsize=(12, 8),
        color=list(colors.values()),
        linewidth=5,
        legend=False)
    plot.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    plot.grid(color='#d4d4d4')
    plot.set_xlabel('Date')
    plot.set_ylabel('# of Cases')

    # Section 8 - Assigning Colour
    for country in list(colors.keys()):
        plot.text(
            x=covid.index[-1],
            y=covid[country].max(),
            color=colors[country],
            s=country,
            weight='bold')

    # Section 9 - Adding Labels
    plot.text(
        x=covid.index[1],
        y=int(covid.max().max()) + 45000,
        s="COVID-19 Cases by Country",
        fontsize=23,
        weight='bold',
        alpha=.75)
    plot.text(
        x=covid.index[1],
        y=int(covid.max().max()) + 15000,
        s="",
        fontsize=16,
        alpha=.75)
    plot.text(
        x=percapita.index[1],
        y=-100000,
        s=
        'datagy.io                      Source: https://github.com/datasets/covid-19/blob/master/data/countries-aggregated.csv',
        fontsize=10)
    plt.savefig("Images/Stock.png")
    file = discord.File("Images/Stock.png", filename="Images/Stock.png")
    await ctx.send(file=file)
    os.remove("Images/Stock.png")


@bot.command()
async def Covid19(ctx, Country: str):
    x = covid.get_status_by_country_name(Country)
    await ctx.send(x)


@bot.command()
async def HostTest(ctx, Country: str):
  print('----')
  print('TEST')
  print('----')


@bot.command()
async def Logo(ctx):
    await ctx.send('https://i.imgur.com/WkqngoQ.png')


@bot.command()
async def About(ctx):
  embed=discord.Embed(title="About", description="The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.",color=0x5C5D7F)
  embed.set_author(name="Synapse", url="https://github.com/KingRegera", icon_url="https://avatars0.githubusercontent.com/u/56901151?s=460&u=b73775bdb91fcc2c59cb28b066404f3b6b348262&v=4")
  embed.set_thumbnail(url="https://i.imgur.com/WkqngoQ.png")
  embed.add_field(name="Stock Price", value="X Stock (Symbol)", inline=False)
  embed.add_field(name="Graph", value="X Graph (Symbol)", inline=False)
  embed.add_field(name="Custom Graph", value="X CGraph (days) (Symbol)", inline=False)
  embed.add_field(name="Stock Data", value="X Data (Symbol)", inline=False)
  embed.add_field(name="Stock Return", value="X Return (Symbol)", inline=False)
  embed.add_field(name="Prediction", value="X Predict (Symbol)", inline=False)
  embed.add_field(name="Analysis", value="X Analysis (Symbol)", inline=False)
  embed.add_field(name="Weather", value="X Weather (City)", inline=False)
  embed.add_field(name="Logo", value="X Logo", inline=False)
  embed.add_field(name="About", value="X About", inline=False)
  embed.set_footer(text="Synapse https://github.com/KingRegera/Synapse")
  await ctx.send(embed=embed)

keep_alive()
bot.run('')
