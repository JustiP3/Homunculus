import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import scanner
import trade_manager

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


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
async def enter(ctx,symbol, option_type, exp,strike:float,price:float,quantity:int=1):
    #symbol, option_type, strike_price, expiration_date, quantity, entry_price

    try:
        position_id = trade_manager.enter_trade(symbol, option_type, strike, exp, quantity, price)

        response = (
            f"Entering position:\n"
            f"ID: {position_id}\n"
            f"{symbol.upper()} "
            f"{strike} {option_type.upper()} "
            f"{exp}\n"
            f"Qty: {quantity}\n"
            f"Entry: ${price}"
        )
    
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Entry error: {e}")


bot.run(TOKEN)