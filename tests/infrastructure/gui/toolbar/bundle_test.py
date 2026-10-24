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
    Unit tests for ToolbarBundle parameter container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory
from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.canvas.navigation.inavigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.canvas.status.ipresenter import ICanvasStatusPresenter
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarBundleTestCase(TestCase):
    '''
        Test cases verifying ToolbarBundle creation and immutability.

        It defines:

            :methods:
                | test_bundle_creation - Tests creating bundle with attributes.
                | test_bundle_immutability - Verifies frozen immutability behavior.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Tests creating bundle with attributes.

            :exceptions: None.
        '''
        mock_canvas = MagicMock(spec=ICanvas)
        mock_navigator = MagicMock(spec=ICanvasViewNavigator)
        mock_status = MagicMock(spec=ICanvasStatusPresenter)
        mock_history = MagicMock(spec=ITrajectoryPlanHistory)
        settings = CanvasSettings(
            default_z=20.0, default_speed=50.0, enforce_deadzone=True
        )
        bundle = ToolbarBundle(
            canvas=mock_canvas,
            navigator=mock_navigator,
            status_presenter=mock_status,
            history=mock_history,
            r_min=60.0,
            r_max=220.0,
            settings=settings,
        )
        self.assertIs(bundle.canvas, mock_canvas)
        self.assertIs(bundle.navigator, mock_navigator)
        self.assertIs(bundle.status_presenter, mock_status)
        self.assertIs(bundle.history, mock_history)
        self.assertEqual(bundle.r_min, 60.0)
        self.assertEqual(bundle.r_max, 220.0)
        self.assertEqual(bundle.settings, settings)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies frozen immutability behavior.

            :exceptions: None.
        '''
        bundle = ToolbarBundle(
            canvas=MagicMock(spec=ICanvas),
            navigator=MagicMock(spec=ICanvasViewNavigator),
            status_presenter=MagicMock(spec=ICanvasStatusPresenter),
            history=MagicMock(spec=ITrajectoryPlanHistory),
            r_min=60.0,
            r_max=220.0,
            settings=CanvasSettings(
                default_z=20.0, default_speed=50.0, enforce_deadzone=True
            ),
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.r_min = 10.0  # type: ignore[misc]


if __name__ == '__main__':
    main()
