#basic cog setup
import discord
from discord.ext import commands
from __main__ import bot

#cog specific
from __main__ import channel_chat, channel_memes, channel_homework, channel_pictures, channel_music
from bs4 import BeautifulSoup
import requests
import re
import urllib.request as urllib
import os
import argparse
import sys
import json

def get_soup(url,header):
	return BeautifulSoup(urllib.urlopen(urllib.Request(url,headers=header)),'html.parser')

def download_images(search: str):
	query = search
	max_images = "1"
	save_directory = '/media/USBHDD/shares/Programming/Discord-Bot/pictures/'
	image_type="Action"
	query= query.split()
	query='+'.join(query)
	url="https://www.google.co.uk/search?q="+query+"&source=lnms&tbm=isch"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)
	ActualImages=[]# contains the link for Large original images, type of image
	for a in soup.find_all("div",{"class":"rg_meta"}):
		link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
		ActualImages.append((link,Type))
	save_location = ""
	for i , (img , Type) in enumerate( ActualImages[0:max_images]):
		try:
			req = urllib.Request(img, headers={'User-Agent' : header})
			raw_img = urllib.urlopen(req).read()
			if len(Type)==0:
				f = open(os.path.join(save_directory , "img" + "_"+ str(i)+".jpg"), 'wb')
				save_location = save_directory + "img" + "_" + str(i) + ".jpg"
			else :
				f = open(os.path.join(save_directory , "img" + "_"+ str(i)+"."+Type), 'wb')
				save_location = save_directory + "img" + "_" + str(i)+"." +Type
			f.write(raw_img)
			f.close()
		except Exception as e:
			print(e)
		return save_location

class Images_Commands:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="summon", pass_context=True)
	async def summon(self, context, search: str):
		await bot.say("done")
		print("done")
		save_directory = download_images(search)
		await bot.say("done")
		print("done")
		await bot.send_file(discord.Object(id=channel_pictures), save_directory)
		await bot.say("done")
		print("done")
		await bot.say(context.message.author.mention)
		await bot.say("done")
		print("done")
		print("summon")

def setup(bot):
	bot.add_cog(Images_Commands(bot))
