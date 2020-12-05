

import discord
from discord.ext import commands



class MyClient(discord.ext.commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

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

client = commands.Bot(command_prefix='/')

@client.command()
async def nameHistory(ctx, name):
    await ctx.send(f"Name: {name}")

client.run(get_key())
