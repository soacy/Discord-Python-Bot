import discord, datetime, random, urllib.parse
from discord import app_commands
from discord.ext import commands

token = "YOUR_DISCORD_BOT_TOKEN" # Replace with your bot token
prefix = "!" # Your command prefix for moderation commands

intents = discord.Intents.all()
intents.members = True

mimic_target = None

client = commands.Bot(command_prefix=prefix,intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('https://github.com/soacy/'))
    print("----------------------")
    print(" Bot is now online!")
    try:
        synced = await client.tree.sync()
        print(f" Synced {len(synced)} command(s)")
        print("----------------------")
    except Exception as e:
        print(e)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Welcome Section
# Just sending a welcome message / leave message

@client.event
async def on_member_join(user, guild):
    channel = client.get_channel(YOUR_WELCOME_CHANNEL) # Replace YOUR_WELCOME_CHANNEL with your welcome channel id
    embed = discord.Embed(title=f"{user.name} has joined {guild}", description=f"Welcome! Please make sure to read the #info channel! :grin:", color=0xffffff)
    embed.set_thumbnail(url=f"{user.avatar}")
    await channel.send(f"||{user.mention}||", embed=embed)
    print(f"\n [+] {user.name} has joined the server.\n")

    role = discord.utils.get(user.guild.roles, id=1204899615350984714)
    await user.add_roles(role)

    welcome_channel = client.get_channel(YOUR_GENERAL_CHANNEL) # Replace YOUR_GENERAL_CHANNEL with your general channel id
    await welcome_channel.send(f"{user.name} has joined {guild}. Everyone please welcome them!")
    print(f" [i] Sucessfully gave {user.name} their role!\n")

@client.event
async def on_member_remove(user, guild):
    channel = client.get_channel(YOUR_WELCOME_CHANNEL) # Replace YOUR_WELCOME_CHANNEL with your welcome channel id
    embed = discord.Embed(title=f"{user.name} has left {guild}", description=f"We will miss you.\nI am now very sad :cry:", color=0xffffff)
    embed.set_thumbnail(url=f"{user.avatar}")
    await channel.send(embed=embed)
    print(f"\n [-] {user.name} has left the server.\n")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Moderation Section
# All of these commands go off of the role "*". You can change that to your moderation roles name.

@client.command() # Ban Command
@commands.has_role("*")
async def ban(ctx, member:discord.Member, *, reason):
    if reason == None:
        reason = "This user was banned by " + ctx.message.author.name
    await member.ban(reason=reason)

@client.command() # Kick Command
@commands.has_role("*")
async def kick(ctx, member:discord.Member, *, reason):
    if reason == None:
        reason = "This user was kicked by " + ctx.message.author.name
    await member.kick(reason=reason)

@client.command() # Mute Command
@commands.has_role("*")
async def mute(ctx, member:discord.Member, timelimit):
    if "s" in timelimit:
        gettime = timelimit.strip("s")
        if int(gettime) > 2419000:
            await ctx.send("The mute time amount cannot be bigger than 28 days")
        else:
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    if "m" in timelimit:
        gettime = timelimit.strip("m")
        if int(gettime) > 40320:
            await ctx.send("The mute time amount cannot be bigger than 28 days")
        else:
            newtime = datetime.timedelta(minutes=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    if "h" in timelimit:
        gettime = timelimit.strip("h")
        if int(gettime) > 672:
            await ctx.send("The mute time amount cannot be bigger than 28 days")
        else:
            newtime = datetime.timedelta(hours=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    if "d" in timelimit:
        gettime = timelimit.strip("d")
        if int(gettime) > 28:
            await ctx.send("The mute time amount cannot be bigger than 28 days")
        else:
            newtime = datetime.timedelta(days=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    if "w" in timelimit:
        gettime = timelimit.strip("w")
        if int(gettime) > 4:
            await ctx.send("The mute time amount cannot be bigger than 4 weeks")
        else:
            newtime = datetime.timedelta(weeks=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    
@client.command() # Unmute Command
@commands.has_role("*")
async def unmute(ctx, member:discord.Member):
    await member.edit(timed_out_until=None)
    await ctx.send(f"Unmuted {member}.")

@client.command() # Poll Command
@commands.has_role("*")
async def poll(ctx, question, *options):
    if len(options) <= 1:
        await ctx.send("You need to provide at least 2 options for the poll.")
        return

    if len(options) > 10:
        await ctx.send("You can provide up to 10 options for the poll.")
        return

    poll_message = f"**{question}**\n\n"
    for i, option in enumerate(options):
        poll_message += f":regional_indicator_{chr(97 + i)}: {option}\n"

    poll_embed = discord.Embed(title="Poll", description=poll_message, color=discord.Color.blue())
    poll_embed.set_footer(text=f"Poll created by {ctx.author.display_name}")
    poll_msg = await ctx.send(embed=poll_embed)

    for i in range(len(options)):
        await poll_msg.add_reaction(chr(127462 + i))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Info Section
# Just /information command stuff

class InfoMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Bot Information", style=discord.ButtonStyle.blurple) # Bot info button
    async def botinfo(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=":robot: About Your Bot", description="Put whatever you want here! This will be like information about your discord bot.", color=0xffffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Server Information", style=discord.ButtonStyle.blurple) # Server info button
    async def serverinfo(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=":desktop: About Your Server", description="Put whatever you want here! This will be like information about your server.", color=0xffffff)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="information", description="Opens the information panel") # Information Command
async def information(interaction: discord.Interaction):
    embed = discord.Embed(title=":information: Information Panel", description=f"Hello {interaction.user.name}! This is the information panel, here you can see more info about the bot, the server!\n\nClick on the buttons below to get started!", color=0xffffff)
    embed.set_thumbnail(url=f"https://i.pinimg.com/736x/a2/58/af/a258afef0a7b9673fe50d3afc4ed7014.jpg")
    view = InfoMenu()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Useful Commands

@client.tree.command(name="commands", description="List of all my commands") # Commands Command
async def commands_(interaction: discord.Interaction):
    embed = discord.Embed(title="</> Bot Commands", description=f"Hello there! This is a list of all the commands that I can do!", color=0xffffff)
    embed.add_field(name="Useful Commands", value=f"/information - All the info you need!\n/commands - This command!\n/sourcecode - Bot source code")
    embed.add_field(name="Other Commands", value=f"/add (x) (y) - Add two numbers\n/subtract (x) (y) - Subtract two numbers\n/multiply (x) (y) - Multiply tow numbers\n/divide (x) (y) - Divide two numbers\n/ping - Check your latency\n/gaypercentage (user) - See how gay someone is\n/diceroll - Roll a dice!\n/eightball - Magic eightball\n/google (prompt) - Google something\n/mimic (user) - Mimic someone\n/mimicstop - Stop mimicing someone")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.tree.command(name="sourcecode", description="Source Code for @soacy's discord bot") # Source Code Command
async def sourcecode(interaction: discord.Interaction):
    await interaction.response.send_message(f"**Here is my souce code!**\n*https://github.com/soacy/Discord-Python-Bot*\n\nIt will be updated soon!", ephemeral=True)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Other Commands

@client.tree.command(name="add", description="Add two numbers together") # Add Command
@app_commands.describe(x = "First number", y = "Second number")
async def add(interaction: discord.Interaction, x: str, y:str):
    result = int(x) + int(y)
    await interaction.response.send_message(f"I'm great at addition! :nerd:\n**{x} + {y} = {result}**")

@client.tree.command(name="subtract", description="Subtract two numbers") # Subtract Command
@app_commands.describe(x = "First number", y = "Second number")
async def subtract(interaction: discord.Interaction, x: str, y:str):
    result = int(x) - int(y)
    await interaction.response.send_message(f"I'm great at subtraction! :nerd:\n**{x} - {y} = {result}**")

@client.tree.command(name="multiply", description="Multiply two numbers together") # Multiply Command
@app_commands.describe(x = "First number", y = "Second number")
async def multiply(interaction: discord.Interaction, x: str, y:str):
    result = int(x) * int(y)
    await interaction.response.send_message(f"I'm great at multipication! :nerd:\n**{x} x {y} = {result}**")

@client.tree.command(name="divide", description="Divide two numbers together") # Divide Command
@app_commands.describe(x = "First number", y = "Second number")
async def divide(interaction: discord.Interaction, x: str, y:str):
    result = int(x) / int(y)
    await interaction.response.send_message(f"I'm great at division! :nerd:\n**{x} ÷ {y} = {result}**")

@client.tree.command(name="ping", description="Check bot latency") # Ping Command
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    message = f"🏓 Pong! Latency is {latency}ms."
    await interaction.response.send_message(message)

@client.tree.command(name="gaypercentage", description="See how gay someone is") # Gay % Command
@app_commands.describe(person = "Pick someone to see how gay they are")
async def gaypercentage(interaction: discord.Interaction, person: str):
    await interaction.response.send_message(f"{person} is {random.randrange(101)}% gay...")

@client.tree.command(name="diceroll", description="Feeling Lucky?") # Diceroll Command
async def diceroll(interaction: discord.Interaction):
    dicenumb = ["1", "2", "3", "4", "5", "6"]
    await interaction.response.send_message(f"It's {random.choice(dicenumb)}")

@client.tree.command(name="eightball", description="Ask away, and the eightball shall answer") # Eightball Command
@app_commands.describe(question = "What is your question for the mighty eightball?")
async def eightball(interaction: discord.Interaction, question:str):
    with open("eightball/response.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    await interaction.response.send_message(f"**{interaction.user.name}'s question was:** *{question}*\n\nThe magic eightball says:\n```{response}```")

@client.tree.command(name="google", description="Google something") # Google Command
@app_commands.describe(question = "What is your question for google?")
async def google(interaction: discord.Interaction, question:str):
    question = urllib.parse.quote(question)
    search_url = f"https://www.google.com/search?q={question}"
    
    await interaction.response.send_message(f"Here are the Google search results for '{question}':\n{search_url}")

@client.tree.command(name="mimic", description="Make your bot mimic someone") # Mimic Command
async def mimic(interaction: discord.Interaction, user: discord.User):
    global mimic_target
    mimic_target = user
    await interaction.response.send_message(f"Mimicking {user.display_name} >:)")

@client.tree.command(name="mimicstop", description="Make your bot stop mimicing someone") # Mimic Stop Command
async def mimicstop(interaction: discord.Interaction):
    global mimic_target
    mimic_target = None
    await interaction.response.send_message("Mimic stopped.")

@client.listen() # Mimic command code
async def on_message(message):
    global mimic_target

    if message.author == client.user:
        return

    if mimic_target is not None and message.author == mimic_target:
        await message.channel.send(message.content)

    await client.process_commands(message)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

client.run(token)