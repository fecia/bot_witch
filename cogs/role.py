import string
import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands
from discord.utils import get
import json

# -----------------------------------------------------------
class judgeisOnly():
    def __init__(self,author:discord.Member,isOnly,e_page:list,v_page:list) -> None:
        self.isOnly=isOnly
        self.author=author
        self.author_name = author.display_name
        self.author_image = author.display_avatar.url
        self.e_page = e_page
        self.v_page = v_page

    def e_isOnly(self,Embeds:discord.Embed):
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds

    def v_isOnly(self,button:discord.ui.View):
        if(self.isOnly == "1"):
            Views = button(author=self.author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page)
        else:
            Views = button(isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page)
        return Views

class embedbox():
    def __init__(self,author:discord.Member,isOnly) -> None:
        self.author =author
        self.isOnly =isOnly
        self.author_name = author.display_name
        self.author_image = author.display_avatar.url

    def e_role_top(self) -> discord.Embed:

        Embeds = discord.Embed(title="ロールメニュー",
                            color=0xffffff,
                            description="ここではロールに関する操作ができます。")
        Embeds.add_field(name=(f"・一覧"), value=(f"ロールの一覧を表示し付与することもできます"))
        Embeds.add_field(name=(f'・追加'), value=(f'フォーム形式でロールを作成できます'))
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds

    def e_attachrole(self,_name:string,_color) ->discord.Embed:
        Embeds = discord.Embed(color=_color)
        Embeds.add_field(name=(f'{_name}を作成しました'), value=(f'作成したロールをつけますか？'))
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds


    # ---------------------------------------------------------
    def doTree(self,channel:discord.Thread,isTree:bool = False):
        if(isTree):
            pass

# いったん凍結　（TypeError: 'RoleMenuButtons' object is not callable）発生
class unlockbutton(discord.ui.Button):
    def __init__(self,e_page:list,v_page:list):
        super().__init__(label='限定モード解除',style=discord.ButtonStyle.red)
        self.e_page = e_page
        self.v_page = v_page

    async def callback(self, interaction: discord.Interaction):
        # await interaction.response.send_message(f'終了します', ephemeral=True)
        # ここにページを見てisonly noneで返すの作る
        judge = judgeisOnly(author=interaction.user,isOnly = None,e_page=self.e_page[-1],v_page=self.v_page)
        self.e_page.append(judge.e_isOnly(self.e_page[-1]))
        # self.v_page.append(judge.v_isOnly(self.v_page[-1]))
        view = judge.v_isOnly(self.v_page[-1])
        self.v_page.append(view)
        await interaction.response.edit_message(embed=self.e_page[-1],view=self.v_page[-1])


class prevbutton(discord.ui.Button):
    def __init__(self,e_page,v_page):
        super().__init__(style=discord.ButtonStyle.gray,label="戻る")
        self.e_page = e_page
        self.v_page = v_page

    async def callback(self, interaction: discord.Interaction):
        del self.e_page[-1]
        del self.v_page[-1]
        await interaction.response.edit_message(embed=self.e_page[-1],view=self.v_page[-1])

class mypage():
    def __init__(self,v_page,e_page) -> None:
        self.e_page = e_page
        self.v_page = v_page

    def prevpage(self):
        del self.e_page[-1]
        del self.v_page[-1]

    def unlockonly(self):
        pass

    # ---------------------------------------------------------
class role_menu(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def role(self,ctx,isOnly=None):
        author = ctx.author
        e_page =[]
        v_page =[]
        await self.role_top(channel=ctx,author=author,isOnly=isOnly,e_page=e_page,v_page=v_page)


    async def role_top(self,channel:discord.Thread,author:discord.Member,*,isOnly = None,isTree:bool = False,e_page:list,v_page:list):
        evs = embedbox(author,isOnly)
        Embeds = evs.e_role_top()
        e_page.append(Embeds)
        judge = judgeisOnly(author,isOnly,e_page=e_page,v_page=v_page)
        Views = judge.v_isOnly(RoleMenuButtons)
        
        await channel.send(embed=Embeds,view=Views)

class RoleMenuButtons(discord.ui.View):
    def __init__(self, *, timeout = None,author:int = None,isOnly,e_page:list,v_page:list):
        super().__init__(timeout=timeout)
        self.author= author
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page

        # if(isOnly == "1"):
        #     self.add_item(unlockbutton(self.e_page,self.v_page))

        v_page.append(self)
        if(len(self.e_page) != 0):
            self.add_item(prevbutton(self.e_page,self.v_page))

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
# 第一ボタン
    @discord.ui.button(
    label=(f'一覧'),
    style=discord.ButtonStyle.primary,)

    async def list(self, interaction: discord.Interaction,button: discord.ui.Button):
        pass
# 第二ボタン
    @discord.ui.button(
    label=(f'作成'),
    style=discord.ButtonStyle.primary,)
    
    async def make(self, interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_modal(Role_question(isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page))

class Role_question(ui.Modal, title='ロール作成フォーム'):
    def __init__(self,isOnly,e_page:list,v_page:list) -> None:
        super().__init__()
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page

    value_name = ui.TextInput(label=(f'名前'),
                            custom_id="name",
                            placeholder=(f"名前を入力してください。"),
                            required=True)
    value_color = ui.TextInput(label=(f'色'),
                            custom_id="color",
                            placeholder=(f"色を#をつけ入力してください(16進数)例:#a1b3f0"),
                            required=True,
                            max_length=7,
                            min_length=7)

    async def on_submit(self, interaction: discord.Interaction,):
        guild = interaction.guild
        author = interaction.user
        R_name = self.value_name.value
        R_color = self.value_color.value
        R_color = int(R_color.replace("#", "0x"), base=16)
        
        evs = embedbox(author,self.isOnly)

        newrole = await guild.create_role(name=R_name,colour=R_color,hoist=0,mentionable=1)
        path = "./bot_witch/guilds/" + str(guild.id) + ".json"
        with open(path,"r") as file:
            rolelist = json.load(file)
            rolelist["role"].append(newrole.id)
        with open(path,"w") as file:
            json.dump(rolelist,file,indent=4)

        Embeds = evs.e_attachrole(_name=R_name,_color=R_color)
        self.e_page.append(Embeds)
        
        judge = judgeisOnly(author,self.isOnly,e_page=self.e_page,v_page=self.v_page)
        # Embeds = judge.e_isOnly(Embeds)
        views = judge.v_isOnly(RoleAttach)
        await interaction.response.edit_message(embed=Embeds,view=views) 

class RoleAttach(discord.ui.View):
    def __init__(self, *, timeout = None,author:discord.Member = None,isOnly,e_page:list,v_page:list):
        super().__init__(timeout=timeout)
        self.author= author
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page
        # if(isOnly == "1"):
        #     self.add_item(unlockbutton(self.e_page,self.v_page))

        v_page.append(self)
        if(len(self.e_page) != 0):
            self.add_item(prevbutton(self.e_page,self.v_page))

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
        label='はい',
        style=discord.ButtonStyle.green,
    )
    async def yes(self, interaction: discord.Interaction,button: discord.ui.Button):
        guild = interaction.guild
        name = str(guild.roles[1])
        role = get(guild.roles, name=str(guild.roles[1]))
        await interaction.response.send_message(f'{name}をつけました。',ephemeral=True)
        await interaction.user.add_roles(role)

    @discord.ui.button(label='いいえ', style=discord.ButtonStyle.grey)
    async def no(self, interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_message(f'終了します', ephemeral=True)

async def setup(bot):
    print(f"role読み込み")
    await bot.add_cog(role_menu(bot))