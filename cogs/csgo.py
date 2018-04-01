#basic cog setup
import discord
from discord.ext import commands
from __main__ import bot


#cog specific
import urllib.request

class CSGO_Commmands:

    __author__ = "Owen"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="csgo.getinfo", pass_context=True)
    async def get_info(self, context):
        contents = urllib.request.urlopen("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=JC").read()
        print(contents)

def setup(bot):
    bot.add_cog(CSGO_Commmands(bot))
