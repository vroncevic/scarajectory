# -*- coding: UTF-8 -*-

'''
Module
    controls_panel_factory_test.py
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
    Unit tests for ControlsPanelFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.model.preferences.connection_preference import ConnectionPreference
from scarajectory.core.service.preferences.iconnection_repository import IConnectionRepository
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.plan.mutation.iplan_mutation_service import IPlanMutationService
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.controls_panel import ControlsPanel
from scarajectory.infrastructure.gui.controls.controls_panel_factory import ControlsPanelFactory
from scarajectory.infrastructure.streaming.bundle import StreamingBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsPanelFactoryTestCase(TestCase):
    '''
        Test cases verifying ControlsPanelFactory creation behavior.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def setUp(self) -> None:
        self.mock_store = MagicMock(spec=IWaypointStore)
        self.mock_store.count = 0
        self.mock_mutation = MagicMock(spec=IPlanMutationService)
        self.mock_validator = MagicMock(spec=ITrajectoryValidator)
        self.mock_streaming = StreamingBundle(
            connection=MagicMock(),
            raw_channel=MagicMock(),
            playback_controller=MagicMock(),
            dispatcher=MagicMock(),
            binary_streamer=MagicMock(),
        )
        self.mock_storage = MagicMock(spec=IPlanStorageService)
        self.mock_dsl_service = MagicMock(spec=IScaraDslService)
        self.mock_connection_repo = MagicMock(spec=IConnectionRepository)
        self.mock_connection_repo.load_preference.return_value = (
            ConnectionPreference(port='', baud=115200)
        )

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(ControlsPanelFactory.get_version(), '1.0.4')

    def test_create_controls_panel(self) -> None:
        '''
            Tests instantiation and assembly of ControlsPanel via factory.
        '''
        bundle: ControlsBundle = ControlsBundle(
            store=self.mock_store,
            mutation=self.mock_mutation,
            validator=self.mock_validator,
            streaming=self.mock_streaming,
            storage=self.mock_storage,
            dsl_service=self.mock_dsl_service,
            connection_repository=self.mock_connection_repo,
        )
        panel: ControlsPanel = ControlsPanelFactory.create(
            self.root,
            bundle=bundle,
        )
        self.assertIsInstance(panel, ControlsPanel)
        panel.destroy()


if __name__ == '__main__':
    main()
