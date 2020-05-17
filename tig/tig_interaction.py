import asyncio
import discord

from discord.utils import get
from tig.tig_db import TigDatabase
from tig.tig import Tig

tig_db = TigDatabase()


def discord_user_to_tig(member, reason: str) -> Tig:
	date = Tig.get_current_plus_hours(2)
	return Tig(member.nick, member.id, reason, date, date, True)


async def send_help_message(ctx):
	embed = discord.Embed(title="Usage", color=0x00ff00)
	embed.add_field(name="Give ТИЖ", value='!give_tig <username | id> <reason>', inline=False)
	embed.add_field(name="Remove ТИЖ", value='!remove_tig <username | id>', inline=False)
	embed.add_field(name="ТИЖ list", value='!tig_list', inline=False)

	await ctx.send(f'<@!{ctx.author.id}>', embed=embed)


async def get_tig_list(ctx):
	tig_list = tig_db.get_tig_list()

	if len(tig_list) == 0:
		embed = discord.Embed(title="ТИЖ list is empty", color=0xff0000)
		await ctx.send(embed=embed)
		return

	embed = discord.Embed(title="Users with ТИЖ", color=0x00ff00)

	for tig in tig_list:
		embed.add_field(name="Username", value=tig.username(), inline=True)
		embed.add_field(name="ТИЖ reason", value=tig.reason, inline=True)
		embed.add_field(name="Last tig date", value=tig.formatted_current_tig_date(), inline=True)

	await ctx.send(embed=embed)


async def _give_or_remove_tig(ctx, member, give_tig, reason):
	role = get(member.guild.roles, name="ТИЖ")
	tig = discord_user_to_tig(member, reason)
	tig_list = tig_db.tig_list_by_user_id(member.id)

	if give_tig:
		if len(tig_list) != 0:
			if tig_list[0].is_active:
				await ctx.send(f'<@!{member.id}> already has ТИЖ till {tig_list[0].formatted_current_tig_date}.')
				return
			else:
				tig_db.update_tig(tig)
		else:
			tig_db.add_tig(tig)

		await member.add_roles(role)
		await ctx.send(f'<@!{member.id}> is given ТИЖ till {tig.formatted_current_tig_date}!')
	else:
		if len(tig_list) == 0:
			await ctx.send(f'<@!{member.id}> does not have ТИЖ.')
			return

		await member.remove_roles(role)
		tig_db.set_tig_inactive(tig)
		await ctx.send(f'<@!{member.id}> is now free from ТИЖ.')


async def manage_tig(ctx, give_tig):
	message_split = ctx.message.content.split()
	split_size = len(message_split)

	if split_size not in range(2, 4):
		await send_help_message(ctx)
		return
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
