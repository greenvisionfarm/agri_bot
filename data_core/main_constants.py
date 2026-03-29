""" Main constants """
# Api url
main_url = 'https://ec.europa.eu/agrifood/api'

# Date range for API requests
begin_date = '01/01/2020'
end_date = '31/12/2030'

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
