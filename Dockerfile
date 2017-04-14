FROM armhf/alpine:3.5
LABEL maintainer "simonf256@googlemail.com"
RUN apk update && apk upgrade && apk add \
	bash \
	bc \
	freetype-dev \
	libpng-dev \
	pkgconf \
	postgresql \
	py-flask \
	py-numpy \
	py-pip \
	py-psycopg2 \
	py-setuptools \
	py-sqlalchemy \
	python2 \
	&& rm -rf /var/cache/apk/*
RUN pip install bokeh
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
COPY daq/cron-acquire /etc/periodic/15min/
RUN su -c "pg_ctl start -w -D /data/db -l /data/db/pg_ctl.logfile && psql -f /home/john/daq/create.sql" - postgres
VOLUME /data
CMD ["/usr/local/bin/startup.sh"]
EXPOSE 5000

