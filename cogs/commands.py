import discord
from discord.ext import commands
from discord import app_commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Pokazuje opóźnienie bota.")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Pong! {bot_latency}ms')

    @app_commands.command(name="server", description="Pokazuje publiczne informacje o serwerze")
    async def server(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"{guild.name} Info", description="Information of this Server",
                              color=discord.Colour.random())
        embed.add_field(name='🆔 ID serwera', value=f"{guild.id}", inline=True)
        embed.add_field(name='📆 Utworzony', value=guild.created_at.strftime("%b %d %Y"), inline=True)
        embed.add_field(name='👑 Właściciel', value=f"{guild.owner}", inline=True)
        embed.add_field(name='👥 Członkowie', value=f'{guild.member_count} Members', inline=True)
        embed.add_field(name='💬 Kanały',
                        value=f'{len(guild.text_channels)} Text📄 | {len(guild.voice_channels)} Voice 🎤',
                        inline=True)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="complex", description="Złożone sprawdzanie autora")
    async def complex_check(self, interaction: discord.Interaction):
        """Kompleksowe sprawdzanie autora"""
        user = interaction.user

        # Informacje o autorze
        embed = discord.Embed(
            title="🔍 Informacje o autorze komendy",
            color=discord.Color.blue()
        )

        # Podstawowe info
        embed.add_field(name="👤 Użytkownik", value=f"{user.mention} (`{user.id}`)", inline=False)
        embed.add_field(name="📅 Dołączył na serwer", value=user.joined_at.strftime("%d.%m.%Y"), inline=True)
        embed.add_field(name="📅 Konto utworzone", value=user.created_at.strftime("%d.%m.%Y"), inline=True)

        # Role
        roles = [role.mention for role in user.roles[1:]]  # Pomijamy @everyone
        embed.add_field(
            name="🎭 Role",
            value=", ".join(roles) if roles else "Brak ról",
            inline=False
        )

        # Uprawnienia
        perms = []
        if user.guild_permissions.administrator:
            perms.append("Administrator")
        if user.guild_permissions.kick_members:
            perms.append("Wyrzucanie")
        if user.guild_permissions.ban_members:
            perms.append("Banowanie")
        if user.guild_permissions.manage_messages:
            perms.append("Zarządzanie wiadomościami")
        if user.guild_permissions.manage_channels:
            perms.append("Zarządzanie kanałami")

        embed.add_field(
            name="🔒 Kluczowe uprawnienia",
            value=", ".join(perms) if perms else "Brak specjalnych uprawnień",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))