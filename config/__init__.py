import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
