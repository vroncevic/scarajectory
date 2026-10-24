# -*- coding: UTF-8 -*-

'''
Module
    icatalog_test.py
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
    Unit tests for IDslExampleCatalog protocol.
'''

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.catalog.icatalog import IDslExampleCatalog

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockExampleCatalog:
    '''Mock implementation satisfying IDslExampleCatalog structurally.'''

    def examples_dir(self) -> Path:
        '''Return path.'''
        return Path('/tmp')

    def get_example_files(self) -> tuple[str, ...]:
        '''Return files.'''
        return ('example.scara',)

    def load_example_content(self, filename: str) -> str:
        '''Return content.'''
        return f'content of {filename}'

    def get_version(self) -> str:
        '''Return version.'''
        return '1.0.3'


class IncompleteCatalog:
    '''Mock class failing to implement IDslExampleCatalog.'''

    def examples_dir(self) -> Path:
        '''Return path.'''
        return Path('/tmp')

    def get_name(self) -> str:
        '''Return mock name.'''
        return 'incomplete'


class IDslExampleCatalogTestCase(TestCase):
    '''
        Unit test suite validating IDslExampleCatalog runtime checking.

        It defines:

            :methods:
                | test_structural_compliance - Tests protocol matching.
                | test_incomplete_compliance - Tests protocol rejection.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Tests that structurally compliant class matches protocol.

            :exceptions: None.
        '''
        mock = MockExampleCatalog()
        self.assertIsInstance(mock, IDslExampleCatalog)

    def test_incomplete_compliance(self) -> None:
        '''
            Tests that incomplete class fails protocol check.

            :exceptions: None.
        '''
        mock = IncompleteCatalog()
        self.assertNotIsInstance(mock, IDslExampleCatalog)


if __name__ == '__main__':
    main()
