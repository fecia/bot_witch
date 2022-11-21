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

        self.add_item(hnbplaybutton(self.e_page,self.v_page))
    
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
    def __init__(self,e_page:list = [],v_page:list = [],labelname:str='!hnb'):
        super().__init__(label=labelname,style=discord.ButtonStyle.blurple)
        self.e_page = e_page
        self.v_page = v_page

    async def callback(self, interaction: discord.Interaction):
        pass

class hnbplaybutton(discord.ui.Button):
    def __init__(self,e_page:list = [],v_page:list = [],labelname:str='!hnb'):
        super().__init__(label=labelname,style=discord.ButtonStyle.blurple)
        self.e_page = e_page
        self.v_page = v_page

    async def callback(self, interaction: discord.Interaction):
        pass

async def setup(bot):
    print(f"game読み込み")
    await bot.add_cog(game_menu(bot))