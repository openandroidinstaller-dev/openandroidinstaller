install:
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install
	poetry run python scripts/download-tools.py

app:
	poetry run python openandroidinstaller/openandroidinstaller.py

build-app: install
	poetry run pyinstaller openandroidinstaller/openandroidinstaller.py --noconsole --noconfirm --onefile --icon "/assets/favicon.ico" --add-data "openandroidinstaller/assets:assets" --add-binary "openandroidinstaller/bin/adb:bin" --add-binary "openandroidinstaller/bin/fastboot:bin" --add-binary "openandroidinstaller/bin/heimdall:bin"


clean-build:
	rm -rf build/ dist/
