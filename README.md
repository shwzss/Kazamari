# TWITCH FOLLOW BOT WITH DISCORD BOT INTEGRATION

## THIS IS STILL IN BETA SO DONT GET TOO EXICTED ABOUT THIS WORKING, BUGS CAN HAPPEN.

### THIS CODE IS FOR EDUCATIONAL PURPOSES ONLY

To use this code, follow these steps:

Install Required Libraries: Ensure you have the required libraries installed. You can install them using pip:

Replace API Keys and Tokens: Replace the placeholder values for twitch_client_id, twitch_client_secret, twitch_token, and discord_token with your actual API keys and tokens.

Run the Bot: Save the code to a file, for example, followbot.py, and run it using Python:

Set Up Channels and Roles: The bot will automatically create channels for each role under a category called "Twitch" when it starts. Ensure you have the roles "free", "basic", "super", "astronomic", and "massive" set up in your Discord server.

Make sure to replace "Your Server Name" with the name of your Discord server and the placeholder API keys and tokens with your actual values.

## Commands

/botfollow <number> <channel>: Follow a channel with a specified number of followers. Restricted to roles "basic", "super", "astronomic", and "massive".
/botview <number> <channel>: View a channel with a specified number of views. Restricted to roles "super", "astronomic", and "massive".
/unfollow <channel>: Unfollow a specified channel. Restricted to roles "basic", "super", "astronomic", and "massive".
/follower_count <channel>: Get the follower count of a specified channel. Available to all users.
/stream_info <channel>: Get the stream info of a specified channel. Available to all users.
/botchat <message> <optionalmessage1> <optionalmessage2> <optionalmessage3> <channel>: Spam the chat with messages. Restricted to roles "astronomic" and "massive".

# I AM NOT LIABLE FOR ANY BANS OR DAMAGES USED IN THIS CODE. ASSUMING YOUR A SCRIPT KIDDIE, YOU ARE LIABLE FOR ANY DAMAGES USING THIS CODE.