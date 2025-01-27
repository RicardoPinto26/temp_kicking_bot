import os
import discord
from discord.ext import commands

# Enable intents
intents = discord.Intents.default()
intents.voice_states = True  # Needed for tracking voice channel changes
intents.guilds = True
intents.members = True  # Required to detect users
intents.message_content = True  # Required for sending commands

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs (Replace with actual values)
GUILD_ID = 722047722311516201  # Your Discord server ID
MUSIC_BOT_ID = 412347257233604609  # Jockie Music bot's ID
TARGET_USER_ID = 363016885325004800  # Pancua's ID

# Toggle state (default: enabled)
pause_enabled = True

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="togglepause")
@commands.has_permissions(administrator=True)  # Only admins can use it
async def toggle_pause(ctx):
    global pause_enabled
    pause_enabled = not pause_enabled  # Toggle state
    status = "enabled" if pause_enabled else "disabled"
    await ctx.send(f"Auto-pause feature is now **{status}**.")

async def send_as_webhook(channel, message):
    """Creates a temporary webhook to send the message"""
    try:
        webhook = await channel.create_webhook(name="Music Control Webhook")
        await webhook.send(content=message, username="Pancua")
        await webhook.delete()
    except Exception as e:
        print(f"Error creating webhook: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    """Triggers when a user joins, leaves, or changes voice state"""
    global pause_enabled

    if not pause_enabled:
        return  # Don't do anything if the feature is disabled

    if member.id == TARGET_USER_ID and after.channel:  # If Pancua joins a channel
        guild = bot.get_guild(GUILD_ID)
        if guild:
            jockie = guild.get_member(MUSIC_BOT_ID)
            if jockie and jockie.voice and jockie.voice.channel == after.channel:
                try:
                    # Find a text channel where the bot can send the message
                    text_channel = discord.utils.get(guild.text_channels, name="lixo-do-bot-privado")  # Change to actual channel name

                    if not text_channel:
                        text_channel = after.channel.guild.system_channel  # Use default system channel if no specific channel

                    if text_channel:
                        await send_as_webhook(text_channel, "m!pause")  # Send message via webhook
                        print(f"Sent 'm!pause' via webhook because {member.name} joined {after.channel.name}.")
                except Exception as e:
                    print(f"Error sending m!pause: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # Use environment variable for security
