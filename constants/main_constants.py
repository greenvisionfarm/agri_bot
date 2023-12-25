""" Main constants """
# Api url
main_url = 'https://ec.europa.eu/agrifood/api'

# Products groups
cereal = 'cereal'
oilseeds = 'oilseeds'

# Products
psenica = 'Pšenica'
kukurica = 'Kukurica'
raps = 'Raps'

# Products Sorts
psenica_sh = 'BLTPAN'
kukurica_sh = 'MAI'
raps_sh = 'Rapeseed'

products = [psenica, kukurica, raps]
products_dict = {
    psenica: psenica_sh,
    kukurica: kukurica_sh,
    raps: raps_sh
}
products_groups = {
    psenica_sh: cereal,
    kukurica_sh: cereal,
    raps_sh: oilseeds
}

# Messages
start_message_text = 'Údaje prevzaté z web-page Central European Commission'
answer_message = 'Cena: {} €\nData: {}'
error_message = 'Nerozumiem. Použite tlačidlá'
