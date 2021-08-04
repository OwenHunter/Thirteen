import discord
from discord.ext import commands
import re

class games(commands.Cog, name="Games"):

    def __init__(self, bot, icMessage: list):
        self.bot = bot
        self.icMessage = icMessage
    
    @commands.command(name="InterestCheck", aliases=["interestcheck", "ic"])
    async def interestCheck(self, context, time=None, *, game=None):
        if time != None and game != None:
            if len(re.findall("^(\d)?\d(:\d\d)?(a|p)m$", time)) > 0:
                await context.send("@everyone")
                embed = discord.Embed(title=f"{time} for {game}?", colour=discord.Colour.red()) #should probably check it is in some date format, not just print text
                embed.add_field(name="Yes: ", value=0)
                embed.add_field(name="No: ", value=0)

                message = await context.send(embed=embed)

                self.icMessage.append(message)

                await message.add_reaction("\U0001F44D")
                await message.add_reaction("\U0001F44E")
            else:
                await context.send("Please format the time as:\n`h(h)(:mm)(am|pm)`")
        elif time == None:
            await context.send("Please input a time to play.")
        elif game == None:
            await context.send("Please input the game.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message in self.icMessage and user.id != 691380228123000872:
            embed = reaction.message.embeds[0]

            yesCount = int(embed.fields[0].value)
            noCount = int(embed.fields[1].value)
            if len(embed.fields) == 2:
                playingString = ""
            else:
                playingString = embed.fields[2].value

            if reaction.emoji == "\U0001F44D":
                yesCount += 1
                playingString += ", " + user.name
            elif reaction.emoji =="\U0001F44E":
                noCount += 1

            embed.set_field_at(0, name="Yes: ", value=yesCount)
            embed.set_field_at(1, name="No: ", value=noCount)

            if playingString != "" and len(embed.fields) == 2:
                playingString = playingString[2:]
                embed.add_field(name="Playing: ", value=playingString, inline=False)
            elif playingString != "":
                embed.set_field_at(2, name="Playing: ", value=playingString, inline=False)
            elif len(embed.fields) != 2:
                embed.remove_field(2)

            await reaction.message.edit(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message in self.icMessage and user.id != 691380228123000872:
            embed = reaction.message.embeds[0]
            if reaction.emoji == "\U0001F44D":
                embed.set_field_at(0, name="Yes: ", value=int(embed.fields[0].value)-1)
                
                if len(embed.fields) != 2:
                    playingString = embed.fields[2].value
                    if user.name in playingString:
                        playingString = playingString.replace(", " + user.name, "")
                        playingString = playingString.replace(user.name, "")
                        
                        if playingString[-2:] == ", ":
                            playingString = playingString[:-2]
                        if playingString[:2] == ", ":
                            playingString = playingString[2:]
                    if playingString != "":
                        embed.set_field_at(2, name="Playing: ", value=playingString, inline=False)
                    else:
                        embed.remove_field(2)
            elif reaction.emoji == "\U0001F44E":
                embed.set_field_at(1, name="No: ", value=int(embed.fields[1].value)-1)

            await reaction.message.edit(embed=embed)