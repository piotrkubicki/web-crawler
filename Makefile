
unit: 
	pytest tests/

lint:
	black main.py tests/

test: lint unit
