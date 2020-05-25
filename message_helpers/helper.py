import re

from message_helpers.words_source import *


def check_ask_bot_condition(text, bot_id):
    return re.match(f'\\s*<@!{bot_id}>.*\\?\\s*$', text) is not None


def format_to_user_address(user_id: int) -> str:
    return f'<@!{user_id}>'


def check_word_is_in_array(text, array):
    a = set(text.split())
    return any(i in a for i in array)


def check_profane_condition(text):
    return check_word_is_in_array(text, profane_words)


def check_cheat_condition(text):
    return check_word_is_in_array(text, cheat_words)


def check_djigurda_condition(text):
    return check_word_is_in_array(text, normal_djigurda_words)


def check_boys_condition(text):
    return check_word_is_in_array(text, boys_boys_boys_words)


def check_valera_condition(text):
    return check_word_is_in_array(text, valera_words)


def check_ogo_condition(text):
    return check_word_is_in_array(text, ogo_chyo_words)


def check_boyan_condition(text):
    return check_word_is_in_array(text, boyan_words)


def check_temperature_condition(text):
    return check_word_is_in_array(text, temperature_words)


def check_p2p_condition(text):
    return check_word_is_in_array(text, best_peer_to_peer_words)
