# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for BinaryHandlerBundle parameter container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.handler.binary.bundle import BinaryHandlerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryHandlerBundle(TestCase):
    '''
        Tests verifying BinaryHandlerBundle fields, properties, and immutability.
    '''

    def test_bundle_creation_and_properties(self) -> None:
        '''
            Tests bundle fields and properties pass-through.

            :exceptions: None.
        '''
        mock_parent = MagicMock()
        mock_editor = MagicMock()
        mock_console = MagicMock()
        mock_dsl = MagicMock()
        mock_loader = MagicMock()
        mock_storer = MagicMock()

        bundle = BinaryHandlerBundle(
            parent=mock_parent,
            editor=mock_editor,
            console=mock_console,
            dsl=mock_dsl,
            loader=mock_loader,
            storer=mock_storer,
        )

        self.assertIs(bundle.parent, mock_parent)
        self.assertIs(bundle.editor, mock_editor)
        self.assertIs(bundle.console, mock_console)
        self.assertIs(bundle.dsl, mock_dsl)
        self.assertIs(bundle.loader, mock_loader)
        self.assertIs(bundle.storer, mock_storer)
        self.assertIs(bundle.compiler, mock_dsl.compiler)
        self.assertIs(bundle.decompiler, mock_dsl.decompiler)
        self.assertIs(bundle.diagnostics, mock_dsl.diagnostics)


if __name__ == '__main__':
    main()
