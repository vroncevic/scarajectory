# -*- coding: UTF-8 -*-

'''
Module
    gui_stream_observer_bridge_test.py
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
    Unit tests for GuiStreamObserverBridge and GuiStreamObserverBridgeFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.observer.iobserver import IObserver
from scarajectory.infrastructure.gui.streaming.observer.gui_stream_observer_bridge import GuiStreamObserverBridge
from scarajectory.infrastructure.gui.streaming.observer.gui_stream_observer_bridge_factory import GuiStreamObserverBridgeFactory
from scarajectory.infrastructure.gui.streaming.observer.igui_stream_observer_bridge import IGuiStreamObserverBridge

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGuiStreamObserverBridge(TestCase):
    '''
        Test cases verifying GuiStreamObserverBridge event marshaling.
    '''

    def setUp(self) -> None:
        self.mock_root = MagicMock()
        self.mock_controls = MagicMock()
        self.bridge: GuiStreamObserverBridge = (
            GuiStreamObserverBridgeFactory.create(
                root=self.mock_root,
                controls=self.mock_controls,
            )
        )

    def test_protocol_conformance(self) -> None:
        '''
            Tests structural protocol conformance against IObserver and IGuiStreamObserverBridge.
        '''
        self.assertIsInstance(self.bridge, IGuiStreamObserverBridge)
        self.assertIsInstance(self.bridge, IObserver)
        self.assertEqual(GuiStreamObserverBridgeFactory.get_version(), '1.0.4')

    def test_on_stream_progress(self) -> None:
        '''
            Tests that on_stream_progress dispatches to root.after with update_progress.
        '''
        mock_progress = MagicMock()
        self.bridge.on_stream_progress(mock_progress)
        self.mock_root.after.assert_called_once_with(
            0,
            self.mock_controls.update_progress,
            mock_progress,
        )

    def test_on_serial_log(self) -> None:
        '''
            Tests that on_serial_log dispatches to root.after with append_log.
        '''
        self.bridge.on_serial_log('test message', True)
        self.mock_root.after.assert_called_once_with(
            0,
            self.mock_controls.append_log,
            'test message',
            True,
        )


if __name__ == '__main__':
    main()
