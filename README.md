![Build](https://github.com/mini-demand-side-platform/bidding-server/workflows/build/badge.svg)
![Test](https://github.com/mini-demand-side-platform/bidding-server/workflows/test/badge.svg)

# bidding-server

```
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