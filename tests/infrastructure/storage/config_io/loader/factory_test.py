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
    Unit tests for LoaderFactory.
'''

from __future__ import annotations

from unittest import TestCase

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from scarajectory.infrastructure.storage.config_io.loader.dependencies import LoaderDependencies
from scarajectory.infrastructure.storage.config_io.loader.factory import LoaderFactory
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestLoaderFactory(TestCase):
    '''
        Test cases verifying LoaderFactory operations.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates LoaderProvides.
                | test_get_version - Verifies factory returns version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory creates LoaderProvides containing IConfigLoader.'''
        context: ContextBundle = ContextBundleFactory.create_bundle()
        provides = LoaderFactory.create(LoaderDependencies(context_bundle=context))
        self.assertIsInstance(provides.config_loader, IConfigLoader)

    def test_get_version(self) -> None:
        '''Verifies factory returns version string.'''
        self.assertEqual(LoaderFactory.get_version(), '1.0.3')
