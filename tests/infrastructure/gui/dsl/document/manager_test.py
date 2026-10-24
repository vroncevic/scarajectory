# -*- coding: UTF-8 -*-

'''
Module
    manager_test.py
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
    Unit tests for DslDocumentManager component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.gui.dsl.document.imanager import IDslDocumentManager
from scarajectory.infrastructure.gui.dsl.document.manager import DslDocumentManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslDocumentManagerTestCase(TestCase):
    '''
        Unit test suite validating DslDocumentManager functionality.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and Tkinter root.
                | tearDown - Cleans up Tkinter root window.
                | test_protocol_compliance - Validates protocol satisfaction.
                | test_open_document_success - Tests successful document open.
                | test_open_document_cancelled - Tests cancelling document open.
                | test_open_document_error - Tests error handling on open.
                | test_save_document_success - Tests successful document save.
                | test_save_document_cancelled - Tests cancelling document save.
                | test_save_document_error - Tests error handling on save.
                | test_get_version - Tests component version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures and Tkinter root.

            :exceptions: None.
        '''
        self.root = Tk()
        self.root.withdraw()
        self.loader = MagicMock(spec=IPlanLoader)
        self.storer = MagicMock(spec=IPlanStorer)
        self.manager = DslDocumentManager(
            loader=self.loader,
            storer=self.storer,
        )

    def tearDown(self) -> None:
        '''
            Cleans up Tkinter root.

            :exceptions: None.
        '''
        self.root.destroy()

    def test_protocol_compliance(self) -> None:
        '''
            Tests that DslDocumentManager satisfies IDslDocumentManager structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.manager, IDslDocumentManager)

    @patch('scarajectory.infrastructure.gui.dsl.document.manager.askopenfilename')
    def test_open_document_success(self, mock_ask: MagicMock) -> None:
        '''
            Tests opening document successfully when file dialog succeeds.

            :param mock_ask: Mocked askopenfilename dialog function.
            :exceptions: None.
        '''
        mock_ask.return_value = '/tmp/test.scara'
        self.loader.load_text_file.return_value = 'DSL CODE'

        content, path = self.manager.open_document(parent=self.root)
        self.assertEqual(content, 'DSL CODE')
        self.assertEqual(path, '/tmp/test.scara')
        self.loader.load_text_file.assert_called_once_with(filepath='/tmp/test.scara')

    @patch('scarajectory.infrastructure.gui.dsl.document.manager.askopenfilename')
    def test_open_document_cancelled(self, mock_ask: MagicMock) -> None:
        '''
            Tests opening document when cancelled by user.

            :param mock_ask: Mocked askopenfilename dialog function.
            :exceptions: None.
        '''
        mock_ask.return_value = ''
        content, path = self.manager.open_document(parent=self.root)
        self.assertEqual(content, '')
        self.assertEqual(path, '')
        self.loader.load_text_file.assert_not_called()

    @patch('scarajectory.infrastructure.gui.dsl.document.manager.showerror')
    @patch('scarajectory.infrastructure.gui.dsl.document.manager.askopenfilename')
    def test_open_document_error(
        self,
        mock_ask: MagicMock,
        mock_err: MagicMock,
    ) -> None:
        '''
            Tests opening document when loader raises OSError.

            :param mock_ask: Mocked askopenfilename dialog function.
            :param mock_err: Mocked showerror message box function.
            :exceptions: None.
        '''
        mock_ask.return_value = '/tmp/error.scara'
        self.loader.load_text_file.side_effect = OSError('Disk read failed')

        content, path = self.manager.open_document(parent=self.root)
        self.assertEqual(content, '')
        self.assertEqual(path, '')
        mock_err.assert_called_once()

    @patch('scarajectory.infrastructure.gui.dsl.document.manager.asksaveasfilename')
    def test_save_document_success(self, mock_ask: MagicMock) -> None:
        '''
            Tests saving document successfully when file dialog succeeds.

            :param mock_ask: Mocked asksaveasfilename dialog function.
            :exceptions: None.
        '''
        mock_ask.return_value = '/tmp/saved.scara'
        result: str = self.manager.save_document(
            parent=self.root,
            content='CODE TO SAVE',
        )
        self.assertEqual(result, '/tmp/saved.scara')
        self.storer.save_text_file.assert_called_once_with(
            content='CODE TO SAVE',
            filepath='/tmp/saved.scara',
        )

    @patch('scarajectory.infrastructure.gui.dsl.document.manager.asksaveasfilename')
    def test_save_document_cancelled(self, mock_ask: MagicMock) -> None:
        '''
            Tests saving document when cancelled by user.

            :param mock_ask: Mocked asksaveasfilename dialog function.
            :exceptions: None.
        '''
        mock_ask.return_value = ''
        result: str = self.manager.save_document(
            parent=self.root,
            content='CODE',
        )
        self.assertEqual(result, '')
        self.storer.save_text_file.assert_not_called()

    @patch('scarajectory.infrastructure.gui.dsl.document.manager.showerror')
    @patch('scarajectory.infrastructure.gui.dsl.document.manager.asksaveasfilename')
    def test_save_document_error(
        self,
        mock_ask: MagicMock,
        mock_err: MagicMock,
    ) -> None:
        '''
            Tests saving document when storer raises OSError.

            :param mock_ask: Mocked asksaveasfilename dialog function.
            :param mock_err: Mocked showerror message box function.
            :exceptions: None.
        '''
        mock_ask.return_value = '/tmp/error.scara'
        self.storer.save_text_file.side_effect = OSError('Disk write failed')

        result: str = self.manager.save_document(
            parent=self.root,
            content='CODE',
        )
        self.assertEqual(result, '')
        mock_err.assert_called_once()

    def test_get_version(self) -> None:
        '''
            Tests component version getter.

            :exceptions: None.
        '''
        self.assertEqual(self.manager.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
