# -*- coding: UTF-8 -*-

'''
Module
    status_test.py
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
    Unit tests for StatusSection component.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Label
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.status.ipresenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.toolbar.section.status import StatusSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StatusSectionTestCase(TestCase):
    '''
        Test cases verifying StatusSection component.

        It defines:

            :methods:
                | setUpClass - Sets up root Tk fixture.
                | tearDownClass - Tears down root Tk fixture.
                | setUp - Sets up mock dependencies and status section.
                | tearDown - Tears down status section widget.
                | test_cursor_label_registered - Tests registration with presenter.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up root Tk fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down root Tk fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def setUp(self) -> None:
        '''
            Sets up mock dependencies and status section.

            :exceptions: None.
        '''
        self.mock_presenter = MagicMock(spec=ICanvasStatusPresenter)
        self.section = StatusSection(self.root, self.mock_presenter)

    def tearDown(self) -> None:
        '''
            Tears down status section widget.

            :exceptions: None.
        '''
        self.section.destroy()

    def test_cursor_label_registered(self) -> None:
        '''
            Tests registration with presenter.

            :exceptions: None.
        '''
        lbl: Label = self.section.cursor_label
        self.assertIsInstance(lbl, Label)
        self.mock_presenter.set_hover_label.assert_called_once_with(lbl)


if __name__ == '__main__':
    main()
