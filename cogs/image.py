import disnake, aiohttp, random
from disnake.ext import commands

def get_love_name(user1, user2):
  self_length = len(user1.name)
  first_length = round(self_length / 2)
  first_half = user1.name[0:first_length]
  usr_length = len(user2.name)
  second_length = round(usr_length / 2)
  second_half = user2.name[second_length:]

  finalName = first_half + second_half
  return finalName

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
        async with session.get("https://nezumiyuiz.glitch.me/api/hayasaka") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
  
    @anime.sub_command()
    async def kaguyashinomiya(self, inter):
      """Shows images of kaguyashinomiya"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://nezumiyuiz.glitch.me/api/kaguyashinomiya") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
  
    @anime.sub_command()
    async def megumin(self, inter):
      """Shows images of megumin"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://nezumiyuiz.glitch.me/api/megumin") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
  
    @anime.sub_command()
    async def oyasumi(self, inter):
      """Shows images of oyasumi"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://nezumiyuiz.glitch.me/api/oyasumi") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
  
    @anime.sub_command()
    async def zerotwo(self, inter):
      """Shows images of zerotwo"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://nezumiyuiz.glitch.me/api/zerotwo") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close() 
            
    @anime.sub_command()
    async def rem(self, inter):
      """Shows images of rem"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://nezumiyuiz.glitch.me/api/rem") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
            
    @anime.sub_command()
    async def random(self, inter):
      """Shows random anime images"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://nezumiyuiz.glitch.me/api/random") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
            
    @anime.sub_command()
    async def chika(self, inter):
      """Shows images of chika"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://nezumiyuiz.glitch.me/api/chika") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
            
    @anime.sub_command()
    async def avatars(self, inter):
      """Shows randon anime images that are for profile pictures"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://api.dbot.dev/images/avatars") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
          
    @anime.sub_command()
    async def wallpapers(self, inter):
      """Shows random anime wallpapers"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://api.dbot.dev/images/wallpapers") as resp:
          r = await resp.json()
          await inter.response.send_message(r['url'])
          await session.close()   
  
    
    @commands.slash_command()
    async def foodporn(self, inter):
      """Get some sexy food ;)"""
      async with aiohttp.ClientSession() as session:
        async with session.get("https://foodish-api.herokuapp.com/api/") as resp:
          r = await resp.json()
          await inter.response.send_message(r['image'])
          await session.close()    
  
    # Neko API  
  
    @commands.slash_command()
    async def ship(self, inter, user1: disnake.User, user2: disnake.User = None):
        """
        See how much you love someone
        Parameters
        ----------
        user1: The person to love
        user2: The 2nd person to love (will be you if left empty)
        """
        if user2 == None:
          user2 = inter.author
        
        love_name = get_love_name(user1, user2)
    
        score = random.randint(0, 100)
        filled_progbar = round(score / 100 * 10)
        counter_ = '█' * filled_progbar + '‍ ‍' * (10 - filled_progbar)
        
        embed = disnake.Embed(title=f"{user1.name} ❤ {user2.name}", description=f"**Love %**\n`{counter_}` **{score}%**\n**Love Name** {love_name}", color=0xDEADBF)
    
        await inter.response.send_message(embed=embed)

def setup(bot):
  bot.add_cog(ImageCommands(bot))