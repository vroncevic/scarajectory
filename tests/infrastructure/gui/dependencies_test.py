# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for GUIDependencies data container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.storage_dependencies import StorageDependencies
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter
from scarajectory.infrastructure.scaralang.provides import ScaralangProvides
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager
from scarajectory.infrastructure.streaming.provides import StreamingProvides
from scarajectory.setup.assembly.dsl.bundle import DslPipelineBundle
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIDependenciesTestCase(TestCase):
    '''
        Tests GUIDependencies construction and immutability.

        It defines:

            :methods:
                | test_init_bundle_creation_and_properties - Verifies all attributes and properties.
                | test_init_bundle_immutability - Verifies frozen dataclass behavior.
    '''

    def test_init_bundle_creation_and_properties(self) -> None:
        '''
            Verifies all attributes and streamer property delegation.

            :exceptions: None.
        '''
        mock_plan = MagicMock(spec=PlanPipelineBundle)
        mock_validator = MagicMock(spec=ITrajectoryValidator)
        mock_streaming = MagicMock(spec=StreamingProvides)
        mock_streaming.playback_controller = MagicMock(spec=IPlaybackController)
        mock_loader = MagicMock(spec=IPlanLoader)
        mock_storer = MagicMock(spec=IPlanStorer)
        mock_workspace = MagicMock(spec=IWorkspaceManager)
        mock_dsl = MagicMock(spec=DslPipelineBundle)
        mock_repo = MagicMock(spec=ISerialPreferenceRepository)
        mock_avoidance = MagicMock(spec=IDeadZoneAvoidanceAdapter)
        mock_planner = MagicMock(spec=IShapePlannerAdapter)
        mock_boundary = MagicMock(spec=IWorkspaceBoundaryAdapter)

        mock_storage = StorageDependencies(
            loader=mock_loader,
            storer=mock_storer,
            workspace=mock_workspace,
        )
        mock_scaralang = ScaralangProvides(
            dead_zone_avoidance=mock_avoidance,
            shape_planner=mock_planner,
            boundary=mock_boundary,
        )

        bundle = GUIDependencies(
            plan=mock_plan,
            validator=mock_validator,
            streaming=mock_streaming,
            dsl=mock_dsl,
            connection_repository=mock_repo,
            storage=mock_storage,
            scaralang=mock_scaralang,
        )

        self.assertIs(bundle.plan, mock_plan)
        self.assertIs(bundle.validator, mock_validator)
        self.assertIs(bundle.streaming, mock_streaming)
        self.assertIs(bundle.dsl, mock_dsl)
        self.assertIs(bundle.connection_repository, mock_repo)
        self.assertIs(bundle.storage, mock_storage)
        self.assertIs(bundle.scaralang, mock_scaralang)
        self.assertIs(bundle.loader, mock_loader)
        self.assertIs(bundle.storer, mock_storer)
        self.assertIs(bundle.workspace, mock_workspace)
        self.assertIs(bundle.avoidance_adapter, mock_avoidance)
        self.assertIs(bundle.planner_adapter, mock_planner)
        self.assertIs(bundle.streamer, mock_streaming.playback_controller)

    def test_init_bundle_immutability(self) -> None:
        '''
            Verifies modifying attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        mock_storage = StorageDependencies(
            loader=MagicMock(spec=IPlanLoader),
            storer=MagicMock(spec=IPlanStorer),
            workspace=MagicMock(spec=IWorkspaceManager),
        )
        mock_scaralang = ScaralangProvides(
            dead_zone_avoidance=MagicMock(spec=IDeadZoneAvoidanceAdapter),
            shape_planner=MagicMock(spec=IShapePlannerAdapter),
            boundary=MagicMock(spec=IWorkspaceBoundaryAdapter),
        )
        bundle = GUIDependencies(
            plan=MagicMock(spec=PlanPipelineBundle),
            validator=MagicMock(spec=ITrajectoryValidator),
            streaming=MagicMock(spec=StreamingProvides),
            dsl=MagicMock(spec=DslPipelineBundle),
            connection_repository=MagicMock(spec=ISerialPreferenceRepository),
            storage=mock_storage,
            scaralang=mock_scaralang,
        )

        with self.assertRaises(FrozenInstanceError):
            bundle.plan = MagicMock(spec=PlanPipelineBundle)  # type: ignore[misc]


if __name__ == '__main__':
    main()
