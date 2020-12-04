

import discord
from discord.ext import commands



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        print(self.guilds)

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith('/'):
            await message.channel.send(f'MESSAGE: {message.content}')

def get_key():

    try:
        fin = open("KEYS.txt", 'r')
        ftext = fin.read().strip()
        fin.close()
        return ftext
        
    except:
        raise FileNotFoundError("!Key file not found!.\n")

client = MyClient()

key = get_key()
print(f"Key is: {key}")
client.run(key)
