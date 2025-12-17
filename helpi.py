import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_role(self, interaction, role_name):
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role:
            await interaction.response.send_message(
                "Rol no encontrado.", ephemeral=True
            )
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"Rol **{role_name}** removido.", ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"Rol **{role_name}** asignado.", ephemeral=True
            )

    @discord.ui.button(label="Gamer", style=discord.ButtonStyle.primary)
    async def gamer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Gamer")

    @discord.ui.button(label="Programador", style=discord.ButtonStyle.success)
    async def dev(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Programador")

    @discord.ui.button(label="Artista", style=discord.ButtonStyle.secondary)
    async def artist(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Artista")


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.command()
@commands.has_permissions(administrator=True)
async def bienvenida(ctx):
    embed = discord.Embed(
        title="¡Bienvenido!",
        description=(
            "Selecciona tus roles usando los botones.\n"
            "Puedes cambiarlos cuando quieras."
        ),
        color=0x2ecc71
    )

    await ctx.send(embed=embed, view=RoleView())


bot.run(TOKEN)
