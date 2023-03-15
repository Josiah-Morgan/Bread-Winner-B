import disnake
from disnake.ext import commands

from utils.database import Database
from utils.tools import list_data, guild_icon_check
from utils.config.config import role_to_low_error, Images, EmojisDict

async def on_or_off(inter, table):
    """Checks if a certain transaction is on or off"""
    data = await Database.get_data(table, inter.guild.id)
    if data == 'Off':
        return await inter.edit_original_message("Transactions are off")
    return True  

async def channel_check(inter, table):
    """Checks if you're using a command in the right channel"""
    data = await Database.get_data(table, inter.guild.id)
    if data == 'None':
        return True

    for row in data:
        if int(inter.channel.id) == int(row):
            return True

    return await list_data(inter, table)      

async def has_role(table, inter, member, role_id=None):
    data = await Database.get_data(table, inter.guild.id)
    if data == 'None':
        return False

    for row in data:
      for role in member.roles:
        if int(role.id) == int(row):
          if role_id == 'id':
            return int(role.id)
          else:  
            return True
            
    return False

async def has_perms(role): # For roles with perms,
  if role.permissions.administrator or role.permissions.ban_members or role.permissions.kick_members or role.permissions.manage_emojis or role.permissions.manage_guild or role.permissions.manage_nicknames or role.permissions.moderate_members or role.permissions.manage_channels: 
    return True
  else:
    return False  

async def transaction_checks(inter, member, role):
    """Checks that all transaction commands use"""
    coach_role_check = await has_role('FranchiseRole', inter, inter.author)
    if not coach_role_check:
        return await inter.edit_original_message("You're not a coach") 
    if role not in inter.author.roles:  
        return await inter.edit_original_message(f"You're not on the `{role.name}`")
    if inter.author.id == member.id:
        return await inter.edit_original_message("You can't do commands on yourself")
    if await has_perms(role):
        return await inter.edit_original_message("To prevent abuse, roles with permissions aren't allowed to be used in signing commands")
    if role > inter.author.top_role:
        return await inter.edit_original_message("To prevent abuse, roles that are higher then your highest role can't be used on the bot")

    return False

async def add_freeagent_roles(inter, member):
    """Adds all the free agent roles you have set"""
    data = await Database.get_data("FreeAgentRole", inter.guild.id)
    if data == 'None':
        return

    for id in data:
        try:
            role = inter.guild.get_role(int(id))
            await member.add_roles(role)
        except disnake.Forbidden:
            return 

async def add_aftersign_roles(inter, member):
    """Adds all the after sign roles you have set"""
    data = await Database.get_data("AfterSignRole", inter.guild.id)
    if data == 'None':
        return

    for id in data:
      try:
        role = inter.guild.get_role(int(id))
        await member.add_roles(role)
      except disnake.Forbidden:
        return 

async def remove_freeagent_roles(inter, member):
    """Removes all the free agent roles you have set"""
    data = await Database.get_data("FreeAgentRole", inter.guild.id)
    if data == 'None':
        return

    for id in data:
      try:
        role = inter.guild.get_role(int(id))
        await member.remove_roles(role)
      except disnake.Forbidden:
        return 

async def remove_aftersign_roles(inter, member):
    """Removes all the after sign roles you have set"""
    data = await Database.get_data("AfterSignRole", inter.guild.id)
    if data == 'None':
        return

    for id in data:
        try:
            role = inter.guild.get_role(int(id))
            await member.remove_roles(role)
        except disnake.Forbidden:
            return 

async def transaction_embed(inter, title, description, color = None):
  #if color == None:
      #color = get_custom_color
  embed = disnake.Embed(
    title=f"{title}",
    description=f"{description}",
    color=color
  )
  image_checkmark = Images.check_mark
  embed.set_thumbnail(url=image_checkmark)

  await inter.edit_original_message(embed=embed)

# Thanks AyoBlue

async def promote_command(inter, member, coach_role):
    author_role_id = await has_role('FranchiseRole', inter, inter.author, 'id')
    author_coach_role = inter.guild.get_role(int(author_role_id))

    coach_roles = await Database.get_data('FranchiseRole', inter.guild.id)
    for ref in coach_roles:
      if int(ref) == int(coach_role):
        member_coach_role = inter.guild.get_role(int(ref))
        break
    try:
        if author_coach_role.position > member_coach_role.position:
          return True, member_coach_role
          
        if author_coach_role.position == member_coach_role.position:
            return False, "You're role is not high enough (You have the same role position)"
          
        if author_coach_role.position < member_coach_role.position:
            return False, f"**You're role is not high enough**\n{member_coach_role} <- His role\n{author_coach_role} <- You're role"
    except UnboundLocalError:
        return False, 'That role is not in the database'

async def demote_command(inter, member):
    member_coach = await has_role("FranchiseRole", inter, member)
    if member_coach:
        member_coach_id = await has_role("FranchiseRole", inter, member, "id")
        member_coach_role = inter.guild.get_role(int(member_coach_id))

        author_coach_id = await has_role("FranchiseRole", inter, inter.author, "id")
        author_coach_role = inter.guild.get_role(int(author_coach_id))

    else:
        return False, f"{member.display_name} is not even a coach BOZO"

    if author_coach_role.position > member_coach_role.position:
        return True, member_coach_role
      
    if author_coach_role.position == member_coach_role.position:
        return False, "You're role is not high enough (You have the same role position)"
      
    if author_coach_role.position < member_coach_role.position:
        return False, f"**You're role is not high enough**\n{member_coach_role} <- His role\n{author_coach_role} <- You're role"

class DemoteThenRelease(disnake.ui.View):
    def __init__(self, inter, member, team_role, coach_role):
        super().__init__()
        self.inter = inter
        self.member = member
        self.team_role = team_role
        self.coach_role = coach_role

    async def interaction_check(self, inter) -> None:
        return inter.author.id == self.inter.author.id

    @disnake.ui.button(label="Demote then release?")
    async def button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
      await inter.response.defer()
      await self.member.remove_roles(self.coach_role)
      await self.member.remove_roles(self.team_role)

        
      await transaction_embed(
          inter, 
          "Transaction Complete", 
          f"{self.member.display_name} ({self.member.mention}) has been **demoted and released** from the {self.team_role.mention}\n > **Coach:** {self.inter.author.mention}", 
          self.team_role.color
      ) 
      await inter.message.edit(view=None)

class OfferButtons(disnake.ui.View):
    def __init__(self, inter, member, role):
        super().__init__(timeout=870) # max is 15 minutes that it can last, 870
        self.inter = inter
        self.member = member
        self.role = role
      
    async def interaction_check(self, inter) -> None:
        return inter.author.id == self.member.id

    async def on_timeout(self) -> None:
        embed = disnake.Embed(
          title = 'Offer Timeout', 
          description = f'The {self.role.mention} offer for {self.member.display_name} ({self.member.mention}) has timed out\n> **Coach:** {self.inter.author.mention}', 
          color = 0xFFFF00
        )
        x = await self.inter.original_message()
        await x.edit(view=None, embed=embed)
 
    @disnake.ui.button(
      label="Accept", 
      emoji=EmojisDict.MEDIA_EMOJIS["Check Mark"], 
      style=disnake.ButtonStyle.green
    )
    async def accept_button(self, button: disnake.ui.Button, inter):
      
        try:
            await self.member.add_roles(self.role)
            await remove_freeagent_roles(self.inter, self.member)
            await add_aftersign_roles(self.inter, self.member)    
        except disnake.Forbidden:
            await inter.send(role_to_low_error) 


        await transaction_embed(
            self.inter, 
            "Offer Accepted", 
            f"{self.member.display_name} ({self.member.mention}) has **accepeted** the {self.role.mention} offer\n > **Coach:** {self.inter.author.mention}", 
            color = 0x008000
        ) 
        await inter.message.edit(view=None)
        self.stop()

    @disnake.ui.button(
      label="Decline", 
      emoji=EmojisDict.MEDIA_EMOJIS["XMark"], 
      style=disnake.ButtonStyle.red
    )
    async def decline_button(self, button: disnake.ui.Button, inter):
      
        embed = disnake.Embed(
          title = 'Offer Declined', 
          description = f'{self.member.display_name} ({self.member.mention}) has **declined** {self.role.mention} offer\n > **Coach:** {self.inter.author.mention}', 
          color = 0xFF0000
        )
        await inter.message.edit(embed=embed, view=None)
        self.stop()

class SigningCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def sign(self, inter: disnake.GuildCommandInteraction, member: disnake.Member, team: disnake.Role):
        """
        Sign a player to your team
        Parameters
        ----------
        member: The player to sign
        team: The team to sign the player to
        """      
        await inter.response.defer()
        role = team

        on_or_off_ = await on_or_off(inter, 'Signing')
        if on_or_off_ == 'Off':
            return await inter.edit_original_message(on_or_off)

        channel_check_ = await channel_check(inter, 'SigningChannel')
        if channel_check_ != True:
            return await inter.edit_original_message(f"You can't do that command here, try doing it in: {channel_check_}")

        if role in member.roles:
            return await inter.edit_original_message(f"**{member.display_name}** is already signed to the `{role}`")
          
        command_checks = await transaction_checks(inter, member, role)
        if not command_checks:
            try:
                await member.add_roles(role)
                await remove_freeagent_roles(inter, member)
                await add_aftersign_roles(inter, member)
            except disnake.Forbidden:
                await inter.send(role_to_low_error)
      
            return await transaction_embed(inter, "Transaction Complete", f"The {role.mention} have **signed** {member.display_name} ({member.mention}) \n > **Coach:** {inter.author.mention}", role.color)       

    @commands.slash_command()
    async def release(self, inter: disnake.GuildCommandInteraction, member: disnake.Member, team: disnake.Role):    
        """
        Release a player from your team
        Parameters
        ----------
        member: The player to release
        team: The team to release the player from
        """  
        await inter.response.defer()
        role = team


        on_or_off_ = await on_or_off(inter, 'Signing')
        if on_or_off_ == 'Off':
            return await inter.edit_original_message(on_or_off)

        channel_check_ = await channel_check(inter, 'SigningChannel')
        if channel_check_ != True:
            return await inter.edit_original_message(f"You can't do that command here, try doing it in: {channel_check_}")

        if role not in member.roles:
            return await inter.edit_original_message(f"**{member.display_name}** is not signed to the `{role}`")

        check_coach_member = await has_role('FranchiseRole', inter, member)
        if check_coach_member:
            coach_role_id = await has_role('FranchiseRole', inter, member, 'id')
            coach_role = inter.guild.get_role(int(coach_role_id))
          
            return await inter.edit_original_message(f"{member.display_name} is a coach, you can't release a coach, demote him first", view=DemoteThenRelease(inter, member, role, coach_role))

      
        command_checks = await transaction_checks(inter, member, role)
        if not command_checks:
            try:
                await member.remove_roles(role)
                await add_freeagent_roles(inter, member)
                await remove_aftersign_roles(inter, member)
            except disnake.Forbidden:
                await inter.send(role_to_low_error)
      
            return await transaction_embed(inter, "Transaction Complete", f"The {role.mention} have **released** {member.mention} \n > **Coach:** {inter.author.mention}", role.color)           


    @commands.slash_command()
    async def offer(self, inter: disnake.GuildCommandInteraction, member: disnake.Member, team: disnake.Role):
        """
        Offer a player to your team
        Parameters
        ----------
        member: The player to offer
        team: The team to offer with
        """  
        await inter.response.defer()
        role = team

        on_or_off_ = await on_or_off(inter, 'Signing')
        if on_or_off_ == 'Off':
            return await inter.edit_original_message(on_or_off)

        channel_check_ = await channel_check(inter, 'OfferingChannel')
        if channel_check_ != True:
            return await inter.edit_original_message(f"You can't do that command here, try doing it in: {channel_check_}")

        if role in member.roles:
            return await inter.edit_original_message(f"**{member.display_name}** is already signed to the `{role}`")
      
        command_checks = await transaction_checks(inter, member, role)
        if not command_checks:

          nick = inter.author.nick
          description = f"**Team:** {role.name}\n**By:** {inter.author.mention} ({nick if nick == None else inter.author.name})\n**Channel Link:** [Link]({inter.channel.jump_url})"
          icon = await guild_icon_check(inter)

          member_embed = disnake.Embed(
            title=f"You have been offered in {inter.guild.name}", 
            description = description,
            color=role.color
          )
          member_embed.set_thumbnail(url=icon)

          guild_embed = disnake.Embed(
            title = "Offer",
            description = f'{member.mention} has been **offered** to join the {role.mention}\n**Coach:** {inter.author.mention}',
            color = role.color
          )

          try:
              await member.send(embed=member_embed)
          except disnake.HTTPException:
              guild_embed.add_field(name="Message Not Send", value=f"\n > Due to {member.display_name} privacy settings, I can't send the message to their DMs")

    
          view = OfferButtons(inter, member, role)
          await inter.send(embed=guild_embed, view=view)

    @commands.slash_command()
    async def demand(self, inter: disnake.GuildCommandInteraction, team: disnake.Role):
        """
        Demand from a team
        Parameters
        ----------
        team: The team to demand from
        """
        await inter.response.defer()
        role = team  

        on_or_off_ = await on_or_off(inter, 'Demands')
        if on_or_off_ == 'Off':
            return await inter.edit_original_message(on_or_off)

        channel_check_ = await channel_check(inter, 'DemandingChannel')
        if channel_check_ != True:
            return await inter.edit_original_message(f"You can't do that command here, try doing it in: {channel_check_}")

        if role not in inter.author.roles:
            return await inter.edit_original_message(f"You're not on the `{role.name}`")
  
        if await has_perms(role):
            return await inter.edit_original_message("To prevent abuse, roles with perms aren't allowed to be used in signing commands")
   
        if role > inter.author.top_role:
            return await inter.edit_original_message("To prevent abuse, roles that are higher then your highest role can't be used on the bot") 

        free_agent_check = await has_role("FreeAgentRole", inter, inter.author)
        if free_agent_check:
            return await inter.edit_original_message("Your a free agent, you = 🐒")  

        coach_check = await has_role("FranchiseRole", inter, inter.author)
        if coach_check:
           return await inter.edit_original_message("Coaches can't demand, get demoted first or released")


        try:
            await inter.author.remove_roles(role)
            await add_freeagent_roles(inter, inter.author)
            await remove_aftersign_roles(inter, inter.author)      
        except disnake.Forbidden:
            await inter.send(role_to_low_error)  

  
        return await transaction_embed(inter, "Demand Complete", f"{inter.author.mention} has **demanded** from the {role.mention}", role.color)


    @commands.slash_command()
    async def promote(self, inter: disnake.GuildCommandInteraction, member: disnake.Member, coach_role: disnake.Role):  
        """
        Promote one of your players to a coach position
        Parameters
        ----------
        member: The player to promote
        coach_role: The coach position to promote your player to
        """
        await inter.response.defer()
        role = coach_role
        
        
        on_or_off_ = await on_or_off(inter, 'Signing')
        if on_or_off_ == 'Off':
            return await inter.edit_original_message(on_or_off)
  
        channel_check_ = await channel_check(inter, 'SigningChannel')
        if channel_check_ != True:
            return await inter.edit_original_message(f"You can't do that command here, try doing it in: {channel_check_}")    

        coach_role_check = await has_role('FranchiseRole', inter, inter.author)
        if not coach_role_check:
            return await inter.edit_original_message("You're not a coach")

        promote = await promote_command(inter, member, role.id)
        if promote[0]:
          try:
            await member.add_roles(promote[1])
          except disnake.Forbidden:
            await inter.send(role_to_low_error)

          return await transaction_embed(inter, "Promotion Complete", f"{member.mention} has been **promoted** to {promote[1].mention}\n > **Coach:** {inter.author.mention}", promote[1].color)
        else:
            return await inter.edit_original_message(promote[1]) 

  
    @commands.slash_command()
    async def demote(self, inter: disnake.GuildCommandInteraction, member: disnake.Member):
          """
          Demote one of your players from a coach position
          Parameters
          ----------
          member: The player to demote
          """
          await inter.response.defer()
      
          on_or_off_ = await on_or_off(inter, 'Signing')
          if on_or_off_ == 'Off':
              return await inter.edit_original_message(on_or_off)
    
          channel_check_ = await channel_check(inter, 'SigningChannel')
          if channel_check_ != True:
              return await inter.edit_original_message(f"You can't do that command here, try doing it in: {channel_check_}")    
  
          coach_role_check = await has_role('FranchiseRole', inter, inter.author)
          if not coach_role_check:
              return await inter.edit_original_message("You're not a coach")

          demote = await demote_command(inter, member)
          if demote[0]:
            try:
                await member.remove_roles(demote[1])
            except disnake.Forbidden:
                await inter.send(role_to_low_error)
      
            return await transaction_embed(inter, "Demotion Complete", f"{member.mention} has been **demoted** from {demote[1].mention}\n > **Coach:** {inter.author.mention}", demote[1].color)
          else:
              return await inter.edit_original_message(demote[1])


def setup(bot):
    bot.add_cog(SigningCommands(bot))