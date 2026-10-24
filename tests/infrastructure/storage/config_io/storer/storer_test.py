# -*- coding: UTF-8 -*-

'''
Module
    storer_test.py
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
    Unit tests for ConfigStorer component.
'''

from __future__ import annotations

from json import load
from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from scarajectory.infrastructure.storage.config_io.storer.storer import ConfigStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestConfigStorer(TestCase):
    '''
        Test cases verifying ConfigStorer operations.

        It defines:

            :methods:
                | setUp - Initializes test context and storer instance.
                | test_store_configuration - Verifies store method writes valid JSON file.
    '''

    def setUp(self) -> None:
        '''Initializes test fixtures.'''
        context: ContextBundle = ContextBundleFactory.create_bundle()
        self.storer = ConfigStorer(context_bundle=context)

    def test_store_configuration(self) -> None:
        '''Verifies storing dictionary writes valid JSON content.'''
        data = {'name': 'test_config', 'enabled': True}
        with NamedTemporaryFile('w', delete=False, suffix='.json') as tmp_file:
            tmp_path = tmp_file.name

        try:
            result = self.storer.store(tmp_path, data)
            self.assertTrue(result)
            with open(tmp_path, 'r', encoding='utf-8') as f:
                saved_data = load(f)
            self.assertEqual(saved_data, data)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_get_version(self) -> None:
        '''Verifies get_version returns component version string.'''
        self.assertEqual(self.storer.get_version(), '1.0.3')
