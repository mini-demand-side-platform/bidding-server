import os

from .data_template import DBServerInfo

oltp_server_info = DBServerInfo(
    host=os.getenv("oltp_host", "localhost"),
    port=os.getenv("oltp_port", "5432"),
    database=os.getenv("oltp_database", "oltp"),
    username=os.getenv("oltp_username", "dsp"),
    password=os.getenv("oltp_password", "dsppassword"),
)
feature_store_hostname = os.getenv("feature_store_hostname", "localhost")
feature_store_id = os.getenv("feature_store_id", "cdc74d4c")
list_feature_uri = os.getenv(
    "list_feature_uri",
    "http://{feature_store_hostname}:8000/feature_store/{feature_store_id}/feature".format(
        feature_store_hostname=feature_store_hostname, feature_store_id=feature_store_id
    ),
)
get_online_features_uri = os.getenv(
    "get_online_features_uri",
    "http://{feature_store_hostname}:8000/online_features".format(
        feature_store_hostname=feature_store_hostname
    ),
)
model_hostname = os.getenv("model_hostname", "localhost")
model_uri = os.getenv(
    "model_uri",
    "http://{model_hostname}:8002/model:predict".format(model_hostname=model_hostname),
)
table_name = os.getenv("table_name", "ad")

default_ctr = float(os.getenv("default_ctr", 0.009905203839797677))
