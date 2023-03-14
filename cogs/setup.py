import disnake
from disnake.ext import commands
from utils.database import Database
from utils.tools import color_check, get_user_response_numbers, vaild_object_check, list_data

async def add_setting_more(self, inter, table):
    """Adds multiple things at one time"""
    response = await get_user_response_numbers(self, inter)
    if not response:
        return await inter.send("This view has timed out or you put a invaild role or channel (or thread)", ephemeral=True)

    CURRENT_DATA = await Database.get_data(table, inter.guild.id)
    if len(CURRENT_DATA) >= 10:
        return await inter.send("You can only have up to 10 items per database, remove some to add more")
      
    IDS_TO_ADD = []
    IDS_TO_NOT_ADD = []
    IDS_TO_NOT_ADD_REASONS = ""

    ids = response.split(" ")
    for id in ids:
        object = vaild_object_check(inter, int(id))
      
        if not object:
            IDS_TO_NOT_ADD.append(id)
            IDS_TO_NOT_ADD_REASONS += f"\n`{id}` is not a vaild role or channel (or thread)"
        if id in IDS_TO_ADD:
            IDS_TO_NOT_ADD.append(id)
            IDS_TO_NOT_ADD_REASONS += f"\nYou provided `{object}` more than once"
          
        if id in CURRENT_DATA:
            IDS_TO_NOT_ADD.append(id)
            IDS_TO_NOT_ADD_REASONS += f'\n`{object}` is already in the database: `{table}`'

        if id not in IDS_TO_NOT_ADD:
            IDS_TO_ADD.append(id)

    if len(CURRENT_DATA) + len(IDS_TO_ADD) >= 10:
        return await inter.send("You can only have up to 10 items per database")

    if not IDS_TO_ADD:
        embed = disnake.Embed(title="Entrys Failed :(", description=f"`Current data:` {await list_data(inter, table)}", color=await color_check(inter))  
        embed.add_field(name="Not Adding", value=IDS_TO_NOT_ADD_REASONS)
        return await inter.send(embed=embed, ephemeral=True)

  
    IDS_TO_ADD_MESSAGE = ""  
    for id in IDS_TO_ADD:
        await Database.add_data_list(table, inter.guild.id, id)

        role = inter.guild.get_role(int(id))
        channel = inter.guild.get_channel_or_thread(int(id))

        save = channel if role == None else role
        IDS_TO_ADD_MESSAGE += f'{save.mention}, '      

  
    embed = disnake.Embed(title="Data Added", description=f"`Current data:` {await list_data(inter, table)}", color=await color_check(inter))  
    embed.add_field(name="Added", value=IDS_TO_ADD_MESSAGE[:-2])
  
    if IDS_TO_NOT_ADD_REASONS:
      embed.add_field(name="Not Adding", value=IDS_TO_NOT_ADD_REASONS)
      
    return await inter.send(embed=embed)

    

async def remove_setting_more(self, inter, table):
    """Removes multiple things at one time"""
    response = await get_user_response_numbers(self, inter)
    if not response:
        return await inter.send("This view has timed out or you put a invaild role or channel (or thread)", ephemeral=True)

    CURRENT_DATA = await Database.get_data(table, inter.guild.id)
    if CURRENT_DATA == 'None':
        return await inter.send("You don't have any data..", ephemeral=True)

    IDS_TO_REMOVE = []
    IDS_TO_NOT_REMOVE = []
    IDS_TO_NOT_REMOVE_REASONS = ""

    ids = response.split(" ")
    for id in ids:
        if id in IDS_TO_REMOVE:
            IDS_TO_NOT_REMOVE.append(id)
            IDS_TO_NOT_REMOVE_REASONS += f"\nYou provided `{object}` more than once"
          
        if id not in CURRENT_DATA:
            IDS_TO_NOT_REMOVE.append(id)
            IDS_TO_NOT_REMOVE_REASONS += f'\n`{object}` is not in the database: `{table}`'  
        if id not in IDS_TO_NOT_REMOVE:
            IDS_TO_REMOVE.append(id)

  
    if not IDS_TO_REMOVE:
        embed = disnake.Embed(title="Entrys Failed :(", description=f"`Current data:` {await list_data(inter, table)}", color=await color_check(inter))  
        embed.add_field(name="Not Removing", value=IDS_TO_NOT_REMOVE_REASONS)
        return await inter.send(embed=embed, ephemeral=True)

  
    IDS_TO_ADD_MESSAGE = ""  
    for id in IDS_TO_REMOVE:
        await Database.remove_data_list(table, inter.guild.id, id)
        role = inter.guild.get_role(int(id))
        channel = inter.guild.get_channel_or_thread(int(id))

        save = channel if role == None else role
        IDS_TO_ADD_MESSAGE += f'{save.mention}, ' 
  
    embed = disnake.Embed(title="Data Removed", description=f"`Current data:` {await list_data(inter, table)}", color=await color_check(inter))  
    embed.add_field(name="Removed", value=IDS_TO_ADD_MESSAGE[:-2])
  
    if IDS_TO_NOT_REMOVE_REASONS:
      embed.add_field(name="Not Removing", value=IDS_TO_NOT_REMOVE_REASONS)
      
    return await inter.send(embed=embed)

async def settings_data_show(inter, list_of_tables):
    """Shows what settings you currently have on or off"""
    current_settings = ""
    for table in list_of_tables:
        data = await Database.get_data(table, inter.guild.id)
        text = "<:BWB_On:1064385210436825118>" if data == 'None' else '<:BWB_Off:1064385194716569650>'
        current_settings += f'{table} {text}\n'
    
    embed = disnake.Embed(
      title="Current On/Off Settings", 
      description=f"{current_settings}\n\nClick on the buttons to turn a setting on or off",
      color=await color_check(inter)
    )
    return embed

async def on_off_settings(inter, table):
    """Turns 'On/Off' settings on or off"""
    await inter.response.defer(ephemeral=True)
  
    CURRENT_DATA = await Database.get_data(table, inter.guild.id)
    if CURRENT_DATA == 'None': # means on
        await Database.add_data(table, inter.guild.id, 'Off')
        return await inter.send(f"{table} is now off", ephemeral=True)
    elif CURRENT_DATA == 'Off':
        await Database.remove_data(table, inter.guild.id)
        return await inter.send(f"{table} is now on", ephemeral=True) 

SETUP_SETTINGS = {
  # Roles
  "FranchiseRole": {"database": "FranchiseRole", "add_message": "Please mention the coach roles you want to add", "remove_message": "Please menton the coach roles you would like to remove", "add_function": add_setting_more, "remove_function": remove_setting_more},
  "FreeAgentRole": {"database": "FreeAgentRole", "add_message": "Please mention the free agent roles you want to add", "remove_message": "Please mention the free agent roles you want to remove", "add_function": add_setting_more, "remove_function": remove_setting_more},
  "AfterSignRole": {"database": "AfterSignRole", "add_message": "Please mention the after sign roles you want to add", "remove_message": "Please mention the after sign roles you want to remove", "add_function": add_setting_more, "remove_function": remove_setting_more},  

  # Channels
  "SigningChannel": {"database": "SigningChannel", "add_message": "Please mention the channels you want to be used for transactions (signing)", "remove_message": "Please mention the channels you want to remove", "add_function": add_setting_more, "remove_function": remove_setting_more},
  "OfferingChannel": {"database": "OfferingChannel", "add_message": "Please mention the channels you want to be used for offering", "remove_message": "Please mention the channels you want to remove", "add_function": add_setting_more, "remove_function": remove_setting_more},
  "DemandingChannel": {"database": "DemandingChannel", "add_message": "Please mention the channels you want to be used for demanding", "remove_message": "Please mention the channels you want to remove", "add_function": add_setting_more, "remove_function": remove_setting_more},

}
  
  

class SetupCommandDropdownView(disnake.ui.View):
    def __init__(self, command_self, inter):
        super().__init__()
        self.command_self = command_self
        self.inter = inter

        self.add_item(SetupCommandDropdown(self.command_self, self.inter))

    async def on_timeout(self) -> None:
        await self.inter.edit_original_message(view=None, content=f"Command has expired, run `/{self.inter.data.name}` to use the command again")

class SetupCommandDropdown(disnake.ui.Select):
    def __init__(self, command_self, inter):
        self.inter = inter  
        self.command_self = command_self
      
        options = [
            disnake.SelectOption(
                label="Roles", description="Coach roles, free agent roles, etc", emoji="<:BWB_Role:1063878701764313180>"
            ),       
            disnake.SelectOption(
                label="Channels", description="Signing channels", emoji="<:BWB_Channel:1064327317519863930>"
            ),  
            disnake.SelectOption(
                label="On/Off", description="Ghostpings, turning signing and demanding on and off, other settings", emoji="<:BWB_Settings:1064390227227058277>"
            ),           
        ]

        super().__init__(
          options=options,
          placeholder="Picks a settings module",
        )

    async def interaction_check(self, inter) -> None:
        return inter.author.id == self.inter.author.id

    async def callback(self, inter):
        if self.values[0] == 'Roles':
            await inter.response.send_message(view=RoleSettings(self.command_self), ephemeral=True)
        elif self.values[0] == 'Channels':
            await inter.response.send_message(view=ChannelSettings(self.command_self), ephemeral=True)
        elif self.values[0] == 'On/Off':
            await inter.response.send_message(view=OnOffSettings(), ephemeral=True, embed=await settings_data_show(inter, ['GhostPings', 'Demands', 'Signing']))
          
class RoleSettings(disnake.ui.View):
    def __init__(self, command_self):
        super().__init__()
        self.command_self = command_self

    @disnake.ui.button(label="Coach Roles")  
    async def coach_button(self, button: disnake.ui.Button, inter):
        view = AddRemoveButton(self.command_self, inter, SETUP_SETTINGS["FranchiseRole"])
        
        await inter.response.send_message("Would you like to add or remove coach roles?", view=view, ephemeral=True)

    @disnake.ui.button(label="Free Agent Roles")  
    async def free_agent_button(self, button: disnake.ui.Button, inter):
        view = AddRemoveButton(self.command_self, inter, SETUP_SETTINGS["FreeAgentRole"])
        
        await inter.response.send_message("Would you like to add or remove free agent roles?", view=view, ephemeral=True)

    @disnake.ui.button(label="After Sign Roles")  
    async def after_sign_button(self, button: disnake.ui.Button, inter):
        view = AddRemoveButton(self.command_self, inter, SETUP_SETTINGS["AfterSignRole"])
        
        await inter.response.send_message("Would you like to add or remove after sign roles?", view=view, ephemeral=True)

class ChannelSettings(disnake.ui.View):
    def __init__(self, command_self):
        super().__init__()
        self.command_self = command_self

    @disnake.ui.button(label="Signing Channels")  
    async def signing_channel(self, button: disnake.ui.Button, inter):
        view = AddRemoveButton(self.command_self, inter, SETUP_SETTINGS["SigningChannel"])
        
        await inter.response.send_message("Would you like to add or remove signing channels?", view=view, ephemeral=True)

    @disnake.ui.button(label="Demanding Channels")  
    async def demanding_channel(self, button: disnake.ui.Button, inter):
        view = AddRemoveButton(self.command_self, inter, SETUP_SETTINGS["DemandingChannel"])
        
        await inter.response.send_message("Would you like to add or remove demanding channels?", view=view, ephemeral=True)

    @disnake.ui.button(label="Offering Channels")  
    async def offering_channel(self, button: disnake.ui.Button, inter):
        view = AddRemoveButton(self.command_self, inter, SETUP_SETTINGS["OfferingChannel"])
        
        await inter.response.send_message("Would you like to add or remove offering channels?", view=view, ephemeral=True)

class OnOffSettings(disnake.ui.View):
  def __init__(self):
    super().__init__()

  @disnake.ui.button(label="Signing")
  async def signing_channel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      await on_off_settings(inter, "Signing")

  @disnake.ui.button(label="Demands")
  async def demanding_channel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      await on_off_settings(inter, "Demands")

  @disnake.ui.button(label="GhostPings")
  async def offering_channel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      await on_off_settings(inter, "GhostPings")

class AddRemoveButton(disnake.ui.View):
    def __init__(self, command_self, inter, config):
        super().__init__()
        self.command_self = command_self
        self.inter = inter
        self.config = config

    @disnake.ui.button(label="Add", style=disnake.ButtonStyle.green)
    async def add(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
      
        embed = disnake.Embed(
          title=f"{self.config['database']} Setting", 
          description=f"{self.config['add_message']}\n`Current data:` {await list_data(inter, self.config['database'])}", 
          color=await color_check(inter)
        )
        await inter.send(embed=embed, ephemeral=True)  
      
        await self.config["add_function"](self.command_self, self.inter, self.config["database"])

    @disnake.ui.button(label="Remove", style=disnake.ButtonStyle.red)
    async def remove(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(
          title=f"{self.config['database']} Setting", 
          description=f"{self.config['remove_message']}\n`Current data:` {await list_data(inter, self.config['database'])}",
          color=await color_check(inter)
        )
        await inter.send(embed=embed, ephemeral=True)
      
        await self.config["remove_function"](self.command_self, self.inter, self.config["database"])  


class SetupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def setup(self, inter: disnake.GuildCommandInteraction):
        """Manage all the settings for the bot"""
        #signing_video = await Database.get_config('bot_assets', 'Youtube', 'SigningVideo')
        await inter.response.send_message(view=SetupCommandDropdownView(self, inter), ephemeral=True, content=f"Setup Menu - See <https://www.youtube.com/watch?v=GIic9B7QIXQ> for an example")
        
def setup(bot):
    bot.add_cog(SetupCommand(bot))