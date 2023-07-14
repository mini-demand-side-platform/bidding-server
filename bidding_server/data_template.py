from dataclasses import dataclass
from typing import Any, List

from pydantic import BaseModel


class BidRequestInput(BaseModel):
    bid_floor: float
    height: float
    width: float
    hist_ctr: float
    hist_cvr: float


class BidRequestOutput(BaseModel):
    price: float
    ad_id: int


@dataclass
class BidRequest:
    bid_floor: float
    height: float
    width: float
    hist_ctr: float
    hist_cvr: float


@dataclass
class Bid:
    price: float
    ad_id: int


@dataclass
class FeaturesInfo:
    feature_id: List[str]
    feature_name: List[str]
    source_table_name: List[str]
    source_column_name: List[str]
    feature_function_type: List[str]


@dataclass
class OnlineFeatureInput:
    inputs: List[Any]
    feature_ids: List[str]
    feature_store_function_types: List[str]


@dataclass
class EligibleAd:
    ad_id: str
    bidding_cpc: int
    advertiser: str
    banner_style: str
    category: str
    layout_style: str
    item_price: float

    def __getitem__(self, key):
        return getattr(self, key)


@dataclass
class DBServerInfo:
    host: str
    port: str
    database: str
    username: str
    password: str
