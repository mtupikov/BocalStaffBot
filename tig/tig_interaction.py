import asyncio

from discord.utils import get
from tig.tig_db import TigDatabase
from tig.tig import Tig

tig_db = TigDatabase()


def discord_user_to_tig(member, reason: str) -> Tig:
	date = Tig.get_current_plus_hours(2)
	return Tig(member.nick, member.id, reason, date, date, True)


async def get_tig_list(ctx):
	tig_list = tig_db.get_tig_list()
	result = ''

	for tig in tig_list:
		result += f'User: {tig.username()};' \
					f'Id: {tig.user_id()};' \
					f'Reason: {tig.reason};' \
					f'Last tig date: {tig.current_tig_date}\n'

	if result == '':
		result = 'Empty tig list.'

	await ctx.send(result)


async def _give_or_remove_tig(ctx, member, give_tig, reason=''):
	role = get(member.guild.roles, name="ТИЖ")
	tig = discord_user_to_tig(member, reason)
	tig_list = tig_db.tig_list_by_user_id(member.id)

	if give_tig:
		if len(tig_list) != 0:
			if tig_list[0].is_active:
				await ctx.send(f'{member.nick} already has ТИЖ till {tig_list[0].current_tig_date}.')
				return
			else:
				tig_db.update_tig(tig)
		else:
			tig_db.add_tig(tig)

		await member.add_roles(role)
		await ctx.send(f'{member.nick} is given ТИЖ till {tig.current_tig_date}!')
	else:
		if len(tig_list) == 0:
			await ctx.send(f'{member.nick} does not have ТИЖ.')
			return

		await member.remove_roles(role)
		tig_db.set_tig_inactive(tig)
		await ctx.send(f'{member.nick} is now free from ТИЖ.')


async def manage_tig(ctx, give_tig):
	message_split = ctx.message.content.split()
	split_size = len(message_split)

	if split_size not in range(2, 4):
		help_message = "Usage:\n - !give_tig <username|id> <reason>;\n - !remove_tig <username|id>;"
		await ctx.send(f'{ctx.author.name}, arguments are not valid.\n{help_message}')
	else:
		members = ctx.author.guild.members
		member_to_ban = message_split[1]
		reason = ''
		if split_size == 3:
			reason = message_split[2]
		for member in members:
			if member.nick == member_to_ban:
				asyncio.create_task(_give_or_remove_tig(ctx, member, give_tig, reason))
				return

		for member in members:
			try:
				if member.id == int(member_to_ban):
					asyncio.create_task(_give_or_remove_tig(ctx, member, give_tig, reason))
					return
			except Exception:
				pass

		await ctx.send('Invalid username.')
