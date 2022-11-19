import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands

import datetime

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
        miscpage_list = [
            self.e_misc1,
            self.e_misc2,
        ]
        return miscpage_list
    def e_misc_menu(self,page:int) -> discord.Embed:
        emisclist = self.allpage()

        Embeds = emisclist[page]()
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
        Embeds = miscpage.e_misc_menu(0)
        pagedict = miscpage.allpage()
        allpage = len(pagedict)
        Views = miscmenu_view(author=author,isOnly=isOnly,e_page=e_page,v_page=v_page,allpage=allpage)

class miscmenu_view(discord.ui.View):
    def __init__(self, *, timeout = None,author:int = None,isOnly,e_page:list = [],v_page:list = [],allpage,currentpage = 0):
        super().__init__(timeout=timeout)
        self.author = author
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page
        self.allpage = allpage
        self.currentpage = currentpage

        if len(self.e_page) == 2 and len(self.v_page) == 2:#ごみおぶごみ
            v_page.append(self) #ただのごりおし。どっかからいけるようにしたらダメになるから注意

        if(len(self.e_page) != 0):
            self.add_item(prevbutton(self.e_page,self.v_page))
        self.add_item(backpage(currentpage=self.currentpage,allpage=self.allpage,author=self.author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page))
        self.add_item(nowpage(currentpage=self.currentpage,allpage=self.allpage))
        self.add_item(nextpage(currentpage=self.currentpage,allpage=self.allpage,author=self.author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page))
        if self.currentpage == 0:
            self.add_item(timebutton(isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page))

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


class backpage(discord.ui.Button):
    def __init__(self,currentpage,allpage,author,isOnly,e_page,v_page):
        self.miscmenu = miscmenu_page(author,isOnly)
        self.currentpage = currentpage
        self.allpage = allpage
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page

        if currentpage == 0:
            super().__init__(style=discord.ButtonStyle.blurple,label="◀",disabled=True)
        else:
            super().__init__(style=discord.ButtonStyle.blurple,label="◀")

    async def callback(self, interaction: discord.Interaction):
        self.currentpage -= 1
        Embeds = self.miscmenu.e_misc_menu(self.currentpage)
        author = interaction.user
        Views = miscmenu_view(author=author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page,currentpage=self.currentpage,allpage=self.allpage)
        await interaction.response.edit_message(embed=Embeds,view=Views)

class nowpage(discord.ui.Button):
    def __init__(self,currentpage,allpage):
        self.currentpage = currentpage
        self.allpage = allpage
        super().__init__(style=discord.ButtonStyle.gray,label=(f"{self.currentpage+1}/{self.allpage}"),disabled=True)

class nextpage(discord.ui.Button):
    def __init__(self,currentpage,allpage,author,isOnly,e_page,v_page):
        self.miscmenu = miscmenu_page(author,isOnly)
        self.currentpage = currentpage
        self.allpage = allpage
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page

        if currentpage == allpage -1:
            super().__init__(style=discord.ButtonStyle.blurple,label="▶",disabled=True)
        else:
            super().__init__(style=discord.ButtonStyle.blurple,label="▶")

    async def callback(self, interaction: discord.Interaction):
        self.currentpage += 1
        Embeds = self.miscmenu.e_misc_menu(self.currentpage)
        author = interaction.user
        Views = miscmenu_view(author=author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page,currentpage=self.currentpage,allpage=self.allpage)
        await interaction.response.edit_message(embed=Embeds,view=Views)

class timebutton(discord.ui.Button):
    def __init__(self,isOnly,e_page,v_page):
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page

        super().__init__(style=discord.ButtonStyle.blurple,label="!time",row=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(timeinput(isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page))

# class timeinputview(discord.ui.View):
#     def __init__(self, *, timeout = None,author:int = None,isOnly,e_page:list = [],v_page:list = []):
#         super().__init__(timeout=timeout)
#         self.author = author
#         self.isOnly = isOnly
#         self.e_page = e_page
#         self.v_page = v_page
        

#     async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
#         try:
#             self.author_id = self.author.id
#         except AttributeError:
#             self.author_id = None
#         if self.author_id == None or self.author_id == interaction.user.id:
#             return True
#         else:
#             await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),ephemeral=True)
#             return False

class timeinput(ui.Modal, title='ロール作成フォーム'):
    def __init__(self,isOnly,e_page:list = [],v_page:list = []) -> None:
        super().__init__()
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page
    
    timeinfo = datetime.datetime.now()
    year = timeinfo.year
    month = timeinfo.month
    day = timeinfo.day
    hour = timeinfo.hour

    value_year = ui.TextInput(label="年",style=discord.TextStyle.short, custom_id="year",placeholder=f"年を入力。デフォルト({str(year)}年)", required=False)
    value_month = ui.TextInput(label="月",style=discord.TextStyle.short, custom_id="month",placeholder=f"月を入力。デフォルト({str(month)}月)", required=False)
    value_day = ui.TextInput(label="日",style=discord.TextStyle.short, custom_id="day",placeholder=f"日を入力。デフォルト({str(day)}日)", required=False)
    value_hour = ui.TextInput(label="時間",style=discord.TextStyle.short, custom_id="hour",placeholder=f"時間を入力。デフォルト({str(hour)}時)", required=False)
    value_timezone = ui.TextInput(label="タイムゾーン",style=discord.TextStyle.short, custom_id=f"timezone",placeholder="タイムゾーンを入力", required=False)

    async def on_submit(self, interaction: discord.Interaction,):
        guild = interaction.guild
        author = interaction.user
        yearvalue = self.value_year.value
        monthvalue = self.value_month.value
        dayvalue = self.value_day.value
        hourvalue = self.value_hour.value
        timezonevalue = self.value_timezone.value

        await interaction.response.send_message((f"あなたは{timevalue}入力"))



async def setup(bot):
    print(f"miscellaneous読み込み")
    await bot.add_cog(miscellaneous_menu(bot))