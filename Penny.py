import discord
import random
import asyncio
from discord.ext import commands

TOKEN = '...Your token'   #replace with your bot token
GUILD_ID = 123456  #replace with your server id
CHANNEL_ID = 123456  #replace with your channel id
MAX_MESSAGE = 5

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

message_count = 0
player_scores = {}

# Bollywood funny dialogues
funny_dialogues = [
    "Basanti, in kutto ke samne mat nachna!",
    "Tera kya hoga Kalia?",
    "Aata majhi satakli!",
    "Mogambo khush hua!",
    "Dosti ka ek usool hai madam, no sorry no thank you."
]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    global message_count
    
    if message.author == bot.user:
        return
    
    if message.channel.id == CHANNEL_ID:
        message_count += 1
        
        if message_count >= MAX_MESSAGE:
            message_count = 0  # Reset counter
            await drop_surprise_box(message.channel)
    
    await bot.process_commands(message)

async def drop_surprise_box(channel):
    embed = discord.Embed(
        title="🎁 Surprise Box Dropped! 🎁",
        description="React first to claim the box!",
        color=discord.Color.gold()
    )
    
    msg = await channel.send(embed=embed)
    
    # Use the custom emoji :surprise: (replace with actual emoji ID if necessary)
    emoji_name = 'surprise'  # The name of your custom emoji, without colons.
    emoji = discord.utils.get(channel.guild.emojis, name=emoji_name)  # Fetch custom emoji

    if emoji:
        await msg.add_reaction(emoji)  # Add custom emoji as reaction
    else:
        await msg.add_reaction("🎁")  # Fallback to the default 🎁 emoji if the custom emoji is not found
    
    def check(reaction, user):
        return reaction.message.id == msg.id and (reaction.emoji == emoji or str(reaction.emoji) == "🎁" )and not user.bot
    
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
        result = random.choice(["flower", "fool"])
        
        if result == "flower":
            points = 10
            player_scores[user.id] = player_scores.get(user.id, 0) + points
            await channel.send(f"🌸 {user.mention} received a flower! (+10 points)")
        else:
            dialogue = random.choice(funny_dialogues)
            await channel.send(f"🤣 {user.mention} got fooled! {dialogue}")
        
    except asyncio.TimeoutError:
        await channel.send("No one claimed the surprise box! 🎁")

@bot.command()
async def leaderboard(ctx):
    if not player_scores:
        await ctx.send("No one has collected any flowers yet!")
        return
    
    sorted_leaderboard = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
    embed = discord.Embed(title="🌸 Leaderboard 🌸", color=discord.Color.green())
    
    for user_id, points in sorted_leaderboard[:10]:
        user = await bot.fetch_user(user_id)
        embed.add_field(name=user.name, value=f"{points} points", inline=False)
    
    await ctx.send(embed=embed)

bot.run(TOKEN)
