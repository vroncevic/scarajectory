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
    Unit testing for MainContentBuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.layout.builder import MainContentBuilder
from scarajectory.infrastructure.gui.layout.factory import MainContentBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MainContentBuilderFactoryTestCase(TestCase):
    '''
        Unit tests for MainContentBuilderFactory.

        It defines:

            :methods:
                | test_create_default - Verifies default factory creation.
                | test_create_with_collaborators - Verifies creation with custom sub-builders.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create_default(self) -> None:
        '''
            Verifies create returns MainContentBuilder instance with default sub-builders.

            :exceptions: None.
        '''
        builder = MainContentBuilderFactory.create()
        self.assertIsInstance(builder, MainContentBuilder)

    def test_create_with_collaborators(self) -> None:
        '''
            Verifies create_with_collaborators wires explicit sub-builders.

            :exceptions: None.
        '''
        builder = MainContentBuilderFactory.create_with_collaborators(
            canvas_pane_builder=MagicMock(),
            toolbar_builder=MagicMock(),
            editor_pane_builder=MagicMock(),
        )
        self.assertIsInstance(builder, MainContentBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        ver = MainContentBuilderFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
