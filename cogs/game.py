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
        Embeds = discord.Embed(title="ゲームメニュー",color=0xffffff,description="ここではゲームに関する操作ができます。")
        Embeds.add_field(name=(f"・!hnb (ヒット&ブロー)"), value=(f"ヒット&ブロー"))
        Embeds.add_field(name=(f'・なし'), value=(f'なしなしなしなしなし'))
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds

    def e_hnb_top(self,startname,startdescription) -> discord.Embed:
        Embeds = discord.Embed(title="ヒット&ブロー",color=0xffffff,)
        Embeds.add_field(name=startname, value=startdescription)
        Embeds.add_field(name=(f'・戦績'), value=(f'戦績を表示します。'))

        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds

    def e_hnb_join(self,player:discord.Member = None) -> discord.Embed:
        if player is None:
            player = "参加者募集中"
        else:
            player = player.mention

        Embeds = discord.Embed(colour=self.author.colour,)
        Embeds.set_author(icon_url=self.author_image,name=f"{self.author_name}のロビー")
        Embeds.add_field(name=(f' 参加者1'), value=(f' {self.author.mention}'),inline=False)
        Embeds.add_field(name=(f' 参加者2'), value=(f' {player}'),inline=False)
        
        return Embeds

class game_menu(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot

    @commands.command()
    async def game(self,ctx,isOnly=None):
        author = ctx.author
        e_page =[]
        v_page =[]
        await self.game_top(channel=ctx,author=author,isOnly=isOnly,e_page=e_page,v_page=v_page)

    async def game_top(self,channel:discord.Thread,author:discord.Member,*,isOnly = None,e_page:list = [],v_page:list = []):
        evs = embedbox_game(author,isOnly)
        Embeds = evs.e_game_top()
        e_page.append(Embeds)
        Views = gamemenuview(isOnly=isOnly,author=author,e_page=e_page,v_page=v_page)
        await channel.send(embed=Embeds,view=Views)

class gamemenuview(discord.ui.View):
    def __init__(self, *, timeout = None,author :discord.Member = None,isOnly = None,e_page:list = [],v_page:list = []):
        super().__init__(timeout=timeout)
        self.e_page = e_page
        self.v_page = v_page
        self.isOnly = isOnly
        self.author = author

        self.v_page.append(self)
        
        if(len(self.e_page) > 1):
            self.add_item(prevbutton(self.e_page,self.v_page))

        self.add_item(gotohnbbutton(self.author,self.e_page,self.v_page,isOnly=self.isOnly))
    
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

class gotohnbbutton(discord.ui.Button):
    def __init__(self,author :discord.Member = None,e_page:list = [],v_page:list = [],labelname:str='!hnb',isOnly = None,):
        super().__init__(label=labelname,style=discord.ButtonStyle.blurple)
        self.e_page = e_page
        self.v_page = v_page
        self.isOnly = isOnly
        self.author = author

    async def callback(self, interaction: discord.Interaction):
        evs = embedbox_game(author=interaction.user,isOnly=self.isOnly)
        if interaction.guild:
            Embeds = evs.e_hnb_top("ルーム作成","ルームを作成し対戦相手を募集します。")
            Views = hitnblow_top(author=self.author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page)
            self.e_page.append(Embeds)
            return await interaction.response.edit_message(embed=Embeds,view=Views)
        else:
            Embeds = evs.e_hnb_top("マッチング開始","マッチングを開始し対戦相手を待ちます。")
            Views = hitnblow_top(author=self.author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page)
            self.e_page.append(Embeds)
            return await interaction.response.edit_message(embed=Embeds,view=Views)

class hitnblow_top(discord.ui.View):
    def __init__(self, *, timeout = None,author :discord.Member = None,isOnly = None,e_page:list = [],v_page:list = [],isdm:bool =False):
        super().__init__(timeout=timeout)
        self.e_page = e_page
        self.v_page = v_page
        self.isOnly = isOnly
        self.author = author
        self.isdm = isdm

        self.v_page.append(self)
        
        if(len(self.e_page) > 1):
            self.add_item(prevbutton(self.e_page,self.v_page))
        if self.isdm == True:
            self.add_item(hnbplaybutton(author=self.author,e_page=self.e_page,v_page=self.v_page,labelname="マッチング開始",isdm = True,isOnly=self.isOnly))
        else:
            self.add_item(hnbplaybutton(author=self.author,e_page=self.e_page,v_page=self.v_page,isOnly=self.isOnly))
        self.add_item(hnbstatsbutton(self.e_page,self.v_page))
    
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

class hnbplaybutton(discord.ui.Button):
    def __init__(self,author :discord.Member = None,e_page:list = [],v_page:list = [],labelname:str='ルーム作成',isdm:bool =False,isOnly = None):
        super().__init__(label=labelname,style=discord.ButtonStyle.blurple)
        self.e_page = e_page
        self.v_page = v_page
        self.isdm = isdm
        self.isOnly = isOnly
        self.author = author

    async def callback(self, interaction: discord.Interaction):
        if self.isdm:
            pass #ｄｍ内の処理
        else:
            evs = embedbox_game(interaction.user,isOnly=self.isOnly)
            Embeds = evs.e_hnb_join()
            self.e_page.append(Embeds)
            Views = hnb_joinview(author=self.author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page)
            await interaction.response.edit_message(embed=Embeds,view=Views)

class hnb_joinview(discord.ui.View):
    def __init__(self, *, timeout = None,author :discord.Member = None,isOnly = None,e_page:list = [],v_page:list = [],isdm:bool =False):
        super().__init__(timeout=timeout)
        self.e_page = e_page
        self.v_page = v_page
        self.isOnly = isOnly
        self.author = author
        self.isdm = isdm

        self.v_page.append(self)

        if(len(self.e_page) > 1):
            self.add_item(prevbutton(self.e_page,self.v_page))

        self.add_item(hnbjoinbutton(self.e_page,v_page=self.v_page,author=self.author))

class hnbjoinbutton(discord.ui.Button):
    def __init__(self,e_page:list = [],v_page:list = [],custom_id="hnbjoinbutton",author:discord.Member =None):
        super().__init__(label="参加",style=discord.ButtonStyle.blurple,custom_id=custom_id)
        self.e_page = e_page
        self.v_page = v_page
        self.author = author

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            await interaction.response.send_message(content=(f"すでに参加済みです。"),ephemeral=True)
            return
        else:
            pass

class hnbstatsbutton(discord.ui.Button):
    def __init__(self,e_page:list = [],v_page:list = []):
        super().__init__(label="戦績",style=discord.ButtonStyle.blurple)
        self.e_page = e_page
        self.v_page = v_page

    async def callback(self, interaction: discord.Interaction):
        pass

class hnb_number(ui.Modal, title='Hit&Blow - 数字決め'):
    def __init__(self,isOnly,e_page:list = [],v_page:list = []) -> None:
        super().__init__()
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page
        

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        try:
            self.author_id = self.author.id
        except AttributeError:
            self.author_id = None
        if self.author_id == None or self.author_id == interaction.user.id:
            return True
        else:
            await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),ephemeral=True)
            return False
        
    value_year = ui.TextInput(label="年",style=discord.TextStyle.short, custom_id="year",placeholder=f"年を入力。デフォルト(年)", required=False)
    value_month = ui.TextInput(label="月",style=discord.TextStyle.short, custom_id="month",placeholder=f"月を入力。デフ月)", required=False)
    value_day = ui.TextInput(label="日",style=discord.TextStyle.short, custom_id="day",placeholder=f"日を日)", required=False)
    value_hour = ui.TextInput(label="時間",style=discord.TextStyle.short, custom_id="hour",placeholder=f"時間時)", required=False)
    value_timezone = ui.TextInput(label="タイムゾーン",style=discord.TextStyle.short, custom_id=f"timezone",placeholder="タイムゾーンを入力。デフォルト(JST)", required=False)

    async def on_submit(self, interaction: discord.Interaction,):
        pass
    


async def setup(bot):
    await bot.add_cog(game_menu(bot))
    print(f"game読み込み")