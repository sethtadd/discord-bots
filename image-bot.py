# image-bot.py

import os
import re
import openai
import discord
import requests
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# TODO figure out slash commands: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=slash#:~:text=async%20def%20record_usage(ctx)%3A%0A%20%20%20%20print(ctx.author%2C%20%27used%27%2C%20ctx.command%2C%20%27at%27%2C%20ctx.message.created_at)
# async def record_usage(ctx):
#     print(ctx.author, 'used', ctx.command, 'at', ctx.message.created_at)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    for guild in client.guilds:
        # print guild info
        print(f"{client.user} is a member of guild:", guild)
        print(f"guild name: {guild.name}")
        print(f"guild id: {guild.id}")
        # guild members
        members = [str(member) for member in guild.members]
        print(f"guild members ({len(members)}):")
        print(" - " + "\n - ".join(members))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if "girl" in message.content.lower():
        await message.channel.send("grill*")
    if "sorry" in message.content.lower():
        await message.channel.send("I forgive you")
    # generate image
    reg_exp = re.compile(r"^image generation (.*): (.*)$")
    match = reg_exp.search(message.content)
    if match:
        num_imgs = 4
        size = match.group(1)
        prompt = match.group(2)
        await message.channel.send(f"generating {num_imgs} images for prompt: " + prompt)
        response = openai.Image.create(
            prompt=prompt,
            n=num_imgs,
            size=size
        )
        for data in response["data"]:
            url = data["url"]
            await message.channel.send(url)
    # image variation
    reg_exp = re.compile(r"^image variations (.*): (.*)$")
    match = reg_exp.search(message.content)
    if match:
        num_imgs = 4
        size = match.group(1)
        img_url = match.group(2)
        img = requests.get(img_url, stream=True).raw
        await message.channel.send(f"generating {num_imgs} image variations")
        response = openai.Image.create_variation(
            image=img,
            n=num_imgs,
            size=size
        )
        for data in response["data"]:
            await message.channel.send(data["url"])
    # image edits
    # reg_exp = re.compile(r"^image edits: (.*) (.*)$")
    # match = reg_exp.search(message.content)
    # if match:
    #     num_imgs = 4
    #     img_url = match.group(1)
    #     prompt = match.group(2)
    #     img = requests.get(img_url, stream=True).raw
    #     await message.channel.send(f"generating {num_imgs} image edits")
    #     response = openai.Image.create_edit(
    #         image=img,
    #         prompt=prompt,
    #         n=num_imgs,
    #         size="512x512"
    #     )
    #     for data in response["data"]:
    #         await message.channel.send(data["url"])


client.run(DISCORD_TOKEN)
