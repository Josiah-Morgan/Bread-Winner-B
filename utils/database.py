import aiohttp
import json
import os

DATABASE_URL = "https://new-bread.jerythemouse.repl.co/"
DATABASE_KEY = "FOuiCnouiomCClsjofjolmlZos"
CONFIG_KEY = "Breadwinnersucks"


class Database:
    async def get_all_values(table):
        """Returns data from a table"""
        headers = {"Content-type": "application/text"}
        async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
            async with session.get(
                f"{DATABASE_URL}/get_all_values?key={DATABASE_KEY}&table={table}"
            ) as resp:
                data = await resp.text()
                data = str(data).replace('"', "").replace("'", '"')
                data = json.loads(data)
                return data

    async def get_data(table, guild_id):
        """Returns data from a table"""
        headers = {"Content-type": "application/text"}
        async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
            async with session.get(
                f"{DATABASE_URL}/get_data?key={DATABASE_KEY}&table={table}&id={guild_id}"
            ) as resp:
                data = await resp.text()

                if "[" in data and "{" not in data:
                    data = (
                        data.replace("[", "")
                        .replace("]", "")
                        .replace("'", "")
                        .replace(",", "")
                    )
                    data = data.split(" ")
                    return data

                elif "{" in data:
                    data = data.replace('"', "").replace("'", '"')
                    data = json.loads(data)
                    return data

                else:
                    return data

    async def add_data(table, guild_id, add):
        """Adds 1 string to a table"""
        headers = {"Content-type": "application/text"}
        async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
            async with session.get(
                f"{DATABASE_URL}/add_data?key={DATABASE_KEY}&table={table}&id={guild_id}&add={add}"
            ) as resp:
                DATA = await resp.text()
                return str(DATA)

    async def add_data_list(table, guild_id, add):
        """Adds 1 string to a table with a list on it"""
        headers = {"Content-type": "application/text"}
        async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
            async with session.get(
                f"{DATABASE_URL}/add_data_list?key={DATABASE_KEY}&&table={table}&id={guild_id}&add={add}"
            ) as resp:
                DATA = await resp.text()
                return str(DATA)

    async def remove_data(table, guild_id):
        """Removes 1 string from a table"""
        headers = {"Content-type": "application/text"}
        async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
            async with session.get(
                f"{DATABASE_URL}/remove_data?key={DATABASE_KEY}&table={table}&id={guild_id}"
            ) as resp:
                DATA = await resp.text()
                return str(DATA)

    async def remove_data_list(table, guild_id, remove):
        """Removes 1 string from a table with a list on it"""
        headers = {"Content-type": "application/text"}
        async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
            async with session.get(
                f"{DATABASE_URL}/remove_data_list?key={DATABASE_KEY}&table={table}&id={guild_id}&remove={remove}"
            ) as resp:
                DATA = await resp.text()
                return str(DATA)

    async def keys():
        """Lists all the tables (keys) from the database"""
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(f"{DATABASE_URL}/keys?key={DATABASE_KEY}") as resp:
                DATA = await resp.text()
                DATA = (
                    DATA.replace("{", "")
                    .replace("}", "")
                    .replace("'", "")
                    .replace(",", "")
                )  # UGLY AS HELL LOL
                return DATA