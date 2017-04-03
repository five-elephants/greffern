all: image

image:
	docker build -t greffern-remote .

run:
	docker run --rm=true -v greffern-data:/data -ti greffern-remote 
