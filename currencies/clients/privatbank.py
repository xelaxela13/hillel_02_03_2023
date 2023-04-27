from currencies.models import CurrencyHistory
from project.api_base_client import APIBaseClient


class PrivatBank(APIBaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def _prepare_data(self) -> list:
        """
        [
            {"ccy":"EUR","base_ccy":"UAH","buy":"40.55000","sale":"41.55000"},
            {"ccy":"USD","base_ccy":"UAH","buy":"37.22000","sale":"37.72000"}
        ]
        [{'code': 'USD', "buy":"40.55000","sale":"41.55000"},]
        :return: dict
        """
        self._request(
            'get',
            params={
                'json': '',
                'exchange': '',
                'coursid': 5
            }
        )
        results = []
        if self.response:
            for i in self.response.json():
                results.append({
                    'code': i['ccy'],
                    'buy': i['buy'],
                    'sale': i['sale'],
                })
        return results

    def save(self):
        results = []
        for i in self._prepare_data():
            results.append(
                CurrencyHistory(
                    **i
                )
            )
        if results:
            CurrencyHistory.objects.bulk_create(results)


privatbank_client = PrivatBank()
