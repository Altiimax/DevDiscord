import discord
import os
from discord.ext import commands
import random


class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        
    
    @commands.command()
    async def cat(self, ctx):
        await ctx.send(file=discord.File(random.choice(os.listdir("./Images/Mido"))))


def setup(bot):
    bot.add_cog(Cat(bot))    
