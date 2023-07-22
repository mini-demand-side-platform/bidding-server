package_name = bidding-server
tag = 0.1.0

help:  
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

server-dev: ## start local dev server
	uvicorn bidding_server.main:app --reload --port 8003

build-dev: ## build image
	docker build -t mini-demand-side-platform/bidding_server:dev -f ./docker/Dockerfile .

run-dev: ## run image locally
	docker run -it --rm --network mini-demand-side-platform -p 8003:8003 \
	-e oltp_host='postgresql' \
	mini-demand-side-platform/bidding_server:dev