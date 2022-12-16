import json

import discord
from discord import Embed, Role, SelectOption, User, ui
from discord.ext import commands
from discord.ui import RoleSelect
from discord.utils import get


# -----------------------------------------------------------
class judgeisOnly():#いらんくね
    def __init__(self,author:discord.Member,isOnly,e_page:list = [],v_page:list = []) -> None:
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
            Views = button(author=self.author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page)
        return Views

class embedbox():
    def __init__(self,author:discord.Member,isOnly) -> None:
        self.author =author
        self.isOnly =isOnly
        self.author_name = author.display_name
        self.author_image = author.display_avatar.url

    def e_role_top(self) -> discord.Embed:

        Embeds = discord.Embed(title="ロールメニュー",color=0xffffff,description="ここではロールに関する操作ができます。")
        Embeds.add_field(name=(f"・!list (一覧)"), value=(f"ロールの一覧を表示し付与することもできます"))
        Embeds.add_field(name=(f'・!make (追加)'), value=(f'フォーム形式でロールを作成できます'))
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds

    def e_attachrole(self,_name:str,_color) ->discord.Embed:
        Embeds = discord.Embed(color=_color)
        Embeds.add_field(name=(f'{_name}を作成しました'), value=(f'作成したロールをつけますか？'))
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds

    def e_rolelist(self,guild :discord.Guild) -> discord.Embed:
        Embeds = discord.Embed(color=0xffffff,title="ロールリスト",description="下のセレクトメニューからロールを選択することで付与されます。")
        guild_id = guild.id
        if(self.isOnly == "1"):
            Embeds.set_footer(text=(f"{self.author_name}のみ操作可能"),icon_url=self.author_image)
        else:
            Embeds.set_footer(text=(f"{self.author_name}が作成"),icon_url=self.author_image)
        return Embeds

# いったん凍結　（TypeError: 'RoleMenuButtons' object is not callable）発生-----------------------------------
# class unlockbutton(discord.ui.Button):
#     def __init__(self,e_page:list = [],v_page:list = []):
#         super().__init__(label='限定モード解除',style=discord.ButtonStyle.red)
#         self.e_page = e_page
#         self.v_page = v_page

#     async def callback(self, interaction: discord.Interaction):
#         # await interaction.response.send_message(f'終了します', ephemeral=True)
#         # ここにページを見てisonly noneで返すの作る
#         judge = judgeisOnly(author=self.author,isOnly = None,e_page=self.e_page[-1],v_page=self.v_page)
#         self.e_page.append(judge.e_isOnly(self.e_page[-1]))
#         # self.v_page.append(judge.v_isOnly(self.v_page[-1]))
#         view = judge.v_isOnly(self.v_page[-1])
#         self.v_page.append(view)
#         await interaction.response.edit_message(embed=self.e_page[-1],view=self.v_page[-1])
# --------------------------------------------------------------------------------------------------------------

class prevbutton(discord.ui.Button):
    def __init__(self,e_page:list = [],v_page:list = []):
        super().__init__(style=discord.ButtonStyle.gray,label="戻る")
        self.e_page = e_page
        self.v_page = v_page

    async def callback(self, interaction: discord.Interaction):
        del self.e_page[-1]
        del self.v_page[-1]
        await interaction.response.edit_message(embed=self.e_page[-1],view=self.v_page[-1],attachments=[])
        print((f"今のページ数はVは{len(self.v_page)}でEは{len(self.e_page)}です"))

class mypage():
    def __init__(self,e_page:list = [],v_page:list = []) -> None:
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
    
    @commands.hybrid_command()
    async def role(self,ctx,isonly=None):
        author = ctx.author
        e_page =[]
        v_page =[]
        await self.role_top(channel=ctx,author=author,isOnly=isonly,e_page=e_page,v_page=v_page)


    async def role_top(self,channel:discord.Thread,author:discord.Member,*,isOnly = None,isTree:bool = False,e_page:list,v_page:list):
        evs = embedbox(author,isOnly)
        Embeds = evs.e_role_top()
        e_page.append(Embeds)
        judge = judgeisOnly(author,isOnly,e_page=e_page,v_page=v_page)
        Views = judge.v_isOnly(RoleMenuButtons)
        
        await channel.send(embed=Embeds,view=Views)

    @commands.command()
    async def make(self,ctx, R_name=None, R_color="0xffffff",isOnly = None):
        guild = ctx.guild
        author = ctx.author
        author_name = author.display_name
        author_image = author.display_avatar.url
        e_page = []
        v_page = []
        await ctx.message.delete(delay=1)

        async def manualrole():
            newrole = await guild.create_role(name=R_name,colour=R_color,hoist=0,mentionable=1
                                                ,reason=(f"{author.name}によって作成(id:{author.id})"))
            botrolepos = guild.self_role.position
            await newrole.edit(position=botrolepos-1)
            Embeds = discord.Embed(color=R_color)
            Embeds.add_field(name=(f'{R_name}を作成しました'), value=(f'作成したロールをつけますか？'))
            if(isOnly == "1"):
                Embeds.set_footer(text=(f"{author_name}のみ操作可能"),icon_url=author_image)
            else:
                Embeds.set_footer(text=(f"{author_name}が作成"),icon_url=author_image)
            views = RoleAttach(author=author,isOnly=isOnly,role=newrole)

            path = "./bot_witch/guilds/" + str(guild.id) + ".json"
            with open(path,"r") as file:
                rolelist = json.load(file)
                rolelist["role"].append(newrole.id)
            with open(path,"w") as file:
                json.dump(rolelist,file,indent=4)

            await ctx.send(embed=Embeds, view=views)

        #---ロール作成(かつ色を16進数変換)
        if (R_name is None):
            return await ctx.send(f'エラー発生作成を中断します。',ephemeral=True)
        elif R_color[0] == '#':
            R_color = int(R_color.replace("#", "0x"), base=16)
            await manualrole()
        elif R_color[:1] == "0x":
            R_color = int(R_color, base=16)
            await manualrole()
        else:
            await ctx.send(f'エラー発生作成を中断します。',ephemeral=True)
            return

    @commands.command()
    async def list(self,ctx,isOnly = None):
        guild = ctx.guild
        author = ctx.author
        author_name = author.display_name
        author_image = author.display_avatar.url
        e_page = []
        v_page = []

        await ctx.message.delete(delay=1)
        path = "./bot_witch/guilds/" + str(guild.id) + ".json"
        evs = embedbox(author=author,isOnly=isOnly)
        judge = judgeisOnly(author,isOnly,e_page,v_page)
        Embeds = evs.e_rolelist(guild)
        # views = judge.v_isOnly(roleview)
        views = roleview_json(guild=guild,isOnly=isOnly,e_page=e_page,v_page=v_page,author=author)
        await ctx.send(embed=Embeds,view=views)

class RoleMenuButtons(discord.ui.View):
    def __init__(self, *, timeout = None,author:int = None,isOnly,e_page:list = [],v_page:list = []):
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
        if self.isOnly == "1":
            if self.author != interaction.user:
                await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),ephemeral=True)
                return False
        return True
# 第一ボタン
    @discord.ui.button(
    label=(f'!list'),
    style=discord.ButtonStyle.primary,)

    async def list(self, interaction: discord.Interaction,button: discord.ui.Button):
        guild = interaction.guild
        path = "./bot_witch/guilds/" + str(guild.id) + ".json"
        evs = embedbox(author=self.author,isOnly=self.isOnly)
        judge = judgeisOnly(self.author,self.isOnly,self.e_page,self.v_page)
        Embeds = evs.e_rolelist(interaction.guild)
        self.e_page.append(Embeds)
        # views = judge.v_isOnly(roleview)
        views = roleview_json(guild=interaction.guild,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page,author=self.author)
        await interaction.response.edit_message(embed=Embeds,view=views)

# 第二ボタン
    @discord.ui.button(
    label=(f'!make'),
    style=discord.ButtonStyle.primary,)
    
    async def make(self, interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_modal(Role_question(isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page))

class Role_question(ui.Modal, title='ロール作成フォーム'):
    def __init__(self,isOnly,e_page:list = [],v_page:list = []) -> None:
        super().__init__()
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page

    value_name = ui.TextInput(label=(f'名前'),custom_id="name",placeholder=(f"名前を入力してください。"),required=True)
    value_color = ui.TextInput(label=(f'色'),custom_id="color",placeholder=(f"色を#をつけ入力してください(16進数)例:#a1b3f0"),required=True,max_length=7,min_length=7)

    async def on_submit(self, interaction: discord.Interaction,):
        guild = interaction.guild
        author = interaction.user
        R_name = self.value_name.value
        R_color = self.value_color.value
        R_color = int(R_color.replace("#", "0x"), base=16)
        
        evs = embedbox(author,self.isOnly)

        newrole = await guild.create_role(name=R_name,colour=R_color,hoist=0,mentionable=1,reason=(f"{author.name}によって作成(id:{author.id})"))
        botrolepos = guild.self_role.position

        await newrole.edit(position=botrolepos-1)
        path = "./bot_witch/guilds/" + str(guild.id) + ".json"
        with open(path,"r") as file:
            rolelist = json.load(file)
            rolelist["role"].append(newrole.id)
        with open(path,"w") as file:
            json.dump(rolelist,file,indent=4)

        Embeds = evs.e_attachrole(_name=R_name,_color=R_color)
        self.e_page.append(Embeds)
        # Embeds = judge.e_isOnly(Embeds)
        views = RoleAttach(author=author,isOnly=self.isOnly,e_page=self.e_page,v_page=self.v_page,role=newrole)
        await interaction.response.edit_message(embed=Embeds,view=views)

class RoleAttach(discord.ui.View):
    def __init__(self, *, timeout = None,author:discord.Member = None,isOnly,e_page:list = [],v_page:list = [],role:discord.Role):
        super().__init__(timeout=timeout)
        self.author= author
        self.isOnly = isOnly
        self.e_page = e_page
        self.v_page = v_page
        self.role = role
        # if(isOnly == "1"):
        #     self.add_item(unlockbutton(self.e_page,self.v_page))

        v_page.append(self)
        if(len(self.e_page) != 0):
            self.add_item(prevbutton(self.e_page,self.v_page))

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if self.isOnly == "1":
            if self.author != interaction.user:
                await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),ephemeral=True)
                return False
        return True

    @discord.ui.button(
        label='はい',
        style=discord.ButtonStyle.green,
    )
    async def yes(self, interaction: discord.Interaction,button: discord.ui.Button):
        guild = interaction.guild
        name = self.role.name
        await interaction.response.send_message(f'{name}をつけました。',ephemeral=True)
        await interaction.user.add_roles(self.role)

    @discord.ui.button(label='いいえ', style=discord.ButtonStyle.grey)
    async def no(self, interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.send_message(f'終了します', ephemeral=True)

class roleview(discord.ui.View):
    def __init__(self,*,author:discord.Member = None,isOnly,e_page:list = [],v_page:list = [],timeout=None):
        super().__init__(timeout=timeout)
        self.e_page = e_page
        self.v_page = v_page
        self.author= author
        self.isOnly = isOnly

        self.add_item(roleselecter())
        v_page.append(self)

        if(len(self.e_page) != 0):
            self.add_item(prevbutton(self.e_page,self.v_page))

class roleselecter(discord.ui.RoleSelect):
    def __init__(self,*,customid="roleselecter") -> None:
        super().__init__()

class roleview_json(discord.ui.View):
    def __init__(self, *,guild,e_page:list = [],isOnly,v_page:list = [],timeout=None,author:discord.Member):
        super().__init__(timeout=timeout)
        self.v_page = v_page
        self.e_page = e_page
        self.v_page.append(self)
        self.add_item(roleselecter_json(guild=guild,isOnly=isOnly,author=author))
        if(len(self.e_page) != 0):
            self.add_item(prevbutton(self.e_page,self.v_page))

class roleselecter_json(discord.ui.Select):
    def __init__(self,*,guild,customid="roleselecter_json",isOnly,timeout=None,author = None) -> None:
        super().__init__()
        self.isOnly = isOnly
        options = []
        self.author = author
        self.guild : discord.Guild = guild
        path = "./bot_witch/guilds/" + str(self.guild.id) + ".json"
        rolecount = 0
        errorcount = 0

        with open(path,"r") as file:
            rolelist = json.load(file)
            for jsonroleid in rolelist["role"]:
                
                role :discord.Role = self.guild.get_role(jsonroleid)
                try:
                    options.append(discord.SelectOption(label=(f"{len(role.members)}人 : {role.name}"),value=jsonroleid))
                    rolecount +=1
                except AttributeError:
                    rolelist["role"].remove(jsonroleid)
                    errorcount +=1

        if(len(options) == 0):
            with open(path,"w") as filew:
                json.dump(rolelist,filew,indent=4)
            options.append(discord.SelectOption(label=(f"ロール無し…")))
            super().__init__(options=options,disabled=True,placeholder="ロール無し…🍂")
        elif (errorcount == 0):
            super().__init__(options=options,placeholder=(f"ロール総数:{rolecount}"))
        else:
            with open(path,"w") as filew:
                json.dump(rolelist,filew,indent=4)
            super().__init__(options=options,placeholder=(f"ロール総数:{rolecount},エラー件数:{errorcount}"))

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        if self.isOnly == "1":
            if self.author != interaction.user:
                await interaction.response.send_message(content=(f"専用モードのため{self.author.mention}のみ操作できます"),ephemeral=True)
                return False
        return True

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        role = guild.get_role(int(self.values[0]))
        rolelist = user.roles
        
        for userrole in rolelist:
            if userrole == role:
                name = role.name
                await user.remove_roles(role,reason=(f"{user.name}によって(id:{user.id}"))
                await interaction.response.send_message(f'{name}を外しました。',ephemeral=True)
                return

        name = role.name
        await interaction.response.send_message(f'{name}をつけました。',ephemeral=True)
        await user.add_roles(role,reason=(f"{user.name}によって(id:{user.id}"))
        return

async def setup(bot):
    await bot.add_cog(role_menu(bot))

    print(f"role読み込み")