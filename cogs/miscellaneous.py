import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands

from cogs.role import prevbutton

class embedbox_misc():
    def __init__(self,author:discord.Member,isOnly) -> None:
        self.author =author
        self.isOnly =isOnly
        self.author_name = author.display_name
        self.author_image = author.display_avatar.url

    def e_misc_top(self) -> discord.Embed:
        Embeds = discord.Embed(title="その他",color=0xffffff,description="色々あります多分。")
        Embeds.add_field(name=(f"・!time"), value=(f"時間表示"))
        Embeds.add_field(name=(f'・なし'), value=(f'value2'))
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds


class miscellaneous_menu(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot

    def misc_top():
        Embeds = ebox


async def setup(bot):
    print(f"miscellaneous読み込み")
    await bot.add_cog(miscellaneous_menu(bot))