import discord
import asyncio
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!',intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('a game!'))
    print("---------------------")
    print(" Bot is now online!")
    try:
        synced = await client.tree.sync()
        print(f" Synced {len(synced)} command(s)")
        print("---------------------")
    except Exception as e:
        print(e)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.event
async def on_member_join(user):
    channel = client.get_channel(YOUR_WELCOME_CHANNEL_HERE)
    embed = discord.Embed(title=f"{user.name} has joined the server", description=f"Welcome! Please make sure to read the rules! :grin:", color=0xffffff)
    embed.set_thumbnail(url=f"{user.avatar}")
    await channel.send(f"||{user.mention}||", embed=embed)
    print(f"\n [+] {user.name} has joined the server.\n")

@client.event
async def on_member_remove(user):
    channel = client.get_channel(YOUR_WELCOME_CHANNEL_HERE)
    embed = discord.Embed(title=f"{user.name} has left the server", description=f"We will miss you. :cry:", color=0xffffff)
    embed.set_thumbnail(url=f"{user.avatar}")
    await channel.send(embed=embed)
    print(f"\n [-] {user.name} has left the server.\n")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command()
async def add(ctx, x, y):
    result = int(x) + int(y)
    async with ctx.typing():
        await asyncio.sleep(2)
    await ctx.send(f"I'm great at addition! :nerd:\n**{x} + {y} = {result}**")

@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Hello World!", description="I just sent a embed! :smile:", color=0xffffff)
    embed.set_image(url="https://images.squarespace-cdn.com/content/v1/5b9d7475ee17598034564bb6/1593378100071-V2YV3MD2O0H893KU0PR9/image-asset.jpeg")
    async with ctx.typing():
        await asyncio.sleep(1)
    await ctx.send(embed=embed)

#@client.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.MissingRequiredArgument):
#        embed = discord.Embed(title="Error :x:", description="Invalid arguments. :(", color=0xff1100)
#        embed.set_thumbnail(url="https://www.cesarsway.com/wp-content/uploads/2019/10/warning-signs-of-dog-depression-cesars-way.jpg")
#        async with ctx.typing():
#            await asyncio.sleep(1)
#        await ctx.send(embed=embed)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.tree.command(name="slashcmd", description="Just a slash command test")
async def slashcmd(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!")

@client.tree.command(name="commands", description="List of all my commands")
async def commands(interaction: discord.Interaction):
    await interaction.response.send_message("**Command List**\n```--- Slash Commands - Normal commands ---\n/commands - This command!\n/add (x y) - Add two numbers together\n/embed - Just a embed slash command test\n/slashcmd - Test out a slash command\n\n--- Custom Commands - Wacky custom commands ---\n!embed - Sends a embed message\n!add (x y) - Adds two numbers together\n\nThats all the commands I can do at the moment.```", ephemeral=True)

@client.tree.command(name="add", description="Add two numbers together")
@app_commands.describe(x = "First number", y = "Second number")
async def add(interaction: discord.Interaction, x: str, y:str):
    result = int(x) + int(y)
    await interaction.response.send_message(f"I'm great at addition! :nerd:\n**{x} + {y} = {result}**")

@client.tree.command(name="embed", description="Just a embed slash command test")
async def embed(interaction: discord.Interaction):
    embed = discord.Embed(title="Hello World!", description="I just sent a embed with a slash command! :smile:", color=0xffffff)
    embed.set_image(url="https://pbs.twimg.com/media/CFUWhV7W8AI3e3D.jpg")
    await interaction.response.send_message(embed=embed)

# Enter your bot token in here
client.run('YOUR_BOT_TOKEN_HERE')