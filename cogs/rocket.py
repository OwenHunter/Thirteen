#basic cog setup
import discord
from discord.ext import commands
from __main__ import bot
import configparser

configParser = configparser.RawConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)

#cog specific
import rocket_snake as rs
from rocket_snake.constants import *
from rocket_snake import basic_requests, custom_exceptions, data_classes
from rocket_snake.constants import *
RocketAPI = configParser.get('api-config', 'rocket')
client = rs.RLS_Client(RocketAPI)

class Rocket_Commands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rocket.getinfo", pass_context=True)
    async def get_player(self, context):
        raw = await client.get_player("mystifiedmeat3", PLATFORM_ID_LUT["STEAM"])
        print(raw)

def setup(bot):
    bot.add_cog(Rocket_Commands(bot))
