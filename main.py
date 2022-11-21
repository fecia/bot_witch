import os
from tokenize import Token

import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()

import datetime
from zoneinfo import ZoneInfo
import json
import random

from cogs.role import *
from cogs.miscellaneous import miscmenu_view, miscmenu_page
from cogs.game import gamemenuview, embedbox_game
# ---------------------------------------

bot_prefix = "!"
Token = os.environ['TOKEN_KEY']

# ---------------------------------------

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# ---------------------------------------

coglist = [
    'cogs.role',
    'cogs.miscellaneous',
    'cogs.game'
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
    author :discord.Member = ctx.author
    author_name = author.display_name
    author_image = author.display_avatar.url
    # ------------------
    embed = discord.Embed(title="メニュー",color=int(randomcolor, base=16),description="メニューを選択できます。")
    e_page = []
    v_page = []
    embed.add_field(name="!role",value="ロールに関するメニュー",inline=True)
    embed.add_field(name="!game",value="ゲームメニュー",inline=True)
    embed.add_field(name="!misc",value="その他、細かいもの",inline=True)

    if isOnly =="1":
        embed.set_footer(text=(f"{author_name}のみ操作可能"),icon_url=author_image)
        e_page.append(embed)
        views = menu_button(author=author,isOnly=isOnly,e_page=e_page,v_page=v_page)
    else:
        embed.set_footer(text=(f"{author_name}が作成"),icon_url=author_image)
        e_page.append(embed)
        views = menu_button(e_page=e_page,v_page=v_page)
    v_page.append(views)

    await ctx.send(embed=e_page[-1],view=v_page[-1])

class menu_button(discord.ui.View):
    def __init__(self, *, timeout = None,author:discord.Member = None,isOnly = None,e_page:list,v_page:list):
        super().__init__(timeout=timeout)
        self.author = author
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page
        v_page.append(self)

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

    async def gotorole(self, interaction: discord.Interaction,button: discord.ui.Button):
        evs = embedbox(author=interaction.user,isOnly = self.isOnly)
        Embeds = evs.e_role_top()
        self.e_page.append(Embeds)
        judge = judgeisOnly(author=interaction.user,isOnly = self.isOnly,e_page=self.e_page,v_page=self.v_page)
        Views = judge.v_isOnly(button=RoleMenuButtons)
        await interaction.response.edit_message(embed=Embeds,view=Views,)

    @discord.ui.button(
        label=(f'!misc'),
        style=discord.ButtonStyle.primary,
    )

    async def gotomisc(self, interaction: discord.Interaction,button: discord.ui.Button):
        author = interaction.user
        miscpage = miscmenu_page(author,self.isOnly)
        Embeds = miscpage.e_misc_menu(0)
        pagedict = miscpage.allpage()
        self.e_page.append(Embeds)
        allpage = len(pagedict)
        Views = miscmenu_view(author=author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page,allpage=allpage)
        await interaction.response.edit_message(embed=Embeds,view = Views)

    @discord.ui.button(
        label=(f'!game'),
        style=discord.ButtonStyle.primary,
    )

    async def gotogame(self,interaction: discord.Interaction,button: discord.ui.Button):
        author = interaction.user
        evs = embedbox_game(author,self.isOnly)
        Embeds = evs.e_game_top()
        self.e_page.append(Embeds)
        Views = gamemenuview(isOnly=self.isOnly,author=author,e_page=self.e_page,v_page=self.v_page)
        await interaction.response.edit_message(embed=Embeds,view=Views)

    @discord.ui.button(
        label=(f'もっかい同じ送る(テスト)'),
        style=discord.ButtonStyle.primary,
    )

    async def aho(self, interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_message(embed=self.e_page[-1],view=self.v_page[-1])

@bot.command()
async def register(ctx):
    if ctx.guild:
        guild :discord.Guild= ctx.guild
        json_data ={
        "name": guild.name,
        "id" : guild.id,
        "registerdate": str(datetime.datetime.now()),
        "role":[]
        }
        path = "./bot_witch/guilds/" + str(guild.id) + ".json"
        if (os.path.isfile(path)):
            embeds = discord.Embed(color=0x880088,title="すでに登録済みです",description="一部の保存されているデータが消去される可能性があります。\n本当に変更しますか？")
            await ctx.send(embed=embeds,view=registerconfirm())
            return
        with open(path, "a+") as file:
            json.dump(json_data,file,indent=4)    # 追加する値を入力
        await ctx.send("登録完了しました")
        return
    else: #DMやったとき
        user = ctx.author
        tz = ZoneInfo('Asia/Tokyo')
        timedate = datetime.datetime.now(tz=tz)
        result = timedate.strftime('%Y/%m/%d (%Z)')
        json_data ={
        "name": user.name,
        "id" : user.id,
        "registerdate": result,
        "battle":"0",
        "win"   :"0",
        "draw"  :"0"
        }
        path = "./bot_witch/users/" + str(user.id) + ".json"
        if (os.path.isfile(path)):
            embeds = discord.Embed(color=0x880088,title="すでに登録済みです",description="一部の保存されているデータが消去される可能性があります。\n本当に変更しますか？")
            await ctx.send(embed=embeds,view=registerconfirm(isdm = True))
            return
        with open(path, "w") as file:
            json.dump(json_data,file,indent=4)    # 追加する値を入力
        await ctx.send("登録完了しました")
        return

class registerconfirm(discord.ui.View):
    def __init__(self,*,timeout=None,isdm:bool = False) -> None:
        super().__init__(timeout=timeout)
        self.isdm = isdm
    @discord.ui.button(
    label=(f'変更する'),
    style=discord.ButtonStyle.green,)

    async def callback(self, interaction: discord.Interaction,button: discord.ui.Button):
        if self.isdm:
            user = interaction.user
            tz = ZoneInfo('Asia/Tokyo')
            timedate = datetime.datetime.now(tz=tz)
            result = timedate.strftime('%Y/%m/%d (%Z)')
            json_data ={
            "name": user.name,
            "id" : user.id,
            "registerdate": result
            }
            path = "./bot_witch/users/" + str(user.id) + ".json"
            with open(path, "w") as file:
                json.dump(json_data,file,indent=4)    # 追加する値を入力
            embed = discord.Embed(color=0x00ff00,description="登録完了しました")
            await interaction.response.edit_message(embed=embed,view=None)
            return
        else:
            guild = interaction.guild
            json_data ={
            "name": guild.name,
            "id" : guild.id,
            "registerdate": str(datetime.datetime.now()),
            "role":[]
            }
            path = "./bot_witch/guilds/" + str(guild.id) + ".json"
            with open(path, "w") as file:
                json.dump(json_data,file,indent=4)    # 追加する値を入力
            embed = discord.Embed(color=0x00ff00,description="登録完了しました")
            await interaction.response.edit_message(embed=embed,view=None)
            return


    @discord.ui.button(
    label=(f'変更しない'),
    style=discord.ButtonStyle.red,)
    async def stop(self, interaction: discord.Interaction,button: discord.ui.Button):
        embed = discord.Embed(color=0xff0000,description="中止しました")
        await interaction.response.edit_message(embed=embed,view=None)


bot.run(Token)
