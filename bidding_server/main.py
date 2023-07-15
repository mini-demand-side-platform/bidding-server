from fastapi import FastAPI

from .bidding_strategy import ClickPerCost
from .config import (
    default_ctr,
    feature_store_id,
    get_online_features_uri,
    list_feature_uri,
    model_uri,
    oltp_server_info,
    table_name,
)
from .ctr_prediction import PredictionServerWithFeatureStore
from .data_template import Bid, BidRequest, BidRequestInput, BidRequestOutput
from .dbs import Postgresql
from .get_ads import GetAdsFromDatabase
from .logger import get_logger

log = get_logger(logger_name="main")

app = FastAPI()
db = Postgresql(db_server_info=oltp_server_info)
get_ad = GetAdsFromDatabase(table_name=table_name, database=db)
ctr_prediction = PredictionServerWithFeatureStore(
    model_uri=model_uri,
    list_feature_uri=list_feature_uri,
    feature_store_id=feature_store_id,
    get_online_features_uri=get_online_features_uri,
)
bidding_stratepy = ClickPerCost()
default_bid = Bid(price=-1, ad_id=-1)


@app.get("/health")
def health_check() -> bool:
    return True


@app.post("/bw_dsp", response_model=BidRequestOutput)
def handle_bid_request(bid_request: BidRequestInput):
    bid_request = BidRequest(
        bid_floor=bid_request.bid_floor,
        height=bid_request.height,
        width=bid_request.width,
        hist_ctr=bid_request.hist_ctr,
        hist_cvr=bid_request.hist_cvr,
    )

    # get ads
    try:
        eligible_ads = get_ad.get_eligible_ads()
        if len(eligible_ads) == 0:
            log.warning("No eligible_ads")
            return default_bid
    except Exception as e:
        log.error("Get ads error: {error}".format(error=e))
        return default_bid

    # get prediction
    try:
        ctr_list = ctr_prediction.get_predictions(
            eligible_ads=eligible_ads, bid_request=bid_request
        )

    except Exception as e:
        log.error(
            "Can not get ctr prediction: {error}, will use default ctr".format(error=e)
        )
        ctr_list = [default_ctr] * len(eligible_ads)

    # decide price
    try:
        bid_response = bidding_stratepy.make_bid(
            eligible_ads=eligible_ads, ctr_list=ctr_list
        )
        if bid_response.price < bid_request.bid_floor:
            return default_bid
        else:
            return bid_response
    except Exception as e:
        log.error("Can not decide the bid price: {error}".format(error=e))
        return default_bid
