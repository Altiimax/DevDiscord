import os
import discord
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True
from dotenv import load_dotenv
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append('cogs.'+ filename[:-3])
        print(initial_extensions)

if __name__ == '__main__':
  for extension in initial_extensions:
    bot.load_extension(extension)

bot.run(TOKEN)