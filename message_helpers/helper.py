import re

from message_helpers.words_source import profane_words, cheat_words


def check_tig_condition(text):
    a = set(text.split())
    return any(i in a for i in profane_words)


def check_cheat_condition(text):
    a = set(text.split())
    return any(i in a for i in cheat_words)


def check_ask_bot_condition(text, bot_id):
    return re.match(f'\\s*<@!{bot_id}>.*\\?\\s*$', text) is not None


def format_to_user_address(user_id: int) -> str:
    return f'<@!{user_id}>'
