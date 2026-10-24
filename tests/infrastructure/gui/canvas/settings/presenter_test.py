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
    Unit tests for CanvasSettingsPresenter component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.settings.ipresenter import ICanvasSettingsPresenter
from scarajectory.infrastructure.gui.canvas.settings.presenter import CanvasSettingsPresenter
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasSettingsPresenterTestCase(TestCase):
    '''
        Tests CanvasSettingsPresenter component behavior and protocol conformance.

        It defines:

            :methods:
                | setUp - Sets up mock collaborators and presenter component.
                | test_satisfies_protocol - Verifies component satisfies ICanvasSettingsPresenter.
                | test_update_settings - Verifies updating settings and triggering redraw.
    '''

    def setUp(self) -> None:
        '''
            Sets up mock collaborators and presenter component.

            :exceptions: None.
        '''
        self.initial_settings = CanvasSettings(
            default_z=10.0,
            default_speed=50.0,
            enforce_deadzone=True,
        )
        self.mock_redraw_delegate = MagicMock()

        self.presenter = CanvasSettingsPresenter(
            initial_settings=self.initial_settings,
            redraw_delegate=self.mock_redraw_delegate,
        )

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies CanvasSettingsPresenter satisfies ICanvasSettingsPresenter.

            :exceptions: None.
        '''
        self.assertIsInstance(self.presenter, ICanvasSettingsPresenter)

    def test_update_settings(self) -> None:
        '''
            Verifies updating settings updates attribute and triggers redraw.

            :exceptions: None.
        '''
        self.assertEqual(self.presenter.settings, self.initial_settings)

        updated = CanvasSettings(
            default_z=25.0,
            default_speed=80.0,
            enforce_deadzone=False,
        )
        self.presenter.update_settings(updated)
        self.assertEqual(self.presenter.settings, updated)
        self.mock_redraw_delegate.redraw.assert_called_once()


if __name__ == '__main__':
    main()
