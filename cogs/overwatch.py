#basic cog setup
import discord
from discord.ext import commands
from __main__ import bot

#cog specific
import feedparser

class Overwatch_Commands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="overwatch.news", pass_context=True)
    async def news(self, context):
        data = feedparser.parse('https://origin-esports-cms.thescore.com/overwatch.rss')
        title = data.entries[0].title
        link = data.entries[0].link

        print("overwatch.news " + title + " " + link)
        await bot.say("** {title} **, {mention}".format(title=title,
                                                        mention=context.message.author.mention))
        await bot.say("{link}".format(link=link))

def setup(bot):
    bot.add_cog(Overwatch_Commands(bot))
