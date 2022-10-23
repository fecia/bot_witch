import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands
from discord.utils import get
from grpc import channel_ready_future

# -----------------------------------------------------------

class role_menu(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
    
    @commands.command
    async def role(self,ctx,isOnly=None):
        author = ctx.author
        await self.role_top(channel=ctx,author=author,isOnly=isOnly)

    async def role_top(self,channel,author,*,isOnly = None):
        author_name = author.display_name
        author_image = author.display_avatar.url
        Embeds = discord.Embed(title="ロールメニュー",
                            color=0xffffff,
                            description="ここではロールに関する操作ができます。")
        Embeds.add_field(name=(f"・一覧"), value=(f"ロールの一覧を表示し付与することもできます"))
        Embeds.add_field(name=(f'・追加'), value=(f'フォーム形式でロールを作成できます'))
        if(isOnly == "1"):
            Embeds.set_footer(text=(f"{author_name}のみ操作可能"),icon_url=author_image)
            Views = RoleMenuButtons(author=author)
        else:
            Embeds.set_footer(text=(f"{author_name}が作成"),icon_url=author_image)
            Views = RoleMenuButtons()

        await channel.send(embed=Embeds,view=Views)

class RoleMenuButtons(discord.ui.View):
    def __init__(self, *, timeout = None,author:int = None):
        super().__init__(timeout=timeout)
        self.author= author

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        try:
            self.author_id = self.author.id
        except AttributeError:
            self.author_id = None
        if self.author_id == None or self.author_id == interaction.user.id:
            return True
        else:
            await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),
                                            ephemeral=True)
            return False
# 第一ボタン
    @discord.ui.button(
    label=(f'一覧'),
    style=discord.ButtonStyle.primary,)

    async def list(self, interaction: discord.Interaction,button: discord.ui.Button):
        pass
# 第二ボタン
    @discord.ui.button(
    label=(f'作成'),
    style=discord.ButtonStyle.primary,)
    
    async def make(self, interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_modal(Role_question())

class Role_question(ui.Modal, title='ロール作成フォーム'):
    def __init__(self) -> None:
        super().__init__()

    value_name = ui.TextInput(label=(f'名前'),
                            custom_id="name",
                            placeholder=(f"名前を入力してください。"),
                            required=True)
    value_color = ui.TextInput(label=(f'色'),
                            custom_id="color",
                            placeholder=(f"色を#をつけ入力してください(16進数)例:#a1b3f0"),
                            required=True,
                            max_length=7,
                            min_length=7)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        R_name = self.value_name.value
        R_color = self.value_color.value
        R_color = int(R_color.replace("#", "0x"), base=16)
        await guild.create_role(name=R_name,
                                colour=R_color,
                                hoist=0,
                                mentionable=1)
        Embed = discord.Embed(color=R_color)
        Embed.add_field(name=(f'{R_name}を作成しました'), value=(f'作成したロールをつけますか？'))
        views = RoleAttach()
        await interaction.response.send_message(embed=Embed, view=views)


async def setup(bot):
    print(f"role読み込み")
    await bot.add_cog(role_menu(bot))