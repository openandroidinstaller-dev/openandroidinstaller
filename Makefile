.phoney: install export format lint typing test app test-app build-app clean-build

help:
	@echo "install - install dependencies"
	@echo "export - export dependencies to requirements.txt"
	@echo "format - format code with black"
	@echo "lint - lint code with ruff"
	@echo "typing - type check code with mypy"
	@echo "test - run tests"
	@echo "app - run app"
	@echo "test-app - run app in test mode with test config for sargo"
	@echo "build-app - build app"
	@echo "clean-build - clean build"

poetry:
	curl -sSL https://install.python-poetry.org | python3 -

install:
	rm poetry.lock
	rm -rf openandroidinstaller/bin
	poetry install --with dev
	poetry run python scripts/download-tools.py
	poetry run pre-commit install

export:
	poetry export -f requirements.txt --output requirements.txt

format:
	poetry run black .

lint:
	poetry run ruff check openandroidinstaller/ --ignore E501

typing:
	poetry run mypy openandroidinstaller/. --ignore-missing-imports

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
