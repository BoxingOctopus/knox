import discord
from discord.ext import commands
import re
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Don't respond to bot messages
    if message.author == bot.user:
        return

    # Check for Twitter/X links using regex
    twitter_pattern = r'https?:\/\/(?:www\.)?(?:twitter\.com|x\.com)\/[a-zA-Z0-9_]+'
    
    if re.search(twitter_pattern, message.content, re.IGNORECASE):
        # Delete the message
        await message.delete()

        try:
            # DM the user
            await message.author.send("Your message was deleted because it contained a Twitter/X link. "
                                    "Please note that Twitter/X links are not allowed on this server.")
        except discord.Forbidden:
            # If we can't DM the user, notify them in the channel
            await message.channel.send(f"{message.author.mention} Your message was deleted because it contained a Twitter/X link. "
                                     "Please note that Twitter/X links are not allowed on this server.")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)