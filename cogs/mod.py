import disnake
from disnake.ext import commands
from typing import Union, Optional
from utils.tools import color_check

class Confirm(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=10.0)
        self.value: Optional[bool] = None

    @disnake.ui.button(label="Confirm", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message("Confirming...", ephemeral=True)
        self.value = True
        self.stop()

    @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.grey)
    async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message("Cancelling...", ephemeral=True)
        self.value = False
        self.stop()

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def slowmode(
      self, 
      inter: disnake.GuildCommandInteraction, 
      channel: Union[disnake.TextChannel, disnake.Thread, disnake.ForumChannel, disnake.VoiceChannel] = None, 
      seconds: int = 0
    ):
        """Sets the slowmode of a channel, to turn it off run the command with no value
        Parameters
        ----------
        channel: The channel to put the slowmode on
        seconds: The amount of time the slowmode should be
        """
        if channel == None:
            channel = inter.channel
        if seconds > 120:
            return await inter.response.send_message("Amount can't be over 120 seconds", ephemeral=True)
          
        if seconds == 0:
            await channel.edit(slowmode_delay=seconds, reason=f"Slowmode command ran by {inter.author.name}")
            embed = disnake.Embed(title="Slowmode Off", description=f"Slowmode has been turned off in {channel.mention}", color=await color_check(inter))
            return await inter.response.send_message(embed=embed)
            
        else:
            await channel.edit(slowmode_delay=seconds, reason=f"Slowmode command ran by {inter.author.name}")
            embed = disnake.Embed(title="Slowmode On", description=f"Slowmode has been set to **{seconds} second(s)** in {channel.mention}, to turn this off, run the command without any value", color=await color_check(inter))
            return await inter.response.send_message(embed=embed)


    @commands.slash_command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    async def lock(
      self, 
      inter: disnake.GuildCommandInteraction, 
      channel: Union[disnake.TextChannel, disnake.Thread, disnake.ForumChannel, disnake.StageChannel, disnake.VoiceChannel, disnake.Thread] = None
    ):
        """Locks a channel, to unlock a channel run the command with no value
        Parameters
        ----------
        channel: The channel to lock or unlock    
        """
      
        channel = channel or inter.channel
      
        if inter.guild.default_role not in channel.overwrites:
            overwrites = {
                inter.guild.default_role: disnake.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites, reason=f"Lock command ran by {inter.author}")
            embed = disnake.Embed(title='Channel Locked', description=f"{channel.mention} has been locked", color=await color_check(inter))
            await inter.response.send_message(embed=embed)
    
        elif channel.overwrites[inter.guild.default_role].send_messages == True or channel.overwrites[inter.guild.default_role].send_messages == None:
          overwrites = channel.overwrites[inter.guild.default_role]
          overwrites.send_messages = False
          await channel.set_permissions(inter.guild.default_role, overwrite=overwrites, reason=f"Lock command ran by {inter.author}")
          embed = disnake.Embed(title='Channel Locked', description=f"{channel.mention} has been locked", color=await color_check(inter))
          await inter.response.send_message(embed=embed)   
    
        else:
          overwrites = channel.overwrites[inter.guild.default_role]
          overwrites.send_messages = True
          await channel.set_permissions(inter.guild.default_role, overwrite=overwrites, reason=f"Lock command ran by {inter.author}")
          embed = disnake.Embed(title='Channel Unlocked', description=f"{channel.mention} has been unlocked", color=await color_check(inter))
          await inter.response.send_message(embed=embed)


    @commands.slash_command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clearall(
      self, 
      inter: disnake.GuildCommandInteraction, 
      channel: Union[disnake.TextChannel, disnake.Thread, disnake.ForumChannel, disnake.StageChannel, disnake.VoiceChannel, disnake.Thread] = None
    ):  
          """Clears all the messages in a channel
          Parameters
          ----------
          channel: The channel to *nuke*   
          """  
        
          if channel == None:
            channel = inter.channel

          view = Confirm()
          confirm_message = await inter.channel.send(f"Are you sure you want to do this? This will delete **all** message in {channel.mention}", view=view)
          await view.wait()
      
          if view.value is None:
              return await confirm_message.edit("Timed out", ephemeral=True)
          if not view.value:  
              return await confirm_message.edit("Cancelled", ephemeral=True) 
            
          channel_name = f'{channel.name}'
          overwritess = channel.overwrites
          category = channel.category
          position = channel.position
          
          try:
            await channel.delete()
          except disnake.HTTPException:
            return await inter.response.send_message(f"Error with deleting the channel possible issues:\n1. {channel.mention} is a community channel (which aren't allow to be deleted)")
          new_channel = await inter.guild.create_text_channel(name=channel_name, overwrites=overwritess, category=category, position=position, reason=f"Clearall command ran by {inter.author}")
           
          embed = disnake.Embed(title='Channel Nuked', description=f"**{channel_name}** has been nuked, this message will disappear in 3 seconds", color=await color_check(inter))
          await new_channel.send(embed=embed, delete_after=3)
       



    @commands.slash_command()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter: disnake.GuildCommandInteraction, amount: int, member: disnake.Member = None):   
        """Clears messages in a channel, won't delete pinned messages
        Parameters
        ----------
        amount: The amount of messages to delete  
        member: Deletes message only from this person
        """
        if member == None:
          def purgecheck(m):
            return not m.pinned
          await inter.channel.purge(limit=amount + 1, check=purgecheck)
          embed = disnake.Embed(title='Messages Purged', description=f"**{amount}** messages have been deleted, This message will disappear in 3 seconds", color=await color_check(inter))
          await inter.response.send_message(embed=embed, delete_after=3)
      
        else:
          def is_user(m):
            return m.author == member
          await inter.channel.purge(limit=amount + 1, check=is_user)
          embed = disnake.Embed(title='Messages Purged', description=f"**{amount}** messages from {member.mention} have been deleted, This message will disappear in 3 seconds", color=await color_check(inter))
          await inter.response.send_message(embed=embed, delete_after=3)

def setup(bot):
    bot.add_cog(ModerationCommands(bot))