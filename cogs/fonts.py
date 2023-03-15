import datetime
import json
from typing import Union, List

import disnake
from disnake.ext import commands, tasks

from utils.database import Database
from utils.tools import color_check

maxtext = 1000
maxtextError = f"Your text has to be under {maxtext} characters"

FONTS = [
    "Ａｅｓｔｈｅｔｉｃ",
    "𝗕𝗼𝗹𝗱",
    "Ⓒⓘⓡⓒⓛⓔ",
    "𝑰𝒕𝒂𝒍𝒊𝒄",
    "𝙄𝙩𝙖𝙡𝙞𝙘𝙗𝙤𝙡𝙙",
    "𝘐𝘵𝘢𝘭𝘪𝘤𝘴𝘢𝘯𝘴",
    "𝖲𝖺𝗇𝗌",
    "𝐒𝐞𝐫𝐢𝐟",
]
async def fonts_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in FONTS if string in lang.lower()]


async def grab_font(font):
    if font in ["Ａｅｓｔｈｅｔｉｃ", "aesthetic"]:
        return "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ１２３４５６７８９0"
    if font in ["𝗕𝗼𝗹𝗱", "bold"]:
        return "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"
    if font in ["Ⓒⓘⓡⓒⓛⓔ", "circle"]:
        return "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ①②③④⑤⑥⑦⑧⑨⓪"
    if font in ["𝑰𝒕𝒂𝒍𝒊𝒄", "italic"]:
        return "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛1234567890"
    if font in ["𝙄𝙩𝙖𝙡𝙞𝙘𝙗𝙤𝙡𝙙", "italicbold"]:
        return "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯1234567890"
    if font in ["𝘐𝘵𝘢𝘭𝘪𝘤𝘴𝘢𝘯𝘴", "italicsans"]:
        return "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻1234567890"
    if font in ["𝖲𝖺𝗇𝗌", "sans"]:
        return "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢"
    if font in ["𝐒𝐞𝐫𝐢𝐟", "serif"]:
        return "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎"


async def font_check(message):
    if len(message) >= maxtext:  # over/is 1000
        return False
    return True


# Ayoblue go brrrr
async def make_font(message, font):
    data = {
        "Regular": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890",
        "Font": font,
    }

    for i in range(0, len(message)):
        if data["Regular"].find(message[i]) != -1:
            message = message.replace(
                message[i], data["Font"][data["Regular"].find(message[i])]
            )

    return message


async def font_command(inter, message, font):
    if await font_check(message):
        font = await grab_font(font)
        text = await make_font(message, font)
        await inter.response.send_message(text)
    else:
        await inter.response.send_message(maxtextError)

class FontCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.font_channel_timer_check.start()

    @tasks.loop(hours=1)
    async def font_channel_timer_check(self):
        await self.bot.wait_until_ready()
      
        try:
          data = await Database.get_all_values("FontChannel")
        except json.decoder.JSONDecodeError:
          return
        for item in data:
            time_obj = datetime.datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S")
            if time_obj < datetime.datetime.now():
                await Database.remove_data("FontChannel", item["channel"])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        data = await Database.get_data("FontChannel", message.channel.id)
        if data == "None":
            return

        if await font_check(message.content):
            for item in data:
                font = await grab_font(f"{item['font']}")
                break

            text = await make_font(message.content, font)
            await message.channel.send(text)

    @commands.slash_command(name="font-channel")
    async def font_channel(
        self,
        inter,
        font: str = commands.Param(autocomplete=fonts_autocomplete),
        channel: Union[disnake.TextChannel, disnake.Thread] = None,
    ):
        """Set a channel that turns all your new messages into a font, does not last forever"""

        # current_font_channels = []
        # for channel in inter.guild.channels:
        # data = await Database.get_data("FontChannel", channel.id)
        # if data != "None":
        # current_font_channels.append(data)

        # if len(current_font_channels) >= 3:
        # return await inter.response.send_message("You can only have up to 3 active font channels", ephemeral=True)

        if channel == None:
            channel = inter.channel

        time_ = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        time_ = time_.strftime("%Y-%m-%d %H:%M:%S")

        embed = disnake.Embed(
            title="Font Channel Set",
            description=f"The channel {channel.mention} (`{channel.name}`) will use the font: {font}",
            color=await color_check(inter),
        )
        embed.set_footer(text=f"Will end at {time_}")

        current_data = await Database.get_data("FontChannel", channel.id)
        if current_data == "None":  # No data, just add
            await Database.add_data_list(
                "FontChannel",
                channel.id,
                {"font": font, "time": time_, "channel": channel.id},
            )
        else:  # has data, replace, only 1 per channel
            await Database.remove_data("FontChannel", channel.id)
            await Database.add_data_list(
                "FontChannel",
                channel.id,
                {"font": font, "time": time_, "channel": channel.id},
            )
            embed.add_field(
                name="Font Channel Replaced",
                value="You can have only one font per-channel, so I have replaced the font you set before",
            )

        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    async def aesthetic(self, inter, sentence: str):
        """
        Ｐｕｔｓ ｙｏｕｒ ｔｅｘｔ ｉｎ ａ ａｅｓｔｈｅｔｉｃ ｆｏｎｔ
        Parameters
        ----------
        sentence: Your text
        """
        await font_command(inter, sentence, "aesthetic")

    @commands.slash_command()
    async def bold(self, inter, sentence: str):
        """
        𝗣𝘂𝘁𝘀 𝘆𝗼𝘂𝗿 𝘁𝗲𝘅𝘁 𝗶𝗻 𝗮 𝗯𝗼𝗹𝗱 𝗳𝗼𝗻𝘁
        Parameters
        ----------
        sentence: Your text
        """
        await font_command(inter, sentence, "bold")

    @commands.slash_command()
    async def circle(self, inter, sentence: str):
        """
        Ⓟⓤⓣⓢ ⓨⓞⓤⓡ ⓣⓔⓧⓣ ⓘⓝ ⓐ ⓑⓘⓖⓒⓘⓡⓒⓛⓔ ⓕⓞⓝⓣ
        Parameters
        ----------
        sentence: Your text
        """
        await font_command(inter, sentence, "circle")

    @commands.slash_command()
    async def italic(self, inter, sentence: str):
        """
        𝑷𝒖𝒕𝒔 𝒚𝒐𝒖𝒓 𝒕𝒆𝒙𝒕 𝒊𝒏 𝒂 𝒊𝒕𝒂𝒍𝒊𝒄 𝒇𝒐𝒏𝒕
        Parameters
        ----------
        sentence: Your text
        """
        await font_command(inter, sentence, "italic")

    @commands.slash_command()
    async def italicbold(self, inter, sentence: str):
        """
        𝙋𝙪𝙩𝙨 𝙮𝙤𝙪𝙧 𝙩𝙚𝙭𝙩 𝙞𝙣 𝙖 𝙞𝙩𝙖𝙡𝙞𝙘𝙗𝙤𝙡𝙙 𝙛𝙤𝙣𝙩
        Parameters
        ----------
        sentence: Your text
        """
        await font_command(inter, sentence, "italicbold")

    @commands.slash_command()
    async def italicsans(self, inter, sentence: str):
        """
        𝘗𝘶𝘵𝘴 𝘺𝘰𝘶𝘳 𝘵𝘦𝘹𝘵 𝘪𝘯 𝘢𝘯 𝘪𝘵𝘢𝘭𝘪𝘤 𝘴𝘢𝘯𝘴 𝘧𝘰𝘯𝘵
        Parameters
        ----------
        sentence: Your text
        """
        await font_command(inter, sentence, "italicsans")

    @commands.slash_command()
    async def sans(self, inter, sentence: str):
        """
        𝖯𝗎𝗍𝗌 𝗒𝗈𝗎𝗋 𝗍𝖾𝗑𝗍 𝗂𝗇 𝖺𝗇 𝗌𝖺𝗇𝗌 𝖿𝗈𝗇𝗍
        Parameters
        ----------
        sentence: Your text
        """
        await font_command(inter, sentence, "sans")

    @commands.slash_command()
    async def serif(self, inter, sentence: str):
        """
        𝐏𝐮𝐭𝐬 𝐲𝐨𝐮𝐫 𝐭𝐞𝐱𝐭 𝐢𝐧 𝐚 𝐬𝐞𝐫𝐢𝐟 𝐟𝐨𝐧𝐭
        Parameters
        ----------
        sentence: Your text
        """
        await font_command(inter, sentence, "serif")


def setup(bot):
    bot.add_cog(FontCommands(bot))