from discord.ext.commands import Bot
import discord
import sys, traceback
import configparser

configParser = configparser.RawConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)

TOKEN = configParser.get('api-config', 'token')

prefix = '.'
bot = Bot(command_prefix=prefix)

channel_chat = 420283899134869504
channel_memes = 420284036037083137
channel_homework = 388362227876495362
channel_pictures = 373092289335263237
channel_music = 400329717372289046

initial_extensions = ['cogs.basic', 'cogs.lol', 'cogs.csgo']

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

    await bot.change_presence(game=discord.Game(name= prefix + 'help'))
    print(f'Logged in and booted...\n\nHistory:')



bot.run(TOKEN, bot=True, reconnect=True)
