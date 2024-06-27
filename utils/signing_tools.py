import disnake
import unidecode

from utils.config import Links, Keywords, SETTINGS
from utils.database import Database
from utils.embed import Embed
from utils.tools import premium_guild_check, get_mentions, guild_members

async def team_check(guild_id: int, team: disnake.Role):
  """Checks if the role being used is in the teams database"""
  team_data = await Database.get_data("TeamRole", guild_id)
  if not team_data:
    return True
    
  for team_id in team_data:
    if int(team.id) == int(team_id):
      return True
  return False  

async def get_team_owner(guild: disnake.Guild, team: disnake.Role):
  """Find a user with a top FranchiseRole on the team, list[0]"""
  coach_roles = await Database.get_data('FranchiseRole', guild.id)
  if not coach_roles:
    return None

  team_users = await guild_members(guild, team)
  owner_role = coach_roles[0]

  if not owner_role:
     return None
  
  owner_role = guild.get_role(int(owner_role))

  for user in team_users:
    if owner_role in user.roles:
       return user
  return None

async def send_notfication_channel(guild: disnake.Guild, embed: disnake.Embed, content: str = None):
  channel_ids = await Database.get_data("NotficationChannel", guild.id)
  if not channel_ids:
    return
    
  for channel_id in channel_ids:
        channel = guild.get_channel_or_thread(int(channel_id))
        await channel.send(embed=embed, content=content, allowed_mentions=disnake.AllowedMentions.all())


async def roster_cap(guild: disnake.Guild, team: disnake.Role, add_amount: int = 0):
  """
  Checks if your under the league's roster cap
  add_amount: Checking if multiple users can fix the cap, like for trading 
  """
  cap = await Database.get_data('RosterCap', guild.id)
  if not cap:
      return True, f'[No roster cap set]({Links.premium_link})'

  current_cap = len(await guild_members(guild, team)) + add_amount
  #current_cap = sum(1 for member in await guild.chunk() if team in member.roles)

  if current_cap >= int(cap):
      return False, f'The {team.name} are currently at or over the roster cap ({current_cap}/{cap})'
  return True, f'{current_cap}/{cap}'


async def under_contract(guild: disnake.Guild, member: disnake.Member):
  contract = await Database.get_data('Users', guild.id)
  if not contract:
    return False, 'No contract data'
  
  for user_id, user_data in contract.items():
    if str(member.id) in user_id:
      if "contract" in user_data:
        return True, f"{member.display_name} is currently under contract, a DM is being sent to see if they want to terminate the contract \n **Contract Details:** {user_data['contract']}"
  return False, f'{member.display_name} not on a contract'


async def suspension_check(guild_id, member: disnake.Member):
  """Checks if a user is suspeneded"""
  data = await Database.get_data("Suspensions", guild_id)
  if not data:
    return False, 'No suspension data'
    
  for user_id, user_data in data.items():
    # setting where they can make it where suspeneded peoeple can be signed
    if str(user_id) == str(member.id):
      return True, f"**{member.display_name}** is suspended and can't be signed till: `{user_data['duration']}`"  
  return False, f'{member.display_name} is not suspended'  


async def demand_limit_check(guild_id, member):
  demand_limit = await Database.get_data('DemandLimit', guild_id)
  if not demand_limit:
    return True, f'[No demand limit set]({Links.premium_link})' 

  # 10
  user_demands = await Database.get_data("Users", f'{guild_id}/{member.id}/demands')
  if not user_demands:
    return True, 'Able to demand'

  if int(demand_limit) <= int(user_demands):
    return False, f'Unable to demand, you have already used all your demands (demand limit: {demand_limit})'
  return True, 'Able to demand'

# Rings
# Logs?
async def auto_setup(guild):
    embed = Embed(
        title = "Signing System has been Automatically Setup!",
        description = "See the more settings with `/setup` or use `/helpsigning` for help",
    )

    for name, keywords in [
        ("Franchise Role", Keywords.FRANCHISE_ROLES_KEYWORDS),
        ("Free Agent Role", Keywords.FREE_AGENT_ROLES_KEYWORDS),
        ('Team Role', Keywords.TEAM_ROLES_KEYWORDS),
        ("Suspension Role", Keywords.SUSPENED_ROLES_KEYWORDS),
        ("Signing Channel", Keywords.TRANSACTION_CHANNELS_KEYWORDS),
        ("Offering Channel", Keywords.OFFER_CHANNELS_KEYWORDS),
        ("Demanding Channel", Keywords.DEMAND_CHANNELS_KEYWORDS)
    ]:
        
        max_limit = SETTINGS[name].get('max')
        ids = [
            str(item.id)
            for item in (guild.roles if "Role" in name else guild.channels)
            if any(keyword.lower() in unidecode.unidecode(item.name).lower() for keyword in keywords)
        ][:max_limit]
        if ids:
            premium_setting = SETTINGS[name].get("premium")
            if premium_setting:
              p_check = await premium_guild_check(guild.id)
              if not p_check:
                continue # consider trying preiume message
                
            table = name.replace(" ", "")
            await Database.add_data(table, {guild.id: ids})
            mentions = await get_mentions(ids, guild)
            embed.add_field(name = name, value = ", ".join(mentions))

    return embed if len(embed.fields) > 0 else None



# make look cooler?
async def auto_add_object(object):
    """PREMIUM: Same as auto_setup but just when a user creates a role or channel"""
    p_check = await premium_guild_check(object.guild.id)
    if not p_check:
      return
  
    embed = Embed(
        title="Role/Channel Added to the Database!",
    )
    embed.set_footer(text="You can remove this with /setup")

    async def check_and_validate_data(current_data, max_limit):
        if current_data and str(object.id) in current_data:
            return None
        if current_data and len(current_data) >= max_limit:
            return None
        return True

    for name, keywords in [
        ("Franchise Role", Keywords.FRANCHISE_ROLES_KEYWORDS),
        ("Free Agent Role", Keywords.FREE_AGENT_ROLES_KEYWORDS),
        ('Team Role', Keywords.TEAM_ROLES_KEYWORDS),
        ("Suspension Role", Keywords.SUSPENED_ROLES_KEYWORDS),
        ("Signing Channel", Keywords.TRANSACTION_CHANNELS_KEYWORDS),
        ("Offering Channel", Keywords.OFFER_CHANNELS_KEYWORDS),
        ("Demanding Channel", Keywords.DEMAND_CHANNELS_KEYWORDS)
    ]:
        table = name.replace(" ", "")
        object_name = [keyword for keyword in keywords if keyword in unidecode.unidecode(object.name).lower()]

        if type(object) == disnake.Role:
            if object_name and 'Role' in table:
                max_limit = SETTINGS[name].get('max')
                current_data = await Database.get_data(table, object.guild.id)
                validation_result = await check_and_validate_data(current_data, max_limit)
                if validation_result is None:
                    return None
                await Database.add_data(table, {object.guild.id: [object.id]})
                embed.add_field(name=name, value=object.mention)
        else:
            if object_name and 'Channel' in table:
                max_limit = SETTINGS[name].get('max')
                current_data = await Database.get_data(table, object.guild.id)
                validation_result = await check_and_validate_data(current_data, max_limit)
                if validation_result is None:
                    return None
                  
                await Database.add_data(table, {object.guild.id: [object.id]})
                embed.add_field(name=name, value=object.mention)

    return embed if len(embed.fields) > 0 else None