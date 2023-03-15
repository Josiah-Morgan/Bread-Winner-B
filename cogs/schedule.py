import random
from io import BytesIO

import disnake
from disnake.ext import commands

from utils.config.roles import Roles
from utils.tools import get_user_response, vaild_object_check
from utils.config.config import EmojisDict


async def get_custom_teams(self, inter):
    await inter.send("Send your teams", ephemeral=True)
    response = await get_user_response(self, inter)
    if not response:
        return await inter.send(
            "This command has timed out",
            ephemeral=True,
        )

    response_list = response.split(" ")

    teams_list = []

    for item in response_list:
        if vaild_object_check(inter, item):
            role = inter.guild.get_role(int(item))
            teams_list.append(role.mention)
        teams_list.append(item)

    clean_message = ", ".join(teams_list)
    await inter.send(
        f"**{clean_message}** will be used in your schedule",
        ephemeral=True,
        view=TypeOfSchedule(inter, teams_list),
    )


async def apply_schedule_settings(inter, teams_list, schedule_settings):
    settings = schedule_settings

    new_teams_list = []

    if settings.get("mention_roles") == True:
        for role, emoji in teams_list.items():
            grab_role = disnake.utils.get(inter.guild.roles, name=role)
            if grab_role == None:
                new_teams_list.append(role)
            else:
                new_teams_list.append(grab_role.mention)

    if settings.get("emojis") == True:
        if type(teams_list) is not dict:
            new_teams_list = teams_list
        else:

            for role, emoji in teams_list.items():
                new_teams_list.append(f"{emoji} {role}")
    else:
        if type(teams_list) is not dict:
            new_teams_list = teams_list
        else:
            for role, emoji in teams_list.items():
                new_teams_list.append(f"{role}")

    if settings["schedule_type"] == "Random":
        await create_random_schedule_maker(inter, new_teams_list)
    elif settings["schedule_type"] == "Round Robin":
        await create_balanced_round_robin(inter, new_teams_list)


async def schedule_design(inter, teams_list):
    design = f"\n★ ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ★\n{teams_list}\n★ ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ★"

    try:
        await inter.send(design)
        await inter.send(
            content="Try using the `/embed` command to make your schedule look better! (This will be deleted in 5 seconds",
            delete_after=5,
        )
    except disnake.HTTPException:
        await inter.send("Please wait... ", ephemeral=True)
        data = BytesIO(design.encode("utf-8"))
        await inter.send(
            file=disnake.File(data, filename=f"{inter.guild.name}_Schedule.txt")
        )


async def create_random_schedule_maker(
    inter, teams_list
):  # Made by time#2932 (untechno)

    schedule = []

    if (len(teams_list) % 2) == 1:
        teams_list.append("None")
    while len(teams_list) != 0:
        first_team = random.choice(teams_list)
        teams_list.remove(f"{first_team}")
        second_team = random.choice(teams_list)
        teams_list.remove(f"{second_team}")
        schedule.append(f"{first_team} @ {second_team}")

    schedule[0] = " 🔹" + schedule[0]
    design_schedule = "\n 🔹".join([team for team in schedule])
    await schedule_design(inter, design_schedule)


# https://gist.github.com/ih84ds/be485a92f334c293ce4f1c84bfba54c9,
async def create_balanced_round_robin(inter, teams_list):
    """Create a schedule for the players in the list and return it"""
    s = []

    if len(teams_list) % 2 == 1:
        teams_list = teams_list + [None]
    # manipulate map (array of indexes for list) instead of list itself
    # this takes advantage of even/odd indexes to determine home vs. away
    n = len(teams_list)
    map = list(range(n))
    mid = n // 2
    for i in range(n - 1):
        l1 = map[:mid]
        l2 = map[mid:]
        l2.reverse()
        round = []
        for j in range(mid):
            t1 = teams_list[l1[j]]
            t2 = teams_list[l2[j]]
            if j == 0 and i % 2 == 1:
                # flip the first match only, every other round
                # (this is because the first match always involves the last player in the list)
                round.append((t2, t1))
            else:
                round.append((t1, t2))
        s.append(round)
        # rotate list by n/2, leaving last element at the end
        map = map[mid:-1] + map[:mid] + map[-1:]

    schedule = s
    add_teams = "\n".join(
        ["{} vs. {}".format(m[0], m[1]) for round in schedule for m in round]
    )
    await schedule_design(inter, add_teams)


class ScheduleTeamsView(disnake.ui.View):
    def __init__(self, command_self, inter):
        super().__init__()
        self.command_self = command_self
        self.inter = inter

        self.add_item(ScheduleTeams(self.command_self))

    async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        return inter.author.id == self.inter.author.id


class ScheduleTeams(disnake.ui.Select):
    def __init__(self, command_self):
        self.command_self = command_self

        options = [
            disnake.SelectOption(
                label="Custom Teams",
                description="Add your own custom teams",
                emoji=EmojisDict.FCF_EMOJIS["8oki"],
            ),
            disnake.SelectOption(
                label="NFL",
                description="All 32 NFL teams",
                emoji=EmojisDict.NFL_LOGOS_EMOJIS["NFL"],
            ),
            disnake.SelectOption(
                label="MLB",
                description="All 30 MLB teams",
                emoji=EmojisDict.MLB_LOGOS_EMOJIS["MLB"],
            ),
            disnake.SelectOption(
                label="NBA",
                description="All 30 NBA teams",
                emoji=EmojisDict.NBA_LOGOS_EMOJIS["NBA"],
            ),
            disnake.SelectOption(
                label="Football Fusion",
                description="All 32 Football Fusion teams",
                emoji="<:roblox:832715957427765268>",
            ),
            # disnake.SelectOption(
            # label = "MLS", description = "26 MLS teams", emoji = "⚽"
            # ), # add xfl, and other leagues
            disnake.SelectOption(
                label="NHL",
                description="All 32 NHL teams",
                emoji=EmojisDict.NHL_LOGOS_EMOJIS["NHL"],
            ),
            disnake.SelectOption(
                label="College",
                description="College teams",
                emoji=EmojisDict.COLLEGE_LOGOS_EMOJIS["NCAA"],
            ),
        ]

        super().__init__(options=options, placeholder="Pick your teams")

    async def callback(self, inter: disnake.MessageInteraction):
        _message = "What type of schedule?"
        if self.values[0] == "NFL":
            await inter.response.send_message(
                _message, view=TypeOfSchedule(inter, EmojisDict.NFL_EMOJIS)
            )
        elif self.values[0] == "Football Fusion":
            await inter.response.send_message(
                _message, view=TypeOfSchedule(inter, EmojisDict.FOOTBALL_FUSION_EMOJIS)
            )
        elif self.values[0] == "NBA":
            await inter.response.send_message(
                _message, view=TypeOfSchedule(inter, EmojisDict.NBA_EMOJIS)
            )
        elif self.values[0] == "MLB":
            await inter.response.send_message(
                _message, view=TypeOfSchedule(inter, EmojisDict.MLB_EMOJIS)
            )
        elif self.values[0] == "MLS":
            await inter.response.send_message(
                _message, view=TypeOfSchedule(inter, Roles.mls)
            )
        elif self.values[0] == "NHL":
            await inter.response.send_message(
                _message, view=TypeOfSchedule(inter, EmojisDict.NHL_EMOJIS)
            )
        elif self.values[0] == "College":
            await inter.response.send_message(
                _message, view=TypeOfSchedule(inter, EmojisDict.COLLEGE_EMOJIS)
            )
        elif self.values[0] == "Custom Teams":
            await get_custom_teams(self.command_self, inter)


class TypeOfSchedule(disnake.ui.View):
    def __init__(self, inter, teams_list):
        super().__init__()
        self.inter = inter
        self.teams_list = teams_list
        self.schedule_settings = {}

    async def interaction_check(self, inter) -> bool:
        return inter.author.id == self.inter.author.id

    @disnake.ui.button(label="Random")
    async def random_schedule(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.schedule_settings.update({"schedule_type": "Random"})
        await inter.response.send_message(
            "Choose Settings:\n`Note: You aren't able to have 'Emojis' and 'Mention Roles' both on\nNote:  Doing 'Emojis' when using 'Custom Teams' won't work`",
            view=ScheduleSettings(self.inter, self.teams_list, self.schedule_settings),
        )

    @disnake.ui.button(label="Round Robin")
    async def round_robin_schedule(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.schedule_settings.update({"schedule_type": "Round Robin"})
        await inter.response.send_message(
            "Choose Settings:\n`Note: You aren't able to have 'Emojis' and 'Mention Roles' both on\nNote: Doing 'Emojis' when using 'Custom Teams' won't work`",
            view=ScheduleSettings(self.inter, self.teams_list, self.schedule_settings),
        )


class ScheduleSettings(disnake.ui.View):
    def __init__(self, inter, teams_list, schedule_settings):
        super().__init__()
        self.inter = inter
        self.teams_list = teams_list
        self.schedule_settings = schedule_settings

        self.add_emojis_value = None
        self.mention_roles_value = None

    async def interaction_check(self, inter) -> bool:
        return inter.author.id == self.inter.author.id

    @disnake.ui.button(label="Emojis")
    async def add_emojis_button(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        if self.add_emojis_value == None:
            self.schedule_settings.update({"emojis": True})
            self.mention_roles_button.disabled = True
            await inter.response.edit_message(
                content="Emojis will be *tried* to be added your schedule", view=self
            )
            self.add_emojis_value = True

        elif self.add_emojis_value == True:
            self.schedule_settings.pop("emojis")
            self.mention_roles_button.disabled = False
            await inter.response.edit_message(
                content="Emojis will no longer be on your schedule", view=self
            )

    @disnake.ui.button(label="Mention Roles")
    async def mention_roles_button(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        if self.mention_roles_value == None:
            self.schedule_settings.update({"mention_roles": True})
            self.add_emojis_button.disabled = True
            await inter.response.edit_message(
                content="Your role will be *tried* to be mentioned on your schedule",
                view=self,
            )
            self.mention_roles_value = True

        elif self.mention_roles_value == True:
            self.schedule_settings.pop("mention_roles")
            self.add_emojis_button.disabled = False
            await inter.response.edit_message(
                content="Your role will no longer be on your schedule", view=self
            )

    @disnake.ui.button(label="Done", style=disnake.ButtonStyle.green)
    async def done(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await apply_schedule_settings(
            self.inter, self.teams_list, self.schedule_settings
        )

class ScheduleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def schedule(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(
            content="What type of schedule do you want?",
            view=ScheduleTeamsView(self, inter),
        )

def setup(bot):
    bot.add_cog(ScheduleCommand(bot))