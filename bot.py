from discord.ext.commands import Bot
import discord
import random

BOT_PREFIX = "/"
TOKEN = "NDIyNDUxODc2Njc2NTAxNTA0.DY76Ow.GTLxwe-erRJawO0ESOnZrFDmlns"

client = Bot(command_prefix=BOT_PREFIX)
role = discord.utils.get(server.roles, name="Good People")


@client.command(name='8ball', description="Answers a yes/no question.", brief="Answers from the beyond", pass_context = True)
async def eight_ball(context):
	possible_responses = [
		'That is a resounding no',
		'It is not looking likely',
		'Too hard to tell',
		'It is quite possible',
		'Definitely',
	]
	random_choice = random.choice(possible_responses)
	await client.say(random_choice + ", " + context.message.author.mention)
	print("eight ball " + random_choice)

@client.command(name='square', description="Squares a number inputted by the user", brief="Squares a number", pass_context = True)
async def square(context, number):
	squared_number = int(number) * int(number)
	await client.say("The answer is " + str(squared_number) + ", " + context.message.author.mention)
	print("square " + str(squared_number))

@client.event
async def on_ready():
	await client.edit_profile(password=None, username="TheBestBot")
	print("Logged in as " + client.user.name)
	print(role)

client.run(TOKEN)
