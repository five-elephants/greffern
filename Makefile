NGINX_PROXY_CONTAINER="docker ps --filter='name=nginx-proxy' -q"

all: image

image:
	docker build -t greffern-remote .

run: nginx-proxy letsencrypt dev

stop:
	docker stop greffern-remote nginx-proxy letsencrypt
	docker rm nginx-proxy letsencrypt

prod:
	docker run \
		--name=greffern-remote-prod \
		-v greffern-data:/data \
		-p 80:5000 \
		-d greffern-remote

dev:
	docker run \
		--name=greffern-remote-dev \
		-v greffern-data-dev:/data \
		-v /home/ubuntu/webcam:/webcam:ro \
		--env="FLASK_DEBUG=1" \
		--env="VIRTUAL_HOST=greffern.duckdns.org" \
		--env="LETSENCRYPT_HOST=greffern.duckdns.org" \
		--env="LETSENCRYPT_EMAIL=simonf256@googlemail.com" \
		--rm=true \
		greffern-remote

sync-dev:
	find daq | xargs -I file docker cp file greffern-remote-dev:/home/john/daq/
	find ui | xargs -I file docker cp file greffern-remote-dev:/home/john/


nginx-proxy:
	docker run -d \
		--name=nginx-proxy \
		-p 80:80 -p 443:443 \
		-v /var/run/docker.sock:/tmp/docker.sock:ro \
		-v /home/ubuntu/volumes/certs:/etc/nginx/certs:ro \
		-v /etc/nginx/vhost.d \
		-v /usr/share/nginx/html \
		jwilder/nginx-proxy

letsencrypt:
	docker run -d \
		--name=letsencrypt \
		-v /home/ubuntu/volumes/certs:/etc/nginx/certs:rw \
		--env="NGINX_PROXY_CONTAINER=nginx-proxy" \
		--env="DEBUG=1" \
		--volumes-from nginx-proxy \
		-v /var/run/docker.sock:/var/run/docker.sock:ro \
		jrcs/letsencrypt-nginx-proxy-companion
