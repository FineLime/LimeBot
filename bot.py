import discord 
from discord.ext import commands
import os 
import aiosqlite
import asyncio

bot = discord.Bot(
    command_prefix=commands.when_mentioned_or(";"),
    intents=discord.Intents.all(),
)
token = os.environ.get("BOT_TOKEN")

async def set_up(): 
    bot.db = await aiosqlite.connect("db.sqlite3")
    
@bot.event
async def on_ready():
    print(f"Running as {bot.user}")

@bot.slash_command(guild_ids=[234119683538812928, 1065746636275453972])
async def ping(ctx):
    
    # Calculate the latency
    latency = bot.latency * 1000


    # Send the response
    message = await ctx.respond(f"Pong! Latency: {latency:.2f}ms")

# Add cogs
for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

asyncio.get_event_loop().run_until_complete(set_up())
bot.run(token)


