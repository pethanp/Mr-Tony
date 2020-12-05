

import discord
from discord.ext import commands


def get_key():

    try:
        fin = open("KEYS.txt", 'r')
        ftext = fin.read().strip()
        fin.close()
        return ftext
        
    except:
        raise FileNotFoundError("!Key file not found!.\n")

intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print("Ready")
    print(f'Logged on as {client.user}!')


@client.command()
async def userTime(ctx, name):
    guild = ctx.guild
    print(guild.members)
    for member in guild.members:
        print("Member '{}' joined at {}".format(member.name, member.joined_at))
    print("Member count: {}".format(guild.member_count))
    

client.run(get_key())
