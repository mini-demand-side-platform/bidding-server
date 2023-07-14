from abc import ABC, abstractmethod
from typing import List

from .data_template import Bid, EligibleAd
from .logger import get_logger

log = get_logger(logger_name="bidding_strategy")


class BiddingStrategy(ABC):
    @abstractmethod
    def make_bid(self):
        pass


class ClickPerCost(BiddingStrategy):
    def make_bid(
        self,
        eligible_ads: List[EligibleAd],
        ctr_list: List[float],
    ) -> Bid:
        bid = Bid(ad_id=None, price=0)
        for i in range(len(ctr_list)):
            ad_price = ctr_list[i] * eligible_ads[i].bidding_cpc
            if ad_price > bid.price:
                bid.ad_id = eligible_ads[i].ad_id
                bid.price = ad_price
        return bid
