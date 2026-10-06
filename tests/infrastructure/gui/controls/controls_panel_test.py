# -*- coding: UTF-8 -*-

'''
Module
    controls_panel_test.py
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
    Unit testing for ControlsPanel component.
'''

from __future__ import annotations

from tkinter import Tk, Widget
from tkinter.ttk import Frame, Notebook
from unittest import TestCase, main

from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.controls.controls_panel import ControlsPanel
from scarajectory.infrastructure.gui.controls.icontrols_panel import IControlsPanel
from scarajectory.infrastructure.gui.controls.tabs_bundle import ControlsTabsBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubStreamerTab(Frame):
    '''Stub streamer tab for controls panel testing.'''

    def __init__(self, parent: Widget) -> None:
        super().__init__(parent)
        self.refreshed: bool = False
        self.logged: tuple[str, bool] | None = None
        self.progress: StreamProgress | None = None

    def refresh_ports(self) -> None:
        '''Records refresh call.'''
        self.refreshed = True

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''Records append log call.'''
        self.logged = (text, is_outgoing)

    def update_progress(self, progress: StreamProgress) -> None:
        '''Records progress update.'''
        self.progress = progress


class ControlsPanelTestCase(TestCase):
    '''
        Unit tests for ControlsPanel widget.

        It defines:

            :methods:
                | setUpClass - Initializes root Tk instance.
                | tearDownClass - Destroys root Tk instance.
                | test_initialization_and_protocol - Tests widget creation and protocol conformance.
                | test_unmounted_delegation_safety - Tests no-op behavior prior to mount_tabs.
                | test_mount_tabs_and_delegation - Tests tab mounting and streamer event forwarding.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def test_initialization_and_protocol(self) -> None:
        '''Verifies ControlsPanel creation and IControlsPanel protocol satisfaction.'''
        panel = ControlsPanel(self.root)
        self.assertIsInstance(panel, IControlsPanel)
        self.assertIsInstance(panel.notebook, Notebook)
        panel.destroy()

    def test_unmounted_delegation_safety(self) -> None:
        '''Verifies methods execute safely without error before tabs are mounted.'''
        panel = ControlsPanel(self.root)
        panel.refresh_ports()
        panel.append_log('Log message', is_outgoing=False)

        progress = StreamProgress(
            state=StreamState.IDLE,
            total_waypoints=0,
            sent_waypoints=0,
            completed_waypoints=0,
            failed_waypoints=0,
            current_line='',
            error_message='',
            elapsed_seconds=0.0,
            percentage=0.0,
        )
        panel.update_progress(progress)
        panel.destroy()

    def test_mount_tabs_and_delegation(self) -> None:
        '''Verifies tab mounting and delegating calls to streamer tab.'''
        panel = ControlsPanel(self.root)

        mock_dsl = Frame(panel.notebook)
        stub_streamer = StubStreamerTab(panel.notebook)
        mock_val = Frame(panel.notebook)
        mock_jog = Frame(panel.notebook)
        mock_preview = Frame(panel.notebook)

        bundle = ControlsTabsBundle(
            dsl_editor_tab=mock_dsl,  # type: ignore[arg-type]
            streamer_tab=stub_streamer,  # type: ignore[arg-type]
            validation_tab=mock_val,  # type: ignore[arg-type]
            jog_tab=mock_jog,  # type: ignore[arg-type]
            preview_tab=mock_preview,  # type: ignore[arg-type]
        )
        panel.mount_tabs(bundle)

        panel.refresh_ports()
        self.assertTrue(stub_streamer.refreshed)

        panel.append_log('Transmit G1', is_outgoing=True)
        self.assertEqual(stub_streamer.logged, ('Transmit G1', True))

        progress = StreamProgress(
            state=StreamState.STREAMING,
            total_waypoints=10,
            sent_waypoints=3,
            completed_waypoints=2,
            failed_waypoints=0,
            current_line='G1 X10',
            error_message='',
            elapsed_seconds=1.0,
            percentage=30.0,
        )
        panel.update_progress(progress)
        self.assertEqual(stub_streamer.progress, progress)

        panel.destroy()


if __name__ == '__main__':
    main()
