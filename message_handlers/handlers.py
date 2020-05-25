import random

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

    random_condition = random.random() > 0.7

    text = msg.content.lower()
    profane_condition = check_profane_condition(text)

    if profane_condition:
        await msg.add_reaction('❗')  # exclamation mark
    elif random_condition:
        cheat_condition = check_cheat_condition(text)
        to_bot_condition = check_ask_bot_condition(text, bot.user.id)
        formatted_message_id = format_to_user_address(msg.author.id)
        djigurda_condition = check_djigurda_condition(text)
        boys_condition = check_boys_condition(text)
        valera_condition = check_valera_condition(text)
        ogo_condition = check_ogo_condition(text)
        boyan_condition = check_boyan_condition(text)
        temperature_condition = check_temperature_condition(text)  # TODO temp handling
        p2p_condition = check_p2p_condition(text)

        if cheat_condition:
            await msg.channel.send('CHEATING IS SLAVERY!')
        elif to_bot_condition:
            await msg.channel.send(f'{formatted_message_id}, ask peer on left, and then on right.')
        elif djigurda_condition:
            await msg.channel.send('http://coub.com/view/l7dseqm')
        elif boys_condition:
            await msg.channel.send('http://coub.com/view/zaf54')
        elif valera_condition:
            await msg.channel.send('https://coub.com/view/zmte7')
        elif ogo_condition:
            await msg.channel.send('https://coub.com/view/zq15r')
        elif boyan_condition:
            await msg.channel.send('https://coub.com/view/1ceayt1i')
        elif p2p_condition:
            await msg.channel.send('https://www.youtube.com/watch?v=XGG_4BLssrg')
