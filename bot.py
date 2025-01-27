import os
import discord
from discord.ext import commands

# Enable intents for tracking voice states and members
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True  # Needed for kick permissions

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs (Replace with actual values)
GUILD_ID = 722047722311516201  # Your Discord server ID
MUSIC_BOT_ID = 412347257233604609  # Jockie Music bot's ID
TARGET_USER_ID = 192010521363349504  # Pancua's ID

# Toggle state (default: enabled)
kicking_enabled = True

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="togglekick")
@commands.has_permissions(administrator=True)  # Only admins can use it
async def toggle_kicking(ctx):
    global kicking_enabled
    kicking_enabled = not kicking_enabled  # Toggle state
    status = "enabled" if kicking_enabled else "disabled"
    await ctx.send(f"Auto-kick feature is now **{status}**.")

@bot.event
async def on_voice_state_update(member, before, after):
    """Triggers when a user joins, leaves, or changes voice state"""
    global kicking_enabled

    if not kicking_enabled:
        return  # Don't do anything if the feature is disabled

    if member.id == TARGET_USER_ID and after.channel:  # If Pancua joins a channel
        guild = bot.get_guild(GUILD_ID)
        if guild:
            jockie = guild.get_member(MUSIC_BOT_ID)
            if jockie and jockie.voice and jockie.voice.channel == after.channel:
                try:
                    await jockie.kick(reason=f"Kicked because {member.name} joined.")
                    print(f"Kicked Jockie Music because {member.name} joined {after.channel.name}.")
                except discord.Forbidden:
                    print("Bot does not have permission to kick Jockie Music!")
                except Exception as e:
                    print(f"Error: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))  # Use environment variable for security
