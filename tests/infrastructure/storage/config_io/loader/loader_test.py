# -*- coding: UTF-8 -*-

'''
Module
    loader_test.py
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
    Unit tests for ConfigLoader component.
'''

from __future__ import annotations

from json import dump
from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from scarajectory.infrastructure.storage.config_io.loader.loader import ConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestConfigLoader(TestCase):
    '''
        Test cases verifying ConfigLoader operations.

        It defines:

            :methods:
                | setUp - Initializes test context and loader instance.
                | test_load_configuration - Verifies load method on valid JSON file.
                | test_load_validated_configuration - Verifies load_validated method.
    '''

    def setUp(self) -> None:
        '''Initializes test fixtures.'''
        context: ContextBundle = ContextBundleFactory.create_bundle()
        self.loader = ConfigLoader(context_bundle=context)

    def test_load_configuration(self) -> None:
        '''Verifies loading JSON configuration returns dictionary payload.'''
        data = {'key': 'value', 'count': 42}
        with NamedTemporaryFile('w', delete=False, suffix='.json') as tmp_file:
            dump(data, tmp_file)
            tmp_path = tmp_file.name

        try:
            result = self.loader.load(tmp_path)
            self.assertEqual(result, data)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_load_validated_configuration(self) -> None:
        '''Verifies loading with schema validation.'''
        data = {'name': 'test'}
        with NamedTemporaryFile('w', delete=False, suffix='.json') as tmp_file:
            dump(data, tmp_file)
            tmp_path = tmp_file.name

        try:
            result = self.loader.load_validated(tmp_path, scheme_path='/nonexistent/schema.json')
            self.assertEqual(result, data)
        finally:
            if exists(tmp_path):
                remove(tmp_path)
