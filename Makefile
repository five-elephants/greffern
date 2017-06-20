NGINX_PROXY_CONTAINER="docker ps --filter='name=nginx-proxy' -q"

all: image

clean:
	docker ps -q -a | xargs -r docker rm
	docker images -q --filter="dangling=true" | xargs -r docker rmi

image:
	docker build --no-cache -t greffern-remote .

run: nginx-proxy letsencrypt dev

stop:
	docker ps -q --filter="name=nginx-proxy" | xargs -r docker stop
	docker ps -q --filter="name=letsencrypt" | xargs -r docker stop
	docker ps -q --filter="name=greffern-remote" | xargs -r docker stop

prod:
	docker run \
		--name=greffern-remote-prod \
		-v greffern-data:/data \
		-p 80:5000 \
		-d greffern-remote

dev:
	docker run -d \
		--name=greffern-remote-dev \
		-v greffern-data-dev:/data \
		-v /home/ubuntu/webcam:/webcam:ro \
		--env="FLASK_DEBUG=1" \
		--env="VIRTUAL_HOST=greffern.duckdns.org" \
		--env="LETSENCRYPT_HOST=greffern.duckdns.org" \
		--env="LETSENCRYPT_EMAIL=simonf256@googlemail.com" \
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
		-v /home/ubuntu/volumes/vhost.d:/etc/nginx/vhost.d \
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
