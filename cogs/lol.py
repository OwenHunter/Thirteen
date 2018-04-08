#basic cog setup
import discord
from discord.ext import commands
from __main__ import bot


#cog specific
import configparser
from riotwatcher import RiotWatcher
import json
import feedparser
configParser = configparser.RawConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)
RiotAPI = configParser.get('api-config', 'riot')
watcher = RiotWatcher(RiotAPI)


class League_Commands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='league.getinfo', decription="Gets information about a summoner", brief="Gets summoner info", pass_context=True)
    async def get_info(self, context, region, summonerName):
        summoner = watcher.summoner.by_name(region.lower() + '1', summonerName)
        print(summoner)
        print("league.getinfo {name} {id} {level} {region}".format(name=summoner['name'],
                                                                    id=summoner['id'],
                                                                    level=summoner['summonerLevel'],
                                                                    region=region))
        await bot.say("** {name} (ID: *{id}*) is a level *{level}* summoner playing on *{region}* **, {mention}".format(name=summoner['name'],
                                                                                                              id=summoner['id'],
                                                                                                              level=summoner['summonerLevel'],
                                                                                                              region=region,
                                                                                                              mention=context.message.author.mention))

    @commands.command(name='league.getrank', decription="Gets ranked info about a summoner", brief="Gets ranked info", pass_context=True)
    async def get_rank(self, context, region, summonerName):
        summoner = watcher.summoner.by_name(region.lower() + '1', summonerName)
        rank_info = watcher.league.by_summoner(region.lower() + '1', summoner['id'])
        queue = 0
        if len(rank_info) == 1:
            queue = 0
        elif rank_info[0]['queueType'] == 'RANKED_SOLO_5x5':
            queue = 0
        elif rank_info[1]['queueType'] == 'RANKED_SOLO_5x5':
            queue = 1
        elif len(ranked_info) == 3:
            queue = 2
        else:
            if rank_info[0]['queueType'] == 'RANKED_FLEX_SR':
                queue = 0
            else:
                queue = 1

        queueType = rank_info[queue]['queueType']
        if queueType == 'RANKED_SOLO_5x5':
            queueType = 'Solo/Duo'
        elif queueType == 'RANKED_FLEX_SR':
            queueType = 'Flex'
        else:
            queueType = 'Twisted Treeline'

        print("league.getrank {summoner} {tier} {div} {lp} {type}".format(name=summoner['name'],
                                                                            tier=rank_info[queue]['tier'],
                                                                            div=rank_info[queue]['rank'],
                                                                            lp=rank_info[queue]['leaguePoints'],
                                                                            type=queueType))
        await bot.say("***{name}* is in *{tier} {div}*, and has *{lp}* LP in *{type}***, {mention}".format(name=summoner['name'],
                                                                                                  tier=rank_info[queue]['tier'],
                                                                                                  div=rank_info[queue]['rank'],
                                                                                                  lp=rank_info[queue]['leaguePoints'],
                                                                                                  type=queueType,
                                                                                                  mention=context.message.author.mention))

    @commands.command(name="league.news", pass_context=True)
    async def news(self, context):
        data = feedparser.parse('https://origin-esports-cms.thescore.com/lol.rss')
        title = data.entries[0].title
        link = data.entries[0].link

        print("csgo.news " + title + " " + link)
        await bot.say("** {title} **, {mention}".format(title=title,
                                                        mention=context.message.author.mention))
        await bot.say("{link}".format(link=link))


def setup(bot):
    bot.add_cog(League_Commands(bot))
