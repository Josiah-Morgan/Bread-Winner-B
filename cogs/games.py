import disnake, random, asyncio, time
from disnake.ext import commands
from fuzzywuzzy import fuzz

PLAYERLIST = [
        {"name": "Tom Brady", "img": "https://cdn-media.theathletic.com/cdn-cgi/image/fit=cover,width=700,height=466/MqvA2meTsacY_MqvA2meTsacY_lFuCMXGbP7qb_original_1440x959.jpg", "position": "QB"},
        {"name": "JJ Watt", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894762707822198814/image0.jpg", "position": "DE"},
        {"name": "Matthew Stafford", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894762734363746384/image0.jpg", "position": "QB"},
        {"name": "Marshon Lattimore", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894763767961886780/image0.jpg", "position": "CB"},
        {"name": "Justin Jefferson", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894763793664598086/image0.jpg", "position": "WR"},
        {"name": "Hunter Henry", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894764036292481084/image0.jpg", "position": "TE"},
        {"name": "Logan Thomas", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894764496202125352/image0.jpg", "position": "TE"},
        {"name": "Saquon Barkley", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894764746895683584/image0.jpg", "position": "RB"},
        {"name": "David Montgomery", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894764848435581000/image0.jpg", "position": "RB"},
        {"name": "Kenny Golladay", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894764956271124480/image0.jpg", "position": "WR"},           
        {"name": "Marquise Brown", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894765137490247730/image0.jpg", "position": "WR"}, 
        {"name": "Travis Kelce", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894765211721023488/image0.webp", "position": "TE"},
        {"name": "Myles Gaskin", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894765499198615552/image0.jpg", "position": "RB"},
        {"name": "Leonard Fournette", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894765630228688956/image0.jpg", "position": "HB"},
        {"name": "Noah Fant", "img": "https://cdn.discordapp.com/attachments/905215877509709835/988497649843986523/IMG_7501.jpg", "position": "TE"},
        {"name": "Kirk Cousins", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894765851532746793/image0.jpg", "position": "QB"},
        {"name": "Devante Parker", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894765954494529547/image0.jpg", "position": "WR"},
        {"name": "Sammy Watkins", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894766058836213760/image0.jpg", "position": "WR"},
        {"name": "Sony Michel", "img": "https://cdn.discordapp.com/attachments/757043848135311390/987954221460627487/IMG_7481.webp", "position": "HB"},
        {"name": "Julio Jones", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894766485539524618/image0.webp", "position": "WR"},
        {"name": "Michael Gallup", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894766597808488528/image0.jpg", "position": "WR"},
        {"name": "Brandin Cooks", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894766769313574932/image0.jpg", "position": "WR"},
        {"name": "Rob Gronkowski", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894767007877177344/image0.webp", "position": "TE"},
        {"name": "Mac Jones", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894767181018066944/image0.jpg", "position": "QB"},
        {"name": "Derek Carr", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894767363264749618/image0.webp", "position": "QB"},
        {"name": "Aaron Donald", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894767605565521930/image0.jpg", "position": "DT"},
        {"name": "Von Miller", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894767726843789322/image0.webp", "position": "LB"},
        {"name": "Nick Bosa", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894767831143555084/image0.webp", "position": "DE"},
        {"name": "Bill Belichick", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894768242181173308/image0.webp", "position": ":imp:"},
        {"name": "Stefon Diggs", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894768434649391175/image0.jpg", "position": "WR"},
        {"name": "Stephon Gilmore", "img": "https://cdn.discordapp.com/attachments/905215877509709835/989571773492252692/IMG_7508.jpg", "position": "CB"},
        {"name": "Darren Waller", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894769138843672647/image0.jpg", "position": "TE"},
        {"name": "Davante Adams", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894769466016145478/image0.jpg", "position": "WR"},
        {"name": "Alvin Kamara", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894769638104268820/image0.jpg", "position": "HB"},
        {"name": "Derrick Henry", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894769783952789504/image0.webp", "position": "HB"},
        {"name": "Christian McCaffrey", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894769923576987708/image0.jpg", "position": "HB"},         
        {"name": "Baker Mayfield", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894770016375951400/image0.webp", "position": "QB"},
        {"name": "Russell Wilson", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894770179509211156/image0.webp", "position": "QB"},
        {"name": "Matt Ryan", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894770340088143933/image0.jpg", "position": "QB"},
        {"name": "Jalen Hurts", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894770475463499796/image0.jpg", "position": "QB"},
        {"name": "Michael Pittman", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894770599002513489/image0.jpg", "position": "WR"},
        {"name": "Trevor Lawrence", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894770719265800222/image0.webp", "position": "QB"},
        {"name": "Zach Wilson", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894770826358960208/image0.jpg", "position": "QB"}, 
        {"name": "Joe Burrow", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894770927210991736/image0.webp", "position": "QB"},
        {"name": "JuJu Smith Schuster", "img": "https://cdn.discordapp.com/attachments/788201684814790677/988488217252737134/IMG_7497.jpg", "position": "WR"},
        {"name": "Justin Herbert", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894771185504637058/image0.webp", "position": "QB"},
        {"name": "Patrick Mahomes", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894771265607442503/image0.webp", "position": "QB"},
        {"name": "David Andrews", "img": "https://cdn.discordapp.com/attachments/894762229315031090/894771548601319454/image0.jpg", "position": "CENTER"}, 
        {"name": "Richard Sherman", "img": "https://cdn.discordapp.com/attachments/905215877509709835/905215987270430730/IMG_2165.jpg", "position": "CB"},       
        {"name": "Harrison Smith", "img": "https://cdn.discordapp.com/attachments/905215877509709835/905216272428576768/IMG_2166.jpg", "position": "Safety"},
        {"name": "Tim Patrick", "img": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Tim_Patrick_2021_%2851651273250%29_%28cropped%29.jpg", "position": "WR"},
		{"name": "Halapoulivaati Vaitai", "img": "https://cdn.discordapp.com/attachments/788201684814790677/988490333279125674/IMG_7499.webp", "position": "OT"}                                            
      ]  

async def playersearch(a, b):

  ratio = fuzz.ratio(a.lower(), b.lower())
  return ratio


async def challenge_offer(self, inter, user):
  def check(m):
    return (m.author == user) and m.content.lower() == 'yes'
  try:
    msg = await self.bot.wait_for('message', timeout=30, check=check) 
  except asyncio.TimeoutError:
    return await inter.edit_original_message(f"Looks like {user.name} doesn't want to play :frowning:") 
  else:
    return True       




async def standoff_command(self, inter, user):

  choices = ['fire', 'draw', 'shoot', 'bang', 'pull', 'boom', 'blast', 'snipe', 'pop']
  gun = random.choice(choices)
  await inter.send(f"{user.mention} **Do you accept the challenge?** `yes`")  
  
  x = await challenge_offer(self, inter, user)
  if x == True:
      tr = random.randrange(5)
      await inter.followup.send(f"{user.name} **has accepted the challenge**\n**Get Ready, it will start at any moment!**")
      await asyncio.sleep(tr)
      await inter.followup.send(f"**Type** ``{gun}`` **now!**")  

  def check(m):
      return (m.author == inter.author or m.author == user) and m.content.lower() == gun
  try:
      TIME = round(time.time() * 100)
      msg = await self.bot.wait_for('message', timeout=10, check=check)
  except asyncio.TimeoutError:
      pass  
  else:   
      elapse = round(time.time() * 100) - TIME  


      embed = disnake.Embed(title='Fight Ended <:gun2:864896094826790923>', description=f"**{msg.author.mention} has won the fight**\n**Time:** {elapse}ms ({elapse/1000} seconds)", color=msg.author.color)   
      await inter.followup.send(embed=embed) 


class ClickButton(disnake.ui.Button):

    def __init__(self, **kwargs):
        super().__init__(label="Click!", **kwargs)

    async def callback(self, inter: disnake.MessageInteraction):
      embed = disnake.Embed(title="Winner!!🏆🥇", description=f"{inter.author.name} has won", color=inter.author.color)
      await inter.response.send_message(embed=embed)
      self.view.stop()


class DontClickButton(disnake.ui.Button):

    def __init__(self, **kwargs):
        super().__init__(label="Don't Click!", **kwargs)

    async def callback(self, inter: disnake.MessageInteraction):
      await inter.response.send_message("Wrong button fool", ephemeral=True)


class ClickView(disnake.ui.View):

    def __init__(self, inter, member):
        super().__init__(timeout=10)

        self.inter = inter
        self.member = member

        buttons = [ClickButton] + [DontClickButton] * 2
        random.shuffle(buttons)
        for row, button in enumerate(buttons):
            self.add_item(button(
                row=row,
                style=random.choice([disnake.ButtonStyle.red, disnake.ButtonStyle.green, disnake.ButtonStyle.blurple, disnake.ButtonStyle.grey]),
            ))


    async def interaction_check(self, inter) -> bool:
      return inter.author.id == self.inter.author.id or inter.author.id == self.member.id
          

class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(options=[disnake.Option('user', "The person to play against", required=True, type=disnake.OptionType.user)])
    async def standoff(self, inter: disnake.GuildCommandInteraction, user):
      """Be the the first one to complete a randomly chosen game"""
      await inter.response.defer()
      
      if user.bot:
          return await inter.edit_original_message("Stop trying to fight my people >:( (can't play against bots)")
      if inter.author == user:
          return await inter.edit_original_message("You can't fight yourself, you slowass")  
  
      GAMEPICKER = random.randint(1, 2)
      if GAMEPICKER == 1:
          await standoff_command(self, inter, user)
      elif GAMEPICKER == 2:
          await inter.edit_original_message(f"{user.mention} **Do you accept the challenge?** `yes`")
          x = await challenge_offer(self, inter, user)
          if x == True:
              await inter.edit_original_message(content="Click the Right Button", view=ClickView(inter, user))



  
  
    @commands.slash_command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def guessplayer(self, inter):
      """Try to guess some of the players that beat your favorite team"""
      await inter.response.defer()
      
      player = random.choice(PLAYERLIST)
      
      embed = disnake.Embed(title="What NFL player is this?", description=f"Position: {player['position']}\nYou have 30 seconds to guess the player")
      embed.set_image(url=player['img'])
      await inter.edit_original_message(embed=embed)
    
      def check(m):
        return (m.author == inter.author) #and m.content == Players_['name'] or m.content == Players_['name2']
      try:     
        msg = await self.bot.wait_for('message', timeout=30, check=check)
        x = await playersearch(player['name'], msg.content)
        if x >= 75.0:
          if x == 100:
              text = " **and you got a perfect score**"
          else:
              text = '\u200b'  
  
          embed = disnake.Embed(title="Winner", color=inter.author.color, description=f"You are right, {player['name']} was the answer{text}\n**Guessing Score:** {x}")
          embed.set_thumbnail(url=player['img'])
  
          await inter.edit_original_message(embed=embed) 
          
        else:
            embed = disnake.Embed(title="Loser",color=inter.author.color, description=f"{player['name']} was the right answer L L L\n**Guessing Score:** {x}")
            embed.set_footer(text="You need a 'Guessing Score' of 75 or higher")
            embed.set_thumbnail(url=player['img'])
            await inter.edit_original_message(embed=embed)  
  
      except asyncio.TimeoutError:
          embed = disnake.Embed(title="Loser",color=inter.author.color, description=f"{player['name']} was the right answer L L L")
          embed.set_thumbnail(url=player['img'])
          await inter.edit_original_message(embed=embed)
      

def setup(bot):
  bot.add_cog(GameCommands(bot))