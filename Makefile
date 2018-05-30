
VER := $(shell python setup.py --version 2> /dev/null)
DJANGO_SECRET_KEY := $(shell python scripts/generate_django_secret.py)

version:
	@echo $(VER)

test_generate_secret:
	@echo "$(DJANGO_SECRET_KEY)"

clean:
	rm -rf financedatahoarder || true

build:
	docker build -t instrument_history_api:$(VER) --build-arg SECRET_KEY="$(DJANGO_SECRET_KEY)" .
	docker tag instrument_history_api:$(VER) instrument_history_api:latest

run:
	docker run -d -v /mnt/docker/djangodb:/db/ -v /path/to/warc:/data/ --name instrument_history_api_app --restart=always instrument_history_api:$(VER)

run.dev:
	# assuming selinux so mount with :z
	docker run -P -d -v /tmp/djangodb:/db/:z -v /home/salski/src/warc-testdata:/data/:z --restart=always instrument_history_api:$(VER)

stop_container:
	docker rm -f instrument_history_api_app
