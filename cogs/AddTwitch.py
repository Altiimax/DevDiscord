import discord
import os
import json
from discord.ext import commands

    
class AddTwitch(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        

    @commands.command(help='Adds your twitch to the live streaming notifications under #live-streams', pass_context=True)
    async def add_twitch(self, ctx, twitch_username):
        # Opens and reads the json file.
        with open('streamers.json', 'r') as file:
            streamers = json.loads(file.read())
    
            # Gets the users id that called the command.
            user_id = ctx.author.id
            # Assigns their given twitch_name to their discord id and adds it to the streamers.json.
            streamers[user_id] = twitch_username
    
            # Adds the changes we made to the json file.
            with open('streamers.json', 'w') as file:
                file.write(json.dumps(streamers))
            # Tells the user it worked.
            await ctx.reply(f"Added {twitch_username} for {ctx.author.mention} to the list of active streamers")

def setup(bot):
    bot.add_cog(AddTwitch(bot))    