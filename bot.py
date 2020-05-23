import os
import asyncio
import multitimer
import logging

from aiohttp import client_exceptions
from datetime import datetime, timezone
from discord.ext import commands
from tig import tig_interaction
from message_helpers.helper import *

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')
logger = logging.getLogger('discord')


@bot.command(name='give_tig')
@commands.has_role("admin")
async def give_tig(ctx):
	await tig_interaction.manage_tig(ctx, True)


@bot.command(name='remove_tig')
@commands.has_role("admin")
async def remove_tig(ctx):
	await tig_interaction.manage_tig(ctx, False)


@bot.command(name='tig_list')
@commands.has_role("admin")
async def tig_list(ctx):
	logger.info(f"{ctx.author} requested active tig list")
	await tig_interaction.get_tig_list(ctx, True)


@bot.command(name='all_tig_list')
@commands.has_role("admin")
async def all_tig_list(ctx):
	logger.info(f"{ctx.author} requested full tig list")
	await tig_interaction.get_tig_list(ctx, False)


@bot.command(name='help')
@commands.has_role("admin")
async def help_message(ctx):
	logger.info(f"{ctx.author} requested help message")
	await tig_interaction.send_help_message(ctx)


@bot.command(name='logout')
@commands.has_role("admin")
async def help_message(ctx):
	logger.info(f"{ctx.author} requested bot logout")
	if ctx.author.nick == 'mtupikov':
		await bot.logout()


async def on_message(message):
	if message.author == bot.user:
		return

	text = message.content.lower()
	tig_condition = check_tig_condition(text)
	cheat_condition = check_cheat_condition(text)
	to_bot_condition = check_ask_bot_condition(text, bot.user.id)
	formatted_message_id = format_to_user_address(message.author.id)

	if tig_condition:
		await message.channel.send(f'{formatted_message_id}, wanna TIG?')
	elif cheat_condition:
		await message.channel.send('CHEATING IS SLAVERY!')
	elif to_bot_condition:
		await message.channel.send(f'{formatted_message_id}, ask peer on left, and then on right.')


def check_tig_expired():
	global bot
	global guild_id
	global loop
	tig_interaction.check_tig_expired_impl(bot, guild_id, loop)


def setup_logging():
	logger.setLevel(logging.INFO)

	current_date = datetime.now()
	current_date_str = current_date.astimezone().replace(microsecond=0, tzinfo=None).isoformat()
	handler = logging.FileHandler(filename=f'{current_date_str}.log', encoding='utf-8', mode='w')
	formatter = logging.Formatter('%(asctime)s %(levelname).1s: %(message)s', "%Y-%m-%dT%H:%M:%S")
	handler.setFormatter(formatter)

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(formatter)

	logger.addHandler(console_handler)
	logger.addHandler(handler)


if __name__ == '__main__':
	setup_logging()

	token = os.getenv('DISCORD_TOKEN')
	guild_id = int(os.getenv('UNIT_GUILD_ID'))

	loop = asyncio.get_event_loop()
	try:
		timer = multitimer.RepeatingTimer(interval=10, function=check_tig_expired)
		timer.start()
		bot.add_listener(on_message, 'on_message')
		loop.run_until_complete(bot.start(token))
	except KeyboardInterrupt:
		loop.run_until_complete(bot.logout())
	except client_exceptions.ClientConnectorError as ex:
		logger.critical(f'Error: {ex.strerror}')
		exit()
	finally:
		loop.close()
