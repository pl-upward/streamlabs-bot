import discord
from dotenv import load_dotenv
from discord.ext import commands
import json
import re
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
KEY = os.getenv('STREAM_KEY')

CONFIG_FILE = "config.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

YOUTUBE_REGEX = r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w\-]+)"


# GET THE CHANNEL ID FROM THE CONFIG
def get_channel():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("channel-id")
    return None


# UPDATE THE CHANNEL ID IN THE CONFIG
def set_channel(id):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"channel-id": id}, f)


# COMMAND TO SET THE MEDIA CHANNEL FROM DMS
@bot.command(name="setmedia")
@commands.has_permissions(administrator=True)
async def set_media_chanel(ctx):
    set_channel(ctx.channel.id)
    await ctx.send("shaving cream is done")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot:
        return

    media_channel_id = get_channel()
    if message.channel.id != media_channel_id:
        return

    matches = re.findall(YOUTUBE_REGEX, message.content)
    for link in matches:
        await message.channel.send(f"{link} added to the queue.")

bot.run(TOKEN)