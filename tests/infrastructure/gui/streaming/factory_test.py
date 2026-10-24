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
    Unit tests for StreamerTabFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.preference.preference import SerialPreference
from scarajectory.core.service.manipulator.ijog import IJogController
from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.core.service.tool.icontroller import IToolController
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.gui.streaming.bundle import StreamerBundle
from scarajectory.infrastructure.gui.streaming.controllers_bundle import StreamerControllersBundle
from scarajectory.infrastructure.gui.streaming.factory import StreamerTabFactory
from scarajectory.infrastructure.gui.streaming.tab import StreamerTab
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerTabFactoryTestCase(TestCase):
    '''
        Test cases verifying StreamerTabFactory creation behavior.

        It defines:

            :methods:
                | setUpClass - Sets up test class fixture.
                | tearDownClass - Tears down test class fixture.
                | setUp - Sets up test fixtures before each test method.
                | test_factory_version - Tests factory version string.
                | test_create_streamer_tab - Tests instantiation and assembly of StreamerTab.
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
        mock_plan = MagicMock(spec=IWaypointQuery)
        mock_validator = MagicMock(spec=ITrajectoryValidator)
        mock_avoidance = MagicMock(spec=IDeadZoneAvoidanceAdapter)
        mock_connection_manager = MagicMock(spec=IConnectionManager)
        mock_playback = MagicMock(spec=IPlaybackController)
        mock_connection_repo = MagicMock(spec=ISerialPreferenceRepository)
        mock_connection_repo.load_preference.return_value = (
            SerialPreference(port='', baud=115200)
        )
        ctrls: StreamerControllersBundle = StreamerControllersBundle(
            motion_controller=MagicMock(spec=IMotionController),
            jog_controller=MagicMock(spec=IJogController),
            tool_controller=MagicMock(spec=IToolController),
        )
        self.bundle: StreamerBundle = StreamerBundle(
            plan=mock_plan,
            validator=mock_validator,
            avoidance_adapter=mock_avoidance,
            connection_manager=mock_connection_manager,
            playback_controller=mock_playback,
            connection_repository=mock_connection_repo,
            controllers=ctrls,
        )

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.

            :exceptions: None.
        '''
        self.assertEqual(StreamerTabFactory.get_version(), '1.0.3')

    def test_create_streamer_tab(self) -> None:
        '''
            Tests instantiation and assembly of StreamerTab via factory.

            :exceptions: None.
        '''
        tab: StreamerTab = StreamerTabFactory.create(
            self.root,
            bundle=self.bundle,
        )
        self.assertIsInstance(tab, StreamerTab)
        tab.destroy()


if __name__ == '__main__':
    main()
