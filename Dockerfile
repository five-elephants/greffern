FROM alpine:3.5
LABEL maintainer "simonf256@googlemail.com"
RUN apk update && apk upgrade && apk add \
	bash \
	bc \
	freetype-dev \
	libpng-dev \
	pkgconf \
	postgresql \
	py-babel \
	py-flask \
	py-numpy \
	py-pip \
	py-psycopg2 \
	py-setuptools \
	py-sqlalchemy \
	python2 \
	py-tz \
	tzdata \
    && cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
    && echo "Europe/Berlin" > /etc/timezone \
    && apk del tzdata \
	&& rm -rf /var/cache/apk/*
RUN pip install \
	bokeh \
	flask-bootstrap \
	flask-login \
	flask-wtf
RUN adduser postgres wheel \
	&& mkdir -p /data/db \
	&& chown postgres:postgres /data/db \
	&& su -c "initdb -D /data/db" - postgres \
	&& adduser -h /home/john -s /bin/bash -D john
COPY daq/temperature.sh \
	sys/startup.sh \
	/usr/local/bin/
COPY daq /home/john/daq
COPY ui /home/john/
#COPY daq/cron-alerts /etc/periodic/hourly/   # disable alerts for now
RUN su -c "pg_ctl start -w -D /data/db -l /data/db/pg_ctl.logfile && psql -f /home/john/daq/create.sql" - postgres
VOLUME /data
CMD ["/usr/local/bin/startup.sh"]
EXPOSE 5000
