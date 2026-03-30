import io
import logging
from datetime import datetime, timedelta

import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from data_core import main_constants

logger = logging.getLogger(__name__)

# plt.style.use('seaborn-whitegrid')

# Константы
DAYS_SHORT = 30
DAYS_LONG = 120
HTTP_TIMEOUT = 10


class ApiData:
    def __init__(self):
        self.url = main_constants.main_url
        self.country = 'SK'
        self.begin_date = self.get_begin_date(DAYS_SHORT)
        logger.debug(f"ApiData инициализирован: url={self.url}, country={self.country}, begin_date={self.begin_date}")

    @staticmethod
    def get_begin_date(days=30):
        date = (datetime.now() - timedelta(days=days)).strftime("%d/%m/%Y")
        logger.debug(f"Рассчитана начальная дата: {date} ({days} дней назад)")
        return date

    @staticmethod
    def get_data(request_url: str) -> list:
        """Получение данных из API с таймаутом и обработкой ошибок"""
        logger.debug(f"HTTP-запрос к: {request_url}")
        try:
            response = requests.get(request_url, timeout=HTTP_TIMEOUT)
            logger.debug(f"Статус HTTP-ответа: {response.status_code}")
            response.raise_for_status()
            json_data = response.json()

            if isinstance(json_data, dict):
                errors = json_data.get("error", False)
                if errors:
                    logger.warning(f"API вернул ошибку для URL: {request_url}")
                    return [False, False]

            logger.debug(f"Данные успешно получены из API")
            return json_data

        except requests.Timeout:
            logger.error(f"Таймаут запроса ({HTTP_TIMEOUT}с) для URL: {request_url}")
            return [False, False]
        except requests.HTTPError as e:
            logger.error(f"HTTP-ошибка {e.response.status_code} для URL: {request_url}")
            return [False, False]
        except requests.RequestException as e:
            logger.error(f"Запрос не выполнен для URL {request_url}: {e}")
            return [False, False]
        except ValueError as e:
            logger.error(f"Не удалось распарсить JSON-ответ: {e}")
            return [False, False]

    def create_requests_url(self, product_type: str, product: str, date: str) -> str:
        """Создание URL запроса API на основе типа продукта"""
        base_url = f'{self.url}/{product_type}/prices?beginDate={date}&memberStateCodes={self.country}&'

        if product_type == main_constants.cereal:
            request_url = f'{base_url}productCodes={product}'
        else:
            request_url = f'{base_url}products={product}'

        logger.debug(f"Создан URL запроса: {request_url}")
        return request_url

    def get_product_prices(self, product: str, **kwargs) -> list:
        """Получение цен на продукт из API"""
        product_type = main_constants.products_groups[product]
        date = kwargs.get("date", self.begin_date)
        logger.debug(f"Получение цен для {product} (тип: {product_type}, дата: {date})")

        request_url = self.create_requests_url(product_type, product, date)
        result = self.get_data(request_url)

        if result == [False, False]:
            logger.warning(f"Нет данных для продукта {product}")
        else:
            logger.debug(f"Получено {len(result) if isinstance(result, list) else 'неизвестно'} записей для {product}")

        return result

    def data_processing(self, product_name: str) -> list:
        """Обработка данных и возврат цены и даты"""
        logger.info(f"Начало обработки данных для продукта: {product_name}")

        try:
            product_code = main_constants.products_dict[product_name]
            logger.debug(f"Сопоставление имени продукта '{product_name}' с кодом '{product_code}'")

            product_group = self.get_product_prices(product_code)[0]

            if not product_group:
                logger.info(f"Нет свежих данных для {product_name}, попытка расширенного диапазона дат ({DAYS_LONG} дней)")
                date = self.get_begin_date(days=DAYS_LONG)
                product_group = self.get_product_prices(product_code, date=date)[0]

                if not product_group:
                    logger.warning(f"Нет данных для продукта {product_name} даже с расширенным диапазоном")
                    return [False, False]

            price = product_group['price']
            begin_date = product_group['beginDate']
            price = price.replace(',', '.')

            logger.info(f"Данные успешно обработаны для {product_name}: price={price}, date={begin_date}")
            return [price, begin_date]

        except KeyError as e:
            logger.error(f"KeyError в data_processing для {product_name}: {e}", exc_info=True)
            return [False, False]
        except Exception as e:
            logger.error(f"Неожиданная ошибка в data_processing для {product_name}: {e}", exc_info=True)
            return [False, False]

    @staticmethod
    def change_date_format(date: str) -> str:
        """Изменение формата даты с DD/MM/YYYY на DD/MM/YYYY"""
        try:
            day, month, year = date.split("/")
            formatted = f"{day}/{month}/{year}"
            logger.debug(f"Формат даты изменён: {date} -> {formatted}")
            return formatted
        except ValueError as e:
            logger.error(f"Неверный формат даты: {date}, ошибка: {e}")
            return date

    @staticmethod
    def change_price(price: str) -> float:
        """Преобразование строки цены в float (поддерживает запятую и точку как десятичный разделитель)"""
        try:
            # Замена запятой на точку для европейского формата
            price = price.replace("€", "").replace(",", ".")
            result = float(price)
            logger.debug(f"Цена преобразована: {price} -> {result}")
            return result
        except (ValueError, AttributeError) as e:
            logger.error(f"Не удалось преобразовать цену '{price}': {e}")
            return 0.0

    def create_graf(self, product_name: str):
        """Создание графика цен для продукта"""
        logger.info(f"Создание графика для продукта: {product_name}")

        try:
            self.begin_date = self.get_begin_date(days=DAYS_LONG)
            product_code = main_constants.products_dict[product_name]
            logger.debug(f"Получение данных для графика: {product_name} ({product_code})")

            product_group = self.get_product_prices(product_code)

            if not product_group or product_group == [False, False]:
                logger.warning(f"Нет данных для графика: {product_name}")
                return False

            data_dict = {
                self.change_date_format(value.get('beginDate')): self.change_price(value.get('price'))
                for value in product_group
            }

            if len(data_dict) <= 2:
                logger.warning(f"Недостаточно точек данных для графика ({len(data_dict)} точек): {product_name}")
                return False

            logger.info(f"Данные для графика подготовлены: {len(data_dict)} точек данных")

            dates, prices = zip(*data_dict.items())
            dates = tuple(reversed(dates))
            prices = tuple(reversed(prices))

            """ Создание графика """
            png_output = io.BytesIO()
            fig, ax = plt.subplots()
            ax.plot(dates, prices)
            ax.set_xlabel('Дата')
            ax.set_ylabel('Цена (€)')
            ax.set_title(f'Динамика цен на {product_name}')
            plt.xticks(rotation=45)
            plt.tight_layout()

            canvas = FigureCanvas(fig)
            canvas.print_png(png_output)
            plt.close(fig)
            logger.debug("График создан, фигура matplotlib закрыта")

            graph_size = len(png_output.getvalue())
            logger.info(f"График успешно создан для {product_name} (размер: {graph_size} байт)")
            return png_output.getvalue()

        except Exception as e:
            logger.error(f"Ошибка создания графика для {product_name}: {e}", exc_info=True)
            return False
