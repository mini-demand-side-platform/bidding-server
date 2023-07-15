from unittest import TestCase

from bidding_server.bidding_strategy import ClickPerCost
from bidding_server.data_template import Bid, EligibleAd


class TestCtrPrediction(TestCase):
    cpc = ClickPerCost()

    def test_get_features(self):
        test_ad_1 = EligibleAd(
            ad_id=1228,
            bidding_cpc=1,
            advertiser="QQ",
            banner_style="VII",
            category="Pullover",
            layout_style="MP",
            item_price=2896.437,
        )
        test_ad_2 = EligibleAd(
            ad_id=1227,
            bidding_cpc=2,
            advertiser="QQ",
            banner_style="VII",
            category="Pullover",
            layout_style="MP",
            item_price=2896.437,
        )
        test_bid = Bid(price=0.4, ad_id=1227)

        assert test_bid == self.cpc.make_bid(
            eligible_ads=[test_ad_1, test_ad_2], ctr_list=[0.1, 0.2]
        )
