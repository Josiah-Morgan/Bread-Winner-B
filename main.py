import disnake, os, traceback
from disnake.ext import commands

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

class Bread(commands.AutoShardedInteractionBot):
    def __init__(self):
        super().__init__(intents=intents, activity=disnake.Game(name="bed wars | /cmds"), allowed_mentions=disnake.AllowedMentions(roles=False, everyone=False, users=False), chunk_guilds_at_startup = False)  #, test_guilds=[817569246103470110, 1000481119088672898, 1057136078861123725]
        self.bot = self

    async def start(self, *args, **kwargs):

      for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
          self.bot.load_extension(f'cogs.{filename[:-3]}')
          print(filename + ' Loaded')
  
      await super().start(*args)
  
    async def on_ready(self):
      print('Bot Online')

bot = Bread()

@bot.slash_command()
@commands.is_owner()
async def load(inter, cogname: str):
    """
    Loads a cog
    Parameters
    ----------
    cogname: The cog to load
    """
    try:
      bot.load_extension(f"cogs.{cogname}")
    except Exception as e:
      await inter.response.send_message(
        f"```py\n{traceback.format_exc()}\n```\n\n\n, {e}")
    else:
      await inter.response.send_message(
        f":gear: Successfully Loaded **{cogname}** Module!") 

@bot.slash_command()
@commands.is_owner()
async def unload(inter, cogname: str):
    """
    Unloads a cog
    Parameters
    ----------
    cogname: The cog to unload
    """
    try:
      bot.unload_extension(f"cogs.{cogname}")
    except Exception as e:
      await inter.response.send_message(
        f"```py\n{traceback.format_exc()}\n```\n\n\n, {e}")
    else:
      await inter.response.send_message(
        f":gear: Successfully Unloaded **{cogname}** Module!")


@bot.slash_command()
@commands.is_owner()
async def reload(inter, cogname: str):
    """
    Loads and unloads a cog
    Parameters
    ----------
    cogname: The cog to reload
    """
    try:
      bot.unload_extension(f"cogs.{cogname}")
      bot.load_extension(f"cogs.{cogname}")
    except Exception as e:
      await inter.response.send_message(
        f"```py\n{traceback.format_exc()}\n```\n\n\n, {e}")
    else:
      await inter.response.send_message(
        f":gear: Successfully Reloaded the **{cogname}** module!")


bot.run("<bot token>")
