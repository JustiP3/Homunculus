import os

import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import time
import zoneinfo
from dotenv import load_dotenv

import scanner
import trade_manager

### CONFIG ###

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
PACIFIC = zoneinfo.ZoneInfo("America/Los_Angeles")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


### SCHEDULED TASKS ###

@tasks.loop(time=time(hour=7, minute=00, tzinfo=PACIFIC))
async def scheduled_scan():

    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    print(channel)
    print("running scheduled scan...")
    try:

        result = scanner.run_scanner()
        await channel.send(
            f"Scheduled scan:\n{result}"
        )

    except Exception as e:

        await channel.send(
            f"Scheduled scan error:\n{e}"
        )

### BOT Startup Event ###

@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    if not scheduled_scan.is_running():
        scheduled_scan.start()



### BOT Commands ###

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def scan(ctx):

    await ctx.send("Running scanner...")

    try:
        result = scanner.run_scanner()
        await ctx.send(result)
    except Exception as e:
        await ctx.send(f"Scanner error: {e}")

@bot.command()
async def enter(
    ctx,
    symbol,
    option_type,
    exp,
    strike: float,
    price: float,

    quantity: int = 1,

    trend_score: float = None,
    entry_score: float = None,

    entry_rsi: float = None,
    relative_volume: float = None,

    sector: str = None
):

    try:

        position_id = trade_manager.enter_trade(

            symbol=symbol.upper(),

            option_type=option_type.upper(),

            strike_price=strike,
            expiration_date=exp,

            quantity=quantity,

            entry_price=price,

            trend_score=trend_score,
            entry_score=entry_score,

            entry_rsi=entry_rsi,

            relative_volume=relative_volume,

            sector=sector
        )

        response = (
            f"📈 Entered Position\n\n"

            f"ID: {position_id}\n"

            f"{symbol.upper()} "
            f"{strike} "
            f"{option_type.upper()} "
            f"{exp}\n\n"

            f"Qty: {quantity}\n"
            f"Entry: ${price}\n"
        )

        if trend_score is not None:
            response += f"Trend Score: {trend_score}\n"

        if entry_score is not None:
            response += f"Entry Score: {entry_score}\n"

        if entry_rsi is not None:
            response += f"RSI: {entry_rsi}\n"

        if relative_volume is not None:
            response += f"Rel Volume: {relative_volume}\n"

        if sector is not None:
            response += f"Sector: {sector}\n"

        await ctx.send(response)

    except Exception as e:
        await ctx.send(f"❌ Entry error: {e}")

@bot.command()
async def exit(ctx, position_id: int, exit_price: float):

    try:
        trade_manager.exit_trade(position_id, exit_price)

        response = (
            f"Exiting position ID {position_id} at ${exit_price}"
        )
    
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Exit error: {e}")

@bot.command()
async def update(ctx, position_id: int, current_price: float,qty:int=None):

    try:
        trade_manager.update_position(position_id, current_price, qty)

        response = (
            f"Updating position ID {position_id} with current price ${current_price}"
        )
    
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Update error: {e}")

@bot.command()
async def positions(ctx):

    try:
        positions = trade_manager.get_all_positions()

        if not positions:
            await ctx.send("No open positions.")
            return

        response = "Current Positions:\n\n"
        for p in positions:
            response += (
                f"ID: {p['id']} | "
                f"{p['symbol']} {p['option_type'].upper()} "
                f"{p['strike']} {p['expiration']} | "
                f"Qty: {p['quantity']} | "
                f"Entry: ${p['entry_price']} | "
                f"Current: ${p['current_price']} | "
                f"Status: {p['status']}\n"
            )
        
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Positions error: {e}")

### RUN BOT ###
bot.run(TOKEN)