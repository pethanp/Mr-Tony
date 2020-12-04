

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


client = MyClient()

client.run('')
