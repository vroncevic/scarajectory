# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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
from unittest.mock import MagicMock

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.model.telemetry.counts import ProgressCounts
from scarajectory.core.model.telemetry.progress import StreamProgress
from scarajectory.infrastructure.gui.controls.assembly.bundle import TabsBundle
from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.ipanel import IControlsPanel
from scarajectory.infrastructure.gui.controls.panel import ControlsPanel

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
        self.logged: tuple[str, bool] = ('', False)
        self.progress: StreamProgress | None = None

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Records append log call.

            :param text: Message string.
            :param is_outgoing: Outgoing transmission flag.
            :exceptions: None.
        '''
        self.logged = (text, is_outgoing)

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Records progress update.

            :param progress: Progress data.
            :exceptions: None.
        '''
        self.progress = progress


class StubTabsAssembler:
    '''Stub tabs assembler satisfying ITabsAssembler for controls panel testing.'''

    def __init__(self, tabs: TabsBundle) -> None:
        self.tabs = tabs
        self.last_notebook: Notebook | None = None
        self.last_bundle: ControlsBundle | None = None

    def assemble_tabs(
        self,
        notebook: Notebook,
        bundle: ControlsBundle,
    ) -> TabsBundle:
        '''
            Returns pre-configured tabs bundle.

            :param notebook: Notebook container widget.
            :param bundle: Controls bundle.
            :return: Pre-configured tabs bundle.
            :exceptions: None.
        '''
        self.last_notebook = notebook
        self.last_bundle = bundle
        return self.tabs

    def get_version(self) -> str:
        '''
            Returns component version.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.3'


class ControlsPanelTestCase(TestCase):
    '''
        Unit tests for ControlsPanel widget.

        It defines:

            :methods:
                | setUpClass - Initializes root Tk instance.
                | tearDownClass - Destroys root Tk instance.
                | test_initialization_and_protocol - Tests widget creation and protocol conformance.
                | test_event_delegation - Tests streamer log and progress event forwarding.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Initializes root Tk test fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Destroys root Tk test fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def test_initialization_and_protocol(self) -> None:
        '''
            Verifies ControlsPanel creation and IControlsPanel protocol satisfaction.

            :exceptions: None.
        '''
        mock_bundle = MagicMock(spec=ControlsBundle)
        stub_tabs = TabsBundle(
            dsl_editor_tab=Frame(self.root),  # type: ignore[arg-type]
            streamer_tab=StubStreamerTab(self.root),  # type: ignore[arg-type]
            validation_tab=Frame(self.root),  # type: ignore[arg-type]
            jog_tab=Frame(self.root),  # type: ignore[arg-type]
            preview_tab=Frame(self.root),  # type: ignore[arg-type]
        )
        assembler = StubTabsAssembler(stub_tabs)
        panel = ControlsPanel(self.root, assembler, mock_bundle)

        self.assertIsInstance(panel, IControlsPanel)
        self.assertIsInstance(panel.notebook, Notebook)
        panel.destroy()

    def test_event_delegation(self) -> None:
        '''
            Verifies tab mounting and delegating calls to streamer tab.

            :exceptions: None.
        '''
        mock_bundle = MagicMock(spec=ControlsBundle)
        stub_streamer = StubStreamerTab(self.root)
        stub_tabs = TabsBundle(
            dsl_editor_tab=Frame(self.root),  # type: ignore[arg-type]
            streamer_tab=stub_streamer,  # type: ignore[arg-type]
            validation_tab=Frame(self.root),  # type: ignore[arg-type]
            jog_tab=Frame(self.root),  # type: ignore[arg-type]
            preview_tab=Frame(self.root),  # type: ignore[arg-type]
        )
        assembler = StubTabsAssembler(stub_tabs)
        panel = ControlsPanel(self.root, assembler, mock_bundle)

        panel.append_log('Transmit G1', is_outgoing=True)
        self.assertEqual(stub_streamer.logged, ('Transmit G1', True))

        progress = StreamProgress(
            state=StreamState.STREAMING,
            counts=ProgressCounts(
                total=10,
                sent=3,
                completed=2,
                failed=0,
            ),
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
