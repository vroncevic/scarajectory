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
    Unit tests for ControlsBundle parameter container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.preferences.iconnection_repository import IConnectionRepository
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.plan.mutation.iplan_mutation_service import IPlanMutationService
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.streaming.bundle import StreamingBundle
from scarajectory.setup.pipeline.dsl_pipeline_bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsBundleTestCase(TestCase):
    '''
        Tests ControlsBundle creation and immutability.

        It defines:

            :methods:
                | test_bundle_creation_and_properties - Verifies attributes and streamer alias.
                | test_bundle_immutability - Verifies frozen dataclass behavior.
    '''

    def test_bundle_creation_and_properties(self) -> None:
        '''Verifies all attributes and streamer property delegation.'''
        mock_store = MagicMock(spec=IWaypointStore)
        mock_mutation = MagicMock(spec=IPlanMutationService)
        mock_validator = MagicMock(spec=ITrajectoryValidator)
        mock_streaming = MagicMock(spec=StreamingBundle)
        mock_storage = MagicMock(spec=IPlanStorageService)
        mock_dsl = MagicMock(spec=DslPipelineBundle)
        mock_repo = MagicMock(spec=IConnectionRepository)

        bundle = ControlsBundle(
            store=mock_store,
            mutation=mock_mutation,
            validator=mock_validator,
            streaming=mock_streaming,
            storage=mock_storage,
            dsl=mock_dsl,
            connection_repository=mock_repo,
        )

        self.assertIs(bundle.store, mock_store)
        self.assertIs(bundle.mutation, mock_mutation)
        self.assertIs(bundle.validator, mock_validator)
        self.assertIs(bundle.streaming, mock_streaming)
        self.assertIs(bundle.storage, mock_storage)
        self.assertIs(bundle.dsl, mock_dsl)
        self.assertIs(bundle.connection_repository, mock_repo)
        self.assertIs(bundle.streamer, mock_streaming)

    def test_bundle_immutability(self) -> None:
        '''Verifies modifying attributes raises FrozenInstanceError.'''
        bundle = ControlsBundle(
            store=MagicMock(spec=IWaypointStore),
            mutation=MagicMock(spec=IPlanMutationService),
            validator=MagicMock(spec=ITrajectoryValidator),
            streaming=MagicMock(spec=StreamingBundle),
            storage=MagicMock(spec=IPlanStorageService),
            dsl=MagicMock(spec=DslPipelineBundle),
            connection_repository=MagicMock(spec=IConnectionRepository),
        )

        with self.assertRaises(FrozenInstanceError):
            bundle.store = MagicMock(spec=IWaypointStore)  # type: ignore[misc]


if __name__ == '__main__':
    main()
