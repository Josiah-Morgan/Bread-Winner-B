import asyncio, re, disnake
from utils.database import Database

def log(message):
    """Custom logger - https://www.geeksforgeeks.org/reading-writing-text-files-python/"""
    file = open("data/logs.log", "a")
    file.write(f"{message} \n")
    file.close()

async def color_check(inter): # for dm commands (and 'Custom Bot' in the future)
  """Can't use 'inter.guild.me.color' in DM commands"""
  if inter.guild:
    return inter.guild.me.color
  else:
    color = 0xFFFFFF 
    #color = await Database.get_config("bot_assets", 'Colors', 'Tan')
    color = int(color, 16) # Thanks AyoBlue
    return color

async def guild_icon_check(inter):
  """If a guild does not have a icon, embed images won't send"""
  if not inter.guild.icon:
    return "https://cdn.discordapp.com/attachments/818647836160819232/903433521434099762/breadwinner_logo_300x300.png" # normal
  else:
    return inter.guild.icon

async def get_user_response(self, inter):
    """Gets a users response"""
    def check(m):
        return (m.author.id == inter.author.id)
    try:
        msg = await self.bot.wait_for("message", timeout=30, check=check)
      
        return msg.content

    except asyncio.TimeoutError:
        return None

async def get_user_response_numbers(self, inter):
    """Gets a users response, but only the numbers"""
    def check(m):
        return (m.author.id == inter.author.id)
    try:
        msg = await self.bot.wait_for("message", timeout=30, check=check)
      
        letter_scrap = re.compile(r'\d+(?:\.\d+)?')
        letter_scrap = letter_scrap.findall(msg.content)

        number = ' '.join(letter_scrap)
        return number

    except asyncio.TimeoutError:
        return None

def vaild_object_check(inter, object):
    """Checks if a user's response is a object (discord role, discord channel, etc.)"""
    CHECK = False
    try:
        item = inter.guild.get_role(object) or inter.guild.get_channel_or_thread(object)
    except ValueError:
        return CHECK

    if item != None: # vaild format
        return item

    return CHECK


async def list_data(inter, table):
    """Shows all the data in a table in a pretty way"""
    data = await Database.get_data(table, inter.guild.id)
    if data == 'None':
        return 'None'

    items = ""
    for id in data:
        role = inter.guild.get_role(int(id))
        channel = inter.guild.get_channel_or_thread(int(id))

        save = channel if role == None else role
        items += f'{save.mention}, '
      
    return f'{items[:-2]}'

async def get_keys():
    keys_ = await Database.keys()
    keys_list = list(keys_.split(" "))
    return keys_list