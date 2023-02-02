import requests

"""
Names of products
Cereal Products     'Milling wheat': "BLTPAN"
                    'Maize': 'MAI'
Oilseed Products    'Rapeseed': 'Rapeseed'
"""

def get_product_prices(product: str, main_url: str, begin_date: str, end_date: str) -> list:
    """ Product Type """
    if product == 'BLTPAN' or product == 'MAI':
        product_type = 'cereal'
    else:
        product_type = 'oilseeds'

    """ Make a Request """
    url = f'{main_url}/{product_type}/prices?beginDate={begin_date}&endDate={end_date}&'

    if product_type == 'cereal':
        request_url = f'{url}productCodes={product}&marketCodes=BRAT'
        response = requests.get(request_url).json()
        return response
    if product_type == 'oilseeds':
        request_url = f'{url}products={product}&memberStateCodes=HU'
        response = requests.get(request_url).json()
        return response
