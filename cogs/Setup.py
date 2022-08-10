import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = int(os.getenv('CHANNEL_ID'))

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(CHANNEL)
        reaction = await channel.send("Select your Role")

        await reaction.add_reaction('❤️')
        await reaction.add_reaction('💛')
        await reaction.add_reaction('💚')
        print("Bot is ready to roll!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) == "❤️":
            test1 = discord.utils.get(payload.member.guild.roles, name="test1")
            await payload.member.add_roles(test1)
    
        elif str(payload.emoji) == "💛":
            test2 = discord.utils.get(payload.member.guild.roles, name="test2")
            await payload.member.add_roles(test2)
    
        elif str(payload.emoji) == "💚":
            test3 = discord.utils.get(payload.member.guild.roles, name="test3")
            await payload.member.add_roles(test3)
    
def setup(bot):
    bot.add_cog(Setup(bot))  