# -*- coding: UTF-8 -*-

'''
Module
    console_view_test.py
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

from scarajectory.infrastructure.gui.dsl.console_view import DslConsoleView

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslConsoleView(TestCase):
    '''
        Test cases verifying DslConsoleView layout, tagging, and logging behavior.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''Creates root Tkinter window in headless hidden mode.'''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''Destroys root Tkinter window.'''
        cls.root.destroy()

    def setUp(self) -> None:
        '''Initializes DslConsoleView instance for each test.'''
        self.console = DslConsoleView(self.root)

    def tearDown(self) -> None:
        '''Destroys console widget after each test.'''
        self.console.destroy()

    def test_init_state(self) -> None:
        '''Verifies initial console state is empty and read-only.'''
        self.assertEqual(self.console.get_text(), '')

    def test_append_log_levels(self) -> None:
        '''Verifies append_log correctly writes multi-level messages.'''
        self.console.append_log('Info message', level='info')
        self.console.append_log('Success message', level='success')
        self.console.append_log('Warning message', level='warning')
        self.console.append_log('Error message', level='error')
        self.console.append_log('Fallback message', level='unknown_level')

        content: str = self.console.get_text()
        self.assertIn('Info message', content)
        self.assertIn('Success message', content)
        self.assertIn('Warning message', content)
        self.assertIn('Error message', content)
        self.assertIn('Fallback message', content)

    def test_log_delegation(self) -> None:
        '''Verifies log method delegates to append_log with success and error levels.'''
        self.console.log('Passed operation', is_error=False)
        self.console.log('Failed operation', is_error=True)

        content: str = self.console.get_text()
        self.assertIn('Passed operation', content)
        self.assertIn('Failed operation', content)

    def test_clear_buffer(self) -> None:
        '''Verifies clear resets the console buffer.'''
        self.console.append_log('Some message to clear')
        self.assertNotEqual(self.console.get_text(), '')

        self.console.clear()
        self.assertEqual(self.console.get_text(), '')


if __name__ == '__main__':
    main()
