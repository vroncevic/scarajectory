# -*- coding: UTF-8 -*-

'''
Module
    streamer_tab_factory_test.py
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

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.model.preferences.connection_preference import ConnectionPreference
from scarajectory.infrastructure.connection.istream_connection import IStreamConnection
from scarajectory.core.service.manipulator.ijog_controller import IJogController
from scarajectory.core.service.manipulator.imotion_controller import IMotionController
from scarajectory.core.service.preferences.iconnection_repository import IConnectionRepository
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.core.service.tool.itool_controller import IToolController
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.infrastructure.gui.streaming.bundle import StreamerBundle
from scarajectory.infrastructure.gui.streaming.streamer_controllers_bundle import StreamerControllersBundle
from scarajectory.infrastructure.gui.streaming.streamer_tab import StreamerTab
from scarajectory.infrastructure.gui.streaming.streamer_tab_factory import StreamerTabFactory

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
        mock_plan = MagicMock(spec=ITrajectoryReadOnly)
        mock_validator = MagicMock(spec=ITrajectoryValidator)
        mock_connection = MagicMock(spec=IStreamConnection)
        mock_playback = MagicMock(spec=IStreamPlaybackController)
        mock_connection_repo = MagicMock(spec=IConnectionRepository)
        mock_connection_repo.load_preference.return_value = (
            ConnectionPreference(port='', baud=115200)
        )
        ctrls: StreamerControllersBundle = StreamerControllersBundle(
            motion_controller=MagicMock(spec=IMotionController),
            jog_controller=MagicMock(spec=IJogController),
            tool_controller=MagicMock(spec=IToolController),
        )
        self.bundle: StreamerBundle = StreamerBundle(
            plan=mock_plan,
            validator=mock_validator,
            connection=mock_connection,
            playback_controller=mock_playback,
            connection_repository=mock_connection_repo,
            controllers=ctrls,
        )

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(StreamerTabFactory.get_version(), '1.0.3')

    def test_create_streamer_tab(self) -> None:
        '''
            Tests instantiation and assembly of StreamerTab via factory.
        '''
        tab: StreamerTab = StreamerTabFactory.create(
            self.root,
            bundle=self.bundle,
        )
        self.assertIsInstance(tab, StreamerTab)
        tab.destroy()


if __name__ == '__main__':
    main()
