#basic cog setup
import discord
from discord.ext import commands
from __main__ import bot


#cog specific
import random

class Basic_Commmands:

    __author__ = "Owen"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='square', description="Squares a number inputted by the user", brief="Squares a number")
    async def square(self, number: int):
    	squared_number = (number * number)
    	await bot.say("The answer is " + str(squared_number))
    	print("square " + str(squared_number))

    @commands.command(name='add', description="Adds two integers together", brief="Adds two numbers", pass_context=True)
    async def do_addition(self, context, first: int, second: int):
        total = first + second
        await bot.say("The sum of **{first}** and **{second}** is **{total}**, {mention}".format(first = first,
                                                                                                 second = second,
                                                                                                 total = total,
                                                                                                 mention = context.message.author.mention))
        print("add " + total)

    @commands.command(pass_context=True, name='8ball', description="Answers a yes/no question.", brief="Answers from the beyond")
    async def eight_ball(self, context):
    	possible_responses = [
    		'That is a resounding no',
    		'It is not looking likely',
    		'Too hard to tell',
    		'It is quite possible',
    		'Definitely',
    	]
    	random_choice = random.choice(possible_responses)
    	await bot.say("**" + random_choice + "** " + context.message.author.mention)
    	print("eight ball " + random_choice)

    @commands.command(name='clear', description="Clears messages from a channel", brief="Clears messages", pass_context=True)
    async def clear(self, context, number):
        mgs = []
        number = int(number)
        async for x in bot.logs_from(context.message.channel, limit=number):
            mgs.append(x)
        print("clear " + str(number))
        await bot.delete_messages(mgs)

def setup(bot):
    bot.add_cog(Basic_Commmands(bot))
