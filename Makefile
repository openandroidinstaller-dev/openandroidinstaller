poetry:
	curl -sSL https://install.python-poetry.org | python3 -

install:
	poetry install
	poetry run python scripts/download-tools.py

export:
	poetry export -f requirements.txt --output requirements.txt

test:
	poetry run pytest tests/

app:
	poetry run python openandroidinstaller/openandroidinstaller.py

build-app:
	poetry run pyinstaller openandroidinstaller/openandroidinstaller.py --noconsole --noconfirm --onefile --icon "openandroidinstaller/assets/favicon.ico" --add-data "openandroidinstaller/assets:assets" --add-data "openandroidinstaller/bin/:bin" --windowed

clean-build:
	rm -rf build/ dist/
