import requests
from typing import List

import disnake
from disnake.ext import commands

from utils.config.config import BotLinks
from utils.config.config import EmojisDict
from utils.tools import color_check


autocomplete_help_message = "That's not a vaild emoji type, see `/emoji` for help"

NFL_COMMANDS = ["Normal", "Neon", "Neon2", "Helmet", "3d", "Logos"]
async def nfl_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in NFL_COMMANDS if string in lang.lower()]


NBA_COMMANDS = ["Teams", "Logos"]
async def nba_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in NBA_COMMANDS if string in lang.lower()]


MLB_COMMANDS = ["Teams", "Logos"]
async def mlb_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in MLB_COMMANDS if string in lang.lower()]


NHL_COMMANDS = ["Teams", "Logos"]
async def nhl_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in NHL_COMMANDS if string in lang.lower()]


OTHER_COMMANDS = ["Football Fusion", "FCF", "USFL", "XFL"]
async def other_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in OTHER_COMMANDS if string in lang.lower()]


COLLEGE_COMMANDS = [
    "ACC",
    "Big 10",
    "Big 12",
    "Pac 12",
    "SEC",
    "More/Extra",
    "Neon ACC",
    "Neon Big 10",
    "Neon Big 12",
    "Neon Pac 12",
    "Neon SEC",
    "Neon More/Extra",
    "Logos",
    "Helmet",
]
async def college_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in COLLEGE_COMMANDS if string in lang.lower()]


MEDIA_COMMANDS = ["Symbol Pack 1", "Symbol Pack 1 Neon", "Media", "Devtraits"]
async def media_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in MEDIA_COMMANDS if string in lang.lower()]


async def emoji_space_check(inter, emoji_guild):
    """Checks if your server has enough emoji spaces to run the command"""
    emoji_count = len([emoji for emoji in inter.guild.emojis if emoji.animated != True])
    emoji_limit = inter.guild.emoji_limit

    current_space = emoji_limit - emoji_count
    if current_space < len(
        emoji_guild.emojis
    ):  # if space emoji is smaller then emoji command
        return f"This command needs {len(emoji_guild.emojis)} emoji spaces and you only have {current_space}, please **delete {len(emoji_guild.emojis) - current_space} emojis**"


async def create_emojis(inter, emoji_guild, dash):
    """Creates the emojis in your server"""

    for emoji in emoji_guild.emojis:
        print(emoji.name)
        emoji_image = requests.get(emoji.url)
        print(emoji_image.url)

        try:
            if dash == False:
                name = emoji.name
                name = name.replace("_", "")
                await inter.guild.create_custom_emoji(
                    name=f"BWB_{name}", image=emoji_image.content
                )
            else:
                await inter.guild.create_custom_emoji(
                    name=f"BWB_{emoji.name}", image=emoji_image.content
                )

        except disnake.HTTPException as e:
            return f"{emoji.name} An error occurred creating the emoji, your server could of gotten rate limited or another issue has happened. Please try again"
            # log(e)
        except disnake.NotFound as e:
            return f"The image for {emoji.name} could not be found, please report this to the support server (not your fault)"
            # log(e)
        except disnake.ValueError as e:
            return f"Wrong image format passed for {emoji.name}, please report this to the support server (not your fault)"
            # log(e)

    return f"Your emojis have been made, {inter.author.mention}"


async def emoji_command(inter, emoji_guild, dash):
    """Adds the 'emoji_space_check' and 'create_emoji' functions together"""
    space_check = await emoji_space_check(inter, emoji_guild)
    if space_check:
        return await inter.response.send_message(space_check, ephemeral=True)

    await inter.response.defer()
    await inter.send("Trying to make your emojis, please wait...")
    x = await create_emojis(inter, emoji_guild, dash)
    await inter.send(f"__**{emoji_guild.name}**__\n{x}")


class EmojiEmbedDropdownView(disnake.ui.View):
    def __init__(self, inter):
        super().__init__()
        self.inter = inter

        self.add_item(EmojiEmbed())

    async def on_timeout(self) -> None:
        await self.inter.edit_original_message(
            view=None,
            content=f"Command has expired, run `/{self.inter.data.name}` to use the command again",
        )

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        return inter.author.id == self.inter.author.id


class EmojiEmbed(disnake.ui.Select):
    """Emoji help menu dropdown view"""

    def __init__(self):
        options = [
            disnake.SelectOption(
                label="NFL",
                description="NFL teams and logos",
                emoji=EmojisDict.NFL_LOGOS_EMOJIS["NFL"],
            ),
            disnake.SelectOption(
                label="NBA",
                description="NBA teams and logos",
                emoji=EmojisDict.NBA_LOGOS_EMOJIS["NBA"],
            ),
            disnake.SelectOption(
                label="MLB",
                description="MLB teams and logos",
                emoji=EmojisDict.MLB_LOGOS_EMOJIS["MLB"],
            ),
            disnake.SelectOption(
                label="NHL",
                description="NHL teams and logos",
                emoji=EmojisDict.NHL_LOGOS_EMOJIS["NHL"],
            ),
            disnake.SelectOption(
                label="College",
                description="College teams and logos",
                emoji=EmojisDict.COLLEGE_LOGOS_EMOJIS["NCAA"],
            ),
            disnake.SelectOption(
                label="Media",
                description="Media things like sponsorships and more",
                emoji=EmojisDict.MEDIA_EMOJIS["Check Mark"],
            ),
            disnake.SelectOption(
                label="Football Fusion/Other",
                description="Other leagues",
                emoji=EmojisDict.FCF_EMOJIS["8oki"],
            ),
        ]

        super().__init__(
            placeholder="Pick the type of emojis you want", options=options
        )

    async def callback_message(inter, emoji_type, image_url):
        embed = disnake.Embed(
            title=f"{emoji_type.upper()} Emojis",
            color=await color_check(inter),
            description=f"Do `/emojis {emoji_type}` <type>, below are the types:",
        )
        embed.set_image(url=image_url)

        return embed

    async def callback(self, inter):
        if self.values[0] == "NFL":
            await inter.response.edit_message(
                embed=await EmojiEmbed.callback_message(
                    inter, "nfl", "https://i.imgur.com/qFSwZSs.png"
                )
            )
        elif self.values[0] == "NBA":
            await inter.response.edit_message(
                embed=await EmojiEmbed.callback_message(
                    inter, "nba", "https://i.imgur.com/jY49QOI.png"
                )
            )
        elif self.values[0] == "MLB":
            await inter.response.edit_message(
                embed=await EmojiEmbed.callback_message(
                    inter, "mlb", "https://i.imgur.com/HuzGp9i.png"
                )
            )
        elif self.values[0] == "NHL":
            await inter.response.edit_message(
                embed=await EmojiEmbed.callback_message(
                    inter, "nhl", "https://i.imgur.com/bdAJWiA.png"
                )
            )
        elif self.values[0] == "College":
            await inter.response.edit_message(
                embed=await EmojiEmbed.callback_message(
                    inter, "college", "https://i.imgur.com/D0q7ujr.png"
                )
            )
        elif self.values[0] == "Media":
            await inter.response.edit_message(
                embed=await EmojiEmbed.callback_message(
                    inter, "media", "https://i.imgur.com/YzBR9AH.png"
                )
            )

        elif self.values[0] == "Football Fusion/Other":
            await inter.response.edit_message(
                embed=await EmojiEmbed.callback_message(
                    inter, "other", "https://i.imgur.com/a89sDF3.png"
                )
            )


class EmojiCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()  # help embed
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def emoji(self, inter: disnake.GuildCommandInteraction):
        """Shows you how to run the emoji commands"""
        link = BotLinks.template_server
        description = f"See all the emojis at once [here]({link})"

        await inter.response.defer()
        await inter.send(content=description, view=EmojiEmbedDropdownView(inter))

    @commands.slash_command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
    async def emojis(self, inter: disnake.GuildCommandInteraction):
        return

    # NFL Emojis

    @emojis.sub_command()
    async def nfl(
        self,
        inter,
        type: str = commands.Param(autocomplete=nfl_autocomplete),
        dash: bool = True,
    ):
        """
        NFL emojis
        Parameters
        ----------
        type: The type of emojis you want
        dash: If you want a dash between words or not (defaults to True)
        """
        option = type

        if option == "Normal":
            guild_id = 1057136078861123725
        elif option == "Neon":
            guild_id = 1057137537656827924
        elif option == "Neon2":
            guild_id = 1057137611040378891
        elif option == "Helmet":
            guild_id = 1057137691621331004
        elif option == "3d":
            guild_id = 1057136419371491428
        elif option == "Logos":
            guild_id = 1057136290044313640
        else:
            return await inter.response.send_message(
                autocomplete_help_message, ephemeral=True
            )

        guild = self.bot.get_guild(guild_id)
        await emoji_command(inter, guild, dash)

    # NBA Emojis

    @emojis.sub_command()
    async def nba(
        self,
        inter,
        type: str = commands.Param(autocomplete=nba_autocomplete),
        dash: bool = True,
    ):
        """
        NBA emojis
        Parameters
        ----------
        type: The type of emojis you want
        dash: If you want a dash between words or not (defaults to True)
        """
        option = type

        if option == "Teams":
            guild_id = 1057136573063381043
        elif option == "Logos":
            guild_id = 1057136623478919238
        else:
            return await inter.response.send_message(
                autocomplete_help_message, ephemeral=True
            )

        guild = self.bot.get_guild(guild_id)
        await emoji_command(inter, guild, dash)

    # MLB Emojis

    @emojis.sub_command()
    async def mlb(
        self,
        inter,
        type: str = commands.Param(autocomplete=mlb_autocomplete),
        dash: bool = True,
    ):
        """
        MLB emojis
        Parameters
        ----------
        type: The type of emojis you want
        dash: If you want a dash between words or not (defaults to True)
        """
        option = type

        if option == "Teams":
            guild_id = 1057136476019769475
        elif option == "Logos":
            guild_id = 1057136517174284438
        else:
            return await inter.response.send_message(
                autocomplete_help_message, ephemeral=True
            )

        guild = self.bot.get_guild(guild_id)
        await emoji_command(inter, guild, dash)

    # NHL Emojis

    @emojis.sub_command()
    async def nhl(
        self,
        inter,
        type: str = commands.Param(autocomplete=nhl_autocomplete),
        dash: bool = True,
    ):
        """
        NHL emojis
        Parameters
        ----------
        type: The type of emojis you want
        dash: If you want a dash between words or not (defaults to True)
        """
        option = type

        if option == "Teams":
            guild_id = 1055313505311535205
        elif option == "Logos":
            guild_id = 1057128362763636899
        else:
            return await inter.response.send_message(
                autocomplete_help_message, ephemeral=True
            )

        guild = self.bot.get_guild(guild_id)
        await emoji_command(inter, guild, dash)

    # Other Leagues, Roblox Emojis

    @emojis.sub_command()
    async def other_leagues(
        self,
        inter,
        type: str = commands.Param(autocomplete=other_autocomplete),
        dash: bool = True,
    ):
        """
        Roblox and other leagues (FCF, USFL, XFL)
        Parameters
        ----------
        type: The type of emojis you want
        dash: If you want a dash between words or not (defaults to True)
        """
        option = type

        if option == "Football Fusion":
            guild_id = 1057137391661490287
        elif option == "FCF":
            guild_id = 1057137891131785327
        elif option == "USFL":
            guild_id = 1057137838149357628
        elif option == "XFL":
            guild_id = 1057137806331359262
        else:
            return await inter.response.send_message(
                autocomplete_help_message, ephemeral=True
            )

        guild = self.bot.get_guild(guild_id)
        await emoji_command(inter, guild, dash)

    # College Emojis

    @emojis.sub_command()
    async def college(
        self,
        inter,
        type: str = commands.Param(autocomplete=college_autocomplete),
        dash: bool = True,
    ):
        """
        NCAA emojis, this command can be confusing check /emoji for help
        Parameters
        ----------
        type: The type of emojis you want
        dash: If you want a dash between words or not (defaults to True)
        """
        option = type
        # Normal
        if option == "ACC":
            guild_id = 1075597096775860244
        elif option == "Big 10":
            guild_id = 1075593576689447007
        elif option == "Big 12":
            guild_id = 1075593621992116284
        elif option == "Pac 12":
            guild_id = 1075594992908763209
        elif option == "SEC":
            guild_id = 1075595045534695424
        elif option == "More/Extra":
            guild_id = 1075972521553317949
        # Neon
        elif option == "Neon ACC":
            guild_id = 1075911596720791632
        elif option == "Neon Big 10":
            guild_id = 1075911742837760183
        elif option == "Neon Big 12":
            guild_id = 1075911781299527712
        elif option == "Neon Pac 12":
            guild_id = 1075919474059923506
        elif option == "Neon SEC":
            guild_id = 1075919528636207114
        elif option == "Neon More/Extra":
            guild_id = 1075971807615656058
        # Other
        elif option == "Helmet":
            guild_id = 1057137773762576476
        elif option == "Logos":
            guild_id = 1057137322916859984
        else:
            return await inter.response.send_message(
                autocomplete_help_message, ephemeral=True
            )

        guild = self.bot.get_guild(guild_id)
        await emoji_command(inter, guild, dash)

    # Media Emojis

    @emojis.sub_command()
    async def media(
        self,
        inter,
        type: str = commands.Param(autocomplete=media_autocomplete),
        dash: bool = True,
    ):
        """
        Emojis used for media like halftime logos and symbols
        Parameters
        ----------
        type: The type of emojis you want
        dash: If you want a dash between words or not (defaults to True)
        """
        option = type

        if option == "Symbol Pack 1":
            guild_id = 1057137422351220827
        elif option == "Symbol Pack 1 Neon":
            guild_id = 1057137456979390526
        elif option == "Media":
            guild_id = 1057137574696714281
        elif option == "Devtraits":
            guild_id = 1057137491292979200
        else:
            return await inter.response.send_message(
                autocomplete_help_message, ephemeral=True
            )

        guild = self.bot.get_guild(guild_id)
        await emoji_command(inter, guild, dash)


def setup(bot):
    bot.add_cog(EmojiCommands(bot))