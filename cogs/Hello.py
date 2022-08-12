import discord
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(help=('Let the bot wave at you and wish you an amazing day !'))
    async def hello(self, ctx):
        await ctx.reply('Hello you ! :wave: , I hope you have an amazing day!')


def setup(bot):
    bot.add_cog(Hello(bot))    
