import disnake, random
from disnake.ext import commands
from utils.tools import color_check, list_data, get_keys
from utils.database import Database
from utils.config.config import error_support_message, BotLinks
from typing import Union

class AvatarLinks(disnake.ui.View):
    def __init__(self, member):
        super().__init__()
        self.member = member

        png_link = self.member.display_avatar.with_format('png').url
        jpg_link = self.member.display_avatar.with_format('jpg').url
        webp_link = self.member.display_avatar.with_format('webp').url
    
        self.add_item(disnake.ui.Button(label='PNG', url=png_link, emoji='🔗')) 
        self.add_item(disnake.ui.Button(label='JPG', url=jpg_link, emoji='🔗'))
        self.add_item(disnake.ui.Button(label='WEBP', url=webp_link, emoji='🔗'))
          
class UtilsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def avatar(self, inter, member: disnake.Member = None):
        """Shows your ugly profile picture"""
        if member == None: 
          member = inter.author
          
        embed = disnake.Embed(title=f"{member.display_name}", color=member.color)
        embed.set_image(url=member.display_avatar)
        embed.set_footer(text=f"I rate your avatar {random.randint(1, 10)}/10")
        await inter.response.send_message(embed=embed, view=AvatarLinks(member))   

    @commands.slash_command()
    async def membercount(self, inter: disnake.GuildCommandInteraction):
        """Shows how many people are in a server, includes bots"""
        embed = disnake.Embed(title="Membercount", description=f"{inter.guild.name} member count is **{inter.guild.member_count}**", color=await color_check(inter))
        embed.set_thumbnail(url=inter.guild.icon)
        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    async def config(self, inter: disnake.GuildCommandInteraction):
        """Shows your current server settings"""
        await inter.response.defer()
        await inter.edit_original_message("This may take a bit...")

        embed = disnake.Embed(title="Server Settings", color=await color_check(inter))
        keys = await get_keys()
        for table in keys:
            if 'Channel' in table or 'Role' in table:
                embed.add_field(name=table, value=await list_data(inter, table))

        # On/Off Settings
        signing_setting = await Database.get_data("Signing", inter.guild.id)
        signing_value = 'On' if signing_setting == 'None' else 'Off'

        demand_setting = await Database.get_data("Demands", inter.guild.id)
        demand_value = 'On' if demand_setting == 'None' else 'Off'

        gp_setting = await Database.get_data("GhostPings", inter.guild.id)
        gp_value = 'On' if gp_setting == 'None' else 'Off'

        embed.add_field(
          name="On/Off Settings", 
          value=f"`Signing:` {signing_value}\n`Demands:` {demand_value}\n`GhostPings:` {gp_value}"
        )

        await inter.edit_original_message(embed=embed, content=None)

    @commands.slash_command()
    async def embed(self, inter, title: str, description: str, channel: Union[disnake.TextChannel, disnake.Thread] = None):
      """
      Sends a embed with a message to a channel
      Parameters
      ----------
      title: The title for the embed (under 256 chars)
      description: The description for the embed (under 4096 chars)
      channel: The channel to send the embed to (defaults to the current chanenl)
      """
      if channel == None:
          channel = inter.channel      
        
      embed = disnake.Embed(title=title, description=description, color=inter.guild.me.color)
      embed.set_author(name=inter.guild.name, icon_url=inter.guild.icon)  	

      try:   
        embed.check_limits()
      except ValueError as ve:
        await inter.response.send_message(content=ve, ephemeral=True)

      try:
          await channel.send(embed=embed)
      except disnake.Forbidden:
          return await inter.response.send_message(f"I do not have the proper permissions to send the message to {channel.mention}", ephemeral=True)
      except disnake.HTTPException:  
          return await inter.response.send_message("Sending the message failed :sob:", ephemeral=True)

      await inter.response.send_message(f"The message has been sent to {channel.mention}", ephemeral=True)    

    @commands.slash_command()
    async def helpsigning(self, inter):
        """Shows you how to setup the signing system"""
       # signing_video = await Database.get_config("bot_assets", "Youtube", "SigningVideo")
        await inter.response.send_message(f"Try watching this video: **<https://www.youtube.com/watch?v=GIic9B7QIXQ>**\n\n{error_support_message}")
      

  
def setup(bot):
    bot.add_cog(UtilsCommands(bot))