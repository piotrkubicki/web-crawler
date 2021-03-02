freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-index --output-file requirements.txt setup.py

install:
	pip install -r requirements.txt

install-dev:
	pip install -e ".[dev]"

unit: 
	pytest tests/

lint:
	black main.py tests/

test: lint unit
