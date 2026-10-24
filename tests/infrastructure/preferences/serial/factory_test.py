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
    Unit tests for SerialFactory component.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scarajectory.infrastructure.preferences.serial.dependencies import SerialDependencies
from scarajectory.infrastructure.preferences.serial.factory import SerialFactory
from scarajectory.infrastructure.preferences.serial.provides import SerialProvides
from scarajectory.infrastructure.preferences.serial.repository import SerialPreferenceRepository
from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialFactoryTest(TestCase):
    '''Test cases verifying SerialFactory creation behavior.'''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test method.

            :exceptions: None.
        '''
        self.context: ContextBundle = ContextBundleFactory.create_bundle()
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=self.context)
        )
        self.loader = io_provides.config_loader
        self.storer = io_provides.config_storer

    def test_create_returns_serial_provides(self) -> None:
        '''
            Verifies SerialFactory.create returns valid SerialProvides wrapping repository.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial_preferences.json'
            deps = SerialDependencies(
                config_loader=self.loader,
                config_storer=self.storer,
                config_file=config_file,
            )
            provides: SerialProvides = SerialFactory.create(deps)
            self.assertIsInstance(provides, SerialProvides)
            self.assertIsInstance(
                provides.serial_preference_repository, ISerialPreferenceRepository
            )
            self.assertIsInstance(
                provides.serial_preference_repository, SerialPreferenceRepository
            )

    def test_create_with_default_config_path(self) -> None:
        '''
            Verifies SerialFactory.create with default config path.

            :exceptions: None.
        '''
        deps = SerialDependencies(
            config_loader=self.loader,
            config_storer=self.storer,
        )
        provides: SerialProvides = SerialFactory.create(deps)
        self.assertIsInstance(provides, SerialProvides)
        self.assertIsInstance(
            provides.serial_preference_repository, ISerialPreferenceRepository
        )

    def test_get_version(self) -> None:
        '''
            Verifies SerialFactory.get_version returns semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(SerialFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
