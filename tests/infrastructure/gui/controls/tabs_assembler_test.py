# -*- coding: UTF-8 -*-

'''
Module
    tabs_assembler_test.py
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
    Unit tests for ControlsTabsAssembler tab assembly service.
'''

from __future__ import annotations

from tkinter.ttk import Notebook
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.manipulator_controllers_bundle import (
    ManipulatorControllersBundle,
)
from scarajectory.infrastructure.gui.controls.tabs_assembler import (
    ControlsTabsAssembler,
)
from scarajectory.infrastructure.gui.controls.tabs_bundle import (
    ControlsTabsBundle,
)
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.manipulator.jog.jog_tab import JogTab
from scarajectory.infrastructure.gui.preview.preview_tab import PreviewTab
from scarajectory.infrastructure.gui.streaming.streamer_tab import StreamerTab
from scarajectory.infrastructure.gui.validation.validation_tab import (
    ValidationTab,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsTabsAssemblerTestCase(TestCase):
    '''
        Tests ControlsTabsAssembler tab construction operations.

        It defines:

            :methods:
                | test_assembler_version - Verifies version string getter.
                | test_assemble_tabs - Verifies instantiation of all child control tabs.
    '''

    def test_assembler_version(self) -> None:
        '''Verifies version string reported by assembler.'''
        assembler = ControlsTabsAssembler()
        self.assertEqual(assembler.get_version(), '1.0.4')

    def test_assemble_tabs(self) -> None:
        '''Verifies all tabs are assembled and bundled correctly.'''
        target_pkg = 'scarajectory.infrastructure.gui.controls.tabs_assembler.'
        with (
            patch(f'{target_pkg}ManipulatorControllersFactory.create') as mock_ctrls_fact,
            patch(f'{target_pkg}DslEditorTabFactory.create') as mock_dsl_fact,
            patch(f'{target_pkg}StreamerTabFactory.create') as mock_stream_fact,
            patch(f'{target_pkg}ValidationTabFactory.create') as mock_val_fact,
            patch(f'{target_pkg}JogTabFactory.create') as mock_jog_fact,
            patch(f'{target_pkg}PreviewTabFactory.create') as mock_prev_fact,
        ):
            mock_ctrls_fact.return_value = MagicMock(
                spec=ManipulatorControllersBundle
            )
            mock_dsl_fact.return_value = MagicMock(spec=DslEditorTab)
            mock_stream_fact.return_value = MagicMock(spec=StreamerTab)
            mock_val_fact.return_value = MagicMock(spec=ValidationTab)
            mock_jog_fact.return_value = MagicMock(spec=JogTab)
            mock_prev_fact.return_value = MagicMock(spec=PreviewTab)

            mock_notebook = MagicMock(spec=Notebook)
            mock_bundle = MagicMock(spec=ControlsBundle)

            assembler = ControlsTabsAssembler()
            result = assembler.assemble_tabs(mock_notebook, mock_bundle)

            self.assertIsInstance(result, ControlsTabsBundle)
            self.assertIs(result.dsl_editor_tab, mock_dsl_fact.return_value)
            self.assertIs(result.streamer_tab, mock_stream_fact.return_value)
            self.assertIs(result.validation_tab, mock_val_fact.return_value)
            self.assertIs(result.jog_tab, mock_jog_fact.return_value)
            self.assertIs(result.preview_tab, mock_prev_fact.return_value)


if __name__ == '__main__':
    main()
