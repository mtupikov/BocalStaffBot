import os

import discord
from discord.ext import commands
from tig.tig_impl import *

token = os.getenv('DISCORD_TOKEN')
guild = 'UNIT Factory Community'
bot = commands.Bot(command_prefix='!', case_insensitive=True)


@bot.command(name='give_tig')
@commands.has_role("admin")
async def give_tig(ctx):
	asyncio.create_task(manage_tig(ctx, True))


@bot.command(name='remove_tig')
@commands.has_role("admin")
async def remove_tig(ctx):
	asyncio.create_task(manage_tig(ctx, False))


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	tig_condition = 'pidor' in message.content or 'пидор' in message.content
	cheat_condition = \
		'-42' in message.content or \
		'cheat' in message.content or \
		'чит' in message.content
	to_bot_condition = f'<@!{bot.user.id}>' in message.content

	if tig_condition:
		await message.channel.send(f'{message.author.name}, wanna TIG?')
	elif cheat_condition:
		await message.channel.send('CHEATING IS SLAVERY!')
	elif to_bot_condition:
		await message.channel.send(
			f'{message.author.name}, ask peer on left, and then on right.'
		)

loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(bot.start(token))
except KeyboardInterrupt:
	loop.run_until_complete(bot.logout())
finally:
	loop.close()
