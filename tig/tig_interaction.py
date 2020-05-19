import discord
import re

from discord.utils import get
from tig.tig_db import TigDatabase
from tig.tig import Tig
from message_helpers.helper import format_to_user_address

tig_db = TigDatabase()


def discord_user_to_tig(member, reason: str) -> Tig:
	date = Tig.get_current_plus_hours(2)
	return Tig(member.nick, member.id, reason, date, date, True)


async def send_help_message(ctx):
	embed = discord.Embed(title="Usage", color=0x00ff00)
	embed.add_field(name="Give ТИЖ", value='!give_tig <username | id> <reason>', inline=False)
	embed.add_field(name="Remove ТИЖ", value='!remove_tig <username | id>', inline=False)
	embed.add_field(name="ТИЖ list", value='!tig_list', inline=False)
	embed.add_field(name="Active ТИЖ list", value='!all_tig_list', inline=False)

	await ctx.send(embed=embed)


async def get_tig_list(ctx, only_active):
	tig_list = tig_db.get_tig_list(only_active)

	active_prefix = ''
	if only_active:
		active_prefix = 'Active '

	if len(tig_list) == 0:
		embed = discord.Embed(title=f"{active_prefix}ТИЖ list is empty", color=0xff0000)
		await ctx.send(embed=embed)
		return

	embed = discord.Embed(title=f"Users with {active_prefix}ТИЖ", color=0x00ff00)

	for tig in tig_list:
		embed.add_field(name="Username", value=tig.username, inline=True)
		embed.add_field(name="ТИЖ reason", value=tig.reason, inline=True)
		embed.add_field(name="Last tig date", value=tig.formatted_current_tig_date(), inline=True)

	await ctx.send(embed=embed)


async def _give_or_remove_tig(ctx, member, give_tig, reason):
	role = get(member.guild.roles, name="ТИЖ")
	tig = discord_user_to_tig(member, reason)
	tig_list = tig_db.tig_list_by_user_id(member.id)
	formatted_member_id = format_to_user_address(member.id)

	if give_tig:
		if len(tig_list) != 0:
			if tig_list[0].is_active:
				await ctx.send(f'{formatted_member_id} already has ТИЖ till {tig_list[0].formatted_current_tig_date()}.')
				return
			else:
				tig_db.update_tig(tig)
		else:
			tig_db.add_tig(tig)

		await member.add_roles(role)
		await ctx.send(f'{formatted_member_id} is given ТИЖ till {tig.formatted_current_tig_date()}!')
	else:
		if len(tig_list) == 0:
			await ctx.send(f'{formatted_member_id} does not have ТИЖ.')
			return

		await member.remove_roles(role)
		tig_db.set_tig_inactive(tig)
		await ctx.send(f'{formatted_member_id} is now free from ТИЖ.')


async def _walk_through_members(ctx, members, member_to_handle, reason, give_tig):
	for member in members:
		if member.nick == member_to_handle:
			await _give_or_remove_tig(ctx, member, give_tig, reason)
			return

	for member in members:
		try:
			if member.id == int(member_to_handle):
				await _give_or_remove_tig(ctx, member, give_tig, reason)
				return
		except Exception:
			pass

	await ctx.send('Invalid username.')


async def manage_tig(ctx, give_tig):
	message = ctx.message.content
	members = ctx.author.guild.members

	incomplete_tig_match = re.match(r'^!give_tig\s+(\w+)\s*$', message)
	give_tig_match = re.match(r'^!give_tig\s+(\w+)\s+(.+)\s*$', message)
	remove_tig_match = re.match(r'^!remove_tig\s+(\w+)\s*$', message)

	if incomplete_tig_match:
		member_to_ban = incomplete_tig_match.group(1)
		await ctx.send(f'You must provide reason to give ТИЖ to {member_to_ban}.')
	elif give_tig_match:
		member_to_ban = give_tig_match.group(1)
		reason = give_tig_match.group(2)
		await _walk_through_members(ctx, members, member_to_ban, reason, give_tig)
	elif remove_tig_match:
		member_to_free = remove_tig_match.group(1)
		await _walk_through_members(ctx, members, member_to_free, '', give_tig)
	else:
		await send_help_message(ctx)
