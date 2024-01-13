"""File to import to manage translations."""

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

import os
import gettext


# Initialize localization
# TODO : Automaticaly check user locale and if available, use it.
fr = gettext.translation('base', localedir='locales', languages=['fr'])
fr.install()
_ = fr.gettext # French
#os.environ['LANGUAGE']='fr'
#_ = gettext.gettext
