install:
	sudo apt update && sudo apt install android-tools-adb android-tools-fastboot
	poetry install

app:
	poetry run python openandroidinstaller/openandroidinstaller.py

build-app:
	poetry run pyinstaller openandroidinstaller/openandroidinstaller.py --noconsole --noconfirm --onefile --icon "/assets/favicon.ico" --add-data "openandroidinstaller/assets:assets" --add-binary "openandroidinstaller/bin/adb:bin/adb" --add-binary "openandroidinstaller/bin/fastboot:bin/fastboot" --add-binary "openandroidinstaller/bin/heimdall:bin/heimdall"


clean-build:
	rm -rf build/ dist/
