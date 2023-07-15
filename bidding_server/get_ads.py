from dataclasses import fields
from typing import List

from dacite import from_dict

from .data_template import EligibleAd
from .dbs import Database
from .logger import get_logger

log = get_logger(logger_name="get_ads")


class GetAds:
    def get_eligible_ads(self):
        raise NotImplementedError


class GetAdsFromDatabase(GetAds):
    def __init__(self, table_name: str, database: Database):
        self._table_name = table_name
        self._database = database

    def get_eligible_ads(self) -> List[EligibleAd]:
        try:
            eligible_ad_fields = fields(EligibleAd)
            data = self._database.read(
                table_name=self._table_name,
                column_names=[
                    eligible_ad_field.name for eligible_ad_field in eligible_ad_fields
                ],
                condiction="WHERE status='True'",
            )
            return [from_dict(data_class=EligibleAd, data=d) for d in data]
        except Exception as e:
            log.error("Get eligible ads error: {}".format(e))
            return []
