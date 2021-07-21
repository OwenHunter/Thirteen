import discord
import asyncio
import json
from discord.ext.commands import Bot
from config import TOKEN

bot = Bot(command_prefix="?", status=discord.Status.dnd, activity=discord.Activity(name="?", type=discord.ActivityType.watching), intents=intents)

loopStop = False
interestCheckMessage = None
interestCheckEmbed = None

@bot.event
async def on_ready():
	print("Logged in as " + bot.user.name)

	### global variables that need it
	global loopStop, interestCheckEmbed, interestCheckMessage

@bot.command(name="killall")
async def stopLoops(context): #needs to check who issued the command - currently can be run by anyone
	loopStop = True

	await context.send("All loops halted.")

@bot.command(name="logout")
async def leavePlease(context):
	if "13hunteo" in str(context.message.author): #shouldn't just be checking the name, should be checking ID
		await context.send("Logging out...")
		await bot.close()
	else:
		await context.send("You do not have the permissions to do that...") #change to a DM? would fill up less room in channel

@bot.command(name="InterestCheck") #should be added into a cod - gaming cog?
async def interestCheck(context, game = None, time=None):
    if time != None and game != None:
        
        await context.send("@everyone")
        embedMsg = discord.Embed(title=f"{game} at {time}?", colour=discord.Colour.red()) #should probably check it is in some date format, not just print text
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
		if "hey 13" in str(message.content).lower() or "hey thirteen" in str(message.content).lower():
			channel = message.channel
			await channel.send("Hey " + message.author.mention)

bot.run(TOKEN)
