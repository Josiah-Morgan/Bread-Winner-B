import disnake
from disnake.ext import commands
from utils.tools import color_check

NFL_LEAGUES = ["https://discord.new/B3U8zHPEMh9K", "https://discord.new/hukwCm6tjEeN", "https://discord.new/7rsNTeqYzDG8", "https://discord.new/ZdN8WtYJkWvZ", "https://discord.new/2rNnQTCEmpum", "https://discord.new/h8CSg7qhRS5x", "https://discord.new/thm2ZGBWt223", "https://discord.new/Kp6nKrPE67Ef",  "https://discord.new/HwDdKDsM4cDP", "https://discord.new/kNaCqHXcPWv5",  "https://discord.new/bfSWCdjswaXH", "https://discord.new/33NRzhy4CY57",  "https://discord.new/NxRt2m6aQFMf", "https://discord.new/GHVtcVMTk6Ru",  "https://discord.new/H8pZRb7r5Vtg", "https://discord.new/2X3UhzMt33DZ",  "https://discord.new/SBZg4TnGjUfu", "https://discord.new/sgCc2qVXCmnB", "https://discord.new/Xc3W4hzEBFFF"]

COLLEGE_LEAGUES = ["https://discord.new/HNhCEfWRSnJ3", "https://discord.new/eHfSGTF7jqDu", "https://discord.new/7znv6u6qpQbF", "https://discord.new/wqrV4dNRXBkK", "https://discord.new/FfYtUd72mAfZ", "https://discord.new/wkNy7SW25ZuF", "https://discord.new/KQj5ptJVxabw", "https://discord.new/jh43abKSC7WZ", "https://discord.new/Qw8Wj9QBrwkt", "https://discord.new/4yZSZghXpZGG", "https://discord.new/gnkRZ2cKPtva", "https://discord.new/7Ac897269DRR", "https://discord.new/A84cJjUq2xnv", "https://discord.new/uavT3DxTXy73", "https://discord.new/mZM7rDVeEQ78", "https://discord.new/9XRdH4nnTqAu", "https://discord.new/RYg62hWuZNMq"] 

NBA_LEAGUES = ["https://discord.new/JDPsRCjabAfr", "https://discord.new/v958EW2XYJaP", "https://discord.new/vagP3pJC5gey", "https://discord.new/gjywmwdJ9XWB", "https://discord.new/7jF7bGymmMSy", "https://discord.new/wrpVBE95uzkT", "https://discord.new/9XVHFSe5pe74", "https://discord.new/SrNyHqRycgQZ"]

NHL_LEAGUES = ["https://discord.new/7mfdCNNdXMke", "https://discord.new/tzemY8mQM5aW", "https://discord.new/Drn25ch7AQBU", "https://discord.new/JtQB7YTXTW6R"]

MLB_LEAGUES = ["https://discord.new/7WBAesXFxbCN", "https://discord.new/FgtKptfunqFM", "https://discord.new/GEcQhCPEESnq", "https://discord.new/h9dUHBgJZV9b"]

# Football fusion
FF_LEAGUES = ["https://discord.new/TxgXxcfqfNb9", "https://discord.new/2nQdQxKFU4DT", "https://discord.new/eVdg9qmVXYzY", "https://discord.new/cnA3mvzkgfcU"]

bars_options = [
  disnake.SelectOption(label="═══", value="═══"),
  disnake.SelectOption(label="---", value="---"),
  disnake.SelectOption(label="———", value="———"),
  disnake.SelectOption(label="▬▬▬", value="▬▬▬"),
  disnake.SelectOption(label="┈┈", value="┈┈"),
  disnake.SelectOption(label="╼╼", value="╼╼"),
  disnake.SelectOption(label="╾╾", value="╾╾"),
  disnake.SelectOption(label="'‎‎‎‎‎‎‎‎‎‎‎‎ ‎‎‎‎‎‎ ‎‎‎‎‎‎ ‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎'", value="'‎‎‎‎‎‎‎‎‎‎‎‎ ‎‎‎‎‎‎ ‎‎‎‎‎‎ ‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎'"),
  disnake.SelectOption(label="＝＝", value="＝＝"),
  disnake.SelectOption(label="≣≣≣", value="≣≣≣") # 10
]

brackets_options = [
  disnake.SelectOption(label="【 】", value="【 】"),
  disnake.SelectOption(label="〚 〛", value="〚 〛"),
  disnake.SelectOption(label="《 》", value="《 》"),
  disnake.SelectOption(label="『 』", value="『 』"),
  disnake.SelectOption(label="〘 〙", value="〘 〙"),
  disnake.SelectOption(label="〖 〗", value="〖 〗"),
  disnake.SelectOption(label="〈 〉", value="〈 〉"),
  disnake.SelectOption(label="（ ）", value="（ ）"),
  disnake.SelectOption(label="「 」", value="「 」"),
  disnake.SelectOption(label="〈 〉", value="〈 〉"),
  disnake.SelectOption(label="« »", value="« »"),
  disnake.SelectOption(label="‹ ›", value="‹ ›") # 12
]

lines_options = [
  disnake.SelectOption(label="┃", value="┃"),
  disnake.SelectOption(label="╵", value="╵"),
  disnake.SelectOption(label="╷", value="╷"),
  disnake.SelectOption(label="┇", value="┇"),
  disnake.SelectOption(label="║", value="║"),
  disnake.SelectOption(label="▕▏", value="▕▏") # 6
]

dots_options = [
  disnake.SelectOption(label="•", value="•"),
  disnake.SelectOption(label="・", value="・"),
  disnake.SelectOption(label="⦿", value="⦿"),
  disnake.SelectOption(label="⦾", value="⦾"),
  disnake.SelectOption(label="○", value="○"),
  disnake.SelectOption(label="◦", value="◦"),
  disnake.SelectOption(label="∙", value="∙"),
  disnake.SelectOption(label="⁍", value="⁍"),
  disnake.SelectOption(label="⁌", value="⁌") # 9
]

stars_options = [
  disnake.SelectOption(label="★", value="★"),
  disnake.SelectOption(label="⍟", value="⍟"),
  disnake.SelectOption(label="✩", value="✩"),
  disnake.SelectOption(label="✦", value="✦"),
  disnake.SelectOption(label="✧", value="✧"),
  disnake.SelectOption(label="✪", value="✪"),
  disnake.SelectOption(label="✫", value="✫"),
  disnake.SelectOption(label="✬", value="✬"),
  disnake.SelectOption(label="⭒", value="⭒") # 9
]

dividers_options = [
  disnake.SelectOption(label=" ⠀⠀⠀⠀⠀⠀𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚⠀⠀⠀⠀⠀", value=" ⠀⠀⠀⠀⠀⠀𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚⠀⠀⠀⠀⠀"),
  disnake.SelectOption(label=" ▬▬▬▬ 👤 Franchise 👤 ▬▬▬▬", value=" ▬▬▬▬ 👤 Franchise 👤 ▬▬▬▬"),
  disnake.SelectOption(label="■▬▬▬▬▬〔👤〕▬▬▬▬▬■", value="■▬▬▬▬▬〔👤〕▬▬▬▬▬■"),
  disnake.SelectOption(label=" ▬▬▬▬・𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚・▬▬▬▬", value=" ▬▬▬▬・𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚・▬▬▬▬"),
  disnake.SelectOption(label="「          ⁣⁣𝗙𝗿𝗮𝗻𝗰𝗵𝗶𝘀𝗲           ⁣」", value="「          ⁣⁣𝗙𝗿𝗮𝗻𝗰𝗵𝗶𝘀𝗲           ⁣」"),
  disnake.SelectOption(label="━━━━━━━┃ 👤 ┃━━━━━━━", value="━━━━━━━┃ 👤 ┃━━━━━━━"),
  disnake.SelectOption(label="■▬▬▬▬﹝𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚﹞▬▬▬▬■", value="■▬▬▬▬﹝𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚﹞▬▬▬▬■"),
  disnake.SelectOption(label="👤 | Franchise", value="👤 | Franchise"),
  disnake.SelectOption(label="‎‎‎‎‎▕▏𝗙𝗿𝗮𝗻𝗰𝗵𝗶𝘀𝗲▕▏", value="‎‎‎‎‎▕▏𝗙𝗿𝗮𝗻𝗰𝗵𝗶𝘀𝗲▕▏"),
  disnake.SelectOption(label="▴         𝗙𝗿𝗮𝗻𝗰𝗵𝗶𝘀𝗲         ▴", value="▴         𝗙𝗿𝗮𝗻𝗰𝗵𝗶𝘀𝗲         ▴"),
  disnake.SelectOption(label="▬▬▬▬▬𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚▬▬▬▬▬", value="▬▬▬▬▬𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚▬▬▬▬▬"),
  disnake.SelectOption(label="‎‎‎‎‎--------𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚--------", value="‎‎‎‎‎--------𝙁𝙧𝙖𝙣𝙘𝙝𝙞𝙨𝙚--------"),
  disnake.SelectOption(label="‎‎‎‎👤", value="‎‎‎‎👤") # 13
]

async def template_embed(inter, league, templates):
      embed = disnake.Embed(title=f"{league} Templates", description="Preview all the templates at once [by clicking here](https://discord.gg/xQs94q4bvE)")
  
      items = ""
      for i in range(0, len(templates)):
          items += f"[{i + 1}]({templates[i]}) "
      
      embed.add_field(name="Leagues", value=items)
      await inter.response.send_message(embed=embed)

class SymbolDropdown(disnake.ui.Select):
    def __init__(self, options, max_value):
        super().__init__(placeholder="Choose your symbols", max_values=max_value, options=options)

    async def callback(self, interaction: disnake.MessageInteraction):
      
        labels = [thing for thing in self.values]
        await interaction.response.send_message(f"Your symbols: {', '.join(labels)}")

class SymbolDropdownView(disnake.ui.View):
    def __init__(self, options):
        super().__init__()
        self.options = options
        self.max_value = len(options)


        self.add_item(SymbolDropdown(self.options, self.max_value))

class LeagueCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.slash_command()
  async def template(self, inter):
    return
  
  @template.sub_command_group()
  async def league(self, inter):
    return

  # teamchats, teamhubs
  @template.sub_command_group()
  async def team(self, inter):
    return

  @league.sub_command()
  async def nfl(self, inter):
    """NFL templates"""
    await template_embed(inter, 'NFL', NFL_LEAGUES)

  @league.sub_command()
  async def college(self, inter):
    """College templates"""
    await template_embed(inter, 'College', COLLEGE_LEAGUES)

  @league.sub_command()
  async def nba(self, inter):
    """NBA templates"""
    await template_embed(inter, 'NBA', NBA_LEAGUES)

  @league.sub_command()
  async def nhl(self, inter):
    """NHL templates"""
    await template_embed(inter, 'NHL', NHL_LEAGUES)
  
  @league.sub_command()
  async def mlb(self, inter):
    """MLB templates"""
    await template_embed(inter, 'MLB', MLB_LEAGUES)
  
  @league.sub_command()
  async def ff(self, inter):
    """Football Fusion templates"""
    await template_embed(inter, 'Football Fusion', FF_LEAGUES)
    
  # Ugly
  @team.sub_command()
  async def teamchats(self, inter):
    """Teamchats templates"""
    embed = disnake.Embed(title='Team Chat Templates', description=f"Preview all the teamchats at once [by clicking here](https://discord.gg/xQs94q4bvE)", color=await color_check(inter))
    embed.add_field(name="Old TC", value="[Here](https://discord.new/Kk2KzaHN2dfK)")
    embed.add_field(name="New TC", value="[Here](https://discord.new/zaJ8fYkgrjgS)")
    embed.add_field(name="Team Chat", value="[Here](https://discord.new/bukA3AjKsUNu)") 
    
    await inter.response.send_message(embed=embed)

  @team.sub_command()
  async def teamhubs(self, inter):
    """Teamchats templates 𝙗𝙪𝙩 𝙗𝙞𝙜𝙜𝙚𝙧"""
    embed = disnake.Embed(title='Teamhub Templates', description=f"Preview all the teamchats at once [by clicking here](https://discord.gg/xQs94q4bvE)", color=await color_check(inter))

    embed.add_field(name="Team Hub", value="[Here](https://discord.new/wvdqjn9Aq22K)")
    embed.add_field(name="Team Hub 2", value="[Here](https://discord.new/JJRc8rf8gjPn)") 
    embed.add_field(name="Team Hub 3", value="[Here](https://discord.new/rK2HXAQEmSpf)") 
    embed.add_field(name="Team Hub 4", value="[Here](https://discord.new/ZrDx39EbfGxf)") 
    embed.add_field(name="Team Hub 5", value="[Here](https://discord.new/6pxjV6RTJtWu)") 
    embed.add_field(name="NBA Teamhub", value="[Here](https://discord.new/yXcHMZd3psS7)")   
    await inter.response.send_message(embed=embed)



  # Symbols

  @commands.slash_command()
  async def symbol(self, inter):
    return
  
  @symbol.sub_command()
  async def bars(self, inter):
    """Bar symbols, roles, categories"""
    await inter.response.send_message("Pick your symbols", view=SymbolDropdownView(bars_options))

  @symbol.sub_command()
  async def brackets(self, inter):
    "Bracket symbols, channels, roles"
    await inter.response.send_message("Pick your symbols", view=SymbolDropdownView(brackets_options))

  @symbol.sub_command()
  async def lines(self, inter):
    """Lines symbols, fits everything"""
    await inter.response.send_message("Pick your symbols", view=SymbolDropdownView(lines_options))

  @symbol.sub_command()
  async def dots(self, inter):
    """Dot symbols, fits everything"""
    await inter.response.send_message("Pick your symbols", view=SymbolDropdownView(dots_options))

  @symbol.sub_command()
  async def stars(self, inter):
    """Star symbols, roles, categories"""
    await inter.response.send_message("Pick your symbols", view=SymbolDropdownView(stars_options))

  @symbol.sub_command()
  async def dividers(self, inter):
    """Divider symbols, roles, categories"""
    await inter.response.send_message("Pick your symbols", view=SymbolDropdownView(dividers_options))
    

def setup(bot): 
  bot.add_cog(LeagueCommands(bot))