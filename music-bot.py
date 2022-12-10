# music-bot.py

import os
import random
import re
import discord
import yt_dlp
import urllib

from urllib.parse import urlparse
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.command(help="roll a die with the specified number of sides")
async def roll(ctx: commands.Context, num_sides: int):
    await ctx.send(str(random.randint(1, num_sides)))


# @bot.command(help="join voice channel")
# async def join(ctx: commands.Context):
#     connected = ctx.author.voice
#     if not connected:
#         await ctx.send("You need to be connected in a voice channel to use this command!")
#         return
#     await ctx.send("joining voice channel")
#     await connected.channel.connect()


@bot.command(help="leave voice channel")
async def stop(ctx: commands.Context):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voice_client.disconnect()


# https://stackoverflow.com/a/66116633/1781821
@bot.command(help="play something")
async def play(ctx: commands.Context, *args):
    if ctx.message.author.voice == None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None:
        voice_client = await voice.connect()
    else:
        await voice_client.move_to(channel)

    # check if user types search keywords or a url to play
    if len(args) > 1:
        search = "+".join(args)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])
        url = video_ids[0]
    elif len(args) == 1 and uri_validator(args[0]):
        url = args[0]

    # https://stackoverflow.com/a/73210027/1781821
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    ydl_opts = {'format': 'bestaudio'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        song_info = ydl.extract_info(url, download=False)
    source = discord.FFmpegPCMAudio(song_info["url"], **ffmpeg_options)

    voice_client.play(source)


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CheckFailure):
#         await ctx.send("something went wrong oopsie poopsie")


# https://stackoverflow.com/a/38020041/1781821
def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

bot.run(DISCORD_TOKEN)
