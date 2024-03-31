import requests

from src import config
from src.models import Products
from src.utils import load_json_file, save_json_file


class MetroParser:
    def __init__(self, store_id: int):
        self.store_id = store_id
        self.headers = config.headers
        self.json_data = config.json_data
        self.url = config.url
        self.json_file = load_json_file()
        self.metro_url = 'https://online.metro-cc.ru'

    def parse(self):
        """ Парсинг данных """
        self.json_data['variables']['storeId'] = self.store_id
        self.json_data['variables']['from'] = 0
        while True:
            response = requests.post(self.url, headers=self.headers, json=self.json_data)
            category_dict = response.json()['data']['category']
            products_obj = Products.parse_obj(category_dict)
            total = category_dict['total']
            if self.json_data['variables']['from'] > total:
                break
            self.add_product_to_json(products_obj, self.json_file)
            self.json_data['variables']['from'] += self.json_data['variables']['size']

    def add_product_to_json(self, data: Products, json_file: list):
        """ Добавление товаров в файл """
        for product in data.products:
            item = {
                'id товара': product.id, 'наименование': product.name,
                'ссылка на товар': self.metro_url + product.url,
                'регулярная цена': f"{product.stocks[0].prices.old_price} ₽",
                'промо цена': f"{product.stocks[0].prices.price} ₽", 'бренд': product.manufacturer.name
            }
            json_file.append(item)
            save_json_file(json_file)

    def check_product_in_json(self, product_id: int):
        """ Проверка на наличие товара """
        file = self.json_file
        for product in file:
            if str(product_id) in product:
                return False
        return True


if __name__ == '__main__':
    MetroParser(10).parse()
    MetroParser(15).parse()
