import json
import logging

from bs4 import BeautifulSoup

from project.api_base_client import APIBaseClient

logger = logging.getLogger(__name__)


class PromUa(APIBaseClient):
    base_url = 'https://prom.ua/ua/Foto-videokamery-i-aksessuary'

    def _prepare_data(self) -> list:
        self._request(
            'get',
        )
        results = []
        if self.response and self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            category = soup.find('div', attrs={'data-qaid': 'caption'}).text
            for item in soup.find_all('div', class_='js-productad'):
                try:
                    results.append({
                        'sku': item.get('data-product-id'),
                        'category': category,
                        'image': item.find('picture').find('img').get('src'),
                        'name': item.find('span', attrs={
                            'data-qaid': 'product_name'}).text,
                        'description': json.loads(item.find('script').text)[
                            'description'],
                        'price': item.find('div', attrs={
                            'data-qaid': 'product_price'}).get('data-qaprice')
                    })
                except Exception as err:
                    logger.error(err)
        return results

    def parse(self) -> list:
        return self._prepare_data()

    def get_image(self, url):
        self._request(
            'get',
            url=url
        )
        return self.response


parser_client = PromUa()
