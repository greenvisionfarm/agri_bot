from bot import constants
from data_core import main_constants


def create_message(result, data):
    return constants.answer_message.format(result, data)


def validation_of_incoming_data(data: str):
    data = data.split(' ')
    first_letter = data[0]

    if first_letter not in main_constants.products:
        return False

    elif len(data) == 1 or (len(data) == 2 and data[1] == 'graf'):
        return data

    return False
