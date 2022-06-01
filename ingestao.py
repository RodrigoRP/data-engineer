import datetime
from abc import abstractmethod, ABC

import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

print(requests.get("https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21").json())


class MercadoBitcoinApi(ABC):
    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        # verifica chamada se esta ok, caso nao retorna uma excecao
        response.raise_for_status()
        return response.json()


class DaySummaryApi(MercadoBitcoinApi):
    type = "day-summary"

    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


print(DaySummaryApi(coin="BTC").get_data(date=datetime.date(2021, 4, 4)))
