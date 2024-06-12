"""File that manages translations."""

# This file is part of OpenAndroidInstaller.
# OpenAndroidInstaller is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# OpenAndroidInstaller is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with OpenAndroidInstaller.
# If not, see <https://www.gnu.org/licenses/>."""
# Author: Tobias Sterbak

import locale
import gettext
from loguru import logger


# Initialize localization with user locale if available
try:
    lang = gettext.translation('base', localedir='locales', languages=[locale.getlocale()[0]])
except FileNotFoundError:
    logger.info("User locale not available, fallback to english")
    lang = gettext.translation('base', localedir='locales', languages=['en'])
lang.install()
_ = lang.gettext
