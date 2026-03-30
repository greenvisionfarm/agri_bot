import logging

from bot import constants
from data_core import main_constants

logger = logging.getLogger(__name__)


def create_message(result: str, data: str) -> str:
    """Format response message"""
    logger.debug(f"Creating message: result={result}, data={data}")
    message = constants.answer_message.format(result, data)
    logger.debug(f"Formatted message: {message}")
    return message


def validation_of_incoming_data(data: str):
    """Validate user input"""
    logger.debug(f"Validating input: '{data}'")
    data = data.split(' ')
    first_letter = data[0]

    if first_letter not in main_constants.products:
        logger.debug(f"Validation failed: product '{first_letter}' not in allowed list")
        return False

    elif len(data) == 1 or (len(data) == 2 and data[1] == 'graf'):
        logger.debug(f"Validation successful: {data}")
        return data

    logger.debug(f"Validation failed: invalid format")
    return False
