all: image

image:
	docker build -t greffern-remote .

run:
	docker run \
		--name=greffern-remote-prod \
		-v greffern-data:/data \
		-p 80:5000 \
		-d greffern-remote

dev:
	docker run \
		--name=greffern-remote-dev \
		-v greffern-data-dev:/data \
		-p 80:5000 \
		--env="FLASK_DEBUG=1" \
		--rm=true \
		-ti greffern-remote

sync-dev:
	find daq | xargs -I file docker cp file greffern-remote-dev:/home/john/daq/
	find ui | xargs -I file docker cp file greffern-remote-dev:/home/john/
