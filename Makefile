APP := app
PORT := 8081
PYTHON3_8 := $(shell command -v python3.8 2> /dev/null)

ifndef PYTHON3_8
    $(error "Python 3.8 is not installed! See README.md")
endif

ifeq (${IS_CI}, true)
	FLAGS := "--ci"
else
	FLAGS := "-s"
endif

.PHONY: mypy test all clean dev timeseries-docker

all: env mypy test
# all: env mypy lint test

env: env/bin/activate

env/bin/activate: requirements.txt
	test -d env || python3.8 -m venv env
	. env/bin/activate; pip install wheel; pip install -Ue ".[dev]"
	touch env/bin/activate

mypy: env
	. env/bin/activate; mypy --ignore-missing-imports app

test: env
	. env/bin/activate; pytest $(FLAGS)

lint: env
	. env/bin/activate; pylint app

clean:
	rm -rf env
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

dev: env
	. env/bin/activate; FLASK_ENV=development FLASK_APP=$(APP) FLASK_DEBUG=1 flask run --port=$(PORT) --host=0.0.0.0

timeseries-docker:
	docker run -p 6379:6379 -it -d --rm redislabs/redistimeseries
