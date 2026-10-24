# -*- coding: UTF-8 -*-

'''
Module
    console_test.py
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
    Unit tests for DslConsoleView component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.console.console import DslConsoleView
from scarajectory.infrastructure.gui.dsl.console.iconsole import IDslConsoleView

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslConsoleViewTestCase(TestCase):
    '''
        Unit test suite validating DslConsoleView component.

        It defines:

            :methods:
                | setUp - Initializes Tkinter root and console instance.
                | tearDown - Cleans up Tkinter root window.
                | test_protocol_compliance - Tests structural protocol satisfaction.
                | test_append_log - Tests appending messages with severity levels.
                | test_log - Tests logging success and error shortcuts.
                | test_clear - Tests clearing output buffer.
                | test_get_version - Tests component version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture and console widget.

            :exceptions: None.
        '''
        self.root = Tk()
        self.root.withdraw()
        self.console = DslConsoleView(self.root)

    def tearDown(self) -> None:
        '''
            Cleans up Tkinter window.

            :exceptions: None.
        '''
        self.console.destroy()
        self.root.destroy()

    def test_protocol_compliance(self) -> None:
        '''
            Tests that DslConsoleView satisfies IDslConsoleView structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.console, IDslConsoleView)

    def test_append_log(self) -> None:
        '''
            Tests appending messages with various tags.

            :exceptions: None.
        '''
        self.console.append_log('Info message', level='info')
        self.console.append_log('Warning message', level='warning')
        self.console.append_log('Fallback message', level='unknown_level')
        text = self.console.get_text()
        self.assertIn('Info message', text)
        self.assertIn('Warning message', text)
        self.assertIn('Fallback message', text)

    def test_log(self) -> None:
        '''
            Tests logging success and error shortcuts.

            :exceptions: None.
        '''
        self.console.log('Success log', is_error=False)
        self.console.log('Error log', is_error=True)
        text = self.console.get_text()
        self.assertIn('Success log', text)
        self.assertIn('Error log', text)

    def test_clear(self) -> None:
        '''
            Tests clearing console output buffer.

            :exceptions: None.
        '''
        self.console.append_log('Message')
        self.console.clear()
        self.assertEqual(self.console.get_text(), '\n')

    def test_get_version(self) -> None:
        '''
            Tests component version string.

            :exceptions: None.
        '''
        self.assertEqual(self.console.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
