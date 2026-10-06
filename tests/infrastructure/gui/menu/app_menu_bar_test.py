# -*- coding: UTF-8 -*-

'''
Module
    app_menu_bar_test.py
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
    Unit tests for AppMenuBar coordinator and file dialog actions.
'''

from __future__ import annotations

from types import SimpleNamespace
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.menu.app_menu_bar import AppMenuBar
from scarajectory.infrastructure.gui.menu.builders_bundle import MenuBuildersBundle
from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.setup.pipeline.dsl_diagnostic_bundle import DslDiagnosticBundle
from scarajectory.setup.pipeline.dsl_pipeline_bundle import DslPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppMenuBarTestCase(TestCase):
    '''
        Tests for AppMenuBar file I/O operations and bindings.

        It defines:

            :methods:
                | setUp - Initializes test fixture with mock collaborators.
                | test_init_builds_and_binds - Verifies layout and hotkey wiring.
                | test_open_json_dialog - Verifies JSON load and error handling.
                | test_save_json_dialog - Verifies JSON save and error handling.
                | test_import_dsl_dialog - Verifies DSL import and compilation error handling.
                | test_export_dsl_dialog - Verifies DSL export and error handling.
    '''

    mocks: SimpleNamespace
    menu_bar: AppMenuBar

    def setUp(self) -> None:
        '''
            Initializes test fixture with mock collaborators.

            :exceptions: None.
        '''
        mocks = SimpleNamespace(
            root=MagicMock(),
            store=MagicMock(),
            mutation=MagicMock(),
            history=MagicMock(),
            storage=MagicMock(),
            compiler=MagicMock(),
            decompiler=MagicMock(),
            plan_compiler=MagicMock(),
            plan_exporter=MagicMock(),
            nav=MagicMock(),
            table=MagicMock(),
            layout=MagicMock(),
            hotkey=MagicMock(),
        )
        dsl_bundle = DslPipelineBundle(
            compiler=mocks.compiler,
            decompiler=mocks.decompiler,
            plan_compiler=mocks.plan_compiler,
            plan_exporter=mocks.plan_exporter,
            validator=MagicMock(),
            diagnostics=MagicMock(spec=DslDiagnosticBundle),
        )
        bundle = MenuBundle(
            store=mocks.store,
            mutation=mocks.mutation,
            history=mocks.history,
            storage=mocks.storage,
            dsl=dsl_bundle,
            navigator=mocks.nav,
            table=mocks.table,
        )
        builders = MenuBuildersBundle(
            layout_builder=mocks.layout,
            hotkey_binder=mocks.hotkey,
        )
        self.mocks = mocks
        self.menu_bar = AppMenuBar(mocks.root, bundle, builders)

    def test_init_builds_and_binds(self) -> None:
        '''
            Verifies that layout builder and hotkey binder are called on init.

            :exceptions: None.
        '''
        self.mocks.layout.build_menu.assert_called_once_with(
            root=self.mocks.root,
            menu_bar=self.menu_bar,
            mutation=self.mocks.mutation,
            history=self.mocks.history,
            navigator=self.mocks.nav,
        )
        self.mocks.hotkey.bind_hotkeys.assert_called_once_with(
            root=self.mocks.root,
            menu_bar=self.menu_bar,
            mutation=self.mocks.mutation,
            history=self.mocks.history,
            table=self.mocks.table,
        )

    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.showerror')
    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.askopenfilename')
    def test_open_json_dialog(
        self,
        mock_askopen: MagicMock,
        mock_showerror: MagicMock,
    ) -> None:
        '''
            Verifies open_json_dialog handles cancel, success, and error flows.

            :exceptions: None.
        '''
        # Case 1: Cancel dialog
        mock_askopen.return_value = ''
        self.menu_bar.open_json_dialog()
        self.mocks.storage.load_plan.assert_not_called()

        # Case 2: Load success
        mock_askopen.return_value = '/tmp/plan.json'
        self.mocks.storage.load_plan.return_value = ['wp1', 'wp2']
        self.menu_bar.open_json_dialog()
        self.mocks.storage.load_plan.assert_called_once_with('/tmp/plan.json')
        self.mocks.mutation.set_waypoints.assert_called_once_with(['wp1', 'wp2'])
        self.mocks.nav.fit_reach_view.assert_called_once()

        # Case 3: OSError handling
        self.mocks.storage.load_plan.side_effect = OSError('Disk failure')
        self.menu_bar.open_json_dialog()
        mock_showerror.assert_called_once()

    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.showerror')
    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.showinfo')
    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.asksaveasfilename')
    def test_save_json_dialog(
        self,
        mock_asksave: MagicMock,
        mock_showinfo: MagicMock,
        mock_showerror: MagicMock,
    ) -> None:
        '''
            Verifies save_json_dialog handles cancel, success, and error flows.

            :exceptions: None.
        '''
        # Case 1: Cancel dialog
        mock_asksave.return_value = ''
        self.menu_bar.save_json_dialog()
        self.mocks.storage.save_plan.assert_not_called()

        # Case 2: Save success
        mock_asksave.return_value = '/tmp/saved.json'
        self.menu_bar.save_json_dialog()
        self.mocks.storage.save_plan.assert_called_once_with(
            self.mocks.store, '/tmp/saved.json'
        )
        mock_showinfo.assert_called_once()

        # Case 3: OSError handling
        self.mocks.storage.save_plan.side_effect = OSError('Permission denied')
        self.menu_bar.save_json_dialog()
        mock_showerror.assert_called_once()

    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.showerror')
    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.showinfo')
    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.askopenfilename')
    def test_import_dsl_dialog(
        self,
        mock_askopen: MagicMock,
        mock_showinfo: MagicMock,
        mock_showerror: MagicMock,
    ) -> None:
        '''
            Verifies import_dsl_dialog compiles DSL scripts and handles exceptions.

            :exceptions: None.
        '''
        # Case 1: Cancel dialog
        mock_askopen.return_value = ''
        self.menu_bar.import_dsl_dialog()
        self.mocks.storage.load_text_file.assert_not_called()

        # Case 2: Import success
        mock_askopen.return_value = '/tmp/script.scara'
        self.mocks.storage.load_text_file.return_value = 'MOVE TO 10, 20'
        mock_plan = SimpleNamespace(waypoints=['wpA'], count=1)
        self.mocks.plan_compiler.compile_script.return_value = mock_plan
        self.menu_bar.import_dsl_dialog()
        self.mocks.storage.load_text_file.assert_called_once_with('/tmp/script.scara')
        self.mocks.plan_compiler.compile_script.assert_called_once_with(
            source='MOVE TO 10, 20'
        )
        self.mocks.mutation.set_waypoints.assert_called_once_with(['wpA'])
        self.mocks.nav.fit_reach_view.assert_called_once()
        mock_showinfo.assert_called_once()

        # Case 3: Compilation error handling
        self.mocks.plan_compiler.compile_script.side_effect = ValueError('Syntax error')
        self.menu_bar.import_dsl_dialog()
        mock_showerror.assert_called_once()

    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.showerror')
    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.showinfo')
    @patch('scarajectory.infrastructure.gui.menu.app_menu_bar.asksaveasfilename')
    def test_export_dsl_dialog(
        self,
        mock_asksave: MagicMock,
        mock_showinfo: MagicMock,
        mock_showerror: MagicMock,
    ) -> None:
        '''
            Verifies export_dsl_dialog exports DSL scripts and handles exceptions.

            :exceptions: None.
        '''
        # Case 1: Cancel dialog
        mock_asksave.return_value = ''
        self.menu_bar.export_dsl_dialog()
        self.mocks.plan_exporter.export_plan.assert_not_called()

        # Case 2: Export success
        mock_asksave.return_value = '/tmp/out.scara'
        self.mocks.plan_exporter.export_plan.return_value = 'MOVE TO 5, 5'
        self.menu_bar.export_dsl_dialog()
        self.mocks.plan_exporter.export_plan.assert_called_once_with(
            plan=self.mocks.store
        )
        self.mocks.storage.save_text_file.assert_called_once_with(
            'MOVE TO 5, 5', '/tmp/out.scara'
        )
        mock_showinfo.assert_called_once()

        # Case 3: OSError handling
        self.mocks.storage.save_text_file.side_effect = OSError('Disk full')
        self.menu_bar.export_dsl_dialog()
        mock_showerror.assert_called_once()


if __name__ == '__main__':
    main()
