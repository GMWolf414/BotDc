import aiohttp
import discord
from discord.ext import commands
import pyjokes

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        guildID = guild.id
        channel = guild.system_channel

        joke = pyjokes.get_joke(language='en', category='all')
        if channel is not None:
            embed = discord.Embed(title='Witamy ', description=member.mention, color=discord.Color.random())
            embed.add_field(name='Żart dla niego', value=joke)
            await channel.send(embed=embed)

        await member.send(joke)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        joke = pyjokes.get_joke(language='en', category='all')
        if channel is not None:
            embed = discord.Embed(title='Żegnamy ', description=member.mention, color=discord.Color.random())
            embed.add_field(name='Żart dla was', value=pyjokes.get_joke())

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if "mem" in message.content.lower():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://meme-api.com/gimme") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        meme_url = data.get("url")
                        title = data.get("title", "Losowy mem")
                        await message.reply("Czy ktoś wspomniał coś o memach?", mention_author=False)
                        embed = discord.Embed(title=title, color=discord.Color.random())
                        embed.set_image(url=meme_url)

                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("Nie udało się pobrać mema 😢")

async def setup(bot):
    await bot.add_cog(Events(bot))