.PHONY: install run-api run-web test clean

install:
	pip install -r requirements.txt

run-api:
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

run-web:
	python web_app.py

test:
	pytest tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
