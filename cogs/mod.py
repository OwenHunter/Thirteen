#basic cog setup
import discord
from discord.ext import commands
from __main__ import bot

#cog specific
import requests
import json
server = discord.Server

class Mod_Commands:
    def __init__(self, bot):
        self.bot = bot

    #@commands.command(name="gamemode")
    #async def gamemode(self, member):
        #await server.

    @commands.command(name="get_roles")
    async def get_roles(self, role):
        roles = server.roles
        for roles[i]:
            print(roles[i] + " " + discord.Role.name(roles[i]))

def setup(bot):
    bot.add_cog(Mod_Commands(bot))
