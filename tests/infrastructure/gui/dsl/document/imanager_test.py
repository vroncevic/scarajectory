# -*- coding: UTF-8 -*-

'''
Module
    imanager_test.py
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
    Unit tests for IDslDocumentManager protocol.
'''

from __future__ import annotations

from tkinter import Widget
from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.document.imanager import IDslDocumentManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockDocumentManager:
    '''Mock implementation satisfying IDslDocumentManager structurally.'''

    def open_document(
        self,
        *,
        parent: Widget,
        initial_dir: str = '',
    ) -> tuple[str, str]:
        '''Open document.'''
        del parent, initial_dir
        return 'content', '/tmp/file.scara'

    def save_document(
        self,
        *,
        parent: Widget,
        content: str,
        initial_dir: str = '',
    ) -> str:
        '''Save document.'''
        del parent, content, initial_dir
        return '/tmp/file.scara'

    def get_version(self) -> str:
        '''Return version.'''
        return '1.0.3'


class IncompleteDocumentManager:
    '''Mock class failing to implement IDslDocumentManager.'''

    def open_document(
        self,
        *,
        parent: Widget,
        initial_dir: str = '',
    ) -> tuple[str, str]:
        '''Open document.'''
        del parent, initial_dir
        return 'content', '/tmp/file.scara'

    def get_name(self) -> str:
        '''Return name.'''
        return 'incomplete'


class IDslDocumentManagerTestCase(TestCase):
    '''
        Unit test suite validating IDslDocumentManager protocol.

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
        mock = MockDocumentManager()
        self.assertIsInstance(mock, IDslDocumentManager)

    def test_incomplete_compliance(self) -> None:
        '''
            Tests that incomplete class fails protocol check.

            :exceptions: None.
        '''
        mock = IncompleteDocumentManager()
        self.assertNotIsInstance(mock, IDslDocumentManager)


if __name__ == '__main__':
    main()
