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

class miscmenu_page():
    def __init__(self,author:discord.Member,isOnly) -> None:
        self.author =author
        self.isOnly =isOnly
        self.author_name = author.display_name
        self.author_image = author.display_avatar.url
        
    def allpage(self):
        miscpage_dict = {
            '1':self.e_misc1,
            '2':self.e_misc2,
        }
        return miscpage_dict
    def e_misc_menu(self,page:int) -> discord.Embed:
        miscdict = self.allpage
        Embeds = miscdict[page]
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds
            #ここじゃなくていいかも　ボタンに実装するとかでも
            
            
    def e_misc1(self) -> discord.Embed:
        Embeds = discord.Embed(title="その他",color=0xffffff,description="色々あります多分。")
        Embeds.add_field(name=(f"・!time"), value=(f"時間表示"))
        Embeds.add_field(name=(f'・なし'), value=(f'value2'))
        return Embeds

    def e_misc2(self) -> discord.Embed:
        Embeds = discord.Embed(title="その他",color=0xffffff,description="色々あります多分。")
        Embeds.add_field(name=(f"・何もなし"), value=(f"テスト"))
        Embeds.add_field(name=(f'・なし'), value=(f'value2'))
        return Embeds
    
    
class miscellaneous_menu(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot

    def misc_top(self,channel:discord.Thread,author:discord.Member,*,isOnly = None,e_page:list = [],v_page:list = []):
        miscpage = miscmenu_page(author,isOnly)
        Embeds = miscpage.e_misc_menu(1)
        pagedict = miscpage.allpage()
        allpage = len(pagedict)
        Views = miscmenu_view(author=author,isOnly=isOnly,e_page=e_page,v_page=v_page)

class miscmenu_view(discord.ui.View):
    def __init__(self, *, timeout = None,author:int = None,isOnly,e_page:list = [],v_page:list = [],allpage,currentpage = 1):
        super().__init__(timeout=timeout)
        self.author = author
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page
        self.allpage = allpage
        self.currentpage = currentpage

        v_page.append(self)
        if(len(self.e_page) != 0):
            self.add_item(prevbutton(self.e_page,self.v_page))

class backpage(discord.ui.Button):
    def __init__(self,currentpage,allpage,author,isOnly):
        self.miscmenu = miscmenu_page(author,isOnly)
        self.currentpage = currentpage
        self.allpage = allpage
        if currentpage == 1:
            super().__init__(style=discord.ButtonStyle.blurple,label="◀",disabled=True)
        else:
            super().__init__(style=discord.ButtonStyle.blurple,label="◀")

    async def callback(self, interaction: discord.Interaction):
        self.currentpage -= 1
        Embeds = self.miscmenu.e_misc_menu(self.currentpage)
        Views = miscmenu_button()
        


async def setup(bot):
    print(f"miscellaneous読み込み")
    await bot.add_cog(miscellaneous_menu(bot))