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
    Unit tests for GUIFactory and ScarajectoryGUI conformance.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.controls.ipanel import IControlsPanel
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.factory import GUIFactory
from scarajectory.infrastructure.gui.gui import ScarajectoryGUI
from scarajectory.infrastructure.gui.igui import IGUI
from scarajectory.infrastructure.gui.provides import GUIProvides
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIFactoryTestCase(TestCase):
    '''
        Test cases for GUIFactory.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and create callable.
                | test_gui_protocol_conformance - Verifies that ScarajectoryGUI satisfies IGUI.
                | test_factory_create - Verifies assembling GUI instance via factory.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''
            Verifies GUIFactory create signature and version.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(GUIFactory, 'create'))
        self.assertTrue(callable(GUIFactory.create))
        self.assertEqual(GUIFactory.get_version(), '1.0.3')

    def test_gui_protocol_conformance(self) -> None:
        '''
            Verifies that ScarajectoryGUI satisfies IGUI structural protocol.

            :exceptions: None.
        '''
        for method_name in (
            'is_initialized', 'start', 'stop', 'load_file', 'set_deadzone'
        ):
            self.assertTrue(hasattr(ScarajectoryGUI, method_name))
        self.assertTrue(issubclass(ScarajectoryGUI, IGUI))

    @patch(
        'scarajectory.infrastructure.gui.factory.AppMenuBarFactory.create'
    )
    @patch(
        'scarajectory.infrastructure.gui.factory.MainContentBuilderFactory.create'
    )
    @patch('scarajectory.infrastructure.gui.factory.Tk')
    def test_factory_create(
        self,
        mock_tk_cls: MagicMock,
        mock_create_builder: MagicMock,
        mock_create_menu: MagicMock,
    ) -> None:
        '''
            Verifies create builds presentation components and returns GUIProvides.

            :exceptions: None.
        '''
        mock_root = MagicMock(spec=Tk)
        mock_tk_cls.return_value = mock_root
        mock_root.winfo_screenwidth.return_value = 1920
        mock_root.winfo_screenheight.return_value = 1080
        mock_root.attributes.side_effect = TclError('Zoomed unsupported')
        mock_root.state.side_effect = TclError('State unsupported')
        mock_splash = MagicMock()

        mock_builder = MagicMock()
        mock_create_builder.return_value = mock_builder
        mock_controls = MagicMock(spec=IControlsPanel)
        mock_canvas = MagicMock(spec=TrajectoryCanvas)
        mock_canvas.navigator = MagicMock()
        mock_builder.build_content.return_value = (
            mock_canvas,
            MagicMock(spec=Toolbar),
            MagicMock(spec=ITable),
            mock_controls,
        )

        with patch(
            'scarajectory.infrastructure.gui.factory.SplashScreenFactory.create',
            return_value=mock_splash,
        ) as mock_create_splash, patch(
            'scarajectory.infrastructure.gui.factory.GuiStreamObserverBridgeFactory.create'
        ) as mock_create_bridge, patch(
            'scarajectory.infrastructure.gui.factory.ThemeManager.apply_theme'
        ) as mock_apply_theme:
            provides = GUIFactory.create(dependencies=MagicMock(spec=GUIDependencies))

        self.assertIsInstance(provides, GUIProvides)
        self.assertIsInstance(provides.gui, ScarajectoryGUI)
        mock_create_splash.assert_called_once_with(mock_root)
        mock_splash.set_progress.assert_called()
        mock_splash.close.assert_called_once()
        mock_root.withdraw.assert_called_once()
        mock_root.deiconify.assert_called_once()
        mock_apply_theme.assert_called_once_with(mock_root)
        mock_create_builder.assert_called_once()
        mock_create_menu.assert_called_once()
        mock_create_bridge.assert_called_once_with(
            root=mock_root, controls=mock_controls
        )
        mock_root.update_idletasks.assert_called_once()
        mock_root.attributes.assert_called_once_with('-zoomed', True)
        mock_root.state.assert_called_once_with('zoomed')
        mock_root.geometry.assert_called_once_with('1920x1080+0+0')

        mock_root.attributes.side_effect = None
        mock_root.state.side_effect = None
        with patch(
            'scarajectory.infrastructure.gui.factory.SplashScreenFactory.create',
            return_value=mock_splash,
        ), patch(
            'scarajectory.infrastructure.gui.factory.GuiStreamObserverBridgeFactory.create'
        ), patch(
            'scarajectory.infrastructure.gui.factory.ThemeManager.apply_theme'
        ):
            provides_zoomed = GUIFactory.create(
                dependencies=MagicMock(spec=GUIDependencies)
            )
        self.assertIsInstance(provides_zoomed, GUIProvides)

        mock_root.attributes.side_effect = TclError('Zoomed unsupported')
        mock_root.state.side_effect = None
        with patch(
            'scarajectory.infrastructure.gui.factory.SplashScreenFactory.create',
            return_value=mock_splash,
        ), patch(
            'scarajectory.infrastructure.gui.factory.GuiStreamObserverBridgeFactory.create'
        ), patch(
            'scarajectory.infrastructure.gui.factory.ThemeManager.apply_theme'
        ):
            provides_fallback = GUIFactory.create(
                dependencies=MagicMock(spec=GUIDependencies)
            )
        self.assertIsInstance(provides_fallback, GUIProvides)



if __name__ == '__main__':
    main()
