# -*- coding: UTF-8 -*-

'''
Module
    main.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scarajectory is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scarajectory is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Main entry point for SCARAjectory Motion Studio.
'''

from __future__ import annotations

from sys import exit as sys_exit

from scarajectory.engine import SCARAjectory
from scarajectory.setup.factory import SCARAjectoryBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


def main() -> bool:
    '''
        Bootstraps and runs SCARAjectory with required adapters and configuration.

        :return: True if successful, False otherwise.
        :exceptions: None.
    '''
    scarajectory: SCARAjectory = SCARAjectory(SCARAjectoryBundleFactory.create_bundle())

    return scarajectory.process()


if __name__ == '__main__':
    '''
        Entry point for SCARAjectory execution.

        :exit code: 0 if successful, 1 otherwise.
        :exceptions: None.
    '''
    sys_exit(0 if main() else 1)
