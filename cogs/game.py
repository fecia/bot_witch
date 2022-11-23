import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands

import random

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

class embedbox_hnb():
    def __init__(self,author:discord.Member,p1:discord.Member = None,p2:discord.Member = None) -> None:
        self.author =author
        self.author_name = author.display_name
        self.author_image = author.display_avatar.url
        self.p1 = p1
        self.p2 = p2
        self.p1num:str = "***"
        self.p2num:str = "***"

    def e_hnb_battle(self,todo = "引数指定されてない") -> discord.Embed:
        Embeds = discord.Embed(colour=self.author.colour,)
        Embeds.add_field(name=(f'・先攻'), value=(f' {self.p1.mention}'),inline=False)
        Embeds.add_field(name=(f'・後攻'), value=(f' {self.p2.mention}'),inline=False)

        Embeds.add_field(name="しないといけないこと。",value=todo)
        Embeds.set_footer(text=(f"{self.author_name}のロビー"),icon_url=self.author_image)

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
    def __init__(self, *, timeout = None,author :discord.Member = None,isOnly = None,e_page:list = [],v_page:list = [],isdm:bool =False,player:discord.Member = None):
        super().__init__(timeout=timeout)
        self.e_page = e_page
        self.v_page = v_page
        self.isOnly = isOnly
        self.author = author
        self.player = player
        self.isdm = isdm
        if self.player is None:
            self.v_page.append(self)

        if(len(self.e_page) > 1):
            self.add_item(prevbutton(self.e_page,self.v_page))
        if self.player is None:
            self.add_item(hnbjoinbutton(e_page=self.e_page,v_page=self.v_page,author=self.author))
        else:
            self.add_item(hnbstartbutton(e_page=self.e_page,v_page=self.v_page,author=self.author,player=self.player))

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
            evs = embedbox_game(author=self.author,isOnly=None,)
            Embeds = evs.e_hnb_join(interaction.user)
            Views = hnb_joinview(e_page=self.e_page,v_page=self.v_page,author=self.author,player=interaction.user) #ここのviewはv_pageに入れないように
            await interaction.response.edit_message(embed = Embeds,view=Views)

class hnbstatsbutton(discord.ui.Button):
    def __init__(self,e_page:list = [],v_page:list = []):
        super().__init__(label="戦績",style=discord.ButtonStyle.blurple)
        self.e_page = e_page
        self.v_page = v_page

    async def callback(self, interaction: discord.Interaction):
        pass

class hnbstartbutton(discord.ui.Button):
    def __init__(self,e_page:list = [],v_page:list = [],custom_id="hnbstartbutton",author:discord.Member =None,player:discord.Member = None):
        super().__init__(label="開始",style=discord.ButtonStyle.blurple,custom_id=custom_id)
        self.e_page = e_page
        self.v_page = v_page
        self.author = author
        self.player = player

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            x = 1 if random.random() >= 0.5 else 0
            if x:
                p1 = self.author
                p2 = self.player
            else:
                p1 = self.player
                p2 = self.author
            evs = embedbox_hnb(author=self.author,p1=p1,p2=p2)
            Embeds = evs.e_hnb_battle(todo="数字を決めてください。")
            Views = hnbbattleview()
            await interaction.response.send_modal(hnb_number())
            return await interaction.response.edit_message(embed=Embeds,view=Views)
        else:
            await interaction.response.send_message("ホストのみが開始できます。",ephemeral=True)
            return

class hnb_number(ui.Modal, title='Hit&Blow - 数字決め'):
    def __init__(self,p1:discord.Member = None,p2:discord.Member = None,p1num:int =None,p2num:int = None) -> None:
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.p1num:int = p1num
        self.p2num:int = p2num
        self.gamenumber:int

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user.id == self.p1.id or interaction.user.id == self.p2.id:
            return True
        else:
            await interaction.response.send_message(content=(f"参加者のみ可能"),ephemeral=True)
            return False

    value_num = ui.TextInput(label="数字",style=discord.TextStyle.short, custom_id=f"num",placeholder=f"数字を入力(無記入でランダムに決まります)", required=True,min_length=0,max_length=3)

    async def on_submit(self, interaction: discord.Interaction,):
        num = self.value_num.value
        if num == None:
            num = ''.join([random.choice('0123456789') for j in range(3)])
            if interaction.id == self.p1.id:
                self.p1num = num
            else:
                self.p2num = num
    


async def setup(bot):
    await bot.add_cog(game_menu(bot))
    print(f"game読み込み")