import discord
import asyncio
from discord.ext import commands

interestCheckMessage = None
interestCheckEmbed = None

class games(commands.Cog):
    @commands.command(name="InterestCheck")
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

    @commands.Cog.listener
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

    @commands.Cog.listener
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