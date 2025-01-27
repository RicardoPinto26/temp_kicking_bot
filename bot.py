import os
import discord
from discord.ext import commands

# Enable intents
intents = discord.Intents.default()
intents.voice_states = True  # Required for tracking voice channel changes
intents.guilds = True
intents.members = True  # Required for disconnecting users
intents.message_content = True  # Required for processing commands

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs (Replace with actual values)
GUILD_ID = 722047722311516201  # Your Discord server ID
MUSIC_BOT_ID = 412347257233604609  # Jockie Music bot's ID
TARGET_USER_ID = 192010521363349504  # Pancua's ID

# Toggle state (default: enabled)
disconnecting_enabled = True

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="toggledisconnect")
@commands.has_permissions(administrator=True)  # Only admins can use it
async def toggle_disconnect(ctx):
    global disconnecting_enabled
    disconnecting_enabled = not disconnecting_enabled  # Toggle state
    status = "enabled" if disconnecting_enabled else "disabled"
    await ctx.send(f"Auto-disconnect feature is now **{status}**.")

@bot.event
async def on_voice_state_update(member, before, after):
    """Triggers when a user joins, leaves, or changes voice state"""
    global disconnecting_enabled

    if not disconnecting_enabled:
        return  # Don't do anything if the feature is disabled

    if member.id == TARGET_USER_ID and after.channel:  # If Pancua joins a channel
        guild = bot.get_guild(GUILD_ID)
        if guild:
            jockie = guild.get_member(MUSIC_BOT_ID)
            if jockie and jockie.voice and jockie.voice.channel == after.channel:
                try:
                    await jockie.move_to(None)  # Disconnect Jockie Music from voice
                    print(f"Disconnected Jockie Music because {member.name} joined {after.channel.name}.")
                except discord.Forbidden:
                    print("Bot does not have permission to disconnect Jockie Music!")
                except Exception as e:
                    print(f"Error: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # Use environment variable for security
