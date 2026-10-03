# -*- coding: UTF-8 -*-

'''
Module
    waypoint_edit_applier_test.py
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
    Unit tests for WaypointEditApplier component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.waypoint_coordinate_inputs import WaypointCoordinateInputs
from scarajectory.infrastructure.gui.editor.waypoint_edit_applier import WaypointEditApplier

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypointEditApplier(TestCase):
    '''
        Test cases for WaypointEditApplier.
    '''

    def test_version(self) -> None:
        '''
            Verifies applier version string.
        '''
        self.assertEqual(WaypointEditApplier.get_version(), '1.0.4')

    def test_apply_edit_success(self) -> None:
        '''
            Verifies apply_edit updates waypoint with parsed floats.
        '''
        mock_store = MagicMock()
        mock_store.count = 2
        mock_store.waypoints = [
            Waypoint(
                x=10.0, y=20.0, z=5.0, phi=0.0, speed=50.0,
                name='P1', command='MOVE'
            ),
            Waypoint(
                x=30.0, y=40.0, z=5.0, phi=0.0, speed=50.0,
                name='P2', command='MOVE'
            ),
        ]
        mock_selection = MagicMock()
        mock_selection.selected_index = 0
        mock_mutation = MagicMock()
        mock_dispatcher = MagicMock()

        bundle = TableBundle(
            store=mock_store,
            selection=mock_selection,
            mutation=mock_mutation,
            dispatcher=mock_dispatcher,
        )
        inputs = WaypointCoordinateInputs(
            x='12.5', y='25.0', z='10.0', phi='45.0', speed='80.0'
        )

        applier = WaypointEditApplier()
        result = applier.apply_edit(inputs, bundle)

        self.assertTrue(result)
        self.assertTrue(mock_mutation.update_point.called)

    @patch(
        'scarajectory.infrastructure.gui.editor.'
        'waypoint_edit_applier.showerror'
    )
    def test_apply_edit_invalid_values(
        self, mock_showerror: MagicMock
    ) -> None:
        '''
            Verifies apply_edit handles invalid float and shows error.
        '''
        mock_store = MagicMock()
        mock_store.count = 1
        mock_store.waypoints = [
            Waypoint(
                x=10.0, y=20.0, z=5.0, phi=0.0, speed=50.0,
                name='P1', command='MOVE'
            ),
        ]
        mock_selection = MagicMock()
        mock_selection.selected_index = 0
        mock_mutation = MagicMock()
        mock_dispatcher = MagicMock()

        bundle = TableBundle(
            store=mock_store,
            selection=mock_selection,
            mutation=mock_mutation,
            dispatcher=mock_dispatcher,
        )
        inputs = WaypointCoordinateInputs(
            x='not_a_num', y='25.0', z='10.0', phi='45.0', speed='80.0'
        )

        applier = WaypointEditApplier()
        result = applier.apply_edit(inputs, bundle)

        self.assertFalse(result)
        self.assertTrue(mock_showerror.called)


if __name__ == '__main__':
    main()
