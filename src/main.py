import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('[Emorce]')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_IDS = [int(id.strip()) for id in os.getenv('OWNER_IDS', '').split(',') if id.strip()]

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Import utilities
from utils.token_manager import TokenManager
bot.token_manager = TokenManager()

# Load cogs
async def load_cogs():
    for filename in os.listdir('./src/commands'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'commands.{filename[:-3]}')
            logger.info(f'Loaded command: {filename[:-3]}')

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    logger.info(f'Tokens loaded: {bot.token_manager.get_count()}')
    
    status = os.getenv('BOT_STATUS', 'Emorce Tokens')
    activity_type = os.getenv('BOT_ACTIVITY', 'watching')
    
    activity_types = {
        'playing': discord.ActivityType.playing,
        'watching': discord.ActivityType.watching,
        'listening': discord.ActivityType.listening,
        'competing': discord.ActivityType.competing,
    }
    
    activity = discord.Activity(
        type=activity_types.get(activity_type.lower(), discord.ActivityType.watching),
        name=status
    )
    await bot.change_presence(activity=activity)
    
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} command(s)')
    except Exception as e:
        logger.error(f'Failed to sync commands: {e}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
