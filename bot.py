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
    """Log a user joining / leaving a channel.

    It is possible that a voice update comes from muting / deafening. Currently,
    this isn't handled and will be logged with join and true both False.

    "leave" is True when we leave the channel previously joined.
    "join" is True when the current channel_id is being joined.
    It is possible to both "leave" and "join" at the same time when swtiching
    channels.

    TODO - we probably don't need to log user name and channel name since we
    should be able to access these from the id.
    We could also handle other voice updates outside of join or leave (such
    as mute) or not log anything when one of these events occurs.
    Instead of using a csv, we could use a database.

    Args:
        member: the member the update is for
        before: the state before the event
        after: the state after the event
    """
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
    """Adds update to logs."""
    log_voice_state_update(member, before, after)


async def make_user_time_response(member: discord.Member) -> str:
    """Make the response to show a client for user time.

    TODO - if we updat the log to use a database, this needs to be
    updated as well.
    We also don't have very good error handling if the bot goes offline, so
    our algorithm could check if times online seem unreasonable to avoid this
    (or something could be improved in the logging).
    Currently doesn't handle multiple guilds (it will just show everything
    for that user in our logs, while we should only show the channels in
    the current guild)

    Args:
        member (discord.member): the member to get time for
    """
    voicePath = os.path.join(logFolder, "voiceUpdates.csv")
    df = pd.read_csv(voicePath)
    user_df = df[df["user_id"] == member.id]
    if len(user_df) == 0:
        print("No entries found for the given user")
    serverToTime = dict()
    # if the user is in the server before the bot loaded
    # that time will be ignored because of this
    channel = user_df["channel_id"].iloc[0]
    startTime = pd.to_datetime(list(user_df["time"])[0])
    for index in user_df.index:
        if user_df["leave"][index]:
            if channel not in serverToTime:
                serverToTime[channel] = datetime.timedelta()
            endTime = pd.to_datetime(user_df["time"][index])
            serverToTime[channel] += endTime - startTime
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

async def get_member_from_name(name: str, guild: discord.Guild) -> discord.Member:
    target = None
    for member in guild.members:
        if member.name == name or member.nick:
            if not target:
                target = member
            else:
                # found 2 of the same name
                raise Exception(f"Found 2 members with the name {name}")
    return target

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

@client.command()
async def nameHistory(ctx, name):
    member = await get_member_from_name(name, ctx.guild)
    await ctx.message.channel.send("Name history command")

client.run(get_key())
