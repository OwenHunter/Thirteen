import discord
from discord.ext.commands import Bot
from cogs.games import games
from cogs.testing import testing
from config import TOKEN, PREFIX

intents = discord.Intents.default()
intents.members = True

bot = Bot(command_prefix=PREFIX, status=discord.Status.dnd, intents=intents)

bot.activity=discord.Activity(name="?", type=discord.ActivityType.listening)

loopStop = False
interestCheckMessage = []

bot.add_cog(games(bot, interestCheckMessage))
bot.add_cog(testing(bot, loopStop))
bot.add_cog()

@bot.event
async def on_ready():
	print("Logged in as " + bot.user.name + "\n")
           
@bot.event
async def on_message(message):
	await bot.process_commands(message)
	if not message.content.startswith("?"):
		if "hey 13" in str(message.content).lower() or "hey thirteen" in str(message.content).lower():
			channel = message.channel
			await channel.send("Hey " + message.author.mention)

class customHelp(discord.ext.commands.HelpCommand):
    def __init__(self, bot):
        self.bot = bot

    # ?help
    async def send_bot_help(self, mapping):
        return await self.context.send("Main help command")

    # ?help <command>
    async def send_command_help(self, command):
        return await self.context.send("Command help command")

    #!help <group>
    async def send_group_help(self, group):
        return await self.context.send("Group help command")

    #!help <cog>
    async def send_cog_help(self, cog):
        return await self.context.send("Cog help command")

bot.help_command = customHelp()

bot.run(TOKEN)