from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import List

import requests
from dacite import from_dict

from .data_template import BidRequest, EligibleAd, FeaturesInfo, OnlineFeatureInput
from .logger import get_logger

log = get_logger(logger_name="ctr_prediction")


class CtrPrediction(ABC):
    @abstractmethod
    def get_predictions(self):
        pass


class PredictionServerWithFeatureStore(ABC):
    def __init__(
        self,
        model_uri: str,
        list_feature_uri: str,
        get_online_features_uri: str,
    ) -> None:
        self._model_uri = model_uri
        self._list_feature_uri = list_feature_uri
        self._get_online_features_uri = get_online_features_uri
        try:
            self._features_info = self._load_feature_info()
            log.info("Loaded feature info")
        except Exception as e:
            log.error("Error during load the feature info: {error}".format(error=e))
            self._features_info = None

    def get_predictions(
        self, eligible_ads: List[EligibleAd], bid_request: BidRequest
    ) -> List[float]:
        if self._features_info is None:
            self._features_info = self._features_info()
            if self._features_info is None:
                raise AttributeError("feature_info is None")
        online_features = []
        for eligible_ad in eligible_ads:
            online_feature_input = self._get_online_feature_input(
                eligible_ad=eligible_ad, bid_request=bid_request
            )
            online_feature = requests.post(
                self._get_online_features_uri, json=asdict(online_feature_input)
            ).json()

            online_features.append(online_feature)
        return requests.post(self._model_uri, json={"inputs": online_features}).json()

    def _load_feature_info(self) -> None:
        response = requests.get(self._list_feature_uri)
        features_info = response.json()
        self._features_info = from_dict(data_class=FeaturesInfo, data=features_info)

    def _get_online_feature_input(
        self, eligible_ad: EligibleAd, bid_request: BidRequest
    ) -> OnlineFeatureInput:
        features = OnlineFeatureInput(
            inputs=[], feature_ids=[], feature_store_function_types=[]
        )

        for i in range(len(self._features_info["source_column_name"])):
            if self._features_info["source_column_name"][i] in eligible_ad.__dict__:
                features.inputs.append(
                    eligible_ad[self._features_info["source_column_name"][i]]
                )
            elif self._features_info["source_column_name"][i] in bid_request.__dict__:
                features.inputs.append(
                    bid_request[self._features_info["source_column_name"][i]]
                )
            else:
                log.error(
                    (
                        "Not able to find the source_column_name: {source_column_name} "
                        "in the ads or bidrequest"
                    ).format(
                        source_column_name=self._features_info["source_column_name"][i]
                    )
                )
                features.inputs.append(None)
        features.feature_ids = self._features_info["feature_id"]
        features.feature_store_function_types = self._features_info[
            "feature_function_type"
        ]
        return features
