from unittest import TestCase

from bidding_server.ctr_prediction import PredictionServerWithFeatureStore
from bidding_server.data_template import BidRequest, EligibleAd, OnlineFeatureInput


class TestCtrPrediction(TestCase):
    cp = PredictionServerWithFeatureStore(
        model_uri="http://localhost:8002/model:predict",
        list_feature_uri="http://localhost:8000/feature_store/{feature_store_id}/feature",
        feature_store_id="test_id",
        get_online_features_uri="http://localhost:8000/online_features",
    )

    def test_get_online_feature_input(self):
        test_ad = EligibleAd(
            ad_id=1228,
            bidding_cpc=1,
            advertiser="QQ",
            banner_style="VII",
            category="Pullover",
            layout_style="MP",
            item_price=2896.437,
        )
        test_bid_request = BidRequest(
            bid_floor=1,
            height=27.341917,
            width=617.5163,
            hist_ctr=0.00036614624,
            hist_cvr=6.790803e-05,
        )
        res = self.cp._get_online_feature_input(
            eligible_ad=test_ad, bid_request=test_bid_request
        )

        test_features = OnlineFeatureInput(
            inputs=["MP", "MP", "MP", "MP", "MP", "MP", "MP", "MP", "Pullover", "MP"],
            feature_ids=[
                "5dbfb549",
                "ea2f676f",
                "0ad63312",
                "a2480212",
                "5aae0b22",
                "65934929",
                "2658049e",
                "717456fc",
                "1d34889f",
                "915a0c3c",
            ],
            feature_store_function_types=[
                "string_mapping",
                "string_mapping",
                "string_mapping",
                "string_mapping",
                "string_mapping",
                "string_mapping",
                "string_mapping",
                "string_mapping",
                "string_mapping",
                "string_mapping",
            ],
        )
        assert test_features == res
