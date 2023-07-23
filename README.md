![Build](https://github.com/mini-demand-side-platform/bidding-server/workflows/build/badge.svg)
![Test](https://github.com/mini-demand-side-platform/bidding-server/workflows/test/badge.svg)

# Bidding Server
This is the bidder server of the [mini-demand-side-platform](https://github.com/mini-demand-side-platform/mini-demand-side-platform). The bidder server handles bid request and returns the most suitable ads and price. 

When the server received a bid request, it

1. Gets the eligible ads in the database.
2. Does the feature engineering by custom feature store service.  
3. Makes the click through rate prediction.
4. Based on the click through rate, comes up a suitable price.

See the whole bidding flow [here](https://github.com/mini-demand-side-platform/mini-demand-side-platform).

## Usages
Send bid request.
```bash
curl -X 'POST' \
  'http://localhost:8003/bw_dsp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "bid_floor": 0,
    "height": 0,
    "width": 0,
    "hist_ctr": 0,
    "hist_cvr": 0
  }'
```
Expected return
```json
{
    "price": 0.011083252882497738,
    "ad_id": 1955
}
```

## Requirements
- docker
- docker-compose 
- make

## Setup
#### 1. Activate databases 
```
git clone git@github.com:mini-demand-side-platform/databases.git
cd databases 
make run-all-with-example-data
```
#### 2. Run Feature Store
```bash
docker run -it --rm --network mini-demand-side-platform \
    -p 8000:8000 \
    -e olap_host='postgresql' \
    -e cache_host='redis' \
    raywu60kg/feature-store
```
#### 3. Run ML Serving 
```bash
docker run -it --rm --network mini-demand-side-platform \
    -p 8002:8002 \
    -e object_storage_host='minio' \
	  raywu60kg/ml-serving
```
#### 4. Run Bidding Server
```bash
docker run -it --rm --network mini-demand-side-platform \
    -p 8003:8003 \
    -e oltp_host='postgresql' \
	  raywu60kg/bidding-server
```

