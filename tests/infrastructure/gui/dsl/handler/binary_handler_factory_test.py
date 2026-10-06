# -*- coding: UTF-8 -*-

'''
Module
    binary_handler_factory_test.py
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
    Unit tests for DslEditorBinaryHandlerFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.handler.binary_handler import DslEditorBinaryHandler
from scarajectory.infrastructure.gui.dsl.handler.binary_handler_bundle import BinaryHandlerBundle
from scarajectory.infrastructure.gui.dsl.handler.binary_handler_factory import DslEditorBinaryHandlerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslEditorBinaryHandlerFactory(TestCase):
    '''
        Test cases verifying DslEditorBinaryHandlerFactory instantiation and versioning.
    '''

    def test_factory_version(self) -> None:
        '''
            Tests that get_version returns expected version string.
        '''
        self.assertEqual(DslEditorBinaryHandlerFactory.get_version(), '1.0.3')

    def test_create_instance(self) -> None:
        '''
            Tests that create returns a configured DslEditorBinaryHandler instance.
        '''
        bundle = BinaryHandlerBundle(
            parent=MagicMock(),
            editor=MagicMock(),
            console=MagicMock(),
            compiler=MagicMock(),
            decompiler=MagicMock(),
            storage=MagicMock(),
            diagnostics=MagicMock(),
        )
        handler: DslEditorBinaryHandler = DslEditorBinaryHandlerFactory.create(bundle=bundle)
        self.assertIsInstance(handler, DslEditorBinaryHandler)


if __name__ == '__main__':
    main()
