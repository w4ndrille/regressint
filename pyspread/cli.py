# -*- coding: utf-8 -*-

# Distributed under the terms of the GNU General Public License

"""
**Provides**

* :func:`check_mandatory_dependencies`:
* :class:`PathAction`:
* :class:`CommandLineParser`:
"""

from argparse import ArgumentParser
from pathlib import Path
import sys

try:
    import PyQt6.QtSvg as pyqtsvg
except ImportError:
    pyqtsvg = None

try:
    from pyspread.__init__ import APP_NAME, VERSION
    from pyspread.installer import REQUIRED_DEPENDENCIES
except ImportError:
    from __init__ import APP_NAME, VERSION
    from installer import REQUIRED_DEPENDENCIES


def check_mandatory_dependencies():
    """Checks mandatory dependencies and exits if they are not met"""

    def dependency_warning(message: str):
        """Print warning message to stdout

        :param message: Warning message to be displayed

        """

        sys.stdout.write(f'Warning: {message}\n')

    # Check Python version
    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro
    if major < 3 or major == 3 and minor < 6:
        msg = f"Python has version {major}.{minor}.{micro}" + \
               " but ≥ 3.6 is required."
        dependency_warning(msg)

    for module in REQUIRED_DEPENDENCIES:
        if module.is_installed() is None or not module.is_installed():
            dependency_warning(f"Required module {module.name} not found.")
        elif module.version < module.required_version:
            msg = f"Module {module.name} has version {module.version}" + \
                  f"but {module.required_version} is required."
            dependency_warning(msg)
    if pyqtsvg is None:
        # Import of mandatory module failed
        msg = "Required module PyQt6.QtSvg not found."
        dependency_warning(msg)


class PyspreadArgumentParser(ArgumentParser):
    """Parser for the command line"""

    def __init__(self):
        check_mandatory_dependencies()

        description = "pyspread is a non-traditional spreadsheet that is " \
                      "based on and written in the programming language " \
                      "Python."

        super().__init__(prog=APP_NAME, description=description)

        self.add_argument('--version', action='version', version=VERSION)

        self.add_argument('--default-settings', action='store_true',
                          help='start with default settings and save them on '
                               'exit')

        self.add_argument('file', type=Path, nargs='?', default=None,
                          help='open pyspread file in pys or pysu format')
