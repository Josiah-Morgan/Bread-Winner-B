import os

import aiohttp

DATABASE_URL = "https://database-errors.jerythemouse.repl.co"
DATABASE_KEY = "FOuiCnouiomCClsjofjolmlZos"

class Database:
  
    async def get_db_all():
        headers = {'Authorization': DATABASE_KEY}
        url = f"{DATABASE_URL}/db"
          
        async with aiohttp.ClientSession(trust_env = True) as session:
            async with session.get(
                url,
                headers = headers
                ) as resp:
                    return await resp.json()
                  
    async def get_data(key, path = None):
      headers = {'Authorization': DATABASE_KEY}
      url = f"{DATABASE_URL}/db/{key}/{path}"
      if path == None:
        url = f"{DATABASE_URL}/db/{key}"
        
      async with aiohttp.ClientSession(trust_env = True) as session:
          async with session.get(
              url,
              headers = headers
              ) as resp:
                  if resp.status != 200:
                      return None
                  data = await resp.json()
                  return data

    async def get_db_prefix(prefix = None):
        headers = {'Authorization': DATABASE_KEY}
        prefix = str(prefix)  
        url = f"{DATABASE_URL}/db_prefix/{prefix}"
          
        async with aiohttp.ClientSession(trust_env = True) as session:
            async with session.get(
                url,
                headers = headers
                ) as resp:
                    return await resp.json()

    async def get_db_keys():
        headers = {'Authorization': DATABASE_KEY}
        url = f"{DATABASE_URL}/db_keys"
          
        async with aiohttp.ClientSession(trust_env = True) as session:
            async with session.get(
                url,
                headers = headers
                ) as resp:
                    return await resp.json()


    async def add_data(key, value):
        headers = {'Authorization': DATABASE_KEY}

        def convert_ints_to_strings(obj):
            if isinstance(obj, int):
                return str(obj)
            elif isinstance(obj, dict):
                return {k: convert_ints_to_strings(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_ints_to_strings(elem) for elem in obj]
            else:
                return obj
    
        value = convert_ints_to_strings(value)
        key = str(key)
      
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.put(
                f"{DATABASE_URL}/db/{key}",
                json={'value': value},
                headers = headers
            ) as resp:
                if resp.status == 404:  # No key with that name
                    async with aiohttp.ClientSession(trust_env=True) as session:
                        async with session.post(
                                f"{DATABASE_URL}/db",
                                json={'key': key, 'value': value},
                        ) as resp:
                            try:
                              return await resp.json()
                            except Exception as e:
                              print(f"ERROR: {e}\nKEY: {key}\n VALUE: {value}",)
                              return None
              
                return await resp.json()


    async def delete_data(key, path = None):
      headers = {'Authorization': DATABASE_KEY}
      key = str(key)

      url = f"{DATABASE_URL}/db/{key}/{path}"
      if path == None:
        url = f"{DATABASE_URL}/db/{key}"

      async with aiohttp.ClientSession(trust_env = True) as session:
        async with session.delete(
          url,
          headers = headers
        ) as resp:
          if resp.status != 200:
            return None
            # log is error
          data = await resp.json()
          return data