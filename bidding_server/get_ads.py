from dataclasses import dataclass, fields
from typing import List

from .data_template import EligibleAd
from .dbs import Database
from .logger import get_logger

log = get_logger(logger_name="get_ads")


class GetAds:
    def get_eligible_ads(self):
        raise NotImplementedError


class GetAdsFromDatabase(GetAds):
    def get_eligible_ads(self, table_name: str, database: Database) -> List[EligibleAd]:
        try:
            eligible_ad_fields = fields(EligibleAd)
            data = database.read(
                table_name=table_name,
                column_names=[
                    eligible_ad_field.name for eligible_ad_field in eligible_ad_fields
                ],
                condiction="WHERE status='True'",
            )
            return [dataclass.from_dict(d, EligibleAd) for d in data]
        except Exception as e:
            log.error("Get eligible ads error: {}".format(e))
            return []
