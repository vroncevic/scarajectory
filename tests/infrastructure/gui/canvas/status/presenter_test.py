# -*- coding: UTF-8 -*-

'''
Module
    presenter_test.py
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
    Unit tests for CanvasStatusPresenter component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.status.ipresenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.canvas.status.presenter import CanvasStatusPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasStatusPresenter(TestCase):
    '''
        Test cases verifying CanvasStatusPresenter behavior.

        It defines:

            :methods:
                | setUp - Prepares presenter instance for test execution.
                | test_satisfies_protocol - Verifies structural protocol conformance.
                | test_update_status_before_label_set - Verifies update before label.
                | test_update_status_with_label - Verifies readout updates with label.
    '''

    def setUp(self) -> None:
        '''
            Prepares presenter instance for test execution.

            :exceptions: None.
        '''
        self.presenter: CanvasStatusPresenter = CanvasStatusPresenter()

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies that presenter satisfies ICanvasStatusPresenter.

            :exceptions: None.
        '''
        self.assertIsInstance(self.presenter, ICanvasStatusPresenter)

    def test_update_status_before_label_set(self) -> None:
        '''
            Verifies updating status before setting label does not raise.

            :exceptions: None.
        '''
        self.presenter.update_cursor_status('X: 10.0 Y: 20.0')
        self.presenter.clear_status()

    def test_update_status_with_label(self) -> None:
        '''
            Verifies setting hover label updates widget text.

            :exceptions: None.
        '''
        mock_label = MagicMock()
        self.presenter.set_hover_label(mock_label)
        self.presenter.update_cursor_status('X: 15.0 Y: 25.0')
        mock_label.config.assert_called_with(text='X: 15.0 Y: 25.0')

        self.presenter.clear_status()
        mock_label.config.assert_called_with(text='')


if __name__ == '__main__':
    main()
