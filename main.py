from discord.ext.commands import Bot
import discord
import sys, traceback
import configparser

configParser = configparser.RawConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)

TOKEN = configParser.get('api-config', 'token')

bot = Bot(command_prefix='.')

initial_extensions = ['cogs.basic', 'cogs.lol']

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
        print(f'Loaded {extension}')
    except Exception as e:
        print("Failed to load extension {extension}.", file=sys.stderr)
        traceback.print_exc()

@bot.event
async def on_ready():

    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(game=discord.Game(name='.help'))
    print(f'Successfully logged in and booted...\n\nHistory:')


bot.run(TOKEN, bot=True, reconnect=True)
