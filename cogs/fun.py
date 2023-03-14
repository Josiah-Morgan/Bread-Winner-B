import disnake, random, aiohttp, re
from disnake.ext import commands

class FunCommands(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
  
    @commands.slash_command()
    async def roast(self, inter, name=None):
        """
        Roast your stupid friends ;)
        Parameters
        ----------
        name: The person to roast
        """     
        if name == None: 
            name = inter.author.mention
          
        async with aiohttp.ClientSession() as session:
          async with session.get("https://evilinsult.com/generate_insult.php?lang=en&type=json") as resp:
            r = await resp.json()
            text = r['insult']
    
        embed = disnake.Embed(title="Get Roasted Nerd", description=f"{name}, {text}", color=disnake.Color.random())
        await inter.response.send_message(embed=embed)
        await session.close()
  
    @commands.slash_command()
    async def black(self, inter, name=None):
        """
        See if your black or not
        Parameters
        ----------
        name: The person to find the blackness of
        """ 
        if name == None:
            name = inter.author.mention      
              
        blackness = random.randint(0,100)
    
        embed = disnake.Embed(title="Black Machine", description=f"{name} is **{blackness}%** black", color=0x000000)
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command()
    async def gay(self, inter, name=None):
        """
        Find out if today is the day your friends comeout
        Parameters
        ----------
        name: The person to find the gayness of
        """     
        if name == None:
          name = inter.author.mention      
              
        gayness = random.randint(0,100)
        if gayness == 0:
            gayStatus = random.choice(["100% straight", "No homo", 'Like girls'])
            gayColor = 0xffdae3
        elif gayness <= 33:
            gayStatus = random.choice(["No homo", "Wearing socks", '"Only sometimes"',"Straight-ish", "No homo bro", "Girl-kisser", "Hella straight"])
            gayColor = 0xFFC0CB
        elif 33 < gayness < 66:
            gayStatus = random.choice(["Possible homo", "My gay-sensor is picking something up", "I can't tell if the socks are on or off", "Gay-ish", "Looking a bit homo", "lol half  g a y", "Only a little sus", "safely in between for now", "Only for the homies", "The socks were on"])
            gayColor = 0xFF69B4
        elif gayness == 69:
            gayStatus = 'haha funny number'
            gayColor = 0xFF69B4  
        else:
            gayStatus = random.choice(["LOL YOU GAY XDDD FUNNY", "HOMO ALERT", "MY GAY-SENSOR IS OFF THE CHARTS", "STINKY GAY", "BIG GEAY", "THE SOCKS ARE OFF", "HELLA GAY", "Even the homes don't like it", "FULL HOMO"])
            gayColor = 0xFF00FF
    
        emb = disnake.Embed(description=f"Gayness for **{name}**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
        emb.set_author(name="Gay-Scanner™", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png")
        await inter.response.send_message(embed=emb)
    
    @commands.slash_command(name="8ball")
    async def eightball(self, inter, question):
        """
        Ask this 100% accurate 8ball a question
        Parameters
        ----------
        question: The question to ask the 8ball
        """     
        list_ = ["Hell no","No you idiot", "NO", "Yeah no","lol no","Don't ask stupid questions","\ud83d\ude10","Your weird for asking that","im an 8ball, not a deal with ur crap ball","idc","Don't really care","never dumbass","sure, I literally couldn't care less","Yes","Signs point to yes","Concentrate and ask again","yes???","hell to the yes","heck off, you know that's a no","No, you ape","no lmfao","dont sass me bitch","yes idiot","ask again later when I'm less busy with ur mum","I have better things to do","\ud83d\ude02\ud83e\udd23","no???","maybe","dont count on it","Is this a joke?","get a life","Your weird no","yes!!!","wtf are you asking me","lol literally no","smh fine","Yes (only bc you paid me)","ok, whatever yes","NOOOOOOOOOOOOOOOOOOOOOOOOOOO","YESSSSSSSSSSSSSSSSSS","I'll answer when im done talking with your mum","https://tenor.com/view/boi-what-the-hell-boi-gif-22147158","ok yes","yes cuz your a little bitch","nah your to gay", "Why are you asking me??"]
        if '?' not in question:
          question += "?"
        await inter.response.send_message(f"{question}\n> 🎱 {random.choice(list_)}")
  
    @commands.slash_command() # should make it log big numbers like 100
    async def pp(self, inter, name=None):
        """
        Shows how big your pp is
        Parameters
        ----------
        name: The person to the get pp size of
        """       
        name = name or inter.author.mention
        size = random.randint(1, 16)
        if size == 16:
           size = random.randint(30, 100)
        dong = "=" * size
         
        embed=disnake.Embed(title=f"🍆 pp size 🍆", description=f"**{name}:** 8{dong}D", color=disnake.Color.random())
        embed.set_footer(text=f"{size} inch{' LOL' if size == 1 else 'es'}")
        await inter.response.send_message(embed=embed)
  
    @commands.slash_command()
    async def superbowl(self, inter):
      """The 2023 Superbowl matchup"""
      superbowl_number  = "57"
      NFC = ["<:Washington_Football_Team:802669671919910952>", "<:Tampa_Bay_Buccaneers:802669619398574080>","<:Seattle_Seahawks:802669601834008588>","<:San_Francisco_49ers:802669584108093450>","<:Philadelphia_Eagles:802669338897285121>","<:New_York_Giants:802669514160078888>","<:Los_Angeles_Rams:802669426649858119>","<:New_Orleans_Saints:802669496426823682>","<:Carolina_Panthers:802669215453806632>","<:Green_Bay_Packers:802669356147540009>", "<:Atlanta_Falcons:802669127683538945>","<:Detroit_Lions:802669444299882516>","<:Arizona_Cardinals:802669233204101182>","<:Dallas_Cowboys:802669321167175723>","<:Chicago_Bears:802669145317048351>", "<:Minnesota_Vikings:816493674799824896>"]
  
      AFC = ["<:Tennessee_Titans:802669637024088064>", "<:JacksonvilleJaguarsHelmet:842530820702601278>", "<:Kansas_City_Chiefs:802669409142439986>","<:Pittsburgh_Steelers:802669549094436864>","<:Las_Vegas_Raiders:802669531738538044>","<:Los_Angeles_Chargers:802669268629585961>","<:Miami_Dolphins:802669303631052800>","<:New_England_Patriots:802669461701132358>","<:Indianapolis_Colts:802669286095192104>","<:Buffalo_Bills:802669163159224320>","<:Houston_Texans:802669374003609650>","<:Baltimore_Ravens:802669566542479380>","<:Denver_Broncos:802669180524298240>","<:Cleveland_Browns:802669197921484840>","<:Cincinnati_Bengals:802669250849538061>"]    
      nfc = random.choice(NFC)
      afc = random.choice(AFC)
      score1 = random.choice(["3", "7", "14", "21", "24", "28", "35", "10", "32", "27", "28", "30", "55", "9", "31", "17", "2"])                                       
      score2 = random.choice(["3", "7", "14", "21", "24", "28", "35", "10", "32", "27", "28", "30", "55", "9", "31", "17", "2"]) 
  
      if score1 == score2:
        score2 = "51"
      await inter.response.send_message(f"‎‎‎‎**<:Super_Bowl:834975097806127117> SuperBowl {superbowl_number}**\n\n<:nfc:861994828866781205> {nfc} **{score1}** || **{score2}** <:AFC:858819622400819211>: {afc}")
  
    
    @commands.slash_command(name="1v1")
    async def onevsone(self, inter, member: disnake.Member): 
        """
        Lose in a 1v1 match
        Parameters
        ----------
        member: The person you are going to lose to
        """
        roast = random.choice(["YOU HONESTLY NEED TO STOP PLAYING THIS GAME", "GOD DAM YOU SUCK", "YOU FRICKING SUCK", "BRO EVEN I COULD BEAT YOU", "YOU ARE THE WORSE PLAYER I HAVE EVER SEEN IN MY WHOLE ENTRIE LIFE WHY ARE YOU SO FUCKING BAD OMG PLS GET BETTER IT MAKES ME MAD AND CRINGE HOW DOG SHIT YOU ARE"])
        win = random.choice(["10-1", "10-2", '10-3', '10-4', '10-5', '10-6', '10-7', '10-8', '10-9', '10-0'])     
        WINNER = random.randint(1, 2)
        if win == "10-0":
            win = f"10-0\u200b {roast}"
    
        if WINNER == 1:
            text = f"{inter.author.mention} has won with the score **{win}**"
            color = inter.author.color
        else: # 2
            text = f"{member.mention} has won with the score **{win}**"
            color = member.color
    
        embed = disnake.Embed(title=f"🏈 {inter.author.display_name} **vs** {member.display_name} 🏈", description=text, color=color)
        await inter.response.send_message(embed=embed)
  
    @commands.slash_command()
    async def leaguename(self, inter):
      """Gives you really good names for your league"""
      which = random.randint(1, 2)
      letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      a = random.choice(letters)
      b = random.choice(letters)
      c = random.choice(letters)
      d = random.choice(letters)
      if which == 1:
        await inter.response.send_message(f"Your league name should be **{a}{b}{c}**")
      else:
        await inter.response.send_message(f"Your league name should be **{a}{b}{c}{d}**")
  
    @commands.slash_command()
    async def overall(self, inter, name=None):
        """
        Shows how much of a low overall you are lol
        Parameters
        ----------
        name: The user who has a higher overall then you
        """
        if name is None:
            name = inter.author.mention               
        ps = {
          "legend": ["100", "99", "98", "97", "96", "95"],  
    
          "elite": ["94", '93', '92', '91', '90', '89', '88', '87', '86'],    
    
          "gold": ['85', '84', '83', '82', '81', '80', '79', '78', '77', '76 Your not even a 80 your not good', '75 your ass', '74', '73', '72', '71', '70'],
    
          "copper": ['69 You make this number not funny', '68 😂😂😂', '67', '65 YOUR ASS', '64 YOUR TRASH', '63 https://resize.mut.gg/BjdyS8oS46ZCIHW3vl6o5xYcnmM6-RUZVnFAJQqKaFE/fill/208/356/ce/0/czM6Ly9tZWRpYS5tdXQuZ2cvMjIvbXV0ZGIvcGxheWVyaXRlbS8xMDEyMTkyNi5qcGc YOUR A LOWER OVER THEN THIS NIGGA LMAO', '62', '61 😂😂😂', '60', '59', '58', '57', '56 😂😂😂', '55', '54', '53', '52', '51 Your lucky its not lower', '50 didnt even know you could be this low', '49', '48', '47 YOUR ASS KID', '46 Can you pls get better?', '45 LMAOOOO', '44', '43 Your ass', '42 LMFAO', '41 You should be sad being this low', '40 YOU SUCK', '1 You shitter']
        }
    
        choice = random.choice(random.choice(list(ps.values())))
    
        if choice in ps["copper"]:
            color = disnake.Color(0xb87333)
        elif choice in ps["gold"]:
            color = disnake.Color(0xFFD700)
        elif choice in ps["elite"]:
            color = disnake.Color(0xDC143C)
        elif choice in ps["legend"]:
            color = disnake.Color(0x3498DB)
    
        embed = disnake.Embed(title="Overall", description=f"**{name}**'s overall is **{choice}**", color=color)
        await inter.response.send_message(embed=embed)
    
    @commands.slash_command()
    async def devtrait(self, inter, name: str = None):
        """
        Find out your shitty devtrait you have (ps. its not good)
        Parameters
        ----------
        name: The user to get the devtrait from
        """    
        if name == None:
          name = inter.author.mention
    
        Devstuff_ = random.choice(['Ankle Breaker', 'Bazooka', 'Blitz Radar',' Double Me', 'First One Free', 'Freight Train', 'Gambler', 'Max Security', 'Pro Reads', 'RAC\'em Up', 'Satellite', 'Truzz', 'Wrecking Ball', 'YAC\'em Up', 'Avalanche', 'Blitz', 'Bottleneck', 'Fearmonger', 'Momentum Shift', 'Reinforcement', 'Relentless', 'Run Stuffer', 'Shutdown', 'Unstoppable Force', 'Zone Hawk'])	 	     
    
        YourBad = random.choice(['Your bad', 'You suck', 'Retire now','Did you really think you were going to get a devtrait??', 'LMAOAO YOU SUCK', 'lol try again', 'Stop trying', 'You need to get a LOT better', 'Your fucking shit', 'Watching you play makes me sad', 'Your worse then Joe Flacco', 'You play like your sped', 'You play lego football', 'Your ass kid', 'Stop playing this game', 'I could be your ass', 'Your 1v1 record is 1-50', 'You look like Tom Brady', 'Your a virgin', 'You play for LFG college team', 'You are dreaming that you play in LFG', 'you dick ride main leaguers', 'You have a small dick', 'I could beat you in a 1v1', 'You are the first one out in lob games', 'Your worse then JaMarcus Russell', 'LMAO YOUR SHIT'])
    					            
        ps = {"red": [f"<:SuperStar_X_Factor:850147331864789022> Superstar X Factor\nAbility: {Devstuff_}",],
    
          "gold": ["<:SuperStar_Dev:850147314165481533> Superstar Dev",],            
          "sliver": ["<:Star_Dev:850147296757678120> Star Dev",],
    			"hidden": ['<:Hidden_Dev_Trait:850147349278883840> Hidden Dev Trait'],
          "copper": ["<:Normal_Dev:850147279288401950> Normal Dev",],
          "nodev": [f"No Dev - {YourBad}",],						
          }
        choice = random.choice(random.choice(list(ps.values())))
    
        if choice in ps["copper"]:
          color = disnake.Color(0x9A5D33)       
        elif choice in ps["gold"]:
          color = disnake.Color(0xF8D26D)
        elif choice in ps["red"]:
          color = disnake.Color(0xDC0C10) 
        elif choice in ps["sliver"]:
          color = disnake.Color(0xABACB0)
        elif choice in ps["hidden"]:
          color = disnake.Color(0x418EDF)
        elif choice in ps["nodev"]:
          color = disnake.Color(0x000000)													
    
        embed = disnake.Embed(title="Devtrait", description=f"**{name}**'s devtrait is **{choice}**", color=color)
        await inter.response.send_message(embed=embed)
  
    @commands.slash_command()
    async def age(self, inter, name: str):
        """
        Find out how old you are
        Parameters
        ----------
        name: The name to lookup the age of
        """
      
        x = re.search("<(@!(&!)?|#)[0-9]+>", name)
        if x:
    	    return await inter.response.send_message("You can't ping someone, you have to type in a name (Example: Bob, Jackson, Tom)", ephemeral=True)
  
        async with aiohttp.ClientSession() as session:
          async with session.get(f"https://api.agify.io?name={name}") as resp:
            r = await resp.json()
            embed = disnake.Embed(title=f"⌛ Age Guesser for {r['name']}", color=inter.author.color)
            embed.add_field(name="`Age`:", value=r['age'])
            embed.add_field(name="`People with this name`:", value=r['count'])
            await inter.response.send_message(embed=embed)
            await session.close()
              
def setup(bot):
  bot.add_cog(FunCommands(bot))    