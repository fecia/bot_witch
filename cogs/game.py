import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands

import os
import random

from cogs.role import prevbutton

class embedbox_game():
    def __init__(self,author:discord.Member,isOnly) -> None:
        self.author =author
        self.isOnly =isOnly
    
    def e_game_top(self) -> discord.Embed:
        Embeds = discord.Embed(title="ゲームメニュー",color=0xffffff,description="ここではゲームに関する操作ができます。")
        Embeds.add_field(name=(f"・!hnb (ヒット&ブロー)"), value=(f"ヒット&ブロー"))
        Embeds.add_field(name=(f'・なし'), value=(f'なしなしなしなしなし'))
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author.display_name}のみ操作可能"),icon_url=self.author.display_avatar.url)
        else:
            Embeds.set_footer(text=(f"{self.author.display_name}が作成"),icon_url=self.author.display_avatar.url)
        return Embeds

    def e_hnb_top(self,startname,startdescription) -> discord.Embed:
        Embeds = discord.Embed(title="ヒット&ブロー",color=0xffffff,)
        Embeds.add_field(name=startname, value=startdescription)
        Embeds.add_field(name=(f'・戦績'), value=(f'戦績を表示します。'))

        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author.display_name}のみ操作可能"),icon_url=self.author.display_avatar.url)
        else:
            Embeds.set_footer(text=(f"{self.author.display_name}が作成"),icon_url=self.author.display_avatar.url)
        return Embeds

    def e_hnb_join(self,player:discord.Member = None) -> discord.Embed:
        if player is None:
            player = "参加者募集中"
        else:
            player = player.mention

        Embeds = discord.Embed(colour=self.author.colour,)
        Embeds.set_author(icon_url=self.author.display_avatar.url,name=f"{self.author.display_name}のロビー")
        Embeds.add_field(name=(f' 参加者1'), value=(f' {self.author.mention}'),inline=False)
        Embeds.add_field(name=(f' 参加者2'), value=(f' {player}'),inline=False)
        
        return Embeds
    def error(self) -> discord.Embed:
        Embeds = discord.Embed(colour=discord.Colour.red())
        Embeds.add_field(name="エラー",value="もう一度部屋を作り直してください。")
        return Embeds

class embedbox_hnb():
    def __init__(self,author:discord.Member,p1:discord.Member = None,p2:discord.Member = None) -> None:
        self.author =author
        self.p1 = p1
        self.p2 = p2

    def e_hnb_battle(self,todo = "引数指定されてない") -> discord.Embed:
        Embeds = discord.Embed(colour=self.author.colour,)
        Embeds.add_field(name=(f'・先攻'), value=(f' {self.p1.mention}'),inline=True)
        Embeds.add_field(name=(f'・後攻'), value=(f' {self.p2.mention}'),inline=True)

        Embeds.add_field(name="--------------------",value=todo,inline=False)
        Embeds.set_footer(text=(f"{self.author.display_name}のロビー"),icon_url=self.author.display_avatar.url)
        return Embeds

    def e_turn(self,p1sturn=True,gamedate:list = None) -> discord.Embed:
        Embeds = discord.Embed(colour=self.author.colour,)
        Embeds.add_field(name=(f'・先攻'), value=(f' {self.p1.mention}'),inline=True)
        Embeds.add_field(name=(f'・後攻'), value=(f' {self.p2.mention}'),inline=True)
        if p1sturn:
            Embeds.add_field(name=f"{self.p1.display_name}のターン。",value="数字を決めてください。",inline=False)
        else:
            Embeds.add_field(name=f"{self.p2.display_name}のターン。",value="数字を決めてください。",inline=False)
        Embeds.set_footer(text=(f"{self.author.display_name}のロビー"),icon_url=self.author.display_avatar.url)
        Embeds.set_footer(text=(f"ゲームID:{gamedate[0]}"),icon_url=gamedate[5][0].display_avatar.url)
        return Embeds

    def e_hnb_progress(self,p1sturn:bool,gamedate) -> discord.Embed:
        Embeds = discord.Embed(colour=self.author.colour,)
        Embeds.set_author(icon_url=self.author.display_avatar.url,name=f"{self.author.display_name}のロビー")
        Embeds.add_field(name=(f'・先攻'), value=(f' {self.p1.mention}'),inline=True)
        Embeds.add_field(name=(f'・後攻'), value=(f' {self.p2.mention}'),inline=True)
        Embeds.add_field(name='--------------------------------',value="ログ",inline=False)
        Embeds.add_field(name=(f'先攻'), value=(f' {gamedate[7][0]}'),inline=True)
        Embeds.add_field(name=(f'後攻'), value=(f' {gamedate[7][1]}'),inline=True)
        if p1sturn:
            Embeds.add_field(name=f"--------------------\n{self.p1.display_name}のターン。",value="数字を決めてください。",inline=False)
        else:
            Embeds.add_field(name=f"--------------------\n{self.p2.display_name}のターン。",value="数字を決めてください。",inline=False)
        Embeds.set_footer(text=(f"ゲームID:{gamedate[0]}"),icon_url=gamedate[5][0].display_avatar.url)
        return Embeds

    def e_hnb_drawbattle(self,gamedate,) -> discord.Embed:
        Embeds = discord.Embed(colour=self.author.colour,)
        Embeds.set_author(icon_url=self.author.display_avatar.url,name=f"{self.author.display_name}のロビー")
        Embeds.add_field(name=(f'・先攻'), value=(f' {self.p1.mention}'),inline=True)
        Embeds.add_field(name=(f'・後攻'), value=(f' {self.p2.mention}'),inline=True)
        Embeds.add_field(name='--------------------------------',value="ログ",inline=False)
        Embeds.add_field(name=(f'先攻'), value=(f' {gamedate[7][0]}'),inline=True)
        Embeds.add_field(name=(f'後攻'), value=(f' {gamedate[7][1]}'),inline=True)
        Embeds.add_field(name=f"--------------------\n**{self.p1.display_name}が的中させました。**",value=f"\n的中で**引き分け**。\n外すと先攻の**勝利**。",inline=False)
        Embeds.set_footer(text=(f"ゲームID:{gamedate[0]}"),icon_url=gamedate[5][0].display_avatar.url)
        return Embeds

    def e_hnb_winresult(self,gamedate,) -> discord.Embed:
        Embeds = discord.Embed(colour=self.author.colour,title=f"勝利:{gamedate[8][0].display_name}",description=f"敗北:{gamedate[8][1].display_name}")
        Embeds.add_field(name=(f'・先攻'), value=(f' {gamedate[1].mention}\n番号:{gamedate[2]}'),inline=True)
        Embeds.add_field(name=(f'・後攻'), value=(f' {gamedate[3].mention}\n番号:{gamedate[4]}'),inline=True)
        Embeds.add_field(name=(f'{gamedate[6]}ターン目で{gamedate[8][0].display_name}が的中。'), value=(f"--------------------"),inline=False)
        Embeds.add_field(name='--------------------------------',value="ログ",inline=False)
        Embeds.add_field(name=(f'先攻'), value=(f' {gamedate[7][0]}'),inline=True)
        Embeds.add_field(name=(f'後攻'), value=(f' {gamedate[7][1]}'),inline=True)
        Embeds.set_footer(text=(f"ゲームID:{gamedate[0]}"),icon_url=gamedate[5][0].display_avatar.url)
        return Embeds

    def e_hnb_drawresult(self,gamedate,) -> discord.Embed:
        Embeds = discord.Embed(color=gamedate[5][0].accent_color,title=f"引き分け")
        Embeds.add_field(name=(f'・先攻'), value=(f' {gamedate[1].mention}\n番号:{gamedate[2]}'),inline=True)
        Embeds.add_field(name=(f'・後攻'), value=(f' {gamedate[3].mention}\n番号:{gamedate[4]}'),inline=True)
        Embeds.add_field(name=(f'{gamedate[6]}ターン目で両者的中。'), value=(f"--------------------"),inline=False)
        Embeds.add_field(name='--------------------------------',value="ログ",inline=False)
        Embeds.add_field(name=(f'先攻'), value=(f' {gamedate[7][0]}'),inline=True)
        Embeds.add_field(name=(f'後攻'), value=(f' {gamedate[7][1]}'),inline=True)
        Embeds.set_footer(text=(f"ゲームID:{gamedate[0]}"),icon_url=gamedate[5][0].display_avatar.url)
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
        if self.isOnly == "1":
            if self.author != interaction.user:
                await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),ephemeral=True)
                return False
        return True

class gotohnbbutton(discord.ui.Button):
    def __init__(self,author :discord.Member = None,e_page:list = [],v_page:list = [],labelname:str='!hnb',isOnly = None,):
        super().__init__(label=labelname,style=discord.ButtonStyle.blurple)
        self.e_page = e_page
        self.v_page = v_page
        self.isOnly = isOnly
        self.author = author

    async def callback(self, interaction: discord.Interaction):
        evs = embedbox_game(author=self.author,isOnly=self.isOnly)
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
        if self.isOnly == "1":
            if self.author != interaction.user:
                await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),ephemeral=True)
                return False
        return True

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
    def __init__(self,label="開始",e_page:list = [],v_page:list = [],author:discord.Member =None,player:discord.Member = None):
        super().__init__(label=label,style=discord.ButtonStyle.blurple)
        self.e_page = e_page
        self.v_page = v_page
        self.author = author
        self.player = player
        self.gameid = self.custom_id

    async def callback(self, interaction: discord.Interaction):
        path = "./bot_witch/hitandblow/" + str(self.gameid) + ".txt"
        with open(path,"w"):
            pass
        playerlist =[self.author,self.player]
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
            Views = hnbbattleview(p1=p1,p2=p2,author=self.author,gameid = self.gameid,playerlist=playerlist)
            
            # if p1.dm_channel is None: await p1.create_dm()
            # if p2.dm_channel is None: await p2.create_dm()
            # p1_dm = p1.dm_channel
            # p2_dm = p2.dm_channel
            # p1msg = await p1_dm.send(embed=Embeds,view=Views)
            # p2msg = await p2_dm.send(embed=Embeds,view=Views)
            if self.label == "再戦":
                return await interaction.response.send_message(embed=Embeds,view=Views)
            await interaction.response.edit_message(embed=Embeds,view=Views)
            return
        else:
            await interaction.response.send_message("ホストのみが開始できます。",ephemeral=True)
            return

class hnb_numberforp1(ui.Modal, title='Hit&Blow - 数字決め'):
    def __init__(self,p1:discord.Member = None,p2:discord.Member = None,author:discord.Member = None,gameid = None,playerlist:list =None) -> None:
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.author = author
        self.p1num = None
        self.p2num = None
        self.gameid = gameid
        self.playerlist = playerlist

    inputnum = ui.TextInput(label="数字",style=discord.TextStyle.short,placeholder=f"数字を入力(無記入でランダムに決まります)", required=True,min_length=0)

    async def on_submit(self, interaction: discord.Interaction,):
        path = "./bot_witch/hitandblow/" + str(self.gameid) + ".txt"
        if not os.path.isfile(path=path):
            evs =embedbox_game(None,None)
            return await interaction.response.edit_message(embed=evs.error(),view=None)
        for y in range(0,10):
            if self.inputnum.value.count(str(y)) >=2:
                return await interaction.response.send_message(content="同じ文字が2回以上使われています。もう一度決め直してください。",ephemeral=True)
        with open(path,"r+") as file:
            allline = file.readlines()
            await interaction.user.create_dm()
            if self.inputnum.value == "r":
                numlist = ["0","1","2","3","4","5","6","7","8","9"]
                defaultnum = ''.join(random.sample(numlist,3))
                allline.insert(0,defaultnum)
                await interaction.user.dm_channel.send(content=f"あなたの番号は{defaultnum}に決まりました。")
            else:
                allline.insert(0,self.inputnum.value)
                await interaction.user.create_dm()
                await interaction.user.dm_channel.send(content=f"{self.inputnum.value}で受け付けました。")

            p1_num = allline[0]
            print(allline)
            if len(allline) == 2:
                p2_num = allline[1]
                file.truncate(0)
                file.write(allline[0]+"\n"+allline[1])
                evs = embedbox_hnb(author=self.author,p1=self.p1,p2=self.p2)
                # await self.p1.dm_channel.send(embed=Embeds)
                # await self.p2.dm_channel.send(embed=Embeds)
                turncount:int = 1
                p1log:str ="考え中"
                p2log:str =""
                log = [p1log,p2log]
                gamedate=[self.gameid,self.p1,p1_num,self.p2,p2_num,self.playerlist,turncount,log]
                Embeds = evs.e_turn(p1sturn=True,gamedate=gamedate)
                Views = yournumberview(gamedate,isp1turn=True)
                await interaction.response.edit_message(embed=Embeds,view=Views)
            else:
                file.write(allline[0])
                x = discord.Colour.gold() if random.uniform(0,100) <= 1 else discord.Colour.blue()
                Embeds = discord.Embed(colour=x)
                Embeds.add_field(name="受付完了",value="相手の入力が終わるまでお待ち下さい。")
                Embeds.set_footer(text="このメッセージは5秒後に自動的に削除されます。")
                await interaction.response.send_message(embed=Embeds,ephemeral=True,delete_after=5)
            return

class hnb_numberforp2(ui.Modal, title='Hit&Blow - 数字決め'):
    def __init__(self,p1:discord.Member = None,p2:discord.Member = None,author:discord.Member = None,gameid = None,playerlist:list =None) -> None:
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.author = author
        self.gameid = gameid
        self.playerlist = playerlist

    inputnum = ui.TextInput(label="数字(例)",style=discord.TextStyle.short,placeholder=f"数字(0~9)を重複無しで入力(無記入でランダムに決まります)", required=True,min_length=0)

    async def on_submit(self, interaction: discord.Interaction,):
        path = "./bot_witch/hitandblow/" + str(self.gameid) + ".txt"
        if not os.path.isfile(path=path):
            evs =embedbox_game(None,None)
            return await interaction.response.edit_message(embed=evs.error(),view=None)
        for y in range(0,10):
            if self.inputnum.value.count(str(y)) >=2:
                return await interaction.response.send_message(content="同じ文字が2回以上使われています。もう一度決め直してください。",ephemeral=True)
        with open(path,"r+") as file:
            allline = file.readlines()
            await interaction.user.create_dm()
            if self.inputnum.value == "r":
                numlist = ["0","1","2","3","4","5","6","7","8","9"]
                defaultnum = ''.join(random.sample(numlist,3))
                allline.append(defaultnum)
                await interaction.user.dm_channel.send(content=f"あなたの番号は{defaultnum}に決まりました。")
            else:
                allline.append(self.inputnum.value)
                await interaction.user.dm_channel.send(content=f"{self.inputnum.value}で受け付けました。")

            p1_num = allline[0]
            print(allline)
            if len(allline) == 2:
                p2_num = allline[1]
                file.write("\n"+allline[1])
                evs = embedbox_hnb(author=self.author,p1=self.p1,p2=self.p2)
                # await self.p1.dm_channel.send(embed=Embeds)
                turncount:int = 1
                p1log:str ="考え中"
                p2log:str =""
                log = [p1log,p2log]
                gamedate=[self.gameid,self.p1,p1_num,self.p2,p2_num,self.playerlist,turncount,log]
                Embeds = evs.e_turn(p1sturn=True,gamedate=gamedate)
                Views = yournumberview(gamedate,isp1turn=True)
                await interaction.response.edit_message(embed=Embeds,view=Views)
            else:
                file.write(allline[0])
                x = discord.Colour.gold() if random.uniform(0,100) <= 1 else discord.Colour.blue()
                Embeds = discord.Embed(colour=x)
                Embeds.add_field(name="受付完了",value="相手の入力が終わるまでお待ち下さい。")
                Embeds.set_footer(text="このメッセージは5秒後に自動的に削除されます。")
                await interaction.response.send_message(embed=Embeds,ephemeral=True,delete_after=5)
            return

class hnbbattleview(discord.ui.View):
    def __init__(self,timeout = None,p1:discord.Member = None,p2:discord.Member = None,author:discord.Member = None,gameid =None,playerlist:list =None) -> None:
        super().__init__(timeout=timeout)
        self.p1 = p1
        self.p2 = p2
        self.gamenumber:int
        self.author = author

        self.add_item(mynumberbutton(p1=self.p1,p2=self.p2,author=self.author,gameid=gameid,playerlist=playerlist))

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        user = interaction.user
        if user == self.p1 or user == self.p2:
            return True
        await interaction.response.send_message("参加者のみ可能。",ephemeral=True)
        return False

class mynumberbutton(discord.ui.Button):
    def __init__(self,p1:discord.Member = None,p2:discord.Member = None,author:discord.Member = None,gameid =None,playerlist:list =None):
        super().__init__(label="自分の数字を決める",style=discord.ButtonStyle.blurple,)
        self.p1 = p1
        self.p2 = p2
        self.author = author
        self.gameid = gameid
        self.playerlist = playerlist

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.p1.id: #先攻プレイヤ
            await interaction.response.send_modal(hnb_numberforp1(p1=self.p1,p2=self.p2,author=self.author,gameid = self.gameid,playerlist=self.playerlist))
        else: #後攻プレイヤ
            await interaction.response.send_modal(hnb_numberforp2(p1=self.p1,p2=self.p2,author=self.author,gameid = self.gameid,playerlist=self.playerlist))

class yournumberview(discord.ui.View):
    def __init__(self,gamedate:list,isp1turn:bool = True,isreach:bool = False):
        super().__init__(timeout=None)
        # gamedate = [gameid,p1,p1_num,p2,p2_num,author,turncount,log] #ゲームid,先攻、先攻番号、後攻、後攻番号、ロビー設立者,ターン数=先１:後１：先２：後２と続いていく
        
        self.add_item(yournumberbutton(gamedate=gamedate,isp1turn=isp1turn,isreach=isreach))

class yournumberbutton(discord.ui.Button):
    def __init__(self,gamedate:list,isp1turn:bool = True,isreach:bool = False):
        super().__init__(label="数字決定",style=discord.ButtonStyle.blurple,)
        self.gamedate = gamedate
        self.isp1turn = isp1turn
        self.isreach = isreach

    async def callback(self, interaction: discord.Interaction):
        if interaction.user == self.gamedate[1] or interaction.user == self.gamedate[3]: #inで見ないほうがいいのかわからん ~~.user in self.~~
            if self.isp1turn and interaction.user == self.gamedate[1] or not self.isp1turn and interaction.user == self.gamedate[3]:
                return await interaction.response.send_modal(yournumbermodal(gamedate=self.gamedate,isp1turn=self.isp1turn,isreach=self.isreach))
            else:
                await interaction.response.send_message("相手のターンです。",ephemeral=True)
        else:
            await interaction.response.send_message("参加者のみ可能です。",ephemeral=True)
        return

class yournumbermodal(ui.Modal, title='Hit&Blow - 数字あて'):
    def __init__(self,gamedate:list,isp1turn:bool,isreach:bool = False) -> None:
        super().__init__()
        self.gamedate = gamedate
        self.isp1turn = isp1turn
        self.isreach = isreach

    inputnum = ui.TextInput(label="数字",style=discord.TextStyle.short,placeholder=f"数字を入力してください", required=True)

    async def on_submit(self, interaction: discord.Interaction,):
        number = self.inputnum.value
        gm = gmhitandblow(gamedate=self.gamedate,isp1turn=self.isp1turn)
        evs = embedbox_hnb(author=self.gamedate[5][0],p1=self.gamedate[1],p2=self.gamedate[3])
        self.isp1turn = False if self.isp1turn else True #p1turn　ヒックリかえし
        hit,blow = gm.hitblow(number)
        if self.isreach:#引き分け勝負判定
            gtl = gametypelist(gamedate=self.gamedate)
            onemorebutton = gtl.gamelist(gametype="hnb",rematchtype=0)
            Views = onemorebattleview(gamedate=self.gamedate,button=onemorebutton)
            if gm.iscorrect(number):#引き分け
                self.gamedate[7][1] += f"**{number} -- {hit}H0B**\n"
                result =[self.gamedate[1],self.gamedate[3]]
                self.gamedate.append(result)
                Embeds = evs.e_hnb_drawresult(gamedate=self.gamedate)
                return await interaction.response.edit_message(embed=Embeds,view=Views)
            else:#p1のみ勝ち
                self.gamedate[7][1] = self.gamedate[7][1].replace("考え中",f"{number} \t-- {hit}H{blow}B\n")
                result =[self.gamedate[1],self.gamedate[3]]
                self.gamedate.append(result)
                Embeds = evs.e_hnb_winresult(gamedate=self.gamedate)
                return await interaction.response.edit_message(embed=Embeds,view=Views)
        if gm.iscorrect(number):#正解処理 p1なら引き分け勝負に入る
            if self.isp1turn: #上でisp1turn 入れ替えてて逆やから注意 True =p2が答えた処理,False = p1が答えたときの処理
                self.gamedate[7][1] = self.gamedate[7][1].replace("考え中",f"**{number} \t-- {hit}H0B**\n")
                #p2のみ勝ち
                gtl = gametypelist(gamedate=self.gamedate)
                onemorebutton = gtl.gamelist(gametype="hnb",rematchtype=0)
                Views = onemorebattleview(gamedate=self.gamedate,button=onemorebutton)
                result =[self.gamedate[3],self.gamedate[1]]
                self.gamedate.append(result)
                Embeds = evs.e_hnb_winresult(gamedate=self.gamedate)
                return await interaction.response.edit_message(embed=Embeds,view=Views)
            else:
                self.gamedate[7][0] = self.gamedate[7][0].replace("考え中",f"{number} \t-- {hit}H0B\n")
                self.gamedate[7][1] += f"考え中"
                Embeds = evs.e_hnb_drawbattle(gamedate=self.gamedate)
                Views = yournumberview(gamedate=self.gamedate,isp1turn=self.isp1turn,isreach=True)
                await interaction.response.edit_message(embed=Embeds,view=Views)

        else:
            self.gamedate[6] += 1 if self.isp1turn else 0
            if self.isp1turn: #上でisp1turn 入れ替えてて逆やから注意 True =p2が答えた処理,False = p1が答えたときの処理
                self.gamedate[7][1] = self.gamedate[7][1].replace("考え中",f"{number} \t-- {hit}H{blow}B\n")
                self.gamedate[7][0] += f"考え中"
            else:
                self.gamedate[7][0] = self.gamedate[7][0].replace("考え中",f"{number} \t-- {hit}H{blow}B\n")
                self.gamedate[7][1] += f"考え中"
            Embeds = evs.e_hnb_progress(p1sturn=self.isp1turn,gamedate=self.gamedate)
            Views = yournumberview(gamedate=self.gamedate,isp1turn=self.isp1turn)
            await interaction.response.edit_message(embed=Embeds,view=Views)

class onemorebattleview(discord.ui.View):
    def __init__(self,gamedate,button):#勝敗画面の方でgmlist = gametypelist(self.gamedate)つかって
                                            #embedとボタン見つけてこいそれでviewにはbuttonつっこんでeditmessageしろ
        super().__init__(timeout=None)
        self.gamedate = gamedate
        self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if interaction.user == self.gamedate[5][0]:
            return True
        else:
            await interaction.response.send_message("ホストのみ可能です。",ephemeral=True)

# class onemorebattlebutton(discord.ui.Button):
#     def __init__(self,gamedate:list,gametype):
#         super().__init__(label="再戦",style=discord.ButtonStyle.blurple)
#         self.gamedate = gamedate
#         self.gametype = gametype

    
#     async def callback(self, interaction: discord.Interaction):

#         Embeds,

class gametypelist():
    def __init__(self,gamedate) -> None:
        self.gamedate = gamedate
        self.evs = embedbox_game(author=gamedate[5][0],isOnly=None)
        self.evshnb = embedbox_hnb(author=gamedate[5][0],p1=gamedate[1],p2=gamedate[3])
    def gamelist(self,gametype,rematchtype = 0):
        if gametype == "hnb":
            if rematchtype:
                pass
            else:
                button = hnbstartbutton(label="再戦",e_page=None,v_page=None,author=self.gamedate[5][0],player=self.gamedate[5][1])
        
        ombutton = button
        return ombutton

class gmhitandblow():
    def __init__(self,gamedate:list,isp1turn:bool):
        self.gamedate = gamedate #gameid,p1,p1num,p2,p2num,author
        self.isp1turn = isp1turn

    def iscorrect(self,num):
        if self.isp1turn:
            if num == self.gamedate[4]:
                return True
        else:
            if num == self.gamedate[2]:
                return True
        return False

    def hitblow(self,num):
        truenum :str = self.gamedate[4] if self.isp1turn else self.gamedate[2] 
        hit :int = 0
        blow:int = 0
        for x in range(0,len(truenum)):
            if truenum[x] == num[x]:
                hit += 1
                continue
            if num[x] in truenum:
                blow +=1
                continue
        return hit,blow

        # truenum = self.gamedate[4] if self.isp1turn else self.gamedate[2] #ルール勘違いしてて作ったやつ桁数多いやつとかに使えそうやから残しておく（隣り合ってないとblowにならない)
        # hit :int = 0
        # blow:int = 0
        # for x in range(0,len(truenum)):
        #     if truenum[x] == num[x]:
        #         hit += 1
        #         continue
        #     if not x == (0 or len(truenum) - 1):
        #         if truenum[x-1] == num[x] or truenum[x+1] == num[x]:
        #             blow+=1  #あんまりきれいじゃないとおもう
        #     elif x == 0:
        #         if truenum[x+1] == num[x]:
        #             blow +=1
        #     else:
        #         if truenum[x-1] == num[x]:
        #             blow +=1
        #     continue
        # return hit,blow

async def setup(bot):
    await bot.add_cog(game_menu(bot))
    print(f"game読み込み")