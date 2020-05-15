import os

import discord
import asyncio
from discord.ext import commands

from tig import *

token = os.getenv('DISCORD_TOKEN')
guild = 'UNIT 42'

bot = commands.Bot(command_prefix='!', case_insensitive=True)

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

	if 'pidor' in message.content or 'пидор' in message.content:
		await message.channel.send(f'{message.author.name}, wanna TIG?')
	elif '-42' in message.content:
		await message.channel.send('CHEATING IS SLAVERY!')
	elif f'<@!{bot.user.id}>' in message.content:
		await message.channel.send(
			f'{message.author.name}, ask peer on left, and then ot right.'
		)

bot.add_listener(on_message, 'on_message')
bot.run(token)
