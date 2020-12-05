import os
import datetime
import pandas as pd

import discord
from discord.ext import commands

# this can be changed for prod
logFolder = "testLogs"

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

@client.event
async def on_member_update(before, after):
    # check name changes here
    pass


def log_voice_state_update(member, before, after):
    logFile = os.path.join(logFolder, "voiceUpdates.csv")
    if not os.path.isfile(logFile):
        df = pd.DataFrame(columns = ["time", "user_id", "user_name", "join", "leave", "channel_id", "channel_name"])
    else:
        df = pd.read_csv(logFile)
    userId = member.id
    userName = member.name
    if before.channel != after.channel and after.channel is not None:
        join = True
    else:
        join = False
    if before.channel is not None and before.channel != after.channel:
        leave = True
    else:
        leave = False
    if after.channel:
        channel_id = after.channel.id
        channel_name = after.channel.name
    else:
        channel_id = None
        channel_name = None
    d = {"time": datetime.datetime.now(),
         "user_id": str(userId),
         "user_name": userName,
         "join": join,
         "leave" : leave,
         "channel_id": str(channel_id),
         "channel_name": channel_name
        }
    print(f"Adding {d} to voice logs")
    df = df.append(d, ignore_index = True)
    df.to_csv(logFile, index=False)
    

@client.event
async def on_voice_state_update(member, before, after):
    log_voice_state_update(member, before, after)


async def make_user_time_response(member: discord.Member):
    voicePath = os.path.join(logFolder, "voiceUpdates.csv")
    df = pd.read_csv(voicePath)
    user_df = df[df["user_id"] == member.id]
    if len(user_df) == 0:
        print("No entries found for the given user")
    serverToTime = dict()
    # if the user is in the server before the bot loaded
    # that time will be ignored because of this
    channel = list(user_df["channel_id"])[0]
    startTime = pd.to_datetime(list(user_df["time"])[0])
    for index in user_df.index:
        if user_df["leave"][index]:
            if channel not in serverToTime:
                serverToTime[channel] = datetime.timedelta()
            endTime = pd.to_datetime(user_df["time"][index])
            serverToTime[channel] = endTime - startTime
            # set channel to none to track leaving all servers
            channel = None
        if user_df["join"][index]:
            channel = user_df["channel_id"][index]
            startTime = pd.to_datetime(user_df["time"][index])
    if channel is not None:
        serverToTime[channel] += datetime.datetime.now() - startTime

    channelTimeStrings = []
    for channelId, time in serverToTime.items():
        channelName = (await client.fetch_channel(channelId)).name
        days = time.days
        seconds = time.seconds
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60

        timeStr = f"{hours} hours, {minutes} minutes and {seconds} seconds"
        if days > 0:
            timeStr = f"{days} days, " + timeStr
        channelTimeStrings.append(f"{channelName}: {timeStr}")
    return "\n".join(channelTimeStrings)

@client.command()
async def userTime(ctx, name):
    guild = ctx.guild
    targetMember = None
    for member in guild.members:
        if member.name == name or member.nick:
            targetMember = member
            break
    if targetMember is None:
        responseMsg = f"Member '{name}' could not be found"
    else:
        responseMsg = await make_user_time_response(member)
    await ctx.message.channel.send(responseMsg)

client.run(get_key())
