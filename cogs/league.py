import random
import urllib.parse

import disnake
from disnake.ext import commands

from utils.config import SETTINGS, Links, not_premium_message
from utils.database import Database
from utils.embed import Embed
from utils.signing_tools import send_notfication_channel, team_check, under_contract
from utils.tools import (
    format_database_data,
    get_user_response,
    guild_members,
    has_perms,
    has_role,
    premium_guild_check,
    premium_user_check,
    search_role_emoji,
    search_embed_ids,
)

NO_RINGS_ROAST = [
    "Bro has no rings 😂",
    "You have no rings and will never get one",
    "You realy thought you were going to have a ring?",
    "You are to bad to have a ring",
    "You fucking suck bro, why would you have a ring",
    "You have no lego rings, and will never get a wedding ring either. You loser 😂",
    "Maybe try looking for a ring next season. Trash can.",
    "You're not good enough for a ring",
    "You suck bro, you have no rings",
    "You have no rings, and will never have any",
    "Stop wasting your time running this command. You do not have any rings 💀",
    "Bro the only ring you have ever gotten is a Ring Pop. You fatass",
    "Fucking retard you suck at this game and will never get a ring you good for nothing sack of shit",
    "cuh has no rings 👎👎💯💯🔥🔥",
    "No rings? Not surprised",
    "You are beyond trash little bro we all know you do not have any rings",
    "You suck git no rings",
    "Tom Brady has 7 rings, and you have 0",
    "Giveup on all your dreams, you can't even win in lego football. Trash no rings lol 😆😆",
    "Did you really think you had a ring? lmao you're trash kid",
    "Dawg you're not even good at this game. You have no rings and won't ever get one",
    "Little bro you're fucking TRASH LMAO YOU DON'T HAVE ANY RINGS AND I MEAN ZERO RINGS LIKE NOTHING 😂😂",
    "You and I have the same amount of rings, and I have zero rings",
    "You have no rings cuh",
    "Shit can you have no rings",
    "You don't have any rings. Go get some bitches instead",
    "It's ok bro not everyone can get rings. Just try harder and one day you will get one. Nah, just kidding you fucking suck little dude. You won't ever win a ring LOL 😂",
    "How is it even possible to have no rings?",
    "I hope my kids don't grow up to be ringless like you. Loser.",
    "Kid you have zero rings and will never get any",
    "You really wish you had a ring huh? Yeah, you have none lol.",
    "No rings, No bitches, No money, No nothing. You suck at life",
    "if you want a ring. How bout you get good?",
    "Dumbass you don't have a ring",
    "Bro stop asking me if you have a ring. You will never get one df LMAO 💀💀",
    "You're trash kid no rings",
    "https://media.tenor.com/AO_jTkCSPP8AAAAM/itsbare-ring.gif",
]


# admin command
def error_embed(title, description):
    embed = Embed(title, description).danger_embed()
    return embed


user_choices = ["contract", "demands"]

# put in userinfo in pickup host, drafted info
# maybe from preium save how many pickups have happneddddd


async def update_game_embed(bot, inter, message_type):
    await inter.response.defer()
    await inter.send("Send a message", ephemeral=True, delete_after=5)
    response = await get_user_response(bot, inter)
    if not response:
        return await inter.send("Response has timed out", ephemeral=True)

    if message_type == "🎥 Stream Link":
        parsed_url = urllib.parse.urlparse(response)
        if not parsed_url.scheme in ("http", "https"):
            return await inter.send(
                "Make sure you are sending a vaild link, if you don't have a link then use the `Notes` button",
                ephemeral=True,
            )

    embed = inter.message.embeds[0]
    new_desc = (
        embed.description
        + f"\n > **{message_type}:** {response} - `{inter.author.display_name}`"
    )
    setattr(embed, "description", new_desc)  # embed.description = ...
    await inter.edit_original_message(embed=embed)


class LinkButton(disnake.ui.View):
    def __init__(self, button_name, button_url):
        super().__init__(timeout=None)
        self.add_item(disnake.ui.Button(label=button_name, url=button_url, emoji="🔗"))


class GameInformationView(disnake.ui.View):
    def __init__(self, inter):
        super().__init__(timeout=None)
        self.inter = inter

        self.add_item(
            disnake.ui.Button(
                label="Team Thread",
                emoji="🛠️",
                style=disnake.ButtonStyle.green,
                custom_id=f"teamthread-{inter.author.id}",
            )
        )

        self.add_item(
            disnake.ui.Button(
                label="Game Time",
                emoji="⏰",
                style=disnake.ButtonStyle.blurple,
                custom_id=f"gametime-{inter.author.id}",
            )
        )
        self.add_item(
            disnake.ui.Button(
                label="Stream Link",
                emoji="🎥",
                style=disnake.ButtonStyle.blurple,
                custom_id=f"streamlink-{inter.author.id}",
            )
        )

        self.add_item(
            disnake.ui.Button(
                label="Referee",
                emoji="🏁",
                style=disnake.ButtonStyle.blurple,
                custom_id=f"referee-{inter.author.id}",
            )
        )

        self.add_item(
            disnake.ui.Button(
                label="Scores Update",
                emoji="💯",
                style=disnake.ButtonStyle.blurple,
                custom_id=f"scoresupdate-{inter.author.id}",
            )
        )

        self.add_item(
            disnake.ui.Button(
                label="Notes",
                emoji="📝",
                style=disnake.ButtonStyle.blurple,
                custom_id=f"notes-{inter.author.id}",
            )
        )

        self.add_item(
            disnake.ui.Button(
                label="End Game",
                style=disnake.ButtonStyle.red,
                custom_id=f"endgame-{inter.author.id}",
            )
        )


class LeagueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        custom_id = inter.component.custom_id

        try:
            og_author = custom_id.split("-")
            og_author_id = og_author[-1]  # The last part contains the ID

            staff = inter.channel.permissions_for(inter.author).administrator
            author = int(inter.author.id) == int(og_author_id)
        except ValueError:
            return

        if custom_id == f"teamthread-{og_author_id}":
            if not staff or author:
                return await inter.response.send_message(
                    "You do not have access to use this button", ephemeral=True
                )

            roles = await search_embed_ids(
                inter.message.embeds[0].description, "role", inter.guild
            )

            thread_name = " vs ".join([role.name for role in roles])
            try:
                thread = await inter.channel.create_thread(
                    name=thread_name,
                    type=disnake.ChannelType.private_thread,
                    invitable=False,
                )
            except Exception as e:
                return await inter.response.send_message(e, ephemeral=True)

            for role in roles:
                members = await guild_members(inter.guild, role)
                for member in members:
                    await thread.add_user(member)
            await inter.response.send_message(thread.jump_url, ephemeral=True)

        if custom_id == f"gametime-{og_author_id}":
            if staff or author:
                return await update_game_embed(self, inter, "⏰ Game Time")

            coach = await has_role("FranchiseRole", inter.guild.id, inter.author)
            roles = await search_embed_ids(
                inter.message.embeds[0].description, "role", inter.guild
            )
            if coach:
                for role in inter.author.roles:
                    if role in roles:
                        return await update_game_embed(self, inter, "⏰ Game Time")
            return await inter.response.send_message(
                "You do not have access to use this button", ephemeral=True
            )

        if custom_id == f"streamlink-{og_author_id}":
            streamer = await has_role("StreamerRole", inter.guild.id, inter.author)
            if staff or author or streamer:
                return await update_game_embed(self, inter, "🎥 Stream Link")
            return await inter.response.send_message(
                "You do not have access to use this button", ephemeral=True
            )

        if custom_id == f"referee-{og_author_id}":
            streamer = await has_role("RefereeRole", inter.guild.id, inter.author)
            if staff or author or streamer:
                return await update_game_embed(self, inter, "🏁 Referee")
            return await inter.response.send_message(
                "You do not have access to use this button", ephemeral=True
            )

        if custom_id == f"scoresupdate-{og_author_id}":
            if staff or author:
                return await update_game_embed(self, inter, "💯 Score")
            return await inter.response.send_message(
                "You do not have access to use this button", ephemeral=True
            )

        if custom_id == f"notes-{og_author_id}":
            if staff or author:
                return await update_game_embed(self, inter, "📝 Note")
            return await inter.response.send_message(
                "You do not have access to use this button", ephemeral=True
            )

        if custom_id == f"endgame-{og_author_id}":
            if staff or author:
                return await inter.response.edit_message(
                    view=None, content="🎉 Game Over 🎉"
                )
            return await inter.response.send_message(
                "You do not have access to use this button", ephemeral=True
            )

    @commands.slash_command()
    async def gametime(self, inter):
        await inter.response.send_message("Use `/game`", ephemeral=True)

    @commands.slash_command()
    async def game(
        self,
        inter: disnake.GuildCommandInteraction,
        team1: disnake.Role,
        team2: disnake.Role,
    ):
        """
        Show live updates of a game
        Parameters
        ----------
        team1: Team 1
        team2: Team 2
        """
        # send a video link on how to use the command
        icon = inter.guild.icon or inter.guild.me.avatar.url
        coach_avatar = inter.author.display_avatar.url or inter.guild.me.avatar.url
        team1_emoji = await search_role_emoji(inter.guild, team1.name) or ""
        team2_emoji = await search_role_emoji(inter.guild, team2.name) or ""

        embed = Embed(
            title="Game Information",
            description=f"{team1_emoji} {team1.mention} vs {team2_emoji} {team2.mention}",
        )  #   \n > **⏰ Game Time:** {time}
        embed.set_thumbnail(url=icon)
        embed.timestamp = disnake.utils.utcnow()
        embed.set_author(name=f"{inter.guild.name} Transactions", icon_url=icon)
        embed.set_footer(text=f"{inter.author.name}", icon_url=coach_avatar)

        await inter.response.send_message(embed=embed, view=GameInformationView(inter))

    @commands.slash_command()
    async def admin(self, inter: disnake.GuildCommandInteraction):
        return

    @admin.sub_command(name="user-clear")
    async def user_clear(
        self,
        inter,
        table: str = commands.Param(choices=user_choices, default=None),
        member: disnake.Member = None,
    ):
        """
        Clears all the data for users, put no table to remove all user data
        Parameters
        ----------
        table: To remove only one table
        member: Removes the data for only one player
        """
        pc = await premium_guild_check(inter.guild.id)
        if not pc:
            await inter.response.send_message(not_premium_message)

        user_data = await Database.get_data("Users", inter.guild.id)
        if not user_data:
            return await inter.response.send_message(
                "No users have any data", ephemeral=True
            )

        if member:  # test dis
            if table:
                delete = await Database.delete_data(
                    "Users", f"{inter.guild.id}/{str(member.id)}"
                )
                if not delete:
                    return await inter.response.send_message(
                        f"{member.mention} does not have any data", ephemeral=True
                    )
                embed = Embed(
                    title="Player Data Deleted",
                    description=f"{member.mention} {table} data has been deleted",
                    user=inter.author,
                )
                return await inter.response.send_message(embed=embed)
            else:
                delete = await Database.delete_data(
                    "Users", f"{inter.guild.id}/{str(member.id)}/{table}"
                )
                if not delete:
                    return await inter.response.send_message(
                        f"{member.mention} does not have any data", ephemeral=True
                    )
                embed = Embed(
                    title="Player Data Deleted",
                    description=f"{member.mention} {table} data has been deleted",
                    user=inter.author,
                )
                return await inter.response.send_message(embed=embed)
        else:
            if not table:
                delete = await Database.delete_data("Users", f"{inter.guild.id}")
                if not delete:
                    return await inter.response.send_message(
                        "No users currently have any data", ephemeral=True
                    )
                embed = Embed(
                    title="Data Wiped", description="All user data has been removed"
                )
                await inter.response.send_message(embed=embed)
            else:
                data = await Database.get_data("Users", f"{inter.guild.id}")
                for user_id, user_data in data.items():
                    delete = await Database.delete_data(
                        "Users", f"{inter.guild.id}/{str(user_id)}/{table}"
                    )
                    if not delete:
                        return await inter.response.send_message(
                            f"No users currently have any {table} data", ephemeral=True
                        )
                embed = Embed(
                    title="Data Wiped", description=f"All {table} data has been removed"
                )
                await inter.response.send_message(embed=embed)

    # make a command that shows all the current offers and amount ig
    # contract_data = await Database.get_db_key(guild.id, 'Users')
    # contract_len = 0
    # for user_id, user_data in contract_data.items():
    # for data in user_data:
    # if 'contract' in user_data:
    # contract_len  = contract_len + 1
    # embed.add_field(name="Current Contracts", value=f"{contract_len}")

    @commands.slash_command()
    async def userinfo(
        self, inter: disnake.GuildCommandInteraction, user: disnake.Member = None
    ):
        """
        Shows league information about a user
        Paremeters
        ----------
        user: The user to show information about
        """
        guild = inter.guild
        user = user or inter.author
        pl = Links.premium_link

        await inter.response.defer()
        embed = Embed(
            title=f"{user.name} Information", description=f"`ID:` {user.id}", user=user
        )
        embed.set_thumbnail(user.display_avatar)

        # loop through user data
        user_data = await Database.get_data("Users", f"{guild.id}/{user.id}")
        if user_data:
            for key, value in user_data.items():
                embed.add_field(name=key.capitalize(), value=value)

        user_p_check = await premium_user_check(self.bot, user)
        if not user_p_check:
            user_p_check = f"[False]({pl})"
        embed.add_field(name="Preimum User?", value=user_p_check)

        await inter.send(embed=embed)

    # team info

    @commands.slash_command()
    async def leagueinfo(self, inter: disnake.GuildCommandInteraction):
        """
        Shows information about a league
        """
        guild = inter.guild

        await inter.response.defer()
        embed = Embed(
            title=f"{guild.name} Information",
        )
        embed.set_thumbnail(guild.icon)

        p_check = await premium_guild_check(inter.guild.id)
        if not p_check:
            p_check = f"[False]({Links.premium_link})"
        embed.add_field(name="Preimum?", value=p_check)

        roster_cap = await Database.get_data("RosterCap", guild.id)
        if not roster_cap:
            roster_cap = "No roster cap set"
        embed.add_field(name="Roster Cap", value=roster_cap)

        demand_limit = await Database.get_data("DemandLimit", guild.id)
        if not demand_limit:
            demand_limit = "No roster cap set"
        embed.add_field(name="Demand Limit", value=demand_limit)

        suspended_data = await Database.get_data("Suspensions", guild.id)
        if suspended_data:
            suspended_text = []
            for user_id, user_data in suspended_data.items():
                await guild_members(inter.guild)
                user = guild.get_member(int(user_id))
                if user:
                    suspended_text.append(
                        f"{user.mention} - duration: {user_data['duration']}, reason: {user_data['reason']}, bail: {user_data['bail']}"
                    )
                    suspended_field_value = (
                        "\n".join(suspended_text) if suspended_text else "None"
                    )
                    embed.add_field(
                        name="Suspeneded Users", value=suspended_field_value
                    )

        await inter.send(embed=embed)

    @commands.slash_command()
    async def lfp(
        self,
        inter: disnake.ApplicationCommandInteraction,
        team: disnake.Role,
        description: str,
    ):
        """
        Send a message that your are currently looking for players
        Parameters
        ----------
        team: The team looking for players
        description: What the team is looking for
        """
        coach_check = await has_role("FranchiseRole", inter.guild.id, inter.author)
        if not coach_check:
            return await inter.send(
                embed=error_embed(
                    "Not a Coach", "You have to be a coach to use this command"
                ),
                delete_after=10,
            )

        if team not in inter.author.roles:
            return await inter.send(
                embed=error_embed("Not On Team", f"You're not on the `{team.name}`"),
                delete_after=10,
            )

        team_check_ = await team_check(inter.guild.id, team)
        if not team_check_:
            return await inter.send(
                embed=error_embed(
                    "Team Not in Database",
                    f"The `{team}` role is not in the teams database",
                ),
                delete_after=10,
            )

        embed = Embed(
            title="Looking For Player",
            description=f"The {team.mention} are currently looking for players \n > **Description:** {description}\n > **Coach:** {inter.author.mention} `{inter.author.display_name}`",
        )
        await embed.league_embed(user=inter.author, guild=inter.guild, role=team)
        await inter.response.send_message(embed=embed)

    @commands.slash_command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def disband(self, inter: disnake.GuildCommandInteraction, team: disnake.Role):
        """
        Gets rid of all the players and coaches on a team
        Parameters
        ----------
        team: The team to disband
        """
        await inter.response.defer()

        if await has_perms(team):
            return await inter.response.send_message(
                "To prevent abuse, roles with permissions aren't allowed to be used in signing commands",
                ephemeral=True,
            )

        team_check_ = await team_check(inter.guild.id, team)
        if not team_check_:
            return await inter.send(
                embed=error_embed(
                    "Team Not in Database",
                    f"The `{team}` role is not in the teams database()",
                ),
                delete_after=10,
            )

        removed_members = []
        removed_coaches = []
        error_members = []

        members = await guild_members(inter.guild, team)
        for member in members:
            # if team in member.roles:
            try:
                await member.remove_roles(team)
                removed_members.append(member.mention)
            except disnake.Forbidden:
                error_members.append(member.mention)
                continue

            coach_role_check = await has_role("FranchiseRole", inter.guild.id, member)
            if coach_role_check:
                role_id = await has_role("FranchiseRole", inter.guild.id, member, "id")
                coach_role = inter.guild.get_role(int(role_id))
                await member.remove_roles(coach_role)
                removed_coaches.append(f"{member.mention} - {coach_role.mention}")

        if removed_members:
            embed = Embed(
                title="Team Disbanded",
                description=f"The {team.mention} have been disbanded \n > **Command By:** {inter.author.mention} `{inter.author.display_name}`",
            )
            await embed.league_embed(user=inter.author, guild=inter.guild, role=team)
            player_amount = len(removed_members)
            embed.add_field(
                name=f"Players - {player_amount}", value=" ".join(removed_members)
            )

        if removed_coaches:
            embed.add_field(name="Coaches", value="\n".join(removed_coaches))

        if error_members:
            embed.add_field(
                name="I was unable to remove these users roles",
                value="".join(error_members),
            )

        if embed:
            await inter.send(embed=embed)
            await send_notfication_channel(inter.guild, embed)
        else:
            await inter.send("I could find no players on that team", ephemeral=True)

    @commands.slash_command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def swap(
        self,
        inter: disnake.GuildCommandInteraction,
        team1: disnake.Role,
        team2: disnake.Role,
    ):
        """
        Swaps the teams players are on
        Parameters
        ----------
        team1: These players get the role from "team2"
        team2: These players get the role from "team1"
        """
        await inter.response.defer()

        if await has_perms(team1) or await has_perms(team2):
            return await inter.response.send_message(
                "To prevent abuse, roles with permissions aren't allowed to be used in signing commands",
                ephemeral=True,
            )

        good_members_1 = []
        error_members_1 = []

        good_members_2 = []
        error_members_2 = []

        team1_members = await guild_members(inter.guild, team1)
        for member in team1_members:
            try:
                await member.remove_roles(team1)
                await member.add_roles(team2)
                good_members_1.append(member.mention)
            except disnake.Forbidden:
                error_members_1.append(member.mention)
                continue

        team2_members = await guild_members(inter.guild, team2)
        for member in team2_members:
            try:
                await member.remove_roles(team2)
                await member.add_roles(team1)
                good_members_2.append(member.mention)
            except disnake.Forbidden:
                error_members_2.append(member.mention)
                continue

        if good_members_1 and good_members_2:
            # not using embed.league_embed, bc we using 2 emojis and using the emojis in the description
            icon = inter.guild.icon or inter.guild.me.avatar.url
            coach_avatar = inter.author.display_avatar.url or inter.guild.me.avatar.url

            embed = Embed(
                title="Team Swap Results",
                description=f"The {team1.mention} and {team2.mention} have been swapped \n > **Command By:** {inter.author.mention} `{inter.author.display_name}`",
            )
            embed.set_thumbnail(url=icon)
            embed.timestamp = disnake.utils.utcnow()
            embed.set_author(name=f"{inter.guild.name} Transactions", icon_url=icon)
            embed.set_footer(text=f"{inter.author.name}", icon_url=coach_avatar)

            team1_emoji = await search_role_emoji(inter.guild, team1.name) or ""
            team1_players = " ".join(good_members_1)

            team2_emoji = await search_role_emoji(inter.guild, team2.name) or ""
            team2_players = " ".join(good_members_2)

            embed.add_field(
                name="Players",
                value=f"{team1_emoji} {team1.mention}: {team1_players}\n{team2_emoji} {team2.mention}: {team2_players}",
            )

            if error_members_1:
                embed.add_field(
                    name=f"I was unable to switch these players for {team1.name}",
                    value=" ".join(error_members_1),
                    inline=False,
                )
            if error_members_2:
                embed.add_field(
                    name=f"I was unable to switch these players for {team2.name}",
                    value=" ".join(error_members_2),
                    inline=True,
                )

            await inter.send(embed=embed)
            await send_notfication_channel(inter.guild, embed)
        else:
            await inter.send(
                "I could not find players on both those teams", ephemeral=True
            )

    @commands.slash_command()
    async def members(self, inter: disnake.GuildCommandInteraction, role: disnake.Role):
        """Show all the members that have a certain role"""
        await inter.response.defer()

        members_list = []
        coaches_list = []

        members = await guild_members(inter.guild, role)
        for member in members:
            members_list.append(
                f"**{member.display_name}** ({member.mention}, `{member.id}`)"
            )

            coach = await has_role("FranchiseRole", inter.guild.id, member)
            if coach:
                coaches_list.append(f"{member.display_name}")

        embed = Embed(
            title=f"{role} - {len(members)}",
            description="\n".join(members_list),
            color=role.color,
        )
        emoji = await search_role_emoji(inter.guild, role.name) or None
        embed.set_thumbnail(url=emoji.url if emoji else None)

        if coaches_list:
            embed.add_field(name="Coaches", value=", ".join(coaches_list))

        await inter.send(embed=embed)

    # challenge-ruling - your_team, other_team, reason, proof

    @commands.slash_command(name="challenge-play")
    async def challenge_play(
        self,
        inter: disnake.GuildCommandInteraction,
        opposing_team: disnake.Role,
        reason: str,
        proof: disnake.Attachment,
        your_team: disnake.Role = None,
        more_proof1: disnake.Attachment = None,
        more_proof2: disnake.Attachment = None,
    ):
        """
        Challenge a play or ruling
        Parameters
        ----------
        opposing_team: The team you are putting the challenge againsted
        reason: The reason why you are challenging
        proof: The proof that the ruling is wrong
        your_team: If you don't have teams saved, manually put your team
        more_proof1: Extra proof
        more_proof2: Extra proof
        """
        guild = inter.guild
        author = inter.author
        await inter.response.defer(ephemeral=True)

        coach_role_check = await has_role("FranchiseRole", inter.guild.id, inter.author)
        if not coach_role_check:
            return await inter.send(
                "You have to be a coach to use this command", ephemeral=True
            )

        # Checks for author's team role
        db_author_role = await has_role("TeamRole", guild.id, author, "id")
        if db_author_role:
            author_team_role = guild.get_role(int(db_author_role))
        else:
            author_team_role = your_team

        if not author_team_role:
            return await inter.send(
                f"You don't have [team roles saved]({Links.premium_link}), so please use the `your_team` parameter",
                ephemeral=True,
            )

        if opposing_team == author_team_role:
            return await inter.send("You can't challenge with yourself", ephemeral=True)

        if author_team_role not in author.roles:
            return await inter.send(
                f"You are not on the {author_team_role}", ephemeral=True
            )

        db_team_role = await team_check(guild.id, opposing_team)
        if not db_team_role:
            return await inter.send(
                f"{opposing_team.mention} is not in the teams database", ephemeral=True
            )
        
        ref = await Database.get_data('RefereeRole', inter.guild.id)
        if not ref:
            return await inter.send(
                "There is not a referee role, so the command won't work (`/setup roles referee role`)",
                ephemeral=True,
            )

        refs = [
            inter.guild.get_role(int(role_id))
            for role_id in ref
        ]
        refs = [role.mention for role in refs]

        channel = await Database.get_data("RefereeChannel", inter.guild.id)
        if not channel:
            return await inter.send(
                "There is no referee channel, set on with `/setup channels referee channel`",
                ephemeral=True,
            )
        channel = inter.guild.get_channel_or_thread(int(channel[0]))

        team1_emoji = await search_role_emoji(inter.guild, author_team_role.name) or ""
        team2_emoji = await search_role_emoji(inter.guild, opposing_team.name) or ""

        embed = Embed(
            title="Challenge Sent",
            description=f"{team1_emoji} {author_team_role.mention} has challenged {team2_emoji} {opposing_team.mention} \n > **Reason:** {reason} \n > **Challenged By:** {inter.author.mention} `{inter.author.display_name}`",
        ).set_thumbnail(url="https://breadwinner.dev/images/referee_image.png")
        await channel.send(
            embed=embed,
            content=f"{''.join(refs)} \n **Proof:** \n {proof.url} {more_proof1 if more_proof1 else ''}",
            allowed_mentions=disnake.AllowedMentions(roles=True),
        )

        await inter.send(
            f"Your challenge has been sent to {channel.mention}, please wait for a referee response",
            ephemeral=True,
        )

    @commands.slash_command()
    async def referee(
        self,
        inter: disnake.GuildCommandInteraction,
        challenging_team: disnake.Role,
        opposing_team: disnake.Role,
        call_on_the_field: str,
        ruling: str,
    ):
        """
        Make a call on a challenged play
        Parameters
        ----------
        challenging_team: The team that challenged the play
        opposing_team: The other team
        call_on_the_field: The play they were challenging
        ruling: The outcome of the challenge
        """
        await inter.response.defer(ephemeral=True)
        ref = await has_role("RefereeRole", inter.guild.id, inter.author)
        if not ref:
            return await inter.send("You're not a referee little dude", ephemeral=True)

        channel = await Database.get_data("RefereeChannel", inter.guild.id)
        if not channel:
            return await inter.send(
                "There is no referee channel, set on with `/setup channels referee channel`",
                ephemeral=True,
            )
        channel = inter.guild.get_channel_or_thread(int(channel[0]))

        team1_emoji = await search_role_emoji(inter.guild, challenging_team.name) or ""
        team2_emoji = await search_role_emoji(inter.guild, opposing_team.name) or ""

        embed = Embed(
            title="Referee Decision",
            description=f"{team1_emoji} {challenging_team.mention} challenged {team2_emoji} {opposing_team.mention} \n > **Challenged Item:** {call_on_the_field} \n > **Decision:** {ruling} \n > **Referee:** {inter.author.mention} `{inter.author.display_name}`",
        ).set_thumbnail(url="https://breadwinner.dev/images/referee_image")
        await channel.send(
            embed=embed,
            content=f"{challenging_team.mention} {opposing_team.mention}",
            allowed_mentions=disnake.AllowedMentions(roles=True),
        )

        await inter.send(
            f"Your decision has been sent to {channel.mention}", ephemeral=True
        )

    @commands.slash_command()
    async def stream(
        self,
        inter: disnake.GuildCommandInteraction,
        team1: disnake.Role,
        team2: disnake.Role,
        stream_link: str,
    ):
        """
        Annouce a stream
        Parameters
        ----------
        team1: Team 1
        team2: Team 2
        stream_link: Where the stream is happening
        """
        guild = inter.guild
        await inter.response.defer(ephemeral=True)
        streamer = await has_role("StreamerRole", guild.id, inter.author)
        if not streamer:
            await inter.send("You are not a streamer", ephemeral=True)

        channel_ids = await Database.get_data("StreamingChannel", guild.id)
        if not channel_ids:
            channel_ids = [inter.channel.id]

        team1_emoji = await search_role_emoji(inter.guild, team1.name) or ""
        team2_emoji = await search_role_emoji(inter.guild, team2.name) or ""

        embed = Embed(
            title=f"{guild.name} Stream",
            description=f"{team1_emoji} {team1.mention} vs {team2_emoji} {team2.mention} \n > **Streamer:** {inter.author.mention} `{inter.author.display_name}`",
        ).set_thumbnail(guild.icon or None)
        for channel_id in channel_ids:
            channel = guild.get_channel_or_thread(int(channel_id))
            await channel.send(embed=embed, view=LinkButton("Watch", stream_link))
            await inter.send(f"Stream sent to {channel.mention}")

    @commands.slash_command()
    async def ringcheck(
        self, inter: disnake.GuildCommandInteraction, member: disnake.Member = None
    ):
        """
        Show off your rings
        Parameters
        ----------
        member: The member to check for rings
        """
        if not member:
            member = inter.author

        guild = inter.guild
        has_rings = []
        rings = await Database.get_data("RingRole", guild.id)
        if not rings:
            await inter.send("This server has no ring roles set :sob:", ephemeral=True)

        has_rings = [
            guild.get_role(int(role_id))
            for role_id in rings
            if guild.get_role(int(role_id)) in member.roles
        ]

        if not has_rings:
            roast = random.choice(NO_RINGS_ROAST)
            return await inter.send(roast)  # ROAST LIST

        has_rings = [role.mention for role in has_rings]
        embed = Embed(
            title=f"Ring Check - {len(has_rings)}", description=", ".join(has_rings)
        )
        embed.set_author(
            name=member.name,
            icon_url=member.display_avatar.url or None,
            url=Links.premium_link,
        )
        embed.set_thumbnail(url="https://breadwinner.dev/images/ring")
        await inter.send(embed=embed)

    @commands.slash_command()
    async def config(self, inter: disnake.GuildCommandInteraction):
        """Shows the server's current settings"""
        await inter.response.defer()
        guild = inter.guild
        embed = Embed(title="Server Settings")

        for value in SETTINGS.values():
            table = value["table"]
            data = await Database.get_data(table, guild.id)
            if data:
                if isinstance(data, (dict, list)):
                    embed.add_field(
                        name=table,
                        value=await format_database_data(inter, table, guild.id),
                        inline=False,
                    )
                else:
                    embed.add_field(name=table, value=value, inline=False)

        await inter.edit_original_message(embed=embed, content=None)


def setup(bot):
    bot.add_cog(LeagueCommands(bot))