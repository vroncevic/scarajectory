# -*- coding: UTF-8 -*-

'''
Module
    coordinator_test.py
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
    Unit tests for ShapePlanCoordinator component.
'''

from __future__ import annotations

from typing import ClassVar
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.handler.coordinator.bundle import ShapePlanCoordinatorBundle
from scarajectory.infrastructure.gui.canvas.handler.coordinator.coordinator import ShapePlanCoordinator
from scarajectory.infrastructure.gui.canvas.handler.coordinator.factory import ShapePlanCoordinatorFactory
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestShapePlanCoordinator(TestCase):
    '''
        Test cases verifying ShapePlanCoordinator functionality.

        It defines:

            :attributes:
                | SETTINGS - Active test canvas settings.
                | mock_store - Mock waypoint store.
                | mock_point - Mock point mutator.
                | mock_bulk - Mock bulk mutator.
                | mock_avoidance - Mock dead zone avoidance adapter.
                | mock_planner - Mock shape planner adapter.
                | mock_validator - Mock trajectory validator.
                | coordinator - Tested ShapePlanCoordinator instance.
            :methods:
                | setUp - Initializes mock dependencies and coordinator instance.
                | test_commit_point_in_dead_zone_rejected - Tests rejection in dead zone.
                | test_commit_point_empty_store - Tests direct point insertion.
                | test_commit_point_with_detour - Tests contour routing for detour.
                | test_commit_line_short_distance_ignored - Tests line drag threshold.
                | test_commit_line_endpoint_in_deadzone_aborted - Tests dead zone abort.
                | test_commit_line_success - Tests successful line commitment.
                | test_commit_rectangle_small_dimensions_ignored - Tests small rectangle ignore.
                | test_commit_rectangle_success - Tests successful rectangle commitment.
                | test_commit_circle_small_radius_ignored - Tests small circle radius ignore.
                | test_commit_circle_success - Tests successful circle commitment.
    '''

    SETTINGS: ClassVar[CanvasSettings] = CanvasSettings(
        default_z=15.0,
        default_speed=40.0,
    )

    mock_store: MagicMock
    mock_point: MagicMock
    mock_bulk: MagicMock
    mock_avoidance: MagicMock
    mock_planner: MagicMock
    mock_validator: MagicMock
    coordinator: ShapePlanCoordinator

    def setUp(self) -> None:
        '''
            Initializes mock dependencies and coordinator instance.

            :exceptions: None.
        '''
        self.mock_store = MagicMock(spec=IWaypointStore)
        self.mock_point = MagicMock(spec=IPlanPointMutator)
        self.mock_bulk = MagicMock(spec=IPlanBulkMutator)
        self.mock_avoidance = MagicMock(spec=IDeadZoneAvoidanceAdapter)
        self.mock_planner = MagicMock(spec=IShapePlannerAdapter)
        self.mock_validator = MagicMock(spec=ITrajectoryValidator)
        self.mock_validator.validate_point.return_value.is_valid = True
        bundle = ShapePlanCoordinatorBundle(
            store=self.mock_store,
            point_mutator=self.mock_point,
            bulk_mutator=self.mock_bulk,
            avoidance_adapter=self.mock_avoidance,
            planner_adapter=self.mock_planner,
            validator=self.mock_validator,
        )
        self.coordinator = ShapePlanCoordinatorFactory.create(bundle)

    def test_commit_point_in_dead_zone_rejected(self) -> None:
        '''
            Verifies commit_point aborts if point resides in dead zone.

            :exceptions: None.
        '''
        self.mock_avoidance.is_point_in_dead_zone.return_value = True
        self.coordinator.commit_point(10.0, 10.0, self.SETTINGS)
        self.mock_point.add_point.assert_not_called()

        self.mock_avoidance.is_point_in_dead_zone.return_value = False
        self.mock_validator.validate_point.return_value.is_valid = False
        self.coordinator.commit_point(20.0, 20.0, self.SETTINGS)
        self.mock_point.add_point.assert_not_called()
        self.mock_validator.validate_point.return_value.is_valid = True

    def test_commit_point_empty_store(self) -> None:
        '''
            Verifies commit_point appends directly when store has zero waypoints.

            :exceptions: None.
        '''
        self.mock_avoidance.is_point_in_dead_zone.return_value = False
        self.mock_store.count = 0
        self.coordinator.commit_point(150.0, 100.0, self.SETTINGS)
        expected: TrajectoryWaypoint = TrajectoryWaypoint(
            x=150.0,
            y=100.0,
            z=15.0,
            phi=0.0,
            speed=40.0,
            name='',
            command='',
        )
        self.mock_point.add_point.assert_called_once_with(expected)

    def test_commit_point_with_detour(self) -> None:
        '''
            Verifies commit_point routes contour when crossing dead zone.

            :exceptions: None.
        '''
        self.mock_avoidance.is_point_in_dead_zone.return_value = False
        self.mock_avoidance.crosses_dead_zone.return_value = True
        self.mock_store.count = 1
        last_pt: TrajectoryWaypoint = TrajectoryWaypoint(
            x=120.0, y=-50.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
        )
        self.mock_store.waypoints = [last_pt]
        detour_pt: TrajectoryWaypoint = TrajectoryWaypoint(
            x=90.0, y=0.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
        )
        target_pt: TrajectoryWaypoint = TrajectoryWaypoint(
            x=120.0, y=50.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
        )
        self.mock_avoidance.plan_detour.return_value = [
            last_pt,
            detour_pt,
            target_pt,
        ]

        self.coordinator.commit_point(120.0, 50.0, self.SETTINGS)
        self.assertEqual(self.mock_point.add_point.call_count, 2)

        self.mock_avoidance.crosses_dead_zone.return_value = False
        self.coordinator.commit_point(130.0, 60.0, self.SETTINGS)
        self.assertEqual(self.mock_point.add_point.call_count, 3)

        self.mock_avoidance.crosses_dead_zone.return_value = True

        def validate_detour(pt: TrajectoryWaypoint) -> MagicMock:
            res: MagicMock = MagicMock()
            res.is_valid = pt.x == 140.0
            return res

        self.mock_validator.validate_point.side_effect = validate_detour
        self.coordinator.commit_point(140.0, 70.0, self.SETTINGS)
        self.assertEqual(self.mock_point.add_point.call_count, 3)
        self.mock_validator.validate_point.side_effect = None
        self.mock_validator.validate_point.return_value.is_valid = True


    def test_commit_line_short_distance_ignored(self) -> None:
        '''
            Verifies commit_line ignores sub-millimeter drag events.

            :exceptions: None.
        '''
        self.coordinator.commit_line(
            (100.0, 100.0), (100.5, 100.5), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_not_called()

    def test_commit_line_endpoint_in_deadzone_aborted(self) -> None:
        '''
            Verifies commit_line aborts if destination endpoint is in dead zone.

            :exceptions: None.
        '''
        self.mock_avoidance.is_point_in_dead_zone.return_value = True
        self.coordinator.commit_line(
            (150.0, 150.0), (10.0, 10.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_not_called()

        self.mock_avoidance.is_point_in_dead_zone.return_value = False
        self.mock_validator.validate_point.return_value.is_valid = False
        self.coordinator.commit_line(
            (150.0, 150.0), (200.0, 200.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_not_called()

        def validate_mock(pt: TrajectoryWaypoint) -> MagicMock:
            res: MagicMock = MagicMock()
            res.is_valid = pt.x != 200.0
            return res

        self.mock_validator.validate_point.side_effect = validate_mock
        line_wps: list[TrajectoryWaypoint] = [
            TrajectoryWaypoint(
                x=100.0, y=100.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
            TrajectoryWaypoint(
                x=200.0, y=200.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
        ]
        self.mock_planner.plan_contour.return_value = line_wps
        self.coordinator.commit_line(
            (100.0, 100.0), (199.0, 199.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_not_called()
        self.mock_validator.validate_point.side_effect = None
        self.mock_validator.validate_point.return_value.is_valid = True

    def test_commit_line_success(self) -> None:
        '''
            Verifies commit_line plans contour and commits waypoints.

            :exceptions: None.
        '''
        self.mock_avoidance.is_point_in_dead_zone.return_value = False
        self.mock_store.waypoints = ()
        line_wps: list[TrajectoryWaypoint] = [
            TrajectoryWaypoint(
                x=100.0, y=100.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
            TrajectoryWaypoint(
                x=200.0, y=200.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
        ]
        self.mock_planner.plan_contour.return_value = line_wps

        self.coordinator.commit_line(
            (100.0, 100.0), (200.0, 200.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_called_once_with(line_wps)

    def test_commit_rectangle_small_dimensions_ignored(self) -> None:
        '''
            Verifies commit_rectangle ignores tiny rectangle sizes.

            :exceptions: None.
        '''
        self.coordinator.commit_rectangle(
            (100.0, 100.0), (101.0, 101.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_not_called()

        self.mock_validator.validate_point.return_value.is_valid = False
        rect_wps: list[TrajectoryWaypoint] = [
            TrajectoryWaypoint(
                x=100.0, y=100.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
        ]
        self.mock_planner.plan_contour.return_value = rect_wps
        self.coordinator.commit_rectangle(
            (100.0, 100.0), (200.0, 200.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_not_called()
        self.mock_validator.validate_point.return_value.is_valid = True

    def test_commit_rectangle_success(self) -> None:
        '''
            Verifies commit_rectangle plans closed contour and commits waypoints.

            :exceptions: None.
        '''
        self.mock_store.waypoints = ()
        rect_wps: list[TrajectoryWaypoint] = [
            TrajectoryWaypoint(
                x=100.0, y=100.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
            TrajectoryWaypoint(
                x=200.0, y=100.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
        ]
        self.mock_planner.plan_contour.return_value = rect_wps

        self.coordinator.commit_rectangle(
            (100.0, 100.0), (200.0, 200.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_called_once_with(rect_wps)

    def test_commit_circle_small_radius_ignored(self) -> None:
        '''
            Verifies commit_circle ignores radius below minimum threshold.

            :exceptions: None.
        '''
        self.coordinator.commit_circle(
            (100.0, 100.0), (102.0, 100.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_not_called()

        self.mock_validator.validate_point.return_value.is_valid = False
        circle_wps: list[TrajectoryWaypoint] = [
            TrajectoryWaypoint(
                x=150.0, y=100.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
        ]
        self.mock_planner.plan_circle.return_value = circle_wps
        self.coordinator.commit_circle(
            (100.0, 100.0), (150.0, 100.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_not_called()
        self.mock_validator.validate_point.return_value.is_valid = True

    def test_commit_circle_success(self) -> None:
        '''
            Verifies commit_circle plans circular waypoints and commits to plan.

            :exceptions: None.
        '''
        self.mock_store.waypoints = ()
        circle_wps: list[TrajectoryWaypoint] = [
            TrajectoryWaypoint(
                x=150.0, y=100.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
            TrajectoryWaypoint(
                x=100.0, y=150.0, z=15.0, speed=40.0, phi=0.0, name='', command=''
            ),
        ]
        self.mock_planner.plan_circle.return_value = circle_wps

        self.coordinator.commit_circle(
            (100.0, 100.0), (150.0, 100.0), self.SETTINGS
        )
        self.mock_bulk.set_waypoints.assert_called_once_with(circle_wps)



if __name__ == '__main__':
    main()
