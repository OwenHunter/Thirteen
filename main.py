import discord
import random
import time
import asyncio
import requests
import json
from datetime import date, timedelta
from discord.ext.commands import Bot
from config import TOKEN

bot = Bot(command_prefix="?", status=discord.Status.dnd, activity=discord.Activity(name="?", type=discord.ActivityType.watching))

loopStop = False

@bot.event
async def on_ready():
	print("Logged in as " + bot.user.name)

@bot.command(name="chad")
async def chad(context):
	await context.message.delete()
	if "13hunteo" not in str(context.message.author):
		await context.send(context.message.author.mention + random.choice([" is not a chad. :rofl: :rofl: :rofl:", " is a chad. :sunglasses: :sunglasses: :sunglasses: "]))
	else:
		await context.send(context.message.author.mention + " is an epic gamer. :sunglasses: :sunglasses: :sunglasses: :sunglasses: :sunglasses: ")

@bot.command(name="chungus")
async def chungus(context):
	await context.message.delete()
	await context.send(context.message.author.mention + " Chungus is " + f"{random.randint(1, 50)} feet and {random.randint(1, 12)} inches tall.")
	await context.send(f"His penis is {random.randint(5, 20)} feet long.")

@bot.command(name="spam")
async def spam(context, user:discord.Member):
	count = 0
	bot.loop.create_task(channel_rename(context.message.channel, count))

	while not loopStop:
		await context.send(user.mention)
		count += 1
		await asyncio.sleep(.5)

@bot.command(name="announce")
async def announce(context, *, message=None):
	calendar_events = requests.get("https://www.googleapis.com/calendar/v3/calendars/c2dn00h57qr69k3p732seqsai0@group.calendar.google.com/events?key=AIzaSyDyIYb-wPcMJeCmdO9dcLq_8DIQ5qAewJ4")
	***REMOVED***

	sdate = date.today()
	edate = sdate + timedelta(days=365)
	delta = edate - sdate

	next_date = None

	for i in range(delta.days + 1):
		day = sdate + timedelta(days=i)
		if day.weekday() == 0 or day.weekday() == 2:
			if day != date.today():
				next_date = day
				break
	
	peopleNotHere = []
	for item in json.loads(calendar_events.content)["items"]:
		sDate = date.fromisoformat(item["start"]["date"])
		eDate = date.fromisoformat(item["end"]["date"])
		delta = eDate - sDate

		for i in range(delta.days + 1):
			day = sDate + timedelta(days = i)
			if day == next_date:
				peopleNotHere.append(people.get(item["creator"]["email"]))
	
	peopleNotHere_message = ""
	for person in peopleNotHere:
		peopleNotHere_message += person + ", "
	if peopleNotHere_message != "":
		peopleNotHere_message = peopleNotHere_message[:-2]

	await context.message.delete()
	await context.send("@everyone")

	embedVar = discord.Embed(title="Next Session", colour=discord.Colour.red())
	embedVar.add_field(name="Date:", value=next_date.strftime("%A %d") + " " + next_date.strftime("%B"))
	embedVar.add_field(name="Time:", value="1:30 PM")
	if message != None:
		embedVar.add_field(name="Comment:", inline=False, value=message)
	if peopleNotHere != []:
		embedVar.add_field(name="Not Here:", inline=False, value=peopleNotHere_message)
	await context.send(embed=embedVar)

async def channel_rename(channel, count):
	time.sleep(20)
	await channel.edit(name = str(count))

@bot.command(name="kilall")
async def stopLoops(context):
	global loopStop
	loopStop = True

	await context.send("All loops halted.")

@bot.command(name="logout")
async def leavePlease(context):
	if "13hunteo" in str(context.message.author):
		await context.send("Logging out...")
		await bot.close()
	else:
		await context.send("You do not have the permissions to do that...")

@bot.event
async def on_message(message):
	await bot.process_commands(message)
	if not message.content.startswith("?"):
		if "goose" in str(message.content).lower() and message.author != bot.user:
			channel = message.channel
			await channel.send("HONK", tts=True, delete_after=True)
			await channel.send("***HONK***")
			await channel.send(file=discord.File('honk.png'))
		if "hey 13" in str(message.content).lower() or "hey thirteen" in str(message.content).lower():
			channel = message.channel
			await channel.send("Hey " + message.author.mention)
		if ("mins" in str(message.content).lower() or "minutes" in str(message.content).lower() or "minute" in str(message.content).lower()) and (message.author.id == 250658105052889089) and (message.channel.id == 691694856350990409):
			await message.channel.send("cOfFeE")
			await message.channel.send(file=discord.File("coffee.jpg"))

bot.run(TOKEN)
