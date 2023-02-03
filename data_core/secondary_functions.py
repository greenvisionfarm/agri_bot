""" Validation of incoming data """


def validation_of_incoming_data(data: str):
    products = ['Pšenica', 'Kukurica', 'Raps']

    data = data.split(' ')
    first_letter = data[0]

    if first_letter not in products:
        return False
    elif len(data) == 1:
        return data
    elif len(data) == 2 and data[1] == 'graf':
        return data
    return False
