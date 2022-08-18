import discord
import os
from discord.ext import commands
import random

class RollDice(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(help='Roll 1 or multiple dices with custom number of sides : !roll [number of dices], [number of sides for the dice]')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.reply('You rolled the dices and obtained :') 
        await ctx.send(' ,'.join(dice))
    
def setup(bot):
    bot.add_cog(RollDice(bot)) 