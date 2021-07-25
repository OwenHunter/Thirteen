import discord
from discord.ext import commands

class games(commands.Cog, name="Games"):

    def __init__(self, bot, interestCheckEmbed, interestCheckMessage):
        self.bot = bot
        self.interestCheckEmbed = interestCheckEmbed
        self.interestCheckMessage = interestCheckMessage
    
    @commands.command(name="InterestCheck", aliases=["interestcheck"])
    async def interestCheck(self, context, time=None, *, game = None):
        if time != None and game != None:
            
            await context.send("@everyone")
            embedMsg = discord.Embed(title=f"{game} at {time}?", colour=discord.Colour.red()) #should probably check it is in some date format, not just print text
            embedMsg.add_field(name="Yes: ", value=0)
            embedMsg.add_field(name="No: ", value=0)

            self.interestCheckEmbed = embedMsg
            
            self.interestCheckMessage = await context.send(embed=embedMsg)
            await self.interestCheckMessage.add_reaction("\U0001F44D")
            await self.interestCheckMessage.add_reaction("\U0001F44E")
        elif time == None:
            await context.send("Please input a time to play.")
        elif game == None:
            await context.send("Please input the game.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message == self.interestCheckMessage and user.id != 691380228123000872:
            yesCount = int(self.interestCheckEmbed.fields[0].value)
            noCount = int(self.interestCheckEmbed.fields[1].value)
            if len(self.interestCheckEmbed.fields) == 2:
                playingString = ""
            else:
                playingString = self.interestCheckEmbed.fields[2].value

            if reaction.emoji == "\U0001F44D":
                yesCount += 1
                playingString += ", " + user.name
            elif reaction.emoji =="\U0001F44E":
                noCount += 1

            self.interestCheckEmbed.set_field_at(0, name="Yes: ", value=yesCount)
            self.interestCheckEmbed.set_field_at(1, name="No: ", value=noCount)

            if playingString != "" and len(self.interestCheckEmbed.fields) == 2:
                playingString = playingString[2:]
                self.interestCheckEmbed.add_field(name="Playing: ", value=playingString, inline=False)
            elif playingString != "":
                self.interestCheckEmbed.set_field_at(2, name="Playing: ", value=playingString, inline=False)
            elif len(self.interestCheckEmbed.fields) != 2:
                self.interestCheckEmbed.remove_field(2)

            await reaction.message.edit(embed=self.interestCheckEmbed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message == self.interestCheckMessage and user.id != 691380228123000872:
            if reaction.emoji == "\U0001F44D":
                self.interestCheckEmbed.set_field_at(0, name="Yes: ", value=int(self.interestCheckEmbed.fields[0].value)-1)
                
                if len(self.interestCheckEmbed.fields) != 2:
                    playingString = self.interestCheckEmbed.fields[2].value
                    if user.name in playingString:
                        playingString = playingString.replace(", " + user.name, "")
                        playingString = playingString.replace(user.name, "")
                        
                        if playingString[-2:] == ", ":
                            playingString = playingString[:-2]
                        if playingString[:2] == ", ":
                            playingString = playingString[2:]
                    if playingString != "":
                        self.interestCheckEmbed.set_field_at(2, name="Playing: ", value=playingString, inline=False)
                    else:
                        self.interestCheckEmbed.remove_field(2)
            elif reaction.emoji == "\U0001F44E":
                self.interestCheckEmbed.set_field_at(1, name="No: ", value=int(self.interestCheckEmbed.fields[1].value)-1)

            await reaction.message.edit(embed=self.interestCheckEmbed)