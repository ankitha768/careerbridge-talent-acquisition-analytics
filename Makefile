install:
	pip install -r requirements.txt
	playwright install chromium
run:
	uvicorn app.main:app --reload
test:
	pytest -q
