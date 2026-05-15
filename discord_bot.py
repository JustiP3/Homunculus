import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import scanner

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


bot.run(TOKEN)