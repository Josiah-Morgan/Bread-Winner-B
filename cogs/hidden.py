import json

import disnake 
from disnake.ext import commands
import requests

from utils.database import Database
from utils.tools import auto_embed

class HiddenCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

 # async def cog_slash_command_check(self, inter) -> bool:
     # return await inter.bot.is_owner(inter.author)
  
  @commands.slash_command()
  async def data_(self, inter):
    embed = await auto_embed(title="Title balls", description="Balls")
    await inter.response.send_message(embed=embed)
    

  @commands.slash_command()
  async def clear_emoji_names(self, inter):
    for emoji in inter.guild.emojis:
      x = emoji.name
      new = x.replace("BWB_", "")

      xx = "".join(["_" + ch if ch.isupper() else ch for ch in new])    
      
      await emoji.edit(name=xx[1:])
      
    await inter.response.send_message("Done")

    
  @commands.slash_command()
  async def auto_emoji_format(self, inter, channel: disnake.TextChannel):
      """Gets all the emojis in a guild and makes them easy to copy and paste"""
      invite = await channel.create_invite()
      print(invite)
    
      emoji_list = ""
      for emoji in reversed(inter.guild.emojis):
          emoji_list += f'<:{emoji.name}:{emoji.id}>'

      await inter.response.send_message(f"`__**{inter.guild.name} Emojis**__\n{emoji_list}`\nPlay around with the emojis here: <{invite.url}>", delete_after=10)

  @commands.slash_command()
  async def emoji_delete(self, inter):
      for emoji in inter.guild.emojis:
          await emoji.delete()
  
  @commands.slash_command()
  async def auto_emoji_format_json(self, inter, guild_id: int = None):
      """Gets all the emojis in a guild and makes them easy to copy and paste"""
      if guild_id == None:
        guild_id = inter.guild.id
      guild = self.bot.get_guild(guild_id)

      emoji_name_list = []
      emoji_list = []
      for emoji in reversed(guild.emojis):
          x = emoji.name.replace("BWB_", "")
          emoji_name_list.append(x)
          emoji_list.append(f"<:{emoji.name}:{emoji.id}>")
       # https://www.geeksforgeeks.org/how-to-add-values-to-dictionary-in-python/
      thing = dict(zip(emoji_name_list, emoji_list))  

      print(json.dumps(thing))
      
        
      await inter.response.send_message(f"`{emoji_list}`")
    
  @commands.slash_command()
  async def bulk_create_emojis(self, inter, emojis):
      print(emojis)
      for emoji in emojis:
        emoji_image = requests.get(emoji.url)
        
        try:
            await inter.guild.create_custom_emoji(name=emoji.name, image=emoji_image.content)
        except disnake.HTTPException as e:
            return ("An error occurred creating the emoji, your server could of gotten rate limited or another issue has happened. Please try again")
            #log(e)
        except disnake.NotFound as e:
            return (f"The image for {emoji.name} could not be found, please report this to the support server (not your fault)")
            #log(e)
        except disnake.ValueError as e:
            return (f"Wrong image format passed for {emoji.name}, please report this to the support server (not your fault)")
            #log(e)          


def setup(bot):
  bot.add_cog(HiddenCommands(bot))
