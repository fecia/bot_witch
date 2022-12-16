import os
from tokenize import Token

import discord
from discord import Embed, Role, SelectOption, User, ui,app_commands
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

import datetime
from zoneinfo import ZoneInfo
import json
import random
from PIL import Image, ImageFilter,ImageDraw,ImageFont
import io

from cogs.role import *
from cogs.miscellaneous import miscmenu_view, miscmenu_page
from cogs.game import gamemenuview, embedbox_game
# ---------------------------------------

bot_prefix = "!"
Token = os.environ['TOKEN_KEY']

# ---------------------------------------

class Mybot(commands.Bot):
    def __init__(self, *, intents: discord.Intents,command_prefix):
        super().__init__(intents=intents,command_prefix=command_prefix)

    async def setup_hook(self):
        for cog in coglist:
            await self.load_extension(cog)
        MY_GUILD = discord.Object(751825027548053605)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.all()
bot = Mybot(command_prefix=bot_prefix, intents=intents)
tree = bot.tree

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

# @bot.listen("on_message")
# async def reload_cogs(msg):
#     if msg.author == bot.user:
#         return
#     if msg.content == "r":
#         for cog in coglist:
#             await bot.reload_extension(cog)
#         await msg.channel.send("リロード完了")

# コマンドテスト-----------------------------------------

@bot.hybrid_command()  # ハイブリッドコマンド
async def ping(ctx):
    await ctx.reply("Pong!")
@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')
@bot.tree.command(name="slash",guild=discord.Object(id=751825027548053605))
async def slash(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(f'{number=} {string=}', ephemeral=True)
# ----------------------------------------------------
    
@bot.hybrid_command()
async def menu(ctx,isonly=None):
    if ctx.interaction is None:
        await ctx.message.delete(delay=1)
    # 変数作成のみ操作可能
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
    print(type(isonly))

    if isonly =="1":
        embed.set_footer(text=(f"{author_name}のみ操作可能"),icon_url=author_image)
        e_page.append(embed)
        views = menu_button(author=author,isonly=isonly,e_page=e_page,v_page=v_page)
    else:
        embed.set_footer(text=(f"{author_name}が作成"),icon_url=author_image)
        e_page.append(embed)
        views = menu_button(author=author,e_page=e_page,v_page=v_page)
    v_page.append(views)

    await ctx.send(embed=e_page[-1],view=v_page[-1])

class menu_button(discord.ui.View):
    def __init__(self, *, timeout = None,author:discord.Member = None,isonly = None,e_page:list,v_page:list):
        super().__init__(timeout=timeout)
        self.author = author
        self.isonly = isonly
        self.e_page = e_page
        self.v_page = v_page
        v_page.append(self)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if self.isonly == "1":
            if self.author != interaction.user:
                await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),ephemeral=True)
                return False
        return True

    @discord.ui.button(
        label=(f'!role'),
        style=discord.ButtonStyle.primary,
    )

    async def gotorole(self, interaction: discord.Interaction,button: discord.ui.Button):
        evs = embedbox(author=self.author,isonly = self.isonly)
        Embeds = evs.e_role_top()
        self.e_page.append(Embeds)
        judge = judgeisonly(author=self.author,isonly = self.isonly,e_page=self.e_page,v_page=self.v_page)
        Views = judge.v_isonly(button=RoleMenuButtons)
        await interaction.response.edit_message(embed=Embeds,view=Views,)

    @discord.ui.button(
        label=(f'!misc'),
        style=discord.ButtonStyle.primary,
    )

    async def gotomisc(self, interaction: discord.Interaction,button: discord.ui.Button):
        miscpage = miscmenu_page(self.author,self.isonly)
        Embeds = miscpage.e_misc_menu(0)
        pagedict = miscpage.allpage()
        self.e_page.append(Embeds)
        allpage = len(pagedict)
        Views = miscmenu_view(author=self.author,isonly=self.isonly,e_page=self.e_page,v_page=self.v_page,allpage=allpage)
        await interaction.response.edit_message(embed=Embeds,view = Views)

    @discord.ui.button(
        label=(f'!game'),
        style=discord.ButtonStyle.primary,
    )

    async def gotogame(self,interaction: discord.Interaction,button: discord.ui.Button):
        evs = embedbox_game(author=self.author,isonly=self.isonly)
        Embeds = evs.e_game_top()
        self.e_page.append(Embeds)
        Views = gamemenuview(isonly=self.isonly,author=self.author,e_page=self.e_page,v_page=self.v_page)
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
            "registerdate": result,
            "hnb":{
                "battle": 0,
                "win": 0,
                "draw": 0,
                "recent":"ddddd"
                }
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

@bot.command()
async def test(ctx):
    Embeds = discord.Embed(title="0",description="0")
    Views = testview()
    await ctx.send(embed=Embeds,view=Views)


class testview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(testbutton())

class testbutton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="test",style=discord.ButtonStyle.blurple)
        self.count = 0
    
    async def callback(self, interaction: discord.Interaction):
        self.count+=1
        Embeds = discord.Embed(title=f"今{self.count}",description=f"今{self.count}")
        Embeds.add_field(name="test",value="v")
        elist = [Embeds]
        await interaction.response.edit_message(embed=elist[0])

@bot.command()
async def test2(ctx):
    path = f"./bot_witch/users/{ctx.author.id}.json"
    if not os.path.isfile(path=path):
        return await ctx.send("データ無し !register")
    else:
        with open(path,"r") as file:
            userinfo = json.load(file)
    
    with open(path,"r") as date:
        info = json.load(date)
    iconbyte = await ctx.author.display_avatar.read()
    icon = Image.open(io.BytesIO(iconbyte))
    icon = icon.resize((200,200))
    alpha = Image.new("RGBA", icon.size, (255, 255, 255, 0))
    background = Image.open("./bot_witch/background.png")
    # background = Image.new("RGBA",(1000,300),(R,G,B,255))
    background_draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("msgothic.ttc", 48)
    textink ="#0a3758"
    background_draw.text((290,55),"ヒット＆ブロー",fill=textink,font=font)
    background_draw.multiline_text((310,135),f"総試合数:\n{info['hnb']['battle']}:"
                            ,fill=textink,font=font,spacing=4,align="right")
    background_draw.multiline_text((595,135),f"勝ち:\n{info['hnb']['win']}:"
                            ,fill=textink,font=font,spacing=4,align="right")
    background_draw.multiline_text((775,135),f"引き分け:\n{info['hnb']['draw']}:"
                            ,fill=textink,font=font,spacing=4,align="right")
    mask = Image.new("L", icon.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 199, 199), fill=255)
    icon_c = Image.composite(icon, alpha, mask)

    background.paste(im=icon_c,box=(50,50),mask=icon_c)
    bufferimg = io.BytesIO()
    background.save(bufferimg,"png")
    bufferimg.seek(0)

    img = discord.File(bufferimg,filename="image.png")
    Embeds = discord.Embed(title="test")
    Embeds.set_image(url="attachment://image.png")
    await ctx.send(file=img,embed=Embeds)

@bot.command()
async def test3(ctx,gamename = "hnb",isdraw = None):
    path = f"./bot_witch/users/{ctx.author.id}.json"
    with open(path,"r") as file:
        text = json.load(file)
    with open(path,"w") as file:
        text[gamename]["win"] += 1
        text[gamename]["battle"] +=1
        json.dump(text,file,indent=4)

bot.run(Token)