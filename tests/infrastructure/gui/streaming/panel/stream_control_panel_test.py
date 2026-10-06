# -*- coding: UTF-8 -*-

'''
Module
    stream_control_panel_test.py
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
    Unit testing for StreamControlPanel component.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Button
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.streaming.panel.stream_control_panel import StreamControlPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamControlPanelTestCase(TestCase):
    '''
        Unit tests for StreamControlPanel widget.

        It defines:

            :methods:
                | setUp - Initializes headless Tk root.
                | tearDown - Destroys Tk root.
                | test_panel_buttons_layout - Verifies 3 action buttons exist.
                | test_panel_button_actions - Verifies button commands invoke delegate.
    '''

    def setUp(self) -> None:
        '''Initializes headless Tk instance before each test.'''
        self.root: Tk = Tk()
        self.root.withdraw()

    def tearDown(self) -> None:
        '''Destroys Tk instance after each test.'''
        self.root.destroy()

    def test_panel_buttons_layout(self) -> None:
        '''Verifies StreamControlPanel instantiates three control buttons.'''
        mock_delegate = MagicMock()
        panel = StreamControlPanel(self.root, control_delegate=mock_delegate)
        buttons = [w for w in panel.winfo_children() if isinstance(w, Button)]
        self.assertEqual(len(buttons), 3)

    def test_panel_button_actions(self) -> None:
        '''Verifies button clicks invoke corresponding delegate methods.'''
        mock_delegate = MagicMock()
        panel = StreamControlPanel(self.root, control_delegate=mock_delegate)
        buttons = [w for w in panel.winfo_children() if isinstance(w, Button)]

        buttons[0].invoke()
        mock_delegate.on_start_stream.assert_called_once()

        buttons[1].invoke()
        mock_delegate.on_pause_resume_stream.assert_called_once()

        buttons[2].invoke()
        mock_delegate.on_stop_stream.assert_called_once()


if __name__ == '__main__':
    main()
