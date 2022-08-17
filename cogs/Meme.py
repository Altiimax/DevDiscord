import discord
from discord.ext import commands
from requests import get
import json


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
    # Define a command to send a randomly picked meme from the heroku api (gatehring posts from reddit) to the channel
    @commands.command(help='Send a random meme from reddit, HELL YEAH BUDDY')
    async def meme(self, ctx):
        request = get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(request,)
        meme_content = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
        await ctx.reply(embed=meme_content)


def setup(bot):
    bot.add_cog(Meme(bot))  