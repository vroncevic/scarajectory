# -*- coding: UTF-8 -*-

'''
Module
    serial_console_test.py
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
    Unit tests for SerialConsole log panel and syntax tagging.
'''

from __future__ import annotations

from tkinter import END, SEL, Text, Tk
from unittest import TestCase, main

from scarajectory.infrastructure.gui.console.serial_console import SerialConsole

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialConsoleTestCase(TestCase):
    '''
        Tests for SerialConsole log viewer component.

        It defines:

            :methods:
                | setUp - Initializes root Tk and SerialConsole fixture.
                | tearDown - Cleans up and destroys widget hierarchy.
                | test_append_log_variants - Verifies incoming, error, and outgoing formats.
                | test_select_all - Verifies all text is selected with SEL tag.
                | test_copy_log - Verifies copy to clipboard with and without active selection.
                | test_clear_log - Verifies log text deletion.
    '''

    root: Tk
    console: SerialConsole

    def setUp(self) -> None:
        '''
            Initializes root Tk and SerialConsole fixture.

            :exceptions: None.
        '''
        self.root = Tk()
        self.console = SerialConsole(self.root)

    def tearDown(self) -> None:
        '''
            Cleans up and destroys widget hierarchy.

            :exceptions: None.
        '''
        self.console.destroy()
        self.root.destroy()

    def test_append_log_variants(self) -> None:
        '''
            Verifies incoming, error, and outgoing log message formats.

            :exceptions: None.
        '''
        self.console.append_log('Ready signal received')
        self.console.append_log('Warning ERR code 12')
        self.console.append_log('G1 X50 Y50', is_outgoing=True)

        text_widgets = [
            w for w in self.console.winfo_children() if isinstance(w, Text)
        ]
        self.assertEqual(len(text_widgets), 1)
        content = text_widgets[0].get('1.0', END)

        self.assertIn('<<< RX: Ready signal received', content)
        self.assertIn('<<< RX: Warning ERR code 12', content)
        self.assertIn('>>> TX: G1 X50 Y50', content)

    def test_select_all(self) -> None:
        '''
            Verifies all text is selected with SEL tag.

            :exceptions: None.
        '''
        self.console.append_log('Sample log line')
        self.console.select_all()

        text_widgets = [
            w for w in self.console.winfo_children() if isinstance(w, Text)
        ]
        self.assertEqual(len(text_widgets), 1)
        ranges = text_widgets[0].tag_ranges(SEL)
        self.assertTrue(len(ranges) >= 2)

    def test_copy_log(self) -> None:
        '''
            Verifies copy to clipboard with and without active selection.

            :exceptions: None.
        '''
        self.console.append_log('Clipboard payload message')

        # Case 1: Without selection (copies entire log)
        self.console.copy_log()
        copied = self.console.clipboard_get()
        self.assertIn('Clipboard payload message', copied)

        # Case 2: With explicit selection
        self.console.select_all()
        self.console.copy_log()
        copied_selected = self.console.clipboard_get()
        self.assertIn('Clipboard payload message', copied_selected)

    def test_clear_log(self) -> None:
        '''
            Verifies log text deletion.

            :exceptions: None.
        '''
        self.console.append_log('Line to be cleared')
        self.console.clear_log()

        text_widgets = [
            w for w in self.console.winfo_children() if isinstance(w, Text)
        ]
        self.assertEqual(len(text_widgets), 1)
        content = text_widgets[0].get('1.0', END).strip()
        self.assertEqual(content, '')


if __name__ == '__main__':
    main()
