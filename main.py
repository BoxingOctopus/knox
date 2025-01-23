import discord
from discord.ext import commands
import re
from config import DISCORD_TOKEN, LOG_LEVEL
import logging

# Set up logging configuration
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user} has connected to Discord!')

@bot.event
async def on_guild_join(guild):
    logger.info(f'Bot has been added to server: {guild.name} (ID: {guild.id}) with {guild.member_count} members')

@bot.event
async def on_guild_remove(guild):
    logger.info(f'Bot has been removed from server: {guild.name} (ID: {guild.id})')

@bot.event
async def on_message(message):
    # Don't respond to bot messages
    if message.author == bot.user:
        return

    # Check for Twitter/X links using regex
    twitter_pattern = r'https?:\/\/(?:www\.)?(?:twitter\.com|x\.com|fxtwitter\.com)\/[a-zA-Z0-9_]+'
    
    if re.search(twitter_pattern, message.content, re.IGNORECASE):
        logger.info(f'Detected Twitter/X link in message from {message.author} (ID: {message.author.id}) in channel #{message.channel.name} on server {message.guild.name}')
        
        # Delete the message
        await message.delete()
        logger.info(f'Deleted message from {message.author} containing Twitter/X link')

        try:
            # DM the user
            await message.author.send("Your message was deleted because it contained a Twitter/X link. "
                                    "Please note that Twitter/X links are not allowed on this server.")
            logger.info(f'Sent DM notification to {message.author}')
        except discord.Forbidden:
            # If we can't DM the user, notify them in the channel
            await message.channel.send(f"{message.author.mention} Your message was deleted because it contained a Twitter/X link. "
                                     "Please note that Twitter/X links are not allowed on this server.")
            logger.warning(f'Could not DM {message.author}, sent channel notification instead')

    await bot.process_commands(message)

# Add error handling with logging
@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f'Error in {event}', exc_info=True)

@bot.event
async def on_command_error(ctx, error):
    logger.error(f'Command error: {str(error)}')

bot.run(DISCORD_TOKEN)