import random

import aiohttp
import disnake
from disnake.ext import commands

from utils.embed import Embed


async def get_image_url(session, url):
    async with session.get(url) as resp:
        if resp.status != 200:
            return "Oops, something went wrong..."
        data = await resp.json()
        await session.close()
        return data['url']
    
class ImageCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def anime(self, inter):
    return
  
  @anime.sub_command()
  async def hayasaka(self, inter):
    """Shows images of hayasaka"""
    async with aiohttp.ClientSession() as session:
      url = "https://nezumiyuiz.glitch.me/api/hayasaka"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)
    
  @anime.sub_command()
  async def kaguyashinomiya(self, inter):
    """Shows images of kaguyashinomiya"""
    async with aiohttp.ClientSession() as session:
      url = "https://nezumiyuiz.glitch.me/api/kaguyashinomiya"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)
    
  @anime.sub_command()
  async def megumin(self, inter):
    """Shows images of megumin"""
    async with aiohttp.ClientSession() as session:
      url = "https://nezumiyuiz.glitch.me/api/megumin"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)
    
  @anime.sub_command()
  async def oyasumi(self, inter):
    """Shows images of oyasumi"""
    async with aiohttp.ClientSession() as session:
      url = "https://nezumiyuiz.glitch.me/api/oyasumi"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)
    
  @anime.sub_command()
  async def zerotwo(self, inter):
    """Shows images of zerotwo"""
    async with aiohttp.ClientSession() as session:
      url = "https://nezumiyuiz.glitch.me/api/zerotwo"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)
    
  @anime.sub_command()
  async def rem(self, inter):
    """Shows images of rem"""
    async with aiohttp.ClientSession() as session:
      url = "https://nezumiyuiz.glitch.me/api/rem"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)
    
  @anime.sub_command()
  async def random(self, inter):
    """Shows random anime images"""
    async with aiohttp.ClientSession() as session:
      url = "https://nezumiyuiz.glitch.me/api/random"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)
    
  @anime.sub_command()
  async def chika(self, inter):
    """Shows images of chika"""
    async with aiohttp.ClientSession() as session:
      url = "https://nezumiyuiz.glitch.me/api/chika"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)  
            
  @anime.sub_command()
  async def avatars(self, inter):
    """Shows randon anime images that are for profile pictures"""
    async with aiohttp.ClientSession() as session:
      url = "https://api.dbot.dev/images/avatars"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)  
      
  @anime.sub_command()
  async def wallpapers(self, inter):
    """Shows random anime wallpapers"""
    async with aiohttp.ClientSession() as session:
      url = "https://api.dbot.dev/images/wallpapers"
      image_url = await get_image_url(session, url)
      await inter.response.send_message(image_url)    
  
      @commands.slash_command()
      async def ship(self, inter, name1: str, name2: str = None):
        """
        See how much you love someone
        Parameters
        ----------
        user1: The person to love
        user2: The 2nd person to love (will be you if left empty)
        """
        if name2 == None:
          name2 = inter.author.display_name
        
        love_name = f"{name1[:len(name1)//2].strip()} {name2[len(name2)//2:].strip()}" 
    
        score = random.randint(0, 100)
        filled_progbar = round(score / 100 * 10)
        counter_ = '█' * filled_progbar + '‍ ‍' * (10 - filled_progbar)
        
        embed = Embed(title=f"{name1} ❤ {name2}", description=f"**Love %**\n`{counter_}` **{score}%**\n**Love Name** {love_name}", color=0xDEADBF)
    
        await inter.response.send_message(embed=embed)

def setup(bot):
  bot.add_cog(ImageCommands(bot))