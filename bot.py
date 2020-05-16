import os

from discord.ext import commands
from tig.tig_impl import *
from message_helpers.helper import *

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

	text = message.content.lower()
	tig_condition = check_tig_condition(text)
	cheat_condition = check_cheat_condition(text)
	to_bot_condition = check_ask_bot_condition(text, bot.user.id)

	if tig_condition:
		await message.channel.send(f'{message.author.name}, wanna TIG?')
	elif cheat_condition:
		await message.channel.send('CHEATING IS SLAVERY!')
	elif to_bot_condition:
		await message.channel.send(f'{message.author.name}, ask peer on left, and then on right.')

if __name__ == '__main__':
	token = os.getenv('DISCORD_TOKEN')
	guild = os.getenv('DISCORD_GUILD_TOKEN')

	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(bot.start(token))
	except KeyboardInterrupt:
		loop.run_until_complete(bot.logout())
	finally:
		loop.close()
