# import cmd
# import json
import sys

import interactions
# import discord
# import os
# import datetime
from asyncio import *

import db
# import db
import twitch
# from discord import Embed
global bot, conn, pid

# Groupe 1
# Envoyer le projet a la fin (après noel)
# Rendu du projet : (29 décembre) → Github ou Archive (.rar, .zip, ...)



config = sys.argv[1:]
print(config)
global bot, conn, role
db.connect(db=config[5], user=config[2], passwd=config[3], ip=config[4])
# conf = db.conf(pid)
tw_token = config[2]
twitch.setup(tw_token)
token = config[1]
scope = config[5]
cmd_chann = config[7]
streams_chann = config[8]
role = config[9]
bot = interactions.Client(token=token, intents=interactions.Intents.ALL)



# ----------------------------INNIT----------------------------

@interactions.slash_command(
	name="add",
	description="Ajouter un streamer",
	options=[{
		"name": "streamer",
		"description": "noms du streamer",
		"type": 3,
		"required": True,
	}]

)
async def add_streamer(ctx: interactions.slash_command, streamer):
	if ctx.author.has_role(role):
		data = twitch.get_user(streamer)
		print(data)
		embed = interactions.Embed(title=data.name, description=data.desc, color=0xff0000)
		embed.set_thumbnail(url=data.pic)
		embed.add_field(name="Is it that?", value="Send y or n", inline=True)
		button1 = interactions.Button(label="Button 1", style=interactions.ButtonStyle.GREEN, custom_id="yes_add_streamer")
		button2 = interactions.Button(label="Button 2", style=interactions.ButtonStyle.RED, custom_id="no_add_streamer")
		msg = await ctx.send(embed=embed, components=[button1, button2])
		db.add_temp_streamer(msg.id, data.id, 1)

	else:
		await ctx.respond("C'est NON")

@interactions.component_callback("yes_add_streamer")
async def yes_add_streamer(ctx: interactions.ComponentContext):
	tw_id = db.get_temp_streamer(pid)
	print(tw_id)
	data = twitch.get_user_by_id(tw_id[0])
	db.add_streamer(user_id=data.id, username=data.name, pp_url=data.pic, by=ctx.author.id)
	await ctx.message.delete()
	embed = interactions.Embed
	embed = interactions.Embed(title="Correctly added :", description=data.name, color=0xff0000)
	embed.set_thumbnail(url=data.pic)
	await ctx.send(embed=embed, delete_after=10)

@interactions.component_callback("no_add_streamer")
async def no_add_streamer(ctx: interactions.ComponentContext):
	db.del_temp_streamer(pid)
	await ctx.send("Okay")


@interactions.slash_command(
	name="supp",
	description="Supprimer un streamer",
	options=[{
			"name": "streamer",
			"description": "noms du streamer",
			"type": 3,
			"required": True,
		}]

)
async def supp(ctx: interactions.slash_command, streamer):
	if ctx.author.has_role(role):
		print("strating deleting")
		id = db.get_streamer_id_by_name(streamer)
		print(id)
		stream = db.was_streaming(id)
		if stream:
			msg = db.get_stream_msg(id)
			msg = await bot.get_channel(cmd_chann).fetch_message(message_id=msg)
			await msg.delete()
			db.del_stream(id)
		db.del_streamer(streamer)
		await ctx.respond("OK")
	else:
		await ctx.respond("C'est NON")


@interactions.slash_command(
	name="list",
	description="liste les streamer"

)
async def list_streamers(ctx: interactions.slash_command):
	if ctx.author.has_role(role):
		streamers = db.get_streamers_name()
		stre = ""
		for i in streamers: stre += f"{i},"
		await ctx.respond(stre)
	else:
		await ctx.respond("C'est NON")



@interactions.slash_command(
	name="stop",
	description="stop the bot"
)
async def stop(ctx: interactions.slash_command):
	await bot.stop()
	exit()


@bot.event()
async def on_connect():
	# def connect(any)
	# conn = db.connect()
	 pass

async def check_streams():
	print("checking streams")
	known_streams = db.get_streams_ids()
	l_streams = db.get_streamers_ids()
	print(l_streams)
	if l_streams:
		print("there is streamers to check")
		stream = twitch.get_stream(l_streams)
		# print(f"stream : {stream}")
		ystreams = stream["yes"]
		# print(f"ystreams : {ystreams}")
		# print(type(ystreams))
		streams_keys = list(ystreams.keys())
		# print(f'streams_keys : {streams_keys}')
		for i in l_streams:
			print(f"known : {known_streams}, i : {i}, strams_keys : {streams_keys}")
			if i not in known_streams and i in streams_keys:
	# 			add it
				print("adding stream")
				msg = await send_msg_stream(ystreams[i])
				stream_obj = ystreams[i]
				db.add_stream(i, stream_obj.id, stream_obj.game_name, stream_obj.title, stream_obj.thumb, stream_obj.lang, stream_obj.nsfw, msg.id)
			elif i in known_streams and i not in streams_keys:
	# 			del it
				print("deleting stream", i)
				msgid = db.get_stream_msg(i)
				# print(msgid)
				chann = bot.get_channel(streams_chann)
				# print(chann)
				await chann.delete_message(msgid)
				# print(msg)
				# await msg.delete()
				db.del_stream(i)
	# 		elif i in known_streams and i in streams:
	# # 			verify


async def send_msg_stream(stream:twitch.Streamer.Stream):
	print("sending stream embed")
	str_cmd = bot.get_channel(streams_chann)
	embed = interactions.Embed(title=stream.title, description=db.get_streamer_name_by_id(stream.sid), color=0xff0000, url=f"https://twitch.tv/{db.get_streamer_name_by_id(stream.sid)}")
	embed.set_image(url=stream.thumb.replace("{width}", "1920").replace("{height}", "1080"))
	embed.set_thumbnail(url=db.get_streamer_pp(stream.sid))
	return await str_cmd.send(embed=embed)


async def start_events():
	while True:
		await check_streams()
		await sleep(120)  # Every 2 minutes



@bot.event()
async def on_ready():
	await start_events()
	cmd = bot.get_channel(cmd_chann)
	await cmd.send("All Set")

def run():
	bot.start()

if __name__ == "__main__":
	# bot.start()
	pass