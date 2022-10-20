from mimetypes import init
import os
from typing import overload
import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands
from discord.utils import get
from tokenize import Token
from dotenv import load_dotenv
load_dotenv()
import random
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

async def on_message(ctx):
    bot = ctx.guild
    if ctx.content == "r":
        for cog in coglist:
            await bot.reload_extension(cog)

@bot.command()
async def menu(ctx,*,local = None):
    await ctx.message.delete(delay=1)
    views = menu_button()
    bot = ctx.guild
    randomcolor = str("0x"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
    embed = discord.Embed(title="メニュー",
    color=int(randomcolor, base=16),
    description="メニューを選択できます。"
    )
    embed.add_field(name="!role",value="ロールに関するメニュー",inline=True)
    embed.add_field(name="name2",value="value2",inline=True)
    embed.add_field(name="name3",value="value3",inline=True)
    embed.set_footer(text=(f"{ctx.author.display_name}が作成"),icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed,view=views)

class menu_button(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(
        label=(f'!role'),
        style=discord.ButtonStyle.primary,
    )
    async def callback(self, interaction: discord.Interaction,button: discord.ui.Button):
        role_cog = bot.get_cog('role')
        await role_cog.Role_Menu()

# -----------------------------------------
bot.run(Token)
