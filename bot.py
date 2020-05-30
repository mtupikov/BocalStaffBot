import os
import asyncio
import multitimer
import logging

from discord.errors import LoginFailure
from datetime import datetime
from discord.ext import commands
from tig import tig_interaction
from message_handlers import handlers

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')
logger = logging.getLogger('discord')


@bot.command(name='give_tig')
@commands.has_any_role("admin", "moderator")
async def give_tig(ctx):
	await tig_interaction.manage_tig(ctx, True)


@bot.command(name='remove_tig')
@commands.has_any_role("admin", "moderator")
async def remove_tig(ctx):
	await tig_interaction.manage_tig(ctx, False)


@bot.command(name='tig_list')
@commands.has_any_role("admin", "moderator")
async def tig_list(ctx):
	logger.info(f"{ctx.author} requested active tig list")
	await tig_interaction.get_tig_list(ctx, True)


@bot.command(name='all_tig_list')
@commands.has_any_role("admin", "moderator")
async def all_tig_list(ctx):
	logger.info(f"{ctx.author} requested full tig list")
	await tig_interaction.get_tig_list(ctx, False)


@bot.command(name='cmds')
@commands.has_any_role("admin", "moderator")
async def help_message(ctx):
	logger.info(f"{ctx.author} requested help message")
	await tig_interaction.send_help_message(ctx)


@bot.command(name='logout')
@commands.has_role("admin")
async def logout(ctx):
	logger.info(f"{ctx.author} requested bot logout")
	if ctx.author.nick == 'mtupikov':
		await bot.logout()


def check_tig_expired():
	global bot
	global guild_id
	global loop
	tig_interaction.check_tig_expired_impl(bot, guild_id, loop)


async def on_message(message):
	global bot
	if message.author == bot.user:
		return
	await handlers.on_message_impl(message, bot)


def setup_logging():
	logger.setLevel(logging.INFO)

	current_date = datetime.now()
	current_date_str: str = current_date.astimezone().replace(microsecond=0, tzinfo=None).strftime('%Y-%m-%dT%H-%M-%S')
	handler = logging.FileHandler(filename=f'{current_date_str}.log', encoding='utf-8', mode='w')
	formatter = logging.Formatter('%(asctime)s %(levelname).1s: %(message)s', "%Y-%m-%dT%H-%M-%S")
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
		timer = multitimer.RepeatingTimer(interval=30, function=check_tig_expired)
		timer.start()
		bot.add_listener(on_message, 'on_message')
		loop.run_until_complete(bot.start(token))
	except KeyboardInterrupt:
		loop.run_until_complete(bot.logout())
	except LoginFailure as ex:
		logger.info(f"Login failure, maybe invalid token passed? '{token}'")
	finally:
		loop.stop()
		loop.close()
