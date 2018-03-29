from discord.ext.commands import Bot
import discord
import sys, traceback

TOKEN = "NDIyNDUxODc2Njc2NTAxNTA0.DY76Ow.GTLxwe-erRJawO0ESOnZrFDmlns"

bot = Bot(command_prefix='/')

initial_extensions = ['cogs.basic']

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
        print(f'Loaded {extension}')
    except Exception as e:
        print("Failed to load extension {extension}.", file=sys.stderr)
        traceback.print_exc()

@bot.event
async def on_ready():

    print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(game=discord.Game(name='Cogs Test'))
    print("Successfully logged in and booted...")

bot.run(TOKEN, bot=True, reconnect=True)
