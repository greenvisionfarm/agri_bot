import io
import logging
from datetime import datetime, timedelta

import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from data_core import main_constants

logger = logging.getLogger(__name__)

# plt.style.use('seaborn-whitegrid')

# Constants
DAYS_SHORT = 30
DAYS_LONG = 120
HTTP_TIMEOUT = 10


class ApiData:
    def __init__(self):
        self.url = main_constants.main_url
        self.country = 'SK'
        self.begin_date = self.get_begin_date(DAYS_SHORT)
        logger.debug(f"ApiData initialized with url={self.url}, country={self.country}, begin_date={self.begin_date}")

    @staticmethod
    def get_begin_date(days=30):
        date = (datetime.now() - timedelta(days=days)).strftime("%d/%m/%Y")
        logger.debug(f"Calculated begin_date: {date} ({days} days ago)")
        return date

    @staticmethod
    def get_data(request_url: str) -> list:
        """Get data from API with timeout and error handling"""
        logger.debug(f"Making HTTP request to: {request_url}")
        try:
            response = requests.get(request_url, timeout=HTTP_TIMEOUT)
            logger.debug(f"HTTP response status: {response.status_code}")
            response.raise_for_status()
            json_data = response.json()
            
            if isinstance(json_data, dict):
                errors = json_data.get("error", False)
                if errors:
                    logger.warning(f"API returned error for URL: {request_url}")
                    return [False, False]
            
            logger.debug(f"Successfully retrieved data from API")
            return json_data
            
        except requests.Timeout:
            logger.error(f"Request timeout ({HTTP_TIMEOUT}s) for URL: {request_url}")
            return [False, False]
        except requests.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code} for URL: {request_url}")
            return [False, False]
        except requests.RequestException as e:
            logger.error(f"Request failed for URL {request_url}: {e}")
            return [False, False]
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return [False, False]

    def create_requests_url(self, product_type: str, product: str, date: str) -> str:
        """Create API request URL based on product type"""
        base_url = f'{self.url}/{product_type}/prices?beginDate={date}&memberStateCodes={self.country}&'
        
        if product_type == main_constants.cereal:
            request_url = f'{base_url}productCodes={product}'
        else:
            request_url = f'{base_url}products={product}'
        
        logger.debug(f"Created request URL: {request_url}")
        return request_url

    def get_product_prices(self, product: str, **kwargs) -> list:
        """Get product prices from API"""
        product_type = main_constants.products_groups[product]
        date = kwargs.get("date", self.begin_date)
        logger.debug(f"Getting prices for {product} (type: {product_type}, date: {date})")
        
        request_url = self.create_requests_url(product_type, product, date)
        result = self.get_data(request_url)
        
        if result == [False, False]:
            logger.warning(f"No data returned for product {product}")
        else:
            logger.debug(f"Retrieved {len(result) if isinstance(result, list) else 'unknown'} items for {product}")
        
        return result

    def data_processing(self, product_name: str) -> list:
        """Process data and return price and date"""
        logger.info(f"Starting data processing for product: {product_name}")
        
        try:
            product_code = main_constants.products_dict[product_name]
            logger.debug(f"Mapped product name '{product_name}' to code '{product_code}'")
            
            product_group = self.get_product_prices(product_code)[0]
            
            if not product_group:
                logger.info(f"No recent data for {product_name}, trying extended date range ({DAYS_LONG} days)")
                date = self.get_begin_date(days=DAYS_LONG)
                product_group = self.get_product_prices(product_code, date=date)[0]
                
                if not product_group:
                    logger.warning(f"No data available for product {product_name} even with extended range")
                    return [False, False]
            
            price = product_group['price']
            begin_date = product_group['beginDate']
            price = price.replace(',', '.')
            
            logger.info(f"Successfully processed data for {product_name}: price={price}, date={begin_date}")
            return [price, begin_date]
            
        except KeyError as e:
            logger.error(f"KeyError in data_processing for {product_name}: {e}", exc_info=True)
            return [False, False]
        except Exception as e:
            logger.error(f"Unexpected error in data_processing for {product_name}: {e}", exc_info=True)
            return [False, False]

    @staticmethod
    def change_date_format(date: str) -> str:
        """Change date format from DD/MM/YYYY to DD/MM/YYYY"""
        try:
            day, month, year = date.split("/")
            formatted = f"{day}/{month}/{year}"
            logger.debug(f"Date format changed: {date} -> {formatted}")
            return formatted
        except ValueError as e:
            logger.error(f"Invalid date format: {date}, error: {e}")
            return date

    @staticmethod
    def change_price(price: str) -> float:
        """Convert price string to float (handles both comma and dot as decimal separator)"""
        try:
            # Replace comma with dot for European format
            price = price.replace("€", "").replace(",", ".")
            result = float(price)
            logger.debug(f"Price converted: {price} -> {result}")
            return result
        except (ValueError, AttributeError) as e:
            logger.error(f"Failed to convert price '{price}': {e}")
            return 0.0

    def create_graf(self, product_name: str):
        """Create price chart for product"""
        logger.info(f"Creating graph for product: {product_name}")
        
        try:
            self.begin_date = self.get_begin_date(days=DAYS_LONG)
            product_code = main_constants.products_dict[product_name]
            logger.debug(f"Fetching data for graph: {product_name} ({product_code})")
            
            product_group = self.get_product_prices(product_code)
            
            if not product_group or product_group == [False, False]:
                logger.warning(f"No data available for graph: {product_name}")
                return False
            
            data_dict = {
                self.change_date_format(value.get('beginDate')): self.change_price(value.get('price'))
                for value in product_group
            }
            
            if len(data_dict) <= 2:
                logger.warning(f"Not enough data points for graph ({len(data_dict)} points): {product_name}")
                return False
            
            logger.info(f"Graph data prepared: {len(data_dict)} data points")
            
            dates, prices = zip(*data_dict.items())
            dates = tuple(reversed(dates))
            prices = tuple(reversed(prices))
            
            """ Creating Graph """
            png_output = io.BytesIO()
            fig, ax = plt.subplots()
            ax.plot(dates, prices)
            ax.set_xlabel('Date')
            ax.set_ylabel('Price (€)')
            ax.set_title(f'{product_name} Price Trend')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            canvas = FigureCanvas(fig)
            canvas.print_png(png_output)
            plt.close(fig)
            logger.debug("Graph created and matplotlib figure closed")
            
            graph_size = len(png_output.getvalue())
            logger.info(f"Graph created successfully for {product_name} (size: {graph_size} bytes)")
            return png_output.getvalue()
            
        except Exception as e:
            logger.error(f"Error creating graph for {product_name}: {e}", exc_info=True)
            return False
