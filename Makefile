poetry:
	curl -sSL https://install.python-poetry.org | python3 -
	export PATH="$HOME/.local/bin:$PATH"

install:
	poetry install
	poetry run python scripts/download-tools.py

test:
	poetry run pytest tests/

app:
	poetry run python openandroidinstaller/openandroidinstaller.py

build-app:
	poetry run pyinstaller openandroidinstaller/openandroidinstaller.py --noconsole --noconfirm --onefile --icon "/assets/favicon.ico" --add-data "openandroidinstaller/assets:assets" --add-binary "openandroidinstaller/bin/adb:bin" --add-binary "openandroidinstaller/bin/fastboot:bin" --add-binary "openandroidinstaller/bin/heimdall:bin"

clean-build:
	rm -rf build/ dist/
