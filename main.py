import discord
import random
import time
import asyncio
import requests
import json
from datetime import date, timedelta
from discord.ext.commands import Bot
from config import TOKEN, people, gcal_key

intents = discord.Intents.all()
bot = Bot(command_prefix="?", status=discord.Status.dnd, activity=discord.Activity(name="?", type=discord.ActivityType.watching), intents=intents)

loopStop = False
interestCheckMessage = ""
interestCheckEmbed = None

@bot.event
async def on_ready():
	print("Logged in as " + bot.user.name)

@bot.command(name="dnd.announce")
async def dndannounce(context, *, message=None):
	calendar_events = requests.get(f"https://www.googleapis.com/calendar/v3/calendars/c2dn00h57qr69k3p732seqsai0@group.calendar.google.com/events?key={gcal_key}")

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

@bot.command(name="killall")
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

@bot.command(name="InterestCheck")
async def interestCheck(context, game = None, time=None):
    if time != None and game != None:
        global interestCheckMessage, interestCheckEmbed
        
        await context.send("@everyone")
        embedMsg = discord.Embed(title=f"{game} at {time}?", colour=discord.Colour.red())
        embedMsg.add_field(name="Yes: ", value=0)
        embedMsg.add_field(name="No: ", value=0)

        interestCheckEmbed = embedMsg
        
        interestCheckMessage = await context.send(embed=embedMsg)
        await interestCheckMessage.add_reaction("\U0001F44D")
        await interestCheckMessage.add_reaction("\U0001F44E")
    elif time == None:
        await context.send("Please input a time to play.")
    elif game == None:
        await context.send("Please input the game.")

@bot.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    if msg == interestCheckMessage and user.name != "thirteen":
        yesCount = int(interestCheckEmbed.fields[0].value)
        noCount = int(interestCheckEmbed.fields[1].value)
        if len(interestCheckEmbed.fields) == 2:
            playingString = ""
        else:
            playingString = interestCheckEmbed.fields[2].value

        if reaction.emoji == "\U0001F44D":
            yesCount += 1
            playingString += ", " + user.name
        elif reaction.emoji =="\U0001F44E":
            noCount += 1

        interestCheckEmbed.set_field_at(0, name="Yes: ", value=yesCount)
        interestCheckEmbed.set_field_at(1, name="No: ", value=noCount)

        if playingString != "" and len(interestCheckEmbed.fields) == 2:
            playingString = playingString[2:]
            interestCheckEmbed.add_field(name="Playing: ", value=playingString, inline=False)
        elif playingString != "":
            interestCheckEmbed.set_field_at(2, name="Playing: ", value=playingString, inline=False)
        elif len(interestCheckEmbed.fields) != 2:
            interestCheckEmbed.remove_field(2)

        await msg.edit(embed=interestCheckEmbed)

@bot.event
async def on_reaction_remove(reaction, user):
    msg = reaction.message
    if msg == interestCheckMessage:
        if reaction.emoji == "\U0001F44D":
            interestCheckEmbed.set_field_at(0, name="Yes: ", value=int(interestCheckEmbed.fields[0].value)-1)
            
            if len(interestCheckEmbed.fields) != 2:
                playingString = interestCheckEmbed.fields[2].value
                if user.name in playingString:
                    playingString = playingString.replace(", " + user.name, "")
                    playingString = playingString.replace(user.name, "")
                    
                    if playingString[-2:] == ", ":
                        playingString = playingString[:-2]
                    if playingString[:2] == ", ":
                        playingString = playingString[2:]
                if playingString != "":
                    interestCheckEmbed.set_field_at(2, name="Playing: ", value=playingString, inline=False)
                else:
                    interestCheckEmbed.remove_field(2)
        elif reaction.emoji == "\U0001F44E":
            interestCheckEmbed.set_field_at(1, name="No: ", value=int(interestCheckEmbed.fields[1].value)-1)

        await msg.edit(embed=interestCheckEmbed)
           
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
