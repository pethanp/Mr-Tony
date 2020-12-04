

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
        ftext = fin.read()
        fin.close()
        return ftext
        
    except:
        print("!Key file not found!.\n")
        return ''

client = MyClient()

client.run(get_key)
