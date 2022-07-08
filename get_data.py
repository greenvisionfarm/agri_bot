import os
import requests

key = os.environ.get('KEY')
url = f'https://flux.agritel.com/agritelwebsite/QuotesAjax.aspx?key={key}'
all_res = requests.get(url).json()


def get_ebm():
    result = all_res['data'][0]
    ebm_v = result['value']
    ebm_t = result['time']
    return [ebm_v, ebm_t]


def get_ema():
    result = all_res['data'][6]
    ema_v = result['value']
    ema_t = result['time']
    return [ema_v, ema_t]


def get_eco():
    result = all_res['data'][10]
    eco_v = result['value']
    eco_t = result['time']
    return [eco_v, eco_t]


