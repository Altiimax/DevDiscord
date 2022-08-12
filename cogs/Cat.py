import discord
import os
from discord.ext import commands
import random

images = os.path.join(os.getcwd(), './Images/Mido')
def select_random_image_path():
        return os.path.join(images, random.choice(os.listdir(images)))
    
class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        

    @commands.command(help=("Posts a random picture of everyone's favourite cat : Mido !"))
    async def mido(self, ctx):
        await ctx.send(file=discord.File(select_random_image_path()))


def setup(bot):
    bot.add_cog(Cat(bot))    
