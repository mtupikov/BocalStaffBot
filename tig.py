import asyncio
import discord
from discord.utils import get

async def giveOrRemoveTig(ctx, member, giveTIG):
	role = get(member.guild.roles, name="ТИЖ")
	if giveTIG:
		await member.add_roles(role)
		await ctx.send(f'{member.display_name} is given ТИЖ!')
	else:
		await member.remove_roles(role)
		await ctx.send(f'{member.display_name} is now free from ТИЖ.')

async def manage_tig(ctx, giveTIG):
	messageSplit = ctx.message.content.split()
	if len(messageSplit) != 2:
		await ctx.send(f'{ctx.author.name}, arguments are not valid.')
	else:
		members = ctx.author.guild.members
		memberToBan = messageSplit[1]
		for member in members:
			if member.nick == memberToBan:
				asyncio.create_task(giveOrRemoveTig(ctx, member, giveTIG))
				return

		for member in members:
			try:
				if member.id == int(memberToBan):
					asyncio.create_task(giveOrRemoveTig(ctx, member, giveTIG))
					return
			except Exception:
				pass

		await ctx.send('Invalid username.')