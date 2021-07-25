import discord
from discord import message
from discord.ext import commands

class testing(commands.Cog):
    def __init__(self, bot, stopLoops):
        self.bot = bot
        self.stopLoops = stopLoops
    
    @commands.command(name="stopLoops", hidden=True)
    @commands.is_owner()
    async def stopLoops(self, context):
        self.stopLoops = True

        await context.author.send("Loops have been stopped...")
    
    @commands.command(name="logout", hidden=True)
    @commands.is_owner()
    async def logOut(self, context):
        await context.author.send("Logging out...")
        await self.bot.close()
        print("logged out")