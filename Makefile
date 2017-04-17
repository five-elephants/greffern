NGINX_PROXY_CONTAINER="docker ps --filter='name=nginx-proxy' -q"

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
		--env="FLASK_DEBUG=1" \
		--env="VIRTUAL_HOST=mrcluster.duckdns.org" \
		--env="LETSENCRYPT_HOST=mrcluster.duckdns.org" \
		--env="LETSENCRYPT_EMAIL=simonf256@googlemail.com" \
		--rm=true \
		-ti greffern-remote

sync-dev:
	find daq | xargs -I file docker cp file greffern-remote-dev:/home/john/daq/
	find ui | xargs -I file docker cp file greffern-remote-dev:/home/john/


nginx-proxy:
	docker run -d \
		--name=nginx-proxy \
		-p 80:80 -p 443:443 \
		-v /var/run/docker.sock:/tmp/docker.sock:ro \
		-v /home/pi/volumes/certs:/etc/nginx/certs:ro \
		-v /etc/nginx/vhost.d \
		-v /usr/share/nginx/html \
		rpi-nginx-proxy

letsencrypt:
	docker run -d \
		--name=letsencrypt \
		-v /home/pi/volumes/certs:/etc/nginx/certs:rw \
		--env="NGINX_PROXY_CONTAINER=nginx-proxy" \
		--env="DEBUG=1" \
		--volumes-from nginx-proxy \
		-v /var/run/docker.sock:/var/run/docker.sock:ro \
		rpi-letsencrypt-nginx-proxy-companion
