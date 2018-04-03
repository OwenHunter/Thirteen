#basic cog setup
import discord
from discord.ext import commands
from __main__ import bot

#cog specific
import requests
import json

def findstat(data, stat_name):
    for stat in data['playerstats']['stats']:
        if stat['name'] == stat_name:
            return stat['value']

class CSGO_Commmands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="csgo.playtime", description="Gets the inputted player's playtime in the game", brief="Gets the playtime", pass_context=True)
    async def playtime(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=FE3C600EB76959F47F80C707467108F2&format=json&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        for stat in data['response']['games']:
            if stat['appid'] == 730:
                playtime = stat['playtime_forever']

        playtime = '{:02d} hours and {:02d} minutes'.format(*divmod(playtime, 60))
        print("csgo.playtime " + player + " " + playtime)
        await bot.say("**{player} has played {time} of CSGO**, {mention}".format(player = player,
                                                                                    time = playtime,
                                                                                    mention = context.message.author.mention))

    @commands.command(name="csgo.overallkills", description="Gets the inputted player's number of overall kills", brief="Gets the number of overall kills", pass_context=True)
    async def overallkills(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_kills = findstat(data, 'total_kills')
        print("csgo.kills " + player + " " + str(total_kills))
        await bot.say("**{player} has a total of {kills} kills**, {mention}".format(player = player,
                                                                            kills = total_kills,
                                                                            mention = context.message.author.mention))

    @commands.command(name="csgo.kills", pass_context=True)
    async def weaponkills(self, context, weapon, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        weapon_name = weapon

        if weapon.lower() == "duals":
            weapon_name = "elite"

        if weapon.lower() == "p2000":
            weapon_name = "hkp2000"

        if weapon.lower() == "scar":
            weapon_name = "scar20"

        if weapon.lower() == "scout":
            weapon_name = "ssg08"

        if weapon.lower() == "pp-bizon":
            weapon_name = "bizon"

        if weapon.lower() == "galil":
            weapon_name = "galilar"

        if weapon.lower() == "zeus":
            weapon_name = "taser"

        try:
            total_kills = findstat(data, 'total_kills_' + weapon_name.lower())
            print("csgo.kills " + weapon + " " + player + " " +str(total_kills))
            await bot.say("**{player} has a total of {kills} kills with {weapon}**, {mention}".format(player=player,
                                                                                                        kills=total_kills,
                                                                                                        weapon=weapon,
                                                                                                        mention=context.message.author.mention))
        except Exception as e:
            await bot.say("Something went wrong!")


    @commands.command(name="csgo.deaths", description="Gets the inputted player's number of deaths", brief="Gets the number of deaths", pass_context=True)
    async def deaths(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_deaths = findstat(data, 'total_deaths')
        print("csgo.deaths " + player + " " + str(total_deaths))
        await bot.say("**{player} has a total of {deaths} deaths**, {mention}".format(player = player,
                                                                                        deaths = total_deaths,
                                                                                        mention = context.message.author.mention))

    @commands.command(name="csgo.bombplants", description="Gets the amount of bombs planted by the player inputted", brief="Gets the amount of bombs planted", pass_context=True)
    async def plants(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_planted_bombs = findstat(data, 'total_planted_bombs')
        print("csgo.bombplants " + player + " " + str(total_planted_bombs))
        await bot.say("**{player} has planted a total of {bombs} bombs **, {mention}".format(player = player,
                                                                                        bombs = total_planted_bombs,
                                                                                        mention = context.message.author.mention))

    @commands.command(name="csgo.defusals", description="Gets the amount of bombs defused by the player inputted", brief="Gets the amount of bombs defused", pass_context=True)
    async def defusals(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_defused_bombs = findstat(data, 'total_defused_bombs')
        print("csgo.defusals " + player + " " + str(total_defused_bombs))
        await bot.say("**{player} has defused a total of {bombs} bombs **, {mention}".format(player = player,
                                                                                        bombs = total_defused_bombs,
                                                                                        mention = context.message.author.mention))

    @commands.command(name="csgo.wins", description="Gets the inputted player's amount of wins", brief="Gets the amount of wins", pass_context=True)
    async def wins(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_wins = findstat(data, 'total_wins')
        print("csgo.wins " + player + " " + str(total_wins))
        await bot.say("**{player} has won a total of {wins} games **, {mention}".format(player = player,
                                                                                        wins = total_wins,
                                                                                        mention = context.message.author.mention))

    @commands.command(name="csgo.damage", description="Gets the amount of damage done by the player inputted", brief="Gets the amount of damage done", pass_context=True)
    async def damage(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_damage_done = findstat(data, 'total_damage_done')
        print("csgo.damage " + player + " " + str(total_damage_done))
        await bot.say("**{player} has done a total of {damage} HP of damage **, {mention}".format(player = player,
                                                                                        damage = total_damage_done,
                                                                                        mention = context.message.author.mention))

    @commands.command(name="csgo.money", description="Gets the amount of money earned by the player inputted", brief="Gets the amount of money earned", pass_context=True)
    async def money(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_money_earned = findstat(data, 'total_money_earned')
        print("csgo.money " + player + " " + str(total_money_earned))
        await bot.say("**{player} has earned a total of ${money} **, {mention}".format(player = player,
                                                                                        money = total_money_earned,
                                                                                        mention = context.message.author.mention))

    @commands.command(name="csgo.headshots", description="Gets the inputted player's amount of headshots", brief="Gets the amount of headshots", pass_context=True)
    async def headshots(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_kills_headshot = findstat(data, 'total_kills_headshot')
        print("csgo.money " + player + " " + str(total_kills_headshot))
        await bot.say("**{player} has hit a total of {headshot} headshots**, {mention}".format(player = player,
                                                                                        headshot = total_kills_headshot,
                                                                                        mention = context.message.author.mention))

    @commands.command(name="csgo.hostages", description="Gets the amount of hostages rescued by the player inputted", brief="Gets the amount of hostages rescued", pass_context=True)
    async def hostages(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_hostages = findstat(data, 'total_rescued_hostages')
        print("csgo.hostages " + player + " " + str(total_hostages))
        await bot.say("**{player} has rescued a total of {hostages} hostages**, {mention}".format(player = player,
                                                                                                        hostages = total_hostages,
                                                                                                        mention = context.message.author.mention))

    @commands.command(name="csgo.pistolwins", description="Gets the amount of pistol rounds won by the player inputted", brief="Gets the amount of pistol rounds won", pass_context=True)
    async def pistolwins(self, context, player):
        try:
            url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=FE3C600EB76959F47F80C707467108F2&vanityurl=" + player
            data = requests.get(url).text
            data = json.loads(data)
            steamid = data['response']['steamid']

            url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=FE3C600EB76959F47F80C707467108F2&steamid=" + steamid
            data = requests.get(url).text
            data = json.loads(data)
        except:
            await bot.say("Something went wrong! Make sure the Steam username is correct.")

        total_pistolwins = findstat(data, 'total_wins_pistolround')
        print("csgo.pistolwins " + player + " " + str(total_pistolwins))
        await bot.say("**{player} has won a total of {pistolwins} pistol rounds**, {mention}".format(player = player,
                                                                                            pistolwins = total_pistolwins,
                                                                                            mention = context.message.author.mention))

def setup(bot):
    bot.add_cog(CSGO_Commmands(bot))
