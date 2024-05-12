import discord
from discord.ext import commands
from datetime import datetime, timezone

# Define the intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Crucial for accessing guild members
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Guild and role IDs
YOUR_GUILD_ID = 1154207161258344458
ACTIVITY_CHECK_ROLE_ID = 1180418781105901590
ACTIVE_MEMBER_ROLE_ID = 1235429432324526090
GSTRP_OWNERSHIP_ID = 1154207161367412779
GSTRP_CO_OWNERSHIP_ID = 1168287636440486018
TECC_ID = 1154207161270935671
MESSAGE_ID_1 = 1235426569233764363
MESSAGE_ID_2 = 1235426570234764364
CHANNEL_ID = 1155249848036114472
AUDIT_CHANNEL_ID = 1154207163175141393

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    await manage_roles()

async def manage_roles():
    guild = await bot.fetch_guild(YOUR_GUILD_ID)
    if guild is None:
        print("Guild not found.")
        return

    activity_check_role = guild.get_role(ACTIVITY_CHECK_ROLE_ID)
    active_member_role = guild.get_role(ACTIVE_MEMBER_ROLE_ID)

    # Reset roles
    print("Resetting roles for all members...")
    async for member in guild.fetch_members(limit=None):
        try:
            await member.remove_roles(activity_check_role, active_member_role)
            print(f'Removed roles from {member.display_name}')
        except Exception as e:
            print(f"Failed to remove roles from {member.display_name}: {e}")

    # Assign activity check role
    print("Assigning Activity Check role to all members...")
    async for member in guild.fetch_members(limit=None):
        try:
            await member.add_roles(activity_check_role)
            print(f'Assigned Activity Check role to {member.display_name}')
        except Exception as e:
            print(f"Failed to assign Activity Check role to {member.display_name}: {e}")

    # Process reactions for both messages and assign active member role
    await process_reactions(guild, MESSAGE_ID_1)
    await process_reactions(guild, MESSAGE_ID_2)

async def process_reactions(guild, message_id):
    channel = guild.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Failed to find channel with ID: {CHANNEL_ID}")
        return

    try:
        message = await channel.fetch_message(message_id)
        for reaction in message.reactions:
            async for user in reaction.users():
                if user != bot.user:
                    member = guild.get_member(user.id)
                    if member:
                        try:
                            await member.remove_roles(guild.get_role(ACTIVITY_CHECK_ROLE_ID))
                            await member.add_roles(guild.get_role(ACTIVE_MEMBER_ROLE_ID))
                            print(f'Updated roles for {member.display_name}')
                        except Exception as e:
                            print(f'Error updating roles for {member.display_name}: {e}')
    except Exception as e:
        print(f"Failed to fetch message with ID: {message_id} from channel: {CHANNEL_ID} - {e}")

async def count_and_print_roles(guild, message_prefix=''):
    activity_check_role = guild.get_role(ACTIVITY_CHECK_ROLE_ID)
    active_member_role = guild.get_role(ACTIVE_MEMBER_ROLE_ID)
    activity_check_count = 0
    active_member_count = 0
    
    async for member in guild.fetch_members(limit=None):
        if activity_check_role in member.roles:
            activity_check_count += 1
        if active_member_role in member.roles:
            active_member_count += 1

    audit_channel = guild.get_channel(AUDIT_CHANNEL_ID)
    await audit_channel.send(f'{message_prefix} Number of members with Activity Check role: {activity_check_count}, Active Member role: {active_member_count}')

# Command: Audit - to display member counts in a specific channel
@bot.command()
async def hr(ctx):
    if ctx.channel.id == AUDIT_CHANNEL_ID:
        await count_and_print_roles(ctx.guild, 'HR Audit:')

bot.run('MTIzNTQyNDMyODU5NDYyMDQ4Nw.GOvwZG.JMcIqrmd4wxAHaefGLMdSsVcgJobzPYMBigDEw')  # Replace with your actual token










