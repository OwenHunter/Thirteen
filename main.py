import discord
from discord.ext.commands import Bot
from cogs.games import games
from cogs.testing import testing
from config import TOKEN

intents = discord.Intents.default()
intents.members = True

bot = Bot(command_prefix="?", status=discord.Status.dnd, intents=intents)

bot.activity=discord.Activity(name="?", type=discord.ActivityType.listening)

loopStop = False
interestCheckMessage = []

bot.add_cog(games(bot, interestCheckMessage))
bot.add_cog(testing(bot, loopStop))

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

bot.run(TOKEN)