import os
import json
import discord
import requests
from discord.ext import tasks, commands
from twitchAPI.twitch import Twitch
from discord.utils import get


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready')


def setup(bot):
    bot.add_cog(Twitch(bot))    
