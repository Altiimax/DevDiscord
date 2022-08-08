import os
import discord
import random
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('CHANNEL_ID')

bot = commands.Bot(command_prefix='!')

@bot.command(name='reaction')
async def roles(ctx):
    global IDMessage
    reaction = await ctx.reply("Select your Role")

    await reaction.add_reaction('❌')

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
  ChID = 1001903262942896290
  if str(payload.emoji) == "❌":
    test1 = discord.utils.get(payload.member.guild.roles, name="test1")
    await payload.member.add_roles(test1)

@bot.command(name='99', help='Responds with a random quiote from Brooklyn Nine-Nine')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))   
    
@bot.command(name='create_channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        await ctx.send('You succesfully created the channel : ' + channel_name)    

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


bot.run(TOKEN)