import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
import os
import json

with open("src/apiKey.txt", "r") as f:
    token = f.readline().strip()

prefixes = {}

def load_prefixes():
    global prefixes
    try:
        with open("src/prefixes.json", "r") as f:
            prefixes = json.load(f)
    except FileNotFoundError:
        prefixes = {}

def save_prefixes():
    with open("src/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

def get_server_prefix(client, message):
    return prefixes.get(str(message.guild.id), "!")

# Wczytaj prefixy przy starcie bota
load_prefixes()

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_server_prefix, intents=intents)

@client.event
async def on_guild_join(guild):
    prefixes[str(guild.id)] = "!"
    save_prefixes()

@client.event
async def on_guild_remove(guild):
    prefixes.pop(str(guild.id), None)
    save_prefixes()

@client.event
async def on_ready():
    await client.tree.sync()
    print("Bot zalogowany i globalne komendy zsynchronizowane")
    # Ustaw status na domyślny, np. z prefixem globalnym (pierwszym z listy lub "!")
    global_prefix = next(iter(prefixes.values()), "!")
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.listening, name=f"prefix: {global_prefix}")
    )

@client.event
async def on_command_completion(ctx):
    # Po każdej komendzie ustaw status z aktualnym prefixem serwera
    prefix = prefixes.get(str(ctx.guild.id), "!")
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.listening, name=f"prefix: {prefix}")
    )

@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    prefixes[str(ctx.guild.id)] = prefix
    save_prefixes()
    await ctx.send(f"Prefix zmieniony na: `{prefix}`")

@setprefix.error
async def setprefix_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Brak wymaganych uprawnień do zmiany prefixa.")

async def load_cogs():
    tasks = []
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            tasks.append(client.load_extension(f"cogs.{filename[:-3]}"))
            print(f"Wczytano {filename[:-3]}.py")
    await asyncio.gather(*tasks)

async def main():
    load_prefixes()
    async with client:
        await load_cogs()
        await client.start(token)

asyncio.run(main())
