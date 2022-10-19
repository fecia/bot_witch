import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands
from discord.utils import get
# -----------------------------------------------------------

class role_menu(commands.Cog):
    def __init__(self,bot,ctx) -> None:
        self.bot = bot
        ctx = ctx

    @commands.command()
    async def role(self):
        Embed = discord.Embed(title="ロールメニュー",
                            color=0xffffff,
                            description="ここではロールに関する操作ができます。")
        Embed.add_field(name=(f"・一覧"), value=(f"ロールの一覧を表示し付与することもできます"))
        Embed.add_field(name=(f'・追加'), value=(f'フォーム形式でロールを作成できます'))
        
        await self.ctx.send(embed=Embed)

    class RoleMenuButtons(discord.ui.View):
        @discord.ui.button(
        label=(f'一覧'),
        style=discord.ButtonStyle.primary,
    )
        
        async def list(self, interaction: discord.Interaction,button: discord.ui.Button):
            pass
        
        @discord.ui.button(
        label=(f'追加'),
        style=discord.ButtonStyle.primary,
    )
        
        async def make(self, interaction: discord.Interaction,button: discord.ui.Button):
            await interaction.response.send_modal()


async def setup(bot):
    print(f"role読み込み")
    await bot.add_cog(role(bot))