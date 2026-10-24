# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit testing for EmulatorLauncherFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.emulator.launcher.factory import EmulatorLauncherFactory
from scarajectory.infrastructure.gui.emulator.launcher.ilauncher import IEmulatorLauncher
from scarajectory.infrastructure.gui.emulator.launcher.launcher import EmulatorLauncher
from scarajectory.infrastructure.gui.emulator.locator.ilocator import IEmulatorLocator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorLauncherFactoryTestCase(TestCase):
    '''
        Unit tests for EmulatorLauncherFactory.

        It defines:

            :methods:
                | test_factory_version - Verifies factory version string.
                | test_factory_creates_instance - Verifies factory creates valid instance.
                | test_factory_create_with_collaborators - Verifies creation with custom locator.
    '''

    def test_factory_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        ver: str = EmulatorLauncherFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)

    def test_factory_creates_instance(self) -> None:
        '''
            Verifies EmulatorLauncherFactory instantiates valid launcher.

            :exceptions: None.
        '''
        launcher: IEmulatorLauncher = EmulatorLauncherFactory.create()
        self.assertIsInstance(launcher, IEmulatorLauncher)
        self.assertIsInstance(launcher, EmulatorLauncher)

    def test_factory_create_with_collaborators(self) -> None:
        '''
            Verifies EmulatorLauncherFactory wires injected locator collaborator.

            :exceptions: None.
        '''
        mock_locator = MagicMock(spec=IEmulatorLocator)
        launcher = EmulatorLauncherFactory.create_with_collaborators(
            locator=mock_locator
        )
        self.assertIsInstance(launcher, EmulatorLauncher)
        self.assertIsInstance(launcher, IEmulatorLauncher)


if __name__ == '__main__':
    main()
