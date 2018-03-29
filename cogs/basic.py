import discord
from discord.ext import commands
import random
from __main__ import bot

class SimpleCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='square', description="Squares a number inputted by the user", brief="Squares a number")
    async def square(number: int):
    	squared_number = (number * number)
    	await bot.say("The answer is " + str(squared_number))
    	print("square " + str(squared_number))

    @commands.command(name='add', aliases=['plus'])
    async def do_addition(self, first: int, second: int):
        """A simple command which does addition on two integer values."""

        total = first + second
        await bot.say(f'The sum of **{first}** and **{second}** is **{total}**')

    @commands.command(pass_context=True, name='8ball', description="Answers a yes/no question.", brief="Answers from the beyond")
    async def eight_ball(ctx, self):
    	possible_responses = [
    		'That is a resounding no',
    		'It is not looking likely',
    		'Too hard to tell',
    		'It is quite possible',
    		'Definitely',
    	]
    	random_choice = random.choice(possible_responses)
    	await bot.say("**" + random_choice + "** " + ctx.message.author.mention)
    	print("eight ball " + random_choice)

def setup(bot):
    bot.add_cog(SimpleCog(bot))
