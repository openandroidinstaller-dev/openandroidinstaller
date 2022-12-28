poetry:
	curl -sSL https://install.python-poetry.org | python3 -

install:
	poetry install
	poetry run python scripts/download-tools.py

export:
	poetry export -f requirements.txt --output requirements.txt

format:
	poetry run black .

lint:
	poetry run ruff openandroidinstaller/ --ignore E501

test: format lint
	PYTHONPATH=openandroidinstaller:$(PYTHONPATH) poetry run pytest --cov=openandroidinstaller tests/

app:
	poetry run python openandroidinstaller/openandroidinstaller.py

test-app:
	poetry run python openandroidinstaller/openandroidinstaller.py --test --test_config sargo

build-app:
	poetry run python scripts/build.py

clean-build:
	rm -rf build/ dist/
