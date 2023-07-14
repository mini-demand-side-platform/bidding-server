import os

from data_template import DBServerInfo

feature_mapping = {
    0: {"layout_style": "AB"},
    1: {"layout_style": "RU"},
    2: {"layout_style": "GY"},
    3: {"layout_style": "MR"},
    4: {"layout_style": "BK"},
    5: {"layout_style": "BX"},
    6: {"layout_style": "RZ"},
    7: {"layout_style": "TY"},
    8: {"category": "Shirt"},
    9: {"layout_style": "DX"},
}


bidding_strategy = os.getenv("bidding_strategy", "cpc")

get_ads_method = os.getenv("get_ads_method", "postgres")


oltp_server_info = DBServerInfo(
    host=os.getenv("oltp_host", "localhost"),
    port=os.getenv("oltp_port", "5432"),
    database=os.getenv("oltp_database", "oltp"),
    username=os.getenv("oltp_username", "dsp"),
    password=os.getenv("oltp_password", "dsppassword"),
)

feature_store_uri = os.getenv(
    "feature_store_uri",
    "http://localhost:8000/feature_store/{feature_store_id}/feature",
)

model_uri = os.getenv("model_uri", "http://localhost:8000/model:predict")
