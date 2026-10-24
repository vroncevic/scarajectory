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
    Unit testing for ConfigIOFactory.
'''

from __future__ import annotations

from unittest import TestCase

from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader
from scarajectory.infrastructure.storage.config_io.provides import ConfigIOProvides
from scarajectory.infrastructure.storage.config_io.storer.istorer import IConfigStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestConfigIOFactory(TestCase):
    '''Unit tests validating ConfigIOFactory creation and version.'''

    def test_create_with_dependencies(self) -> None:
        '''Verifies create with explicit dependencies returns ConfigIOProvides.'''
        context = ContextBundleFactory.create_bundle()
        deps = ConfigIODependencies(context_bundle=context)
        provides = ConfigIOFactory.create(dependencies=deps)
        self.assertIsInstance(provides, ConfigIOProvides)
        self.assertIsInstance(provides.config_loader, IConfigLoader)
        self.assertIsInstance(provides.config_storer, IConfigStorer)

    def test_get_version(self) -> None:
        '''Verifies get_version returns semantic version string.'''
        self.assertEqual(ConfigIOFactory.get_version(), '1.0.3')
