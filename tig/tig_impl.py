import asyncio

from discord.utils import get


async def give_or_remove_tig(ctx, member, give_tig):
	role = get(member.guild.roles, name="ТИЖ")
	if give_tig:
		await member.add_roles(role)
		await ctx.send(f'{member.display_name} is given ТИЖ!')
	else:
		await member.remove_roles(role)
		await ctx.send(f'{member.display_name} is now free from ТИЖ.')


async def manage_tig(ctx, give_tig):
	message_split = ctx.message.content.split()
	if len(message_split) != 2:
		await ctx.send(f'{ctx.author.name}, arguments are not valid.')
	else:
		members = ctx.author.guild.members
		member_to_ban = message_split[1]
		for member in members:
			if member.nick == member_to_ban:
				asyncio.create_task(give_or_remove_tig(ctx, member, give_tig))
				return

		for member in members:
			try:
				if member.id == int(member_to_ban):
					asyncio.create_task(give_or_remove_tig(ctx, member, give_tig))
					return
			except Exception:
				pass

		await ctx.send('Invalid username.')