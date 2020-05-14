import os

import discord
import asyncio
from discord.ext import commands
from discord.utils import get

token = os.getenv('DISCORD_TOKEN')
guild = 'UNIT 42'

bot = commands.Bot(command_prefix='!', case_insensitive=True)

async def giveOrRemoveTig(ctx, member, giveTIG):
	role = get(member.guild.roles, name="ТИЖ")
	if giveTIG:
		await member.add_roles(role)
		await ctx.send(f'{member.display_name} is given ТИЖ!')
	else:
		await member.remove_roles(role)
		await ctx.send(f'{member.display_name} is now free from ТИЖ.')

async def manage_tig(ctx, giveTIG):
	messageSplit = ctx.message.content.split()
	if len(messageSplit) != 2:
		await ctx.send(f'{ctx.author.name}, arguments are not valid.')
	else:
		members = ctx.author.guild.members
		memberToBan = messageSplit[1]
		for member in members:
			if member.nick == memberToBan:
				asyncio.create_task(giveOrRemoveTig(ctx, member, giveTIG))
				return

		for member in members:
			try:
				if member.id == int(memberToBan):
					asyncio.create_task(giveOrRemoveTig(ctx, member, giveTIG))
					return
			except Exception:
				pass

		await ctx.send('Invalid username.')

@bot.command(name='give_tig')
@commands.has_role("admin")
async def give_tig(ctx):
	asyncio.create_task(manage_tig(ctx, True))

@bot.command(name='remove_tig')
@commands.has_role("admin")
async def remove_tig(ctx):
	asyncio.create_task(manage_tig(ctx, False))

async def on_message(message):
	if message.author == bot.user:
		return

	if message.content == 'pidor':
	    await message.author.create_dm()
	    await message.author.dm_channel.send(
	        f'{message.author.name}, wanna TIG?'
	    )

bot.add_listener(on_message, 'on_message')
bot.run(token)
