import discord
from discord.ext import commands
from discord import app_commands

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Usuwa podaną ilość wiadomości")
    @app_commands.describe(amount="Ilość wiadomości do usunięcia (1-100)")
    async def clear(self, interaction: discord.Interaction, amount: int):
        # Sprawdź permisję
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "Nie masz uprawnień do usuwania wiadomości.", ephemeral=True
            )
            return

        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "Podaj ilość wiadomości z zakresu 1-100.", ephemeral=True
            )
            return

        # Usuwanie wiadomości i odpowiedź
        deleted = await interaction.channel.purge(limit=amount)
        embed_msg = discord.Embed(
            title="Wyczyszczono",
            description=f"Usunięto {len(deleted)} wiadomości.",
            color=discord.Color.blue()
        )
        embed_msg.set_footer(
            text=interaction.user.name,
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed_msg, ephemeral=True)



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason):
        await member.kick()
        embed_msg = discord.Embed(title="Wyrzucono",description="Kick", color=discord.Color.red())
        embed_msg.add_field(name="Wyrzucono: ", value=f"{member.name} przez {ctx.author.mention}", inline=False)
        embed_msg.add_field(name="Powód: ", value=reason, inline=False)
        embed_msg.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        await ctx.message.delete()
        await ctx.send(embed=embed_msg)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason):
        await member.ban()
        embed_msg = discord.Embed(title="Zbanowano", color=discord.Color.red())
        embed_msg.add_field(name="Zbanowano: ", value=f"{member.name} przez {ctx.author.mention}", inline=False)
        embed_msg.add_field(name="Powód: ", value=reason, inline=False)
        embed_msg.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        await ctx.message.delete()
        await ctx.send(embed = embed_msg)

    @commands.command(name="unban", aliases=["ub"])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userid):
        user = discord.Object(id=userid)
        await ctx.guild.unban(user)
        embed_msg = discord.Embed(title="Odbanowano", color=discord.Color.green())
        embed_msg.add_field(name="Odbanowano: ", value=f"<@{userid}> przez {ctx.author.mention}", inline=False)
        embed_msg.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        await ctx.message.delete()
        await ctx.send(embed=embed_msg)



async def setup(bot):
    await bot.add_cog(Administration(bot))