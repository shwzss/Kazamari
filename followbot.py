import requests
import json
import discord
from discord.ext import commands
import random
import logging

# Replace these with your actual API keys
twitch_client_id = "your_twitch_client_id"
twitch_client_secret = "your_twitch_client_secret"
twitch_token = "your_twitch_token"
discord_token = "your_discord_token"

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the Discord bot
bot = commands.Bot(command_prefix="/")

@bot.event
async def on_ready():
    logging.info(f"We have logged in as {bot.user}")
    guild = discord.utils.get(bot.guilds, name="Your Server Name")  # Replace with your server name
    category = await guild.create_category("Twitch")

    roles = ["free", "basic", "super", "astronomic", "massive"]
    for role in roles:
        await guild.create_text_channel(role, category=category)

    print(f"Channels created under category 'Twitch'")

# Define role limits
role_limits = {
    "free": 100,
    "basic": 500,
    "super": 1000,
    "astronomic": 3000,
    "massive": 10000
}

@bot.command()
@commands.has_any_role("basic", "super", "astronomic", "massive")
async def botfollow(ctx, number: int, channel: str):
    try:
        role = discord.utils.find(lambda r: r.name in role_limits, ctx.author.roles)
        if role is None or number > role_limits[role.name]:
            await ctx.send(f"Your role does not allow you to follow more than {role_limits[role.name]} users.")
            return

        # Authenticate with the Twitch API
        auth_url = "https://id.twitch.tv/oauth2/token"
        auth_data = {
            "client_id": twitch_client_id,
            "client_secret": twitch_client_secret,
            "grant_type": "client_credentials"
        }
        auth_response = requests.post(auth_url, data=auth_data)
        auth_response.raise_for_status()
        access_token = json.loads(auth_response.text)["access_token"]

        # Set the headers for the API requests
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": twitch_client_id
        }

        # Get the channel ID from the channel name
        channel_url = "https://api.twitch.tv/helix/channels"
        channel_response = requests.get(channel_url, headers=headers, params={"name": channel})
        channel_response.raise_for_status()
        channel_id = json.loads(channel_response.text)["data"][0]["id"]

        # Get the user ID of the bot
        user_url = "https://api.twitch.tv/helix/users"
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()
        user_id = json.loads(user_response.text)["data"][0]["id"]

        # Get the followers of the bot
        followers_url = "https://api.twitch.tv/helix/users/follows"
        followers_response = requests.get(followers_url, headers=headers, params={"from_id": user_id})
        followers_response.raise_for_status()
        followers = [follower["to_id"] for follower in json.loads(followers_response.text)["data"]]

        # Get the users to follow
        users_to_follow = []
        for _ in range(number):
            user_id = random.choice([user for user in followers if user not in users_to_follow])
            users_to_follow.append(user_id)

        # Follow the users
        for user_id in users_to_follow:
            follow_url = "https://api.twitch.tv/helix/subscriptions"
            follow_data = {
                "from_id": user_id,
                "to_id": channel_id
            }
            follow_response = requests.post(follow_url, headers=headers, json=follow_data)
            follow_response.raise_for_status()

        await ctx.send(f"Followed {channel} for {number} followers!")
    except Exception as e:
        logging.error(f"Error in botfollow command: {e}")
        await ctx.send(f"Failed to follow {channel}!")

@bot.command()
@commands.has_any_role("super", "astronomic", "massive")
async def botview(ctx, number: int, channel: str):
    try:
        role = discord.utils.find(lambda r: r.name in role_limits, ctx.author.roles)
        if role is None or number > role_limits[role.name]:
            await ctx.send(f"Your role does not allow you to view more than {role_limits[role.name]} streams.")
            return

        # Authenticate with the Twitch API
        auth_url = "https://id.twitch.tv/oauth2/token"
        auth_data = {
            "client_id": twitch_client_id,
            "client_secret": twitch_client_secret,
            "grant_type": "client_credentials"
        }
        auth_response = requests.post(auth_url, data=auth_data)
        auth_response.raise_for_status()
        access_token = json.loads(auth_response.text)["access_token"]

        # Set the headers for the API requests
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": twitch_client_id
        }

        # Get the channel ID from the channel name
        channel_url = "https://api.twitch.tv/helix/channels"
        channel_response = requests.get(channel_url, headers=headers, params={"name": channel})
        channel_response.raise_for_status()
        channel_id = json.loads(channel_response.text)["data"][0]["id"]

        # Get the user ID of the bot
        user_url = "https://api.twitch.tv/helix/users"
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()
        user_id = json.loads(user_response.text)["data"][0]["id"]

        # Get the views of the bot
        views_url = "https://api.twitch.tv/helix/streams"
        views_response = requests.get(views_url, headers=headers, params={"user_id": user_id})
        views_response.raise_for_status()
        views = [view["id"] for view in json.loads(views_response.text)["data"]]

        # Get the streams to view
        streams_to_view = []
        for _ in range(number):
            stream_id = random.choice([stream for stream in views if stream not in streams_to_view])
            streams_to_view.append(stream_id)

        # View the streams
        for stream_id in streams_to_view:
            view_url = f"https://api.twitch.tv/helix/streams?user_id={stream_id}"
            view_response = requests.get(view_url, headers=headers)
            view_response.raise_for_status()

        await ctx.send(f"Viewed {channel} for {number} views!")
    except Exception as e:
        logging.error(f"Error in botview command: {e}")
        await ctx.send(f"Failed to view {channel}!")

@bot.command()
@commands.has_any_role("astronomic", "massive")
async def botchat(ctx, message: str, optional_message1: str = None, optional_message2: str = None, optional_message3: str = None, channel: str = None):
    try:
        role = discord.utils.find(lambda r: r.name in role_limits, ctx.author.roles)
        if role is None or number > role_limits[role.name]:
            await ctx.send(f"Your role does not allow you to send more than {role_limits[role.name]} messages.")
            return

        # Authenticate with the Twitch API
        auth_url = "https://id.twitch.tv/oauth2/token"
        auth_data = {
            "client_id": twitch_client_id,
            "client_secret": twitch_client_secret,
            "grant_type": "client_credentials"
        }
        auth_response = requests.post(auth_url, data=auth_data)
        auth_response.raise_for_status()
        access_token = json.loads(auth_response.text)["access_token"]

        # Set the headers for the API requests
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": twitch_client_id
        }

        # Get the channel ID from the channel name
        channel_url = "https://api.twitch.tv/helix/channels"
        channel_response = requests.get(channel_url, headers=headers, params={"name": channel})
        channel_response.raise_for_status()
        channel_id = json.loads(channel_response.text)["data"][0]["id"]

        # Send messages to the chat
        chat_url = f"https://api.twitch.tv/helix/chat/messages?broadcaster_id={channel_id}"
        messages = [message, optional_message1, optional_message2, optional_message3]
        for msg in messages:
            if msg:
                chat_data = {
                    "message": msg
                }
                chat_response = requests.post(chat_url, headers=headers, json=chat_data)
                chat_response.raise_for_status()

        await ctx.send(f"Sent messages to {channel} chat!")
    except Exception as e:
        logging.error(f"Error in botchat command: {e}")
        await ctx.send(f"Failed to send messages to {channel} chat!")

@bot.command()
@commands.has_any_role("basic", "super", "astronomic", "massive")
async def unfollow(ctx, channel: str):
    try:
        # Authenticate with the Twitch API
        auth_url = "https://id.twitch.tv/oauth2/token"
        auth_data = {
            "client_id": twitch_client_id,
            "client_secret": twitch_client_secret,
            "grant_type": "client_credentials"
        }
        auth_response = requests.post(auth_url, data=auth_data)
        auth_response.raise_for_status()
        access_token = json.loads(auth_response.text)["access_token"]

        # Set the headers for the API requests
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": twitch_client_id
        }

        # Get the channel ID from the channel name
        channel_url = "https://api.twitch.tv/helix/channels"
        channel_response = requests.get(channel_url, headers=headers, params={"name": channel})
        channel_response.raise_for_status()
        channel_id = json.loads(channel_response.text)["data"][0]["id"]

        # Get the user ID of the bot
        user_url = "https://api.twitch.tv/helix/users"
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()
        user_id = json.loads(user_response.text)["data"][0]["id"]

        # Unfollow the channel
        unfollow_url = f"https://api.twitch.tv/helix/users/follows?from_id={user_id}&to_id={channel_id}"
        unfollow_response = requests.delete(unfollow_url, headers=headers)
        unfollow_response.raise_for_status()

        await ctx.send(f"Unfollowed {channel}!")
    except Exception as e:
        logging.error(f"Error in unfollow command: {e}")
        await ctx.send(f"Failed to unfollow {channel}!")

@bot.command()
async def follower_count(ctx, channel: str):
    try:
        # Authenticate with the Twitch API
        auth_url = "https://id.twitch.tv/oauth2/token"
        auth_data = {
            "client_id": twitch_client_id,
            "client_secret": twitch_client_secret,
            "grant_type": "client_credentials"
        }
        auth_response = requests.post(auth_url, data=auth_data)
        auth_response.raise_for_status()
        access_token = json.loads(auth_response.text)["access_token"]

        # Set the headers for the API requests
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": twitch_client_id
        }

        # Get the channel ID from the channel name
        channel_url = "https://api.twitch.tv/helix/channels"
        channel_response = requests.get(channel_url, headers=headers, params={"name": channel})
        channel_response.raise_for_status()
        channel_id = json.loads(channel_response.text)["data"][0]["id"]

        # Get the follower count
        followers_url = f"https://api.twitch.tv/helix/users/follows?to_id={channel_id}"
        followers_response = requests.get(followers_url, headers=headers)
        followers_response.raise_for_status()
        follower_count = json.loads(followers_response.text)["total"]

        await ctx.send(f"{channel} has {follower_count} followers!")
    except Exception as e:
        logging.error(f"Error in follower_count command: {e}")
        await ctx.send(f"Failed to get follower count for {channel}!")

@bot.command()
async def stream_info(ctx, channel: str):
    try:
        # Authenticate with the Twitch API
        auth_url = "https://id.twitch.tv/oauth2/token"
        auth_data = {
            "client_id": twitch_client_id,
            "client_secret": twitch_client_secret,
            "grant_type": "client_credentials"
        }
        auth_response = requests.post(auth_url, data=auth_data)
        auth_response.raise_for_status()
        access_token = json.loads(auth_response.text)["access_token"]

        # Set the headers for the API requests
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": twitch_client_id
        }

        # Get the channel ID from the channel name
        channel_url = "https://api.twitch.tv/helix/channels"
        channel_response = requests.get(channel_url, headers=headers, params={"name": channel})
        channel_response.raise_for_status()
        channel_id = json.loads(channel_response.text)["data"][0]["id"]

        # Get the stream info
        stream_url = f"https://api.twitch.tv/helix/streams?user_id={channel_id}"
        stream_response = requests.get(stream_url, headers=headers)
        stream_response.raise_for_status()
        stream_info = json.loads(stream_response.text)["data"][0]

        await ctx.send(f"Stream info for {channel}: {stream_info}")
    except Exception as e:
        logging.error(f"Error in stream_info command: {e}")
        await ctx.send(f"Failed to get stream info for {channel}!")

@bot.command()
async def help(ctx):
    help_text = """
    Available commands:
    /botfollow <number> <channel> - Follow a channel with a specified number of followers.
    /botview <number> <channel> - View a channel with a specified number of views.
    /unfollow <channel> - Unfollow a specified channel.
    /follower_count <channel> - Get the follower count of a specified channel.
    /stream_info <channel> - Get the stream info of a specified channel.
    /botchat <message> <optionalmessage1> <optionalmessage2> <optionalmessage3> <channel> - Spam the chat with messages.
    """
    await ctx.send(help_text)

bot.run(discord_token)