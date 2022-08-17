import os
import discord
import requests
import json
from discord.utils import get
from discord import Streaming
from datetime import datetime
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True
from dotenv import load_dotenv
from discord.ext import tasks, commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
STREAM_CHANNEL= int(os.getenv('STREAM_CHANNEL'))
STREAM_ROLE = int(os.getenv('STREAM_ROLE'))
GUILD= int(os.getenv('DISCORD_GUILD'))
# Deaclare a bot variable that we will run later through the discord token associated with it, commands_prefix makes the bot listen to events starting with '!' in the associated discord server
bot = commands.Bot(command_prefix='!', intents=intents)

# Authentication with Twitch API to receive data about a user's streaming status.
client_id = os.getenv('TWITCH_CLIENT')
client_secret = os.getenv('TWITCH_SECRET')
body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
# Request access to authentification from Twitch API
request = requests.post('https://id.twitch.tv/oauth2/token', body)
access_keys = request.json()
headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + access_keys['access_token']
}

# Logs exception to .txt file.
def log_and_print_exception(e):
    logging_file = open("log.txt", "a")
    logging_file.write(f"{datetime.now()}\n{str(e)}\n\n")
    logging_file.close()
    print(f"Exception logged. Error:\n{e}")

# Returns true if online on twitch, false if not.
def checkuser(streamer_username):
    try:
        stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_username,
                              headers=headers)
        if streamer_username is not None and str(stream) == '<Response [200]>':
            stream_data = stream.json()

            if len(stream_data['data']) == 1:
                return True, stream_data
            else:
                return False, stream_data
        else:
            stream_data = None
            return False, stream_data
    except Exception as e:
        log_and_print_exception(e)
        stream_data = None
        return False, stream_data
    
# Declare a function to avoid spamming the chat if the notification has already been sent   
async def message_already_sent(channel, user):
    async for message in channel.history(limit=200):
        if f"{user.mention} is now playing" in message.content:
            return message
    else:
        return False
#Declare a command to add streamer to json file if they connected their twitch to discord and their activity changes to 'Streaming'       
@bot.event
async def on_member_update(before, after):
    if after.guild.id == GUILD:
        with open('streamers.json', 'r') as file:
            streamers = json.loads(file.read())
        if before.activity == after.activity:
            return

        if isinstance(after.activity, Streaming) is False:
            return
        if isinstance(after.activity, Streaming):
            twitch_username = after.activity.twitch_username
            user_id = after.id
            if str(user_id) not in streamers and twitch_username not in streamers:
                streamers[user_id] = twitch_username
                print(f"Added streamer {twitch_username} to streamers.json")

        with open('streamers.json', 'w') as file:
            file.write(json.dumps(streamers))


# Executes when bot is started
@bot.event
async def on_ready():
    # Defines a loop that will run every 10 seconds (checks for live users every 10 seconds).
    @tasks.loop(seconds=10)
    async def live_notifs_loop():
        # Opens and reads the json file that contains names of streamers and their discord ID
        with open('streamers.json', 'r') as file:
            streamers = json.loads(file.read())
        # Makes sure the json isn't empty before continuing.
        try:
            if streamers is not None:
                # Gets the guild(discord server linked to the user id), 'live_streams' channel, and streaming role.
                guild = bot.get_guild(GUILD)
                channel = bot.get_channel(STREAM_CHANNEL)
                role = get(guild.roles, id=STREAM_ROLE)
                # Loops through the json and gets the user_id of the discord user and his associated twitch name
                # every item in the json.
                for user_id, twitch_name in streamers.items():
                    selected_member = ""
                    async for member in guild.fetch_members(limit=None):
                        # If one of the id's of the members in your guild matches the one from the json and they're not
                        # live, remove the streaming role.
                        if member.id == int(user_id):
                            selected_member = member

                    # Checks if user_id, twitch_username is currently streaming on twitch
                    # Returns either true or false.
                    status, stream_data = checkuser(twitch_name)
                    # Define a user variable for ease of use later
                    user = bot.get_user(int(user_id))
                    if status is True:
                        # Checks to see if the live message has already been sent.
                        message = await message_already_sent(channel, user)
                        if message is not False:
                            continue
                        # Give the user a streamer role to ease notifications
                        if selected_member != "":
                            await selected_member.add_roles(role)
                        # Sends the live notification to the 'twitch streams' channel then breaks the loop.
                        await channel.send(
                            f":red_circle: Attention @everyone, our dear : :red_circle:"
                            f"\n{user.mention} is now playing {stream_data['data'][0]['game_name']} on Twitch!"
                            f"\nCheck them out here : https://www.twitch.tv/{twitch_name}")
                        print(f"{user} started streaming. Sending a notification.")
                        continue
                    # If they aren't live do this:
                    elif stream_data is not None:
                        # Remove the streaming role from the member
                        if selected_member != "":
                            await selected_member.remove_roles(role)
                        # Checks to see if the live message was sent.
                        message = await message_already_sent(channel, user)
                        if message is not False:
                            print(f"{user} stopped streaming. Removing the notification.")
                            await message.delete()
        except TypeError as e:
            log_and_print_exception(e)
            raise e

    # Start your loop.
    live_notifs_loop.start()
# Declare an empty array to receive the cogs loading
initial_extensions = []
# Load all the cogs and their associated commands into bot.py
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append('cogs.'+ filename[:-3])
        print(initial_extensions)

if __name__ == '__main__':
  for extension in initial_extensions:
    bot.load_extension(extension)
# Run the discord bot
bot.run(TOKEN)