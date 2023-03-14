import disnake
from disnake.ext import commands
from textwrap import shorten
from utils.tools import color_check
from utils.database import Database

class SnipeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.delsniped = {}
        self.editsniped = {}

    @commands.Cog.listener()
    async def on_message_delete(self, inter):
        try:
            if not inter.author.bot:
              srvid = inter.guild.id
              chid = inter.channel.id
              author_mention = inter.author.mention
              author = inter.author
              content = inter.content
              try:
                attachment_name = inter.attachments[0].filename
                file_attachment = inter.attachments[0].proxy_url
              except IndexError:
                file_attachment = None
                attachment_name = None

              self.delsniped.update({
                srvid : {
                  chid : {
                    'Sender':author,
                    'Mention':author_mention,
                    'Content':content,
                    'Attachment':file_attachment,
                    'Filename':attachment_name
                  }
                }
              })
        except:
          pass
  
        for member in inter.mentions:
          gp_data = await Database.get_data("GhostPings", inter.guild.id)
          if gp_data == 'Off':
            return       
          else:     
            if not inter.author.bot:
                if inter.content == '':
                    content = 'No Message'
                else:
                    content = inter.content  
    
                embed = disnake.Embed(color=inter.author.color, title="<:ghostping:782060673730740275> Ghost Ping Found <:ghostping:782060673730740275>")
                embed.add_field(name="Pinged By", value=inter.author.mention, inline=False)
                embed.add_field(name='Content', value=content, inline=False)
                embed.set_footer(text="To turn this off use /setup")
              
                try:
                    await inter.channel.send(embed=embed)  
                except:
                    return      

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
      try:
          if not before.author.bot:
              srvid = before.guild.id
              chid = before.channel.id
              author = before.author
              author_mention = before.author.mention
              msg_before = before.content
              msg_after = after.content
              self.editsniped.update({
                  srvid : {
                      chid : {
                          'Sender':author,
                          'Mention':author_mention,
                          'Before':msg_before,
                          'After':msg_after
                      }
                  }
              })
      except:
          pass
  
    @commands.slash_command()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def snipe(self, inter: disnake.GuildCommandInteraction):
        """*Snipe* a message that someone deleted"""
        try:
            author = self.delsniped[inter.guild.id][inter.channel.id]["Sender"]
            author_mention = self.delsniped[inter.guild.id][inter.channel.id]["Mention"]
            msg = self.delsniped[inter.guild.id][inter.channel.id]["Content"]
            attachment = self.delsniped[inter.guild.id][inter.channel.id]["Attachment"]
            name = self.delsniped[inter.guild.id][inter.channel.id]["Filename"]
            if len(msg) > 768:
                msg = shorten(msg,width=756,placeholder="...")
      
            embed = disnake.Embed(color=await color_check(inter), title="Message Sniped")
            embed.set_author(name="Sniped!", icon_url=author.display_avatar)
            embed.add_field(name="Author", value=author_mention)
          
            if msg:
                embed.add_field(name="Content", value=msg)
    
            if attachment:
                embed.add_field(name="Attachments",value=f"||[{name}]||({attachment})")
                if str(name).endswith(".png") or str(name).endswith(".gif") or str(name).endswith(".jpg") or str(name).endswith(".mp4"):
                  embed.set_image(url=attachment)
    
            self.delsniped.popitem()
            await inter.response.send_message(embed=embed)
  
        except KeyError:
            embed = disnake.Embed(title="Nothing Found", description="Perhaps you're to slow?")
            return await inter.response.send_message(embed=embed, ephemeral=True)
        except disnake.NotFound:
              pass

    @commands.slash_command()
    @commands.cooldown(2, 5, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def editsnipe(self, inter: disnake.GuildCommandInteraction):
      """*Snipe* a message someone edited"""
      try:
          author = self.editsniped[inter.guild.id][inter.channel.id]["Sender"]
          author_mention = self.editsniped[inter.guild.id][inter.channel.id]["Mention"]
          before = self.editsniped[inter.guild.id][inter.channel.id]["Before"]
          after = self.editsniped[inter.guild.id][inter.channel.id]["After"]
          
          if len(before) > 768:
            shorten(before, width=756,placeholder="...")
    
          if len(after) > 768:
            shorten(after, width=756,placeholder="...")
    
          embed = disnake.Embed(color=await color_check(inter), title="Message Snipged")
          embed.set_author(name="Sniped!", icon_url=author.avatar)
          embed.add_field(name="Author", value=author_mention)
          embed.add_field(name="Before:", value=before)
          embed.add_field(name="After:", value=after)
          await inter.response.send_message(embed=embed)
  
          self.editsniped.popitem()
        
      except KeyError:
          embed = disnake.Embed(title="Nothing Found", description="Perhaps you're to slow?")
          return await inter.response.send_message(embed=embed, ephemeral=True)
      except disnake.NotFound:
          pass

def setup(bot):
    bot.add_cog(SnipeCommands(bot))