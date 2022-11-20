import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands

from cogs.role import prevbutton



class embedbox_game():
    def __init__(self,author:discord.Member,isOnly) -> None:
        self.author =author
        self.isOnly =isOnly
        self.author_name = author.display_name
        self.author_image = author.display_avatar.url
    
    def e_game_top(self) -> discord.Embed:
        Embeds = discord.Embed(title="ゲームメニュー",
                            color=0xffffff,
                            description="ここではゲームに関する操作ができます。")
        Embeds.add_field(name=(f"・!hnb (ヒット＆ブロー)"), value=(f"ヒット&ブロー"))
        Embeds.add_field(name=(f'・なし'), value=(f'なしなしなしなしなし'))
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds

class hnbplaybutton(discord.ui.Button):
    def __init__(self,e_page:list = [],v_page:list = [],labelname:str='!hnb'):
        super().__init__(label=labelname,style=discord.ButtonStyle.red)
        self.e_page = e_page
        self.v_page = v_page

    async def callback(self, interaction: discord.Interaction):
        pass


class game_menu(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot

    async def game_menu():
        pass

async def setup(bot):
    print(f"game読み込み")
    await bot.add_cog(game_menu(bot))