# -*- coding: UTF-8 -*-

'''
Module
    scarajectory_gui_factory.py
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
    Factory module for assembling and instantiating ScarajectoryGUI instances.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from typing import Final

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.controls.icontrols_panel import IControlsPanel
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.layout.main_content_builder import MainContentBuilder
from scarajectory.infrastructure.gui.layout.main_content_builder_factory import MainContentBuilderFactory
from scarajectory.infrastructure.gui.menu.app_menu_bar_factory import AppMenuBarFactory
from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.infrastructure.gui.scarajectory_gui import ScarajectoryGUI
from scarajectory.infrastructure.gui.scarajectory_gui_bundle import ScarajectoryGUIBundle
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle
from scarajectory.infrastructure.gui.streaming.observer.gui_stream_observer_bridge import GuiStreamObserverBridge
from scarajectory.infrastructure.gui.streaming.observer.gui_stream_observer_bridge_factory import GuiStreamObserverBridgeFactory
from scarajectory.infrastructure.gui.theme.theme_manager import ThemeManager
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScarajectoryGUIFactory:
    '''
        Factory responsible for creating ScarajectoryGUI presentation instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a ScarajectoryGUI instance.
                | create_with_root - Assembles a ScarajectoryGUI instance with custom root Tk.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        bundle: ScarajectoryGUIInitBundle,
    ) -> ScarajectoryGUI:
        '''
            Assembles and instantiates a ScarajectoryGUI instance with default root window.

            :param bundle: Injected ScarajectoryGUIInitBundle dependencies.
            :return: Fully assembled ScarajectoryGUI instance.
            :exceptions: None.
        '''
        return cls.create_with_root(bundle=bundle, root=Tk())

    @classmethod
    def create_with_root(
        cls,
        *,
        bundle: ScarajectoryGUIInitBundle,
        root: Tk,
    ) -> ScarajectoryGUI:
        '''
            Assembles and instantiates a ScarajectoryGUI instance with custom root Tk.

            :param bundle: Injected ScarajectoryGUIInitBundle dependencies.
            :param root: Root Tk window.
            :return: Fully assembled ScarajectoryGUI instance.
            :exceptions: None.
        '''
        root.withdraw()
        root.title('SCARAjectory — Motion Trajectory Studio & Streamer')
        sw: int = root.winfo_screenwidth()
        sh: int = root.winfo_screenheight()
        root.geometry(f'{sw}x{sh}+0+0')
        root.minsize(1100, 700)

        ThemeManager.apply_theme(root)
        content_builder: MainContentBuilder = (
            MainContentBuilderFactory.create()
        )
        canvas: ICanvas
        toolbar: Toolbar
        table: ITable
        controls: IControlsPanel
        canvas, toolbar, table, controls = content_builder.build_content(
            root,
            bundle=bundle,
        )

        menu_bundle: Final[MenuBundle] = MenuBundle(
            store=bundle.plan.store,
            mutation=bundle.plan.mutation,
            history=bundle.plan.history,
            storage=bundle.storage,
            dsl_service=bundle.dsl_service,
            navigator=canvas.navigator,
            table=table,
        )
        AppMenuBarFactory.create_default(
            root=root,
            bundle=menu_bundle,
        )

        stream_bridge: Final[GuiStreamObserverBridge] = (
            GuiStreamObserverBridgeFactory.create(
                root=root,
                controls=controls,
            )
        )
        bundle.streaming.dispatcher.set_observer(stream_bridge)

        try:
            root.attributes('-zoomed', True)

        except TclError:
            try:
                root.state('zoomed')

            except TclError:
                pass

        root.deiconify()
        root.after(150, canvas.navigator.fit_reach_view)

        gui_bundle: ScarajectoryGUIBundle = ScarajectoryGUIBundle(
            root=root,
            playback_controller=bundle.streaming.playback_controller,
            storage=bundle.storage,
            mutation=bundle.plan.mutation,
            navigator=canvas.navigator,
            toolbar=toolbar,
        )

        return ScarajectoryGUI(bundle=gui_bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
