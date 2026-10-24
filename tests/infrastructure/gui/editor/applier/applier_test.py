# -*- coding: UTF-8 -*-

'''
Module
    applier_test.py
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

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.editor.applier.applier import WaypointEditApplier
from scarajectory.infrastructure.gui.editor.applier.iapplier import IWaypointEditApplier
from scarajectory.infrastructure.gui.editor.applier.inputs import WaypointCoordinateInputs
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditApplierTestCase(TestCase):
    '''
        Test cases for WaypointEditApplier.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies conformance to IWaypointEditApplier.
                | test_version_and_constants - Verifies applier version string and ClassVar constants.
                | test_apply_edit_success - Verifies successful waypoint edit.
                | test_apply_edit_invalid_values - Verifies error on invalid input.
                | test_apply_edit_no_selection_returns_false - Verifies no selection handling.
                | test_apply_edit_out_of_reach_rejected - Verifies rejection of out-of-reach point.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies WaypointEditApplier conforms structurally to IWaypointEditApplier.

            :exceptions: None.
        '''
        applier = WaypointEditApplier()
        self.assertIsInstance(applier, IWaypointEditApplier)

    def test_version_and_constants(self) -> None:
        '''
            Verifies applier version string and ClassVar constants.

            :exceptions: None.
        '''
        applier = WaypointEditApplier()
        self.assertEqual(applier.get_version(), '1.0.3')
        self.assertEqual(WaypointEditApplier.TITLE_ERROR, 'Input Error')
        self.assertEqual(WaypointEditApplier.MSG_ERROR, 'Invalid numeric values.')

    def test_apply_edit_success(self) -> None:
        '''
            Verifies apply_edit updates waypoint with parsed floats.

            :exceptions: None.
        '''
        mock_store = MagicMock()
        mock_store.count = 2
        mock_store.waypoints = [
            TrajectoryWaypoint(
                x=10.0, y=20.0, z=5.0, phi=0.0, speed=50.0,
                name='P1', command='MOVE'
            ),
            TrajectoryWaypoint(
                x=30.0, y=40.0, z=5.0, phi=0.0, speed=50.0,
                name='P2', command='MOVE'
            ),
        ]
        mock_selection = MagicMock()
        mock_selection.selected_index = 0
        mock_mutation = MagicMock()
        mock_dispatcher = MagicMock()
        mock_validator = MagicMock()
        mock_validator.validate_point.return_value.is_valid = True

        bundle = TableBundle(
            store=mock_store,
            selection=mock_selection,
            mutation=mock_mutation,
            dispatcher=mock_dispatcher,
            validator=mock_validator,
        )
        inputs = WaypointCoordinateInputs(
            x='12.5', y='25.0', z='10.0', phi='45.0', speed='80.0'
        )

        applier = WaypointEditApplier()
        result = applier.apply_edit(inputs=inputs, bundle=bundle)

        self.assertTrue(result)
        self.assertTrue(mock_mutation.update_point.called)

    @patch('scarajectory.infrastructure.gui.editor.applier.applier.showerror')
    def test_apply_edit_invalid_values(
        self, mock_showerror: MagicMock
    ) -> None:
        '''
            Verifies apply_edit handles invalid float and shows error.

            :param mock_showerror: Mocked showerror function.
            :exceptions: None.
        '''
        mock_store = MagicMock()
        mock_store.count = 1
        mock_store.waypoints = [
            TrajectoryWaypoint(
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
            validator=MagicMock(),
        )
        inputs = WaypointCoordinateInputs(
            x='not_a_num', y='25.0', z='10.0', phi='45.0', speed='80.0'
        )

        applier = WaypointEditApplier()
        result = applier.apply_edit(inputs=inputs, bundle=bundle)

        self.assertFalse(result)
        self.assertTrue(mock_showerror.called)

    def test_apply_edit_no_selection_returns_false(self) -> None:
        '''
            Verifies apply_edit returns False when no waypoint is selected.

            :exceptions: None.
        '''
        mock_store = MagicMock()
        mock_store.count = 1
        mock_selection = MagicMock()
        mock_selection.selected_index = -1
        mock_mutation = MagicMock()
        mock_dispatcher = MagicMock()

        bundle = TableBundle(
            store=mock_store,
            selection=mock_selection,
            mutation=mock_mutation,
            dispatcher=mock_dispatcher,
            validator=MagicMock(),
        )
        inputs = WaypointCoordinateInputs(
            x='10.0', y='20.0', z='0.0', phi='0.0', speed='50.0'
        )
        applier = WaypointEditApplier()
        result = applier.apply_edit(inputs=inputs, bundle=bundle)
        self.assertFalse(result)

    @patch('scarajectory.infrastructure.gui.editor.applier.applier.showerror')
    def test_apply_edit_out_of_reach_rejected(
        self, mock_showerror: MagicMock
    ) -> None:
        '''
            Verifies apply_edit rejects out-of-reach point via validator.

            :param mock_showerror: Mocked showerror function.
            :exceptions: None.
        '''
        mock_store = MagicMock()
        mock_store.count = 1
        mock_store.waypoints = [
            TrajectoryWaypoint(
                x=10.0, y=20.0, z=5.0, phi=0.0, speed=50.0,
                name='P1', command='MOVE'
            ),
        ]
        mock_selection = MagicMock()
        mock_selection.selected_index = 0
        mock_mutation = MagicMock()
        mock_dispatcher = MagicMock()
        mock_validator = MagicMock()
        mock_validator.validate_point.return_value.is_valid = False

        bundle = TableBundle(
            store=mock_store,
            selection=mock_selection,
            mutation=mock_mutation,
            dispatcher=mock_dispatcher,
            validator=mock_validator,
        )
        inputs = WaypointCoordinateInputs(
            x='500.0', y='500.0', z='10.0', phi='45.0', speed='80.0'
        )

        applier = WaypointEditApplier()
        result = applier.apply_edit(inputs=inputs, bundle=bundle)

        self.assertFalse(result)
        self.assertTrue(mock_showerror.called)
        self.assertFalse(mock_mutation.update_point.called)


if __name__ == '__main__':
    main()
