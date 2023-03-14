import disnake
from disnake.ext import commands
from utils.tools import color_check
from typing import List

autocomplete_help_message = "That's not a vaild type"

OTHER_COMMANDS = ["Football Fusion", "FCF", "USFL", "XFL"]
async def other_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in OTHER_COMMANDS if string in lang.lower()]


COLLEGE_COMMANDS = ["ACC", "Big 10", "Big 12", "Pac 12", "SEC", "More/Extra"]
async def college_autocomplete(inter, string: str) -> List[str]:
    string = string.lower()
    return [lang for lang in COLLEGE_COMMANDS if string in lang.lower()]


async def roles_space_check(inter, role_guild):
    """Checks if you have enough space in your guild to add the roles"""
    guild_roles = len(inter.guild.roles[1:])

    roles_to_add = len(role_guild.roles)

    space = guild_roles + roles_to_add
    if space > 250:
        return f"You are trying to add {roles_to_add} roles, but you only have {guild_roles} spaces, please delete **{roles_to_add - guild_roles} roles**"


async def add_roles(inter, role_guild):
    """Adds the roles"""
    roles_to_bypass = ["@everyone", "Bread Winner B", "Bread Staff", "Bot"]

    for role in role_guild.roles:
        if role.name not in roles_to_bypass:
            await inter.guild.create_role(name=role.name, color=role.color, hoist=True)


async def roles_command(inter, role_guild):
    "Adds the functions above all together"
    role_space = await roles_space_check(inter, role_guild)
    if role_space:  # not enough space
        await inter.response.send_message(role_space, ephemeral=True)

    await inter.response.defer()
    embed = disnake.Embed(
        title="Trying to make your roles",
        description="Please wait while your roles are trying to be made",
        color=await color_check(inter),
    )
    await inter.edit_original_message(embed=embed)

    await add_roles(inter, role_guild)
    embed = disnake.Embed(
        title="Roles Added",
        description="The roles have been made",
        color=await color_check(inter),
    )
    await inter.edit_original_message(embed=embed)


class RoleCommands_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def roles(self, inter: disnake.GuildCommandInteraction):
        return

    @roles.sub_command()
    async def nfl(self, inter: disnake.GuildCommandInteraction):
        """Adds all 32 NFL teams with colors"""
        guild = self.bot.get_guild(1057136078861123725)
        await roles_command(inter, guild)

    @roles.sub_command()
    async def nba(self, inter: disnake.GuildCommandInteraction):
        """Adds all 32 NBA teams with colors"""
        guild = self.bot.get_guild(1057136573063381043)
        await roles_command(inter, guild)

    @roles.sub_command()
    async def mlb(self, inter: disnake.GuildCommandInteraction):
        """Adds all 30 MLB teams with colors"""
        guild = self.bot.get_guild(1057136476019769475)
        await roles_command(inter, guild)

    @roles.sub_command()
    async def nhl(self, inter: disnake.GuildCommandInteraction):
        """Adds all 32 NHL teams with colors"""
        guild = self.bot.get_guild(1055313505311535205)
        await roles_command(inter, guild)

    @roles.sub_command()
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
        type: The type of roles you want
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
        await roles_command(inter, guild)

    @roles.sub_command()
    async def college(
        self,
        inter,
        type: str = commands.Param(autocomplete=college_autocomplete),
        dash: bool = True,
    ):
        """
        NCAA roles
        Parameters
        ----------
        type: The type of roles you want
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
        await roles_command(inter, guild)  # , color


def setup(bot):
    bot.add_cog(RoleCommands_(bot))