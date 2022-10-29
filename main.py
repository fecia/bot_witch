import os
import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands
from discord.utils import get

from tokenize import Token
from dotenv import load_dotenv
load_dotenv()
import random

from cogs.role import *
# ---------------------------------------

bot_prefix = "!"
Token = os.environ['TOKEN_KEY']

# ---------------------------------------

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# ---------------------------------------

coglist = [
    'cogs.role'
]

# ---------------------------------------

@bot.event
async def on_ready():
    print(f'{bot.user} としてログインしています')
    for cog in coglist:
        await bot.load_extension(cog)
@bot.listen("on_message")
async def reload_cogs(msg):
    if msg.author == bot.user:
        return
    if msg.content == "r":
        for cog in coglist:
            await bot.reload_extension(cog)
        await msg.channel.send("リロード完了")

# ----------------------------------------------------

# ----------------------------------------------------
    
@bot.command()
async def menu(ctx,isOnly=None):
    await ctx.message.delete(delay=1)
    # 変数作成
    randomcolor = str("0x"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
    author = ctx.author
    author_name = author.display_name
    author_image = author.display_avatar.url
    # ------------------
    embed = discord.Embed(title="メニュー",
    color=int(randomcolor, base=16),
    description="メニューを選択できます。"
    )
    embed.add_field(name="!role",value="ロールに関するメニュー",inline=True)
    embed.add_field(name="name2",value="value2",inline=True)
    embed.add_field(name="name3",value="value3",inline=True)
    if isOnly =="1":
        embed.set_footer(text=(f"{author_name}のみ操作可能"),icon_url=author_image)
        views = menu_button(author=author,isOnly=isOnly,isTree=True)
    else:
        embed.set_footer(text=(f"{author_name}が作成"),icon_url=author_image)
        views = menu_button(isTree=True)
    await ctx.send(embed=embed,view=views)

class menu_button(discord.ui.View):
    def __init__(self, *, timeout = None,author:int = None,isOnly = None,isTree:bool = False):
        super().__init__(timeout=timeout)
        self.author = author
        self.isOnly = isOnly
        self.isTree = isTree

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

    @discord.ui.button(
        label=(f'!role'),
        style=discord.ButtonStyle.primary,
    )

    async def callback(self, interaction: discord.Interaction,button: discord.ui.Button):
        # c_RoleMenu = role_menu(bot=bot)
        # Embeds = c_RoleMenu.e_role_top(author=interaction.user,isOnly = self.isOnly)
        # Views = c_RoleMenu.v_role_top(author=interaction.user,isOnly = self.isOnly)
        judge = judgeisOnly(author=interaction.user,isOnly = self.isOnly)
        evs = embedbox(author=interaction.user,isOnly = self.isOnly)
        Embeds = evs.e_role_top()
        Views = judge.v_isOnly(button=RoleMenuButtons)
        await interaction.response.edit_message(embed=Embeds,view=Views,)
        
        # await c_RoleMenu.role_top(channel=interaction.channel,author=interaction.user,isOnly=self.isOnly,isTree=self.isTree)
# ------------------------------------------
#てすと
@bot.command()
async def test(ctx):
    await ctx.message.delete(delay=1)
    # 変数作成
    randomcolor = str("0x"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
    author = ctx.author
    author_name = author.display_name
    author_image = author.display_avatar.url
    # ------------------
    embed = discord.Embed(title="メニュー",
    color=int(randomcolor, base=16),
    description="メニューを選択できます。"
    )
    embed.add_field(name="!fsdfdafae",value="we",inline=True)
    views = test_button()
    await ctx.send(embed=embed,view=views)

def change_embed() -> discord.Embed:
    Embeds = discord.Embed(title="正しいよ正しいよ",
    color=0xffffff,
    description="正しいよ"
    )
    Embeds.add_field(name="!正しいよ",value="正しいよ",inline=True)
    return Embeds

class test_button(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)

    @discord.ui.button(
        label=(f'エディット'),
        style=discord.ButtonStyle.primary,
    )

    async def test(self, interaction: discord.Interaction,button: discord.ui.Button):
        # # sent_message = await interaction.original_response()
        # Embeds = discord.Embed(title="正しいよ正しいよ",
        # color=0xffffff,
        # description="正しいよ"
        # )
        # Embeds.add_field(name="!正しいよ",value="正しいよ",inline=True)
        Embeds = change_embed()
        await interaction.response.edit_message(embed=Embeds)
        
# -----------------------------------------
bot.run(Token)
