# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
from types import SimpleNamespace
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.preference.preference import SerialPreference
from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.factory import ControlsPanelFactory
from scarajectory.infrastructure.gui.controls.panel import ControlsPanel
from scarajectory.infrastructure.gui.storage_dependencies import StorageDependencies
from scarajectory.infrastructure.scaralang.provides import ScaralangProvides
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


class ControlsPanelFactoryTestCase(TestCase):
    '''
        Test cases verifying ControlsPanelFactory creation behavior.

        It defines:

            :methods:
                | setUpClass - Sets up test class fixture.
                | tearDownClass - Tears down test class fixture.
                | setUp - Sets up test fixtures before each test method.
                | test_factory_version - Tests factory version string.
                | test_create_controls_panel - Tests instantiation of ControlsPanel via factory.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up test class fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down test class fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test method.

            :exceptions: None.
        '''
        mock_store = MagicMock(spec=IWaypointStore)
        mock_store.count = 0
        mock_connection_repo = MagicMock(spec=ISerialPreferenceRepository)
        mock_connection_repo.load_preference.return_value = (
            SerialPreference(port='', baud=115200)
        )
        self.mocks = SimpleNamespace(
            store=mock_store,
            mutation=MagicMock(spec=IPlanBulkMutator),
            validator=MagicMock(spec=ITrajectoryValidator),
            streaming=StreamingProvides(
                connection_manager=MagicMock(),
                raw_channel=MagicMock(),
                playback_controller=MagicMock(),
                registry=MagicMock(),
                dispatcher=MagicMock(),
                binary_streamer=MagicMock(),
            ),
            loader=MagicMock(spec=IPlanLoader),
            storer=MagicMock(spec=IPlanStorer),
            dsl=MagicMock(spec=DslPipelineBundle),
            connection_repo=mock_connection_repo,
        )

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.

            :exceptions: None.
        '''
        self.assertEqual(ControlsPanelFactory.get_version(), '1.0.3')

    def test_create_controls_panel(self) -> None:
        '''
            Tests instantiation and assembly of ControlsPanel via factory.

            :exceptions: None.
        '''
        bundle: ControlsBundle = ControlsBundle(
            plan=PlanPipelineBundle(
                store=self.mocks.store,
                selection=MagicMock(),
                point_mutator=MagicMock(),
                bulk_mutator=self.mocks.mutation,
                history=MagicMock(),
                dispatcher=MagicMock(),
            ),
            validator=self.mocks.validator,
            streaming=self.mocks.streaming,
            dsl=self.mocks.dsl,
            connection_repository=self.mocks.connection_repo,
            storage=StorageDependencies(
                loader=self.mocks.loader,
                storer=self.mocks.storer,
                workspace=MagicMock(),
            ),
            scaralang=ScaralangProvides(
                dead_zone_avoidance=MagicMock(),
                shape_planner=MagicMock(),
                boundary=MagicMock(),
            ),
        )
        panel: ControlsPanel = ControlsPanelFactory.create(
            self.root,
            bundle=bundle,
        )
        self.assertIsInstance(panel, ControlsPanel)
        panel.destroy()


if __name__ == '__main__':
    main()
