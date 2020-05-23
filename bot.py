import os
import asyncio
import multitimer
import logging

from discord.ext import commands
from tig import tig_interaction
from message_helpers.helper import *

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')


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
	logging.info(f"{ctx.author} requested active tig list")
	await tig_interaction.get_tig_list(ctx, True)


@bot.command(name='all_tig_list')
@commands.has_role("admin")
async def all_tig_list(ctx):
	logging.info(f"{ctx.author} requested full tig list")
	await tig_interaction.get_tig_list(ctx, False)


@bot.command(name='help')
@commands.has_role("admin")
async def help_message(ctx):
	logging.info(f"{ctx.author} requested help message")
	await tig_interaction.send_help_message(ctx)


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


if __name__ == '__main__':
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
	finally:
		loop.close()
