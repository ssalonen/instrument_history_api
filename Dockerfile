FROM python:3.6

# File Author / Maintainer
MAINTAINER Sami Salonen

RUN apt-get update
RUN apt-get install -y libxml2-dev libxslt1-dev
RUN apt-get install -y python-pip
# pcre for uwsgi
RUN apt-get install -y libpcre3 libpcre3-dev
RUN apt-get install -y libffi-dev
RUN apt-get update && apt-get install -y libssl-dev

# Cache build of heavy dependencies using docker
# (ADD of sources invalidates the cache)

RUN pip install -U setuptools==34.3.1
RUN pip install -U pip==9.0.1

# (generated using pip freeze)
RUN pip install appdirs==1.4.3 \
	attrs==16.3.0 \
	Automat==0.5.0 \
	cffi==1.9.1 \
	constantly==15.1.0 \
	cryptography==1.7.2 \
	cssselect==1.0.1 \
	Django==1.10.6 \
	django-filter==1.0.1 \
	djangorestframework==3.6.1 \
	idna==2.5 \
	incremental==16.10.1 \
	isodate==0.5.4 \
	lxml==3.7.3 \
	numpy==1.12.1rc1 \
	packaging==16.8 \
	pandas==0.19.2 \
	parsel==1.1.0 \
	pyasn1==0.2.3 \
	pyasn1-modules==0.0.8 \
	pycparser==2.17 \
	PyDispatcher==2.0.5 \
	pyOpenSSL==16.2.0 \
	pyparsing==2.2.0 \
	python-dateutil==2.6.0 \
	pytz==2016.10 \
	queuelib==1.4.2 \
	requests==2.13.0 \
	Scrapy==1.3.2 \
	service-identity==16.0.0 \
	six==1.10.0 \
	Twisted==17.1.0 \
	w3lib==1.17.0 \
	Warcat==2.2.4 \
	zope.interface==4.3.3


# for the uwsgi server
RUN pip install uwsgi==2.0.14


#COPY logging.ini /app/logging.ini
COPY instrument_history_api /app/instrument_history_api/
COPY setup.py /app/
COPY manage.py /app/
RUN pip install /app/

ARG SECRET_KEY
ENV SECRET_KEY $SECRET_KEY

# Volume for warc files
VOLUME /data
# Volume for database
VOLUME /db

# wsgi
EXPOSE 8080
# http
EXPOSE 9090
WORKDIR /app

COPY docker_resources/production_settings.py /app/instrument_history_api/api_app/settings/production.py
ENV DJANGO_SETTINGS_MODULE instrument_history_api.api_app.settings.production

RUN cd /app/ && pip freeze && which pip && which python && ls -l --color && \
	 python manage.py collectstatic --no-input
CMD ["/bin/bash", "-c", "python manage.py migrate && /usr/local/bin/uwsgi --ini uwsgi.ini"]
COPY docker_resources/uwsgi.ini /app/
COPY docker_resources/logging.ini /app/logging.ini
ENV LOGGING_INI /app/logging.ini
