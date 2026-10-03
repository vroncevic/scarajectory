# -*- coding: UTF-8 -*-

'''
Module
    scarajectory_gui_test.py
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
    Unit tests for ScarajectoryGUI presentation coordinator.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.core.service.storage.iplan_storage_service import (
    IPlanStorageService,
)
from scarajectory.core.service.streaming.istream_playback_controller import (
    IStreamPlaybackController,
)
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import (
    IPlanBulkMutator,
)
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import (
    ICanvasViewNavigator,
)
from scarajectory.infrastructure.gui.scarajectory_gui import ScarajectoryGUI
from scarajectory.infrastructure.gui.scarajectory_gui_bundle import (
    ScarajectoryGUIBundle,
)
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScarajectoryGUITestCase(TestCase):
    '''
        Tests ScarajectoryGUI presentation adapter operations.

        It defines:

            :methods:
                | test_initialization_and_start - Verifies status check, start and deadzone.
                | test_stop_normal_cleanup - Verifies normal teardown and destruction.
                | test_stop_with_playback_exception - Verifies teardown when controller raises.
                | test_load_file_operations - Verifies loading plan and error handling.
    '''

    def test_initialization_and_start(self) -> None:
        '''Verifies is_initialized, start mainloop, and deadzone delegation.'''
        mock_root = MagicMock(spec=Tk)
        mock_toolbar = MagicMock(spec=Toolbar)
        bundle = ScarajectoryGUIBundle(
            root=mock_root,
            playback_controller=MagicMock(spec=IStreamPlaybackController),
            storage=MagicMock(spec=IPlanStorageService),
            mutation=MagicMock(spec=IPlanBulkMutator),
            navigator=MagicMock(spec=ICanvasViewNavigator),
            toolbar=mock_toolbar,
        )
        gui = ScarajectoryGUI(bundle=bundle)

        self.assertTrue(gui.is_initialized())
        mock_root.protocol.assert_called_with('WM_DELETE_WINDOW', gui.stop)
        gui.start()
        mock_root.mainloop.assert_called_once()

        gui.set_deadzone(True)
        mock_toolbar.set_deadzone.assert_called_with(True)
        gui.set_deadzone(False)
        mock_toolbar.set_deadzone.assert_called_with(False)

    def test_stop_normal_cleanup(self) -> None:
        '''Verifies normal teardown sequence stops playback and destroys root.'''
        mock_root = MagicMock(spec=Tk)
        mock_playback = MagicMock(spec=IStreamPlaybackController)
        bundle = ScarajectoryGUIBundle(
            root=mock_root,
            playback_controller=mock_playback,
            storage=MagicMock(spec=IPlanStorageService),
            mutation=MagicMock(spec=IPlanBulkMutator),
            navigator=MagicMock(spec=ICanvasViewNavigator),
            toolbar=MagicMock(spec=Toolbar),
        )
        gui = ScarajectoryGUI(bundle=bundle)

        gui.stop()
        mock_root.withdraw.assert_called_once()
        mock_playback.stop_streaming.assert_called_once()
        mock_root.quit.assert_called_once()
        mock_root.destroy.assert_called_once()

    def test_stop_with_playback_exception(self) -> None:
        '''Verifies teardown completes even if playback controller raises error.'''
        mock_root = MagicMock(spec=Tk)
        mock_playback = MagicMock(spec=IStreamPlaybackController)
        mock_playback.stop_streaming.side_effect = RuntimeError('stream error')
        bundle = ScarajectoryGUIBundle(
            root=mock_root,
            playback_controller=mock_playback,
            storage=MagicMock(spec=IPlanStorageService),
            mutation=MagicMock(spec=IPlanBulkMutator),
            navigator=MagicMock(spec=ICanvasViewNavigator),
            toolbar=MagicMock(spec=Toolbar),
        )
        gui = ScarajectoryGUI(bundle=bundle)

        gui.stop()
        mock_root.withdraw.assert_called_once()
        mock_playback.stop_streaming.assert_called_once()
        mock_root.quit.assert_called_once()
        mock_root.destroy.assert_called_once()

    def test_stop_idempotent_multiple_calls(self) -> None:
        '''Verifies subsequent calls to stop() are no-ops.'''
        mock_root = MagicMock(spec=Tk)
        mock_playback = MagicMock(spec=IStreamPlaybackController)
        bundle = ScarajectoryGUIBundle(
            root=mock_root,
            playback_controller=mock_playback,
            storage=MagicMock(spec=IPlanStorageService),
            mutation=MagicMock(spec=IPlanBulkMutator),
            navigator=MagicMock(spec=ICanvasViewNavigator),
            toolbar=MagicMock(spec=Toolbar),
        )
        gui = ScarajectoryGUI(bundle=bundle)

        gui.stop()
        gui.stop()
        mock_root.withdraw.assert_called_once()
        mock_playback.stop_streaming.assert_called_once()
        mock_root.quit.assert_called_once()
        mock_root.destroy.assert_called_once()

    def test_stop_with_tcl_error(self) -> None:
        '''Verifies teardown catches TclError if root is already destroyed.'''
        mock_root = MagicMock(spec=Tk)
        mock_root.withdraw.side_effect = TclError('application has been destroyed')
        mock_playback = MagicMock(spec=IStreamPlaybackController)
        bundle = ScarajectoryGUIBundle(
            root=mock_root,
            playback_controller=mock_playback,
            storage=MagicMock(spec=IPlanStorageService),
            mutation=MagicMock(spec=IPlanBulkMutator),
            navigator=MagicMock(spec=ICanvasViewNavigator),
            toolbar=MagicMock(spec=Toolbar),
        )
        gui = ScarajectoryGUI(bundle=bundle)

        gui.stop()
        mock_playback.stop_streaming.assert_called_once()

    @patch('scarajectory.infrastructure.gui.scarajectory_gui.showerror')
    def test_load_file_operations(self, mock_showerror: MagicMock) -> None:
        '''Verifies plan file loading success and error dialogue on failure.'''
        mock_storage = MagicMock(spec=IPlanStorageService)
        mock_mutation = MagicMock(spec=IPlanBulkMutator)
        mock_navigator = MagicMock(spec=ICanvasViewNavigator)
        dummy_waypoints: list[dict[str, float]] = [{'x': 10.0, 'y': 20.0}]
        mock_storage.load_plan.return_value = dummy_waypoints

        bundle = ScarajectoryGUIBundle(
            root=MagicMock(spec=Tk),
            playback_controller=MagicMock(spec=IStreamPlaybackController),
            storage=mock_storage,
            mutation=mock_mutation,
            navigator=mock_navigator,
            toolbar=MagicMock(spec=Toolbar),
        )
        gui = ScarajectoryGUI(bundle=bundle)

        gui.load_file('/path/to/trajectory.json')
        mock_storage.load_plan.assert_called_with('/path/to/trajectory.json')
        mock_mutation.set_waypoints.assert_called_with(dummy_waypoints)
        mock_navigator.fit_reach_view.assert_called_once()

        mock_storage.load_plan.side_effect = OSError('Disk read fault')
        gui.load_file('/path/to/invalid.json')
        mock_showerror.assert_called_once_with(
            'Load Error', 'Failed to load plan: Disk read fault'
        )


if __name__ == '__main__':
    main()
