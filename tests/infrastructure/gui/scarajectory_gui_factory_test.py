# -*- coding: UTF-8 -*-

'''
Module
    scarajectory_gui_factory_test.py
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
    Unit tests for ScarajectoryGUIFactory and ScarajectoryGUI conformance.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import (
    ICanvasViewNavigator,
)
from scarajectory.infrastructure.gui.controls.icontrols_panel import (
    IControlsPanel,
)
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.igui import IGUI
from scarajectory.infrastructure.gui.scarajectory_gui import ScarajectoryGUI
from scarajectory.infrastructure.gui.scarajectory_gui_factory import (
    ScarajectoryGUIFactory,
)
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import (
    ScarajectoryGUIInitBundle,
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


class TestScarajectoryGUIFactory(TestCase):
    '''
        Test cases for ScarajectoryGUIFactory.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and create callable.
                | test_gui_protocol_conformance - Verifies that ScarajectoryGUI satisfies IGUI.
                | test_factory_create_with_root - Verifies assembling GUI instance with root Tk.
                | test_factory_create_default_root - Verifies create delegates to create_with_root.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''Verifies ScarajectoryGUIFactory create signature and version.'''
        self.assertTrue(hasattr(ScarajectoryGUIFactory, 'create'))
        self.assertTrue(callable(ScarajectoryGUIFactory.create))
        self.assertEqual(ScarajectoryGUIFactory.get_version(), '1.0.4')

    def test_gui_protocol_conformance(self) -> None:
        '''Verifies that ScarajectoryGUI satisfies IGUI structural protocol.'''
        for method_name in (
            'is_initialized', 'start', 'stop', 'load_file', 'set_deadzone'
        ):
            self.assertTrue(hasattr(ScarajectoryGUI, method_name))
        self.assertTrue(issubclass(ScarajectoryGUI, IGUI))

    @patch(
        'scarajectory.infrastructure.gui.scarajectory_gui_factory.'
        'GuiStreamObserverBridgeFactory.create'
    )
    @patch(
        'scarajectory.infrastructure.gui.scarajectory_gui_factory.'
        'AppMenuBarFactory.create_default'
    )
    @patch(
        'scarajectory.infrastructure.gui.scarajectory_gui_factory.'
        'MainContentBuilderFactory.create'
    )
    @patch(
        'scarajectory.infrastructure.gui.scarajectory_gui_factory.'
        'ThemeManager.apply_theme'
    )
    def test_factory_create_with_root(
        self,
        mock_apply_theme: MagicMock,
        mock_create_builder: MagicMock,
        mock_create_menu: MagicMock,
        mock_create_bridge: MagicMock,
    ) -> None:
        '''Verifies create_with_root builds components and returns ScarajectoryGUI.'''
        mock_root = MagicMock(spec=Tk)
        mock_root.winfo_screenwidth.return_value = 1920
        mock_root.winfo_screenheight.return_value = 1080
        mock_root.attributes.side_effect = TclError('Zoomed unsupported')
        mock_root.state.side_effect = TclError('State unsupported')

        mock_builder = MagicMock()
        mock_create_builder.return_value = mock_builder
        mock_canvas = MagicMock(spec=ICanvas)
        mock_canvas.navigator = MagicMock(spec=ICanvasViewNavigator)
        mock_toolbar = MagicMock(spec=Toolbar)
        mock_table = MagicMock(spec=ITable)
        mock_controls = MagicMock(spec=IControlsPanel)
        mock_builder.build_content.return_value = (
            mock_canvas,
            mock_toolbar,
            mock_table,
            mock_controls,
        )

        mock_bundle = MagicMock(spec=ScarajectoryGUIInitBundle)
        gui = ScarajectoryGUIFactory.create_with_root(
            bundle=mock_bundle,
            root=mock_root,
        )

        self.assertIsInstance(gui, ScarajectoryGUI)
        mock_root.withdraw.assert_called_once()
        mock_root.deiconify.assert_called_once()
        mock_apply_theme.assert_called_once_with(mock_root)
        mock_create_builder.assert_called_once()
        mock_create_menu.assert_called_once()
        mock_create_bridge.assert_called_once_with(
            root=mock_root, controls=mock_controls
        )

    @patch('scarajectory.infrastructure.gui.scarajectory_gui_factory.Tk')
    def test_factory_create_default_root(self, mock_tk_cls: MagicMock) -> None:
        '''Verifies create instantiates default Tk and delegates to create_with_root.'''
        mock_root = mock_tk_cls.return_value
        with patch.object(
            ScarajectoryGUIFactory, 'create_with_root'
        ) as mock_create_with_root:
            mock_bundle = MagicMock(spec=ScarajectoryGUIInitBundle)
            ScarajectoryGUIFactory.create(bundle=mock_bundle)
            mock_create_with_root.assert_called_once_with(
                bundle=mock_bundle, root=mock_root
            )


if __name__ == '__main__':
    main()
