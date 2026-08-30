# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Core service implementation orchestrating trajectory modeling, validation and streaming.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.model.trajectory_metrics import TrajectoryMetrics
from scarajectory.core.model.validation_result_dto import ValidationResultDTO
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.iserial_streamer import ISerialStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Service:
    '''
        Service orchestrating trajectory domain modeling, validation and execution.

        It defines:

            :attributes:
                | _plan - Trajectory plan domain entity.
                | _validator - Kinematic reachability validator.
                | _streamer - Hardware serial communication streamer.
            :methods:
                | __init__ - Initializes the service with components.
                | is_initialized - Checks if the service is properly initialized.
                | get_plan - Returns the active TrajectoryPlan.
                | get_validator - Returns the active ITrajectoryValidator.
                | get_streamer - Returns the active ISerialStreamer.
                | validate_plan - Validates the current trajectory plan.
                | save_plan - Saves current plan to file path.
                | load_plan - Loads plan from file path.
                | start_streaming - Initiates streaming of current plan.
                | stop_streaming - Aborts active streaming.
    '''

    _plan: Final[TrajectoryPlan]
    _validator: Final[ITrajectoryValidator]
    _streamer: Final[ISerialStreamer]

    def __init__(
        self,
        validator: ITrajectoryValidator,
        streamer: ISerialStreamer,
        plan: TrajectoryPlan | None = None
    ) -> None:
        '''
            Initializes the service with components.

            :param validator: ITrajectoryValidator instance.
            :param streamer: ISerialStreamer instance.
            :param plan: Optional TrajectoryPlan instance.
            :exceptions: None.
        '''
        self._validator = validator
        self._streamer = streamer
        self._plan = plan if plan is not None else TrajectoryPlan()

    def is_initialized(self) -> bool:
        '''
            Checks if the service is properly initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return self._plan is not None and self._validator is not None and self._streamer is not None

    def get_plan(self) -> TrajectoryPlan:
        '''
            Returns the active TrajectoryPlan.

            :return: TrajectoryPlan instance.
            :exceptions: None.
        '''
        return self._plan

    def get_validator(self) -> ITrajectoryValidator:
        '''
            Returns the active ITrajectoryValidator.

            :return: ITrajectoryValidator instance.
            :exceptions: None.
        '''
        return self._validator

    def get_streamer(self) -> ISerialStreamer:
        '''
            Returns the active ISerialStreamer.

            :return: ISerialStreamer instance.
            :exceptions: None.
        '''
        return self._streamer

    def validate_plan(self) -> tuple[bool, list[str]]:
        '''
            Validates the current trajectory plan against robot kinematic bounds.

            :return: Tuple of (is_valid, messages_list).
            :exceptions: None.
        '''
        waypoints = self._plan.waypoints
        if not waypoints:
            return False, ['Trajectory plan is empty. Please add waypoints.']

        messages: list[str] = []
        all_valid: bool = True

        for index, pt in enumerate(waypoints, start=1):
            pt_dto = pt.to_dto()
            res_pt: ValidationResultDTO = self._validator.validate_point_dto(pt_dto)
            if not res_pt.is_valid:
                all_valid = False
                messages.append(f'Point P{index} ({pt.x:.1f}, {pt.y:.1f}, {pt.z:.1f}): {res_pt.message}')

            res_spd: ValidationResultDTO = self._validator.validate_feedrate(pt.speed)
            if not res_spd.is_valid:
                all_valid = False
                messages.append(f'Point P{index} Speed ({pt.speed:.1f} mm/s): {res_spd.message}')

        if all_valid:
            total_dist: float = TrajectoryMetrics.calculate_distance(waypoints)
            est_time: float = TrajectoryMetrics.calculate_duration(waypoints)
            messages.append(
                f'Validation PASSED: All {len(waypoints)} waypoints are within reachable workspace.\n'
                f'Total Path Distance: {total_dist:.2f} mm | Estimated Time: {est_time:.2f} s'
            )

        return all_valid, messages

    def save_plan(self, filepath: str) -> None:
        '''
            Saves current plan to file path.

            :param filepath: Target file path.
            :exceptions: OSError.
        '''
        TrajectoryMetrics.save_json(self._plan.waypoints, filepath)

    def load_plan(self, filepath: str) -> None:
        '''
            Loads plan from file path.

            :param filepath: Source file path.
            :exceptions: OSError.
        '''
        loaded_pts: list[Waypoint] = TrajectoryMetrics.load_json(filepath)
        self._plan.set_waypoints(loaded_pts)

    def start_streaming(self) -> bool:
        '''
            Initiates streaming of current plan.

            :return: True if stream started, False otherwise.
            :exceptions: None.
        '''
        return self._streamer.start_streaming(self._plan.waypoints)

    def stop_streaming(self) -> None:
        '''
            Aborts active streaming.

            :exceptions: None.
        '''
        self._streamer.stop_streaming()
