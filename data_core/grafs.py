import io
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from data_core.data import ApiData

plt.style.use('seaborn-whitegrid')

def create_graf(product_name: str):
    """ Creating Data-set """
    # result = [[float(product['price'][1:].replace(',', '.')), product['beginDate']] for product in product_group]
    data = ApiData().data_processing(product_name=product_name)
    prices = [day_price[0] for day_price in data]
    # change it ->
    dates = [datetime.strptime(day_price[1], '%d/%m/%Y') for day_price in data]

    png_output = io.BytesIO()

    """ Creating Graph """
    fig, ax = plt.subplots()
    ax.plot(dates, prices)

    canvas = FigureCanvas(fig)
    canvas.print_png(png_output)

    return png_output.getvalue()
