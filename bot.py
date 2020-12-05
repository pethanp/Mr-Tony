

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
    targetMember = None
    for member in guild.members:
        if member.name == name:
            targetMember = member
            break
    if targetMember is None:
        responseMsg = f"Member '{name}' could not be found"
    else:
        responseMsg = "Member '{}' joined at {}".format(member.name, member.joined_at)
    await ctx.message.channel.send(responseMsg)

client.run(get_key())
