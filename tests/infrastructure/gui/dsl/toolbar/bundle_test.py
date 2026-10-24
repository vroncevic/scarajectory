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
    Unit tests for DslEditorToolbarBundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.toolbar.bundle import DslEditorToolbarBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslEditorToolbarBundle(TestCase):
    '''
        Tests verifying DslEditorToolbarBundle fields and immutability.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Tests bundle instantiation and field accessibility.

            :exceptions: None.
        '''
        mock_exec = MagicMock()
        mock_file = MagicMock()
        mock_bin = MagicMock()

        bundle = DslEditorToolbarBundle(
            execution_delegate=mock_exec,
            file_delegate=mock_file,
            binary_delegate=mock_bin,
        )

        self.assertIs(bundle.execution_delegate, mock_exec)
        self.assertIs(bundle.file_delegate, mock_file)
        self.assertIs(bundle.binary_delegate, mock_bin)


if __name__ == '__main__':
    main()
