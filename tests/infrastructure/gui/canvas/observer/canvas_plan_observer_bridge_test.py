# -*- coding: UTF-8 -*-

'''
Module
    canvas_plan_observer_bridge_test.py
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
    Unit tests for CanvasPlanObserverBridge component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.observer.itrajectory_observer import ITrajectoryObserver
from scarajectory.infrastructure.gui.canvas.observer.canvas_plan_observer_bridge import CanvasPlanObserverBridge
from scarajectory.infrastructure.gui.canvas.observer.canvas_plan_observer_bridge_factory import CanvasPlanObserverBridgeFactory
from scarajectory.infrastructure.gui.canvas.observer.icanvas_plan_observer_bridge import ICanvasPlanObserverBridge

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasPlanObserverBridge(TestCase):
    '''
        Test cases verifying CanvasPlanObserverBridge behavior.
    '''

    def setUp(self) -> None:
        self.mock_redraw = MagicMock()
        self.bridge: CanvasPlanObserverBridge = (
            CanvasPlanObserverBridgeFactory.create(self.mock_redraw)
        )

    def test_satisfies_protocols(self) -> None:
        '''
            Verifies structural protocol compliance.
        '''
        self.assertIsInstance(self.bridge, ICanvasPlanObserverBridge)
        self.assertIsInstance(self.bridge, ITrajectoryObserver)

    def test_on_trajectory_updated_triggers_redraw(self) -> None:
        '''
            Verifies on_trajectory_updated calls redraw action.
        '''
        self.bridge.on_trajectory_updated()
        self.mock_redraw.assert_called_once()

    def test_on_point_selected_triggers_redraw(self) -> None:
        '''
            Verifies on_point_selected calls redraw action.
        '''
        self.bridge.on_point_selected(3)
        self.mock_redraw.assert_called_once()

    def test_factory_version(self) -> None:
        '''
            Verifies factory version string.
        '''
        self.assertEqual(
            CanvasPlanObserverBridgeFactory.get_version(), '1.0.3'
        )


if __name__ == '__main__':
    main()
