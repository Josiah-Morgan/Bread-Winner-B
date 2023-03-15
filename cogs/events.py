import aiohttp
import json
from time import ctime
import shutil
import os
import unidecode

import disnake
from disnake.ext import commands, tasks
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from utils.database import Database
from utils.config.config import welcome_message, error_support_message
from utils.tools import get_keys


# Thanks AyoBlue
async def auto_add_coach(guild: disnake.Guild):
    for role in guild.roles:
        x = unidecode.unidecode(role.name)
        if x.lower().find("franchise ow") != -1:
            await Database.add_data_list("FranchiseRole", guild.id, role.id)
        elif x.lower().find("general ma") != -1:
            await Database.add_data_list("FranchiseRole", guild.id, role.id)
        elif x.lower().find("head co") != -1:
            await Database.add_data_list("FranchiseRole", guild.id, role.id)
        elif x.lower().find("assistant co") != -1:
            await Database.add_data_list("FranchiseRole", guild.id, role.id)
        elif x.lower().find("free age") != -1:
            await Database.add_data_list("FreeAgentRole", guild.id, role.id)


async def auto_delete_guild_data(var_data, data_to_delete: str):
    keys_list = await get_keys()

    for table in keys_list:
        if str(data_to_delete) in table:
            data = await Database.get_data(table, var_data.guild.id)
            if data == "None":
                return

            for id in data:
                if int(var_data.id) == int(id):
                    await Database.remove_data_list(
                        table, var_data.guild.id, var_data.id
                    )

            return


async def error_embed(title: str, description: str, color: int):
    embed = disnake.Embed(
        title=f"<a:X_:773261860920492062> {title}", description=description, color=color
    )

    return embed


async def custom_logger(file, name):
    with open(file, "r") as f:
        a = json.loads(f.read())

    for x in a:  # x = dict, a = list
        if x["name"] == name:
            x["count"] = str(int(x["count"]) + 1)
            break
    else:
        a.append({"name": name, "count": "1"})

    with open(file, "w") as f:
        f.write(json.dumps(a, indent=4, sort_keys=True, ensure_ascii=False))


scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

#credentials = ServiceAccountCredentials.from_json_keyfile_name(
   # "bread-winner-b-logging-0878c15b922d.json", scopes
#)  # access the json key you downloaded earlier
#file = gspread.authorize(credentials)  # authenticate the JSON key with gspread

#sheet = file.open("Bread Winner B Logs")
#sheet = sheet.sheet1


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        # Loops
        #self.topgg_stats.start()
        #self.googlesheets_stats.start()

    @tasks.loop(hours=336)  # 336 hours
    async def googlesheets_stats(self):
        await self.bot.wait_until_ready()

        with open("data/command_logs.json", "r") as f:
            file = json.loads(f.read())

        row = 1
        new_list = []
        for item in file:
            new_list.append([item["name"], item["count"]])
            row = row + 1

        shutil.copy("data/command_logs.json", "data/command_logs_archive/")
        os.rename(
            "data/command_logs_archive/command_logs.json", f"data/command_logs_archive/{ctime()}.json"
        )

        sheet.update(f"A2:B{str(row)}", new_list)

    @commands.Cog.listener()
    async def on_slash_command(self, inter):
        """
        Logs slash commands and slash commands sub command
          - Is saved using a LIST full of DICTs, uses .json just for the colors
        """
        if inter.data.options:
            for x in inter.data.options:

                if x.type == disnake.OptionType.sub_command:
                    try:
                        await custom_logger(
                            "command_logs.json", f"{inter.data.name} {x.name}"
                        )
                    except:
                        return

        try:
            await custom_logger("command_logs.json", inter.data.name)
        except:
            return

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        # Welcome message, Auto Setup for Signing
        await auto_add_coach(guild)

        embed = disnake.Embed(
            title="Signing System",
            description="Signing has been automatically setup\n**See the other settings with `/helpsigning`**",
            color=guild.me.color,
        )

        coach_roles = await Database.get_data("FranchiseRole", guild.id)
        if coach_roles != "None":
            items = ""
            for id in coach_roles:
                role = guild.get_role(int(id))
                items += f"{role.mention}, "

            embed.add_field(name="Coach Roles", value=items[:-2])

        free_agent_roles = await Database.get_data("FreeAgentRole", guild.id)
        if free_agent_roles != "None":
            items = ""
            for id in free_agent_roles:
                role = guild.get_role(int(id))
                items += f"{role.mention}, "

            embed.add_field(name="Free Agent Roles", value=items[:-2])

        for channel in guild.text_channels:
            if (
                channel.permissions_for(guild.me).send_messages
                and channel.permissions_for(guild.me).embed_links
            ):
                vaild_channel = channel
                if len(embed.fields) > 0:
                    await vaild_channel.send(embed=embed)
                await vaild_channel.send(welcome_message)
                break

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: disnake.Guild):
        keys_list = await get_keys()

        for table in keys_list:
            current_data = await Database.get_data(table, guild.id)
            if current_data != "None":
                await Database.remove_data(table, guild.id)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: disnake.Role):
        await auto_delete_guild_data(role, "Role")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: disnake.abc.GuildChannel):
        await auto_delete_guild_data(channel, "Channel")

    @commands.Cog.listener()
    async def on_thread_delete(self, thread: disnake.Thread):
        await auto_delete_guild_data(thread, "Channel")

    @commands.Cog.listener()
    async def on_slash_command_error(
        self,
        inter: disnake.ApplicationCommandInteraction,
        error: disnake.ext.commands.CommandError,
    ):
        if isinstance(error, commands.errors.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
                _message = (
                    "You need the **{}** permission(s) to run this command".format(fmt)
                )

                embed = await error_embed(
                    title="Missing Permissions",
                    description=f"{_message}",
                    color=0xFF0000,
                )

                try:
                    return await inter.response.send_message(
                        embed=embed, content=error_support_message, ephemeral=True
                    )
                except:
                    return

        elif isinstance(error, commands.CommandOnCooldown):
            if await inter.bot.is_owner(inter.author):
                return inter.application_command.reset_cooldown(inter)

            seconds = error.retry_after
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            embed = disnake.Embed(
                title="<a:Loading_Color:774724065796948008> Command on Cooldown",
                description=f"You still have to wait **{int(h)} hours, {int(m)} minutes and {int(s)} seconds**",
                color=0xFFFF00,
            )
            return await inter.response.send_message(embed=embed, ephemeral=True)

        elif isinstance(error, commands.errors.NotOwner):
            return await inter.response.send_message(
                f"Only the one Mr.Doggy Soggy can use these commands\n{error_support_message}",
                ephemeral=True,
            )

        elif isinstance(error, commands.BotMissingPermissions):
            if not inter.guild:
                return
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_permissions
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)

                _message = "I need the **{}** permission(s) to run this command".format(
                    fmt
                )
                embed = await error_embed(
                    title="Missing Permissions",
                    description=f"{_message}",
                    color=0xFF0000,
                )

                try:
                    return await inter.response.send_message(
                        embed=embed, content=error_support_message, ephemeral=True
                    )
                except:
                    return

    @tasks.loop(minutes=30)
    async def topgg_stats(self):
        await self.bot.wait_until_ready()
        try:
            token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjczMDU5NDA5ODY5NTYzNTAxNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjIxODE3MjM4fQ.yLCCA9hSs1FVH5qktLJKfJxiGOgLL3F5UQ5FXwTQntI"
            headers = {"Authorization": token}
            payload = {"server_count": len(self.bot.guilds)}

            await self.session.post(
                "https://top.gg/api/bots/730594098695635014/stats",
                headers=headers,
                json=payload,
            )
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Events(bot))