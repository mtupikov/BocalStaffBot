from message_helpers.helper import *
from discord import message
from discord.ext import commands


def _message_is_suggestion(msg: message):
    return msg.channel.id == 710071073546305576  # Meta: suggestions channel ID


async def _handle_suggestion(msg: message):
    await msg.add_reaction('➕')  # heavy plus sign
    await msg.add_reaction('➖')  # heavy minus sign


async def on_message_impl(msg: message, bot: commands.bot):
    if _message_is_suggestion(msg):
        await _handle_suggestion(msg)
        return

    text = msg.content.lower()
    profane_condition = check_profane_condition(text)
    cheat_condition = check_cheat_condition(text)
    to_bot_condition = check_ask_bot_condition(text, bot.user.id)
    formatted_message_id = format_to_user_address(msg.author.id)

    if profane_condition:
        await msg.add_reaction('❗')  # exclamation mark
    elif cheat_condition:
        await msg.channel.send('CHEATING IS SLAVERY!')
    elif to_bot_condition:
        await msg.channel.send(f'{formatted_message_id}, ask peer on left, and then on right.')
