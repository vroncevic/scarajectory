# -*- coding: UTF-8 -*-

'''
Module
    adapter.py
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
    Infrastructure adapter delegating trajectory kinematic and boundary validation to scaralang.
'''

from __future__ import annotations

from math import atan2, degrees, sqrt
from typing import Final

from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.trajectory.validation.result import ValidationResult
from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope
from scaralang.core.service.trajectory.validation.plan.ivalidator import ITrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.waypoint.ivalidator import IWaypointValidator

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.infrastructure.scaralang.validation.dependencies import TrajectoryValidationDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryValidationAdapter:
    '''
        Adapter delegating trajectory validation concerns to fine-grained scaralang validators.

        It defines:

            :attributes:
                | _envelope - Injected workspace envelope provider.
                | _waypoint - Injected waypoint reachability validator.
                | _plan - Injected trajectory plan sequence validator.
            :methods:
                | __init__ - Initializes adapter with validation dependencies.
                | r_min - Returns inner workspace reach radius in mm.
                | r_max - Returns outer workspace reach radius in mm.
                | bounds - Returns underlying manipulator kinematic bounds model.
                | validate_point - Validates waypoint coordinates against workspace envelope.
                | validate_plan - Validates complete trajectory plan sequence.
    '''

    _envelope: IWorkspaceEnvelope
    _waypoint: IWaypointValidator
    _plan: ITrajectoryPlanValidator

    def __init__(self, dependencies: TrajectoryValidationDependencies) -> None:
        '''
            Initializes TrajectoryValidationAdapter with required collaborator ports.

            :param dependencies: TrajectoryValidationDependencies collaborator bundle.
            :exceptions: None.
        '''
        self._envelope: Final[IWorkspaceEnvelope] = (
            dependencies.workspace_envelope
        )
        self._waypoint: Final[IWaypointValidator] = (
            dependencies.waypoint_validator
        )
        self._plan: Final[ITrajectoryPlanValidator] = (
            dependencies.plan_validator
        )

    @property
    def r_min(self) -> float:
        '''
            Returns inner workspace reach radius in mm.

            :return: Minimum reach radius float value.
            :exceptions: None.
        '''
        return self._envelope.r_min

    @property
    def r_max(self) -> float:
        '''
            Returns outer workspace reach radius in mm.

            :return: Maximum reach radius float value.
            :exceptions: None.
        '''
        return self._envelope.r_max

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns underlying manipulator kinematic bounds model.

            :return: ScaraBounds domain model.
            :exceptions: None.
        '''
        return self._envelope.bounds

    def validate_point(
        self,
        point: TrajectoryWaypoint,
        elbow_config: ElbowConfig = ElbowConfig.RIGHT,
    ) -> ValidationResult:
        '''
            Validates whether a waypoint is within reachable workspace.

            :param point: TrajectoryWaypoint containing 3D coordinates.
            :param elbow_config: Target kinematic elbow configuration.
            :return: ValidationResult object with pass/fail status and description.
            :exceptions: None.
        '''
        res: ValidationResult = self._waypoint.validate_point(
            point, elbow_config
        )
        if res.is_valid:
            return res

        alt_config: ElbowConfig = (
            ElbowConfig.LEFT
            if elbow_config == ElbowConfig.RIGHT
            else ElbowConfig.RIGHT
        )
        alt_res: ValidationResult = self._waypoint.validate_point(
            point, alt_config
        )
        if alt_res.is_valid:
            return alt_res

        return res

    def validate_plan(
        self,
        plan: IWaypointQuery,
        elbow_config: ElbowConfig = ElbowConfig.RIGHT,
    ) -> tuple[bool, list[str]]:
        '''
            Validates entire trajectory plan against kinematic and feedrate bounds.

            :param plan: IWaypointQuery instance to validate.
            :param elbow_config: Target kinematic elbow configuration.
            :return: Tuple of (is_valid, messages_list).
            :exceptions: None.
        '''
        waypoints = plan.waypoints
        if not waypoints:
            return False, ['Trajectory plan is empty; at least one waypoint required.']

        messages: list[str] = []
        is_plan_valid: bool = True
        bounds = self._envelope.bounds

        for idx, pt in enumerate(waypoints, start=1):
            res_pt: ValidationResult = self._waypoint.validate_point(pt, elbow_config)
            if not res_pt.is_valid:
                cos_q2 = (
                    pt.x * pt.x + pt.y * pt.y
                    - bounds.links.l1 * bounds.links.l1
                    - bounds.links.l2 * bounds.links.l2
                ) / (2.0 * bounds.links.l1 * bounds.links.l2)
                if -1.0 <= cos_q2 <= 1.0:
                    sin_q2 = sqrt(max(0.0, 1.0 - cos_q2 * cos_q2))
                    theta1 = atan2(pt.y, pt.x) - atan2(
                        bounds.links.l2 * sin_q2,
                        bounds.links.l1 + bounds.links.l2 * cos_q2,
                    )
                    theta1_l = atan2(pt.y, pt.x) - atan2(
                        -bounds.links.l2 * sin_q2,
                        bounds.links.l1 + bounds.links.l2 * cos_q2,
                    )
                    if bounds.joints.j1_min_rad <= theta1_l <= bounds.joints.j1_max_rad:
                        messages.append(
                            f'Point P{idx} ({pt.x:.1f}, {pt.y:.1f}) exceeds Righty J1 limit '
                            f'({degrees(theta1):.1f}°); requires Lefty elbow configuration.'
                        )
                    else:
                        is_plan_valid = False
                        messages.append(
                            f'Point P{idx} ({pt.x:.1f}, {pt.y:.1f}) violates J1 limits in both configurations.'
                        )
                else:
                    is_plan_valid = False
                    messages.append(
                        f'Point P{idx} ({pt.x:.1f}, {pt.y:.1f}, {pt.z:.1f}): {res_pt.message}'
                    )

        if is_plan_valid:
            messages.append(
                f'Validation PASSED: All {len(waypoints)} waypoints are within reachable workspace.'
            )

        return is_plan_valid, messages
