# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory module for assembling and instantiating GUI instances.
'''

from __future__ import annotations

from tkinter import TclError, Tk
from typing import Final

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.controls.ipanel import IControlsPanel
from scarajectory.infrastructure.gui.editor.table.itable import ITable
from scarajectory.infrastructure.gui.layout.builder import MainContentBuilder
from scarajectory.infrastructure.gui.layout.factory import MainContentBuilderFactory
from scarajectory.infrastructure.gui.menu.builder.bundle import MenuBuildersBundle
from scarajectory.infrastructure.gui.menu.builder.factory import MenuBuildersFactory
from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.infrastructure.gui.menu.dependencies import MenuBarDependencies
from scarajectory.infrastructure.gui.menu.factory import AppMenuBarFactory
from scarajectory.infrastructure.gui.gui import ScarajectoryGUI
from scarajectory.infrastructure.gui.bundle import GUIBundle
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.provides import GUIProvides
from scarajectory.infrastructure.gui.splash.factory import SplashScreenFactory
from scarajectory.infrastructure.gui.splash.iscreen import ISplashScreen
from scarajectory.infrastructure.gui.streaming.observer.bridge import GuiStreamObserverBridge
from scarajectory.infrastructure.gui.streaming.observer.factory import GuiStreamObserverBridgeFactory
from scarajectory.infrastructure.gui.theme.manager import ThemeManager
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GUIFactory:
    '''
        Factory responsible for creating GUI presentation instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a GUI presentation instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: GUIDependencies,
    ) -> GUIProvides:
        '''
            Assembles and instantiates a GUI presentation instance.

            :param dependencies: Injected GUIDependencies external collaborators.
            :return: Fully assembled GUIProvides instance.
            :exceptions: None.
        '''
        root: Tk = Tk()
        root.withdraw()
        splash: ISplashScreen = SplashScreenFactory.create(root)

        splash.set_progress(15, 'Configuring Motion Studio display...')
        root.title('SCARAjectory — Motion Trajectory Studio & Streamer')
        root.geometry(
            f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0'
        )
        root.minsize(1000, 650)

        splash.set_progress(40, 'Applying dark theme stylesheet...')
        ThemeManager.apply_theme(root)

        splash.set_progress(75, 'Building trajectory canvas and controls...')
        content_builder: MainContentBuilder = (
            MainContentBuilderFactory.create()
        )
        canvas: ICanvas
        toolbar: Toolbar
        table: ITable
        controls: IControlsPanel
        canvas, toolbar, table, controls = content_builder.build_content(
            root,
            bundle=dependencies,
        )

        menu_bundle: Final[MenuBundle] = MenuBundle(
            plan=dependencies.plan,
            loader=dependencies.loader,
            storer=dependencies.storer,
            dsl=dependencies.dsl,
            navigator=canvas.navigator,
            table=table,
        )
        menu_builders: Final[MenuBuildersBundle] = MenuBuildersFactory.create()
        AppMenuBarFactory.create(
            MenuBarDependencies(
                root=root,
                bundle=menu_bundle,
                builders=menu_builders,
            )
        )

        stream_bridge: Final[GuiStreamObserverBridge] = (
            GuiStreamObserverBridgeFactory.create(
                root=root,
                controls=controls,
            )
        )
        dependencies.streaming.registry.set_observer(stream_bridge)

        root.update_idletasks()
        try:
            root.attributes('-zoomed', True)

        except TclError:
            try:
                root.state('zoomed')

            except TclError:
                pass

        root.deiconify()
        root.lift()
        splash.close()


        root.after(150, canvas.navigator.fit_reach_view)

        gui_bundle: GUIBundle = GUIBundle(
            root=root,
            playback_controller=dependencies.streaming.playback_controller,
            loader=dependencies.loader,
            mutation=dependencies.plan.mutation,
            navigator=canvas.navigator,
            toolbar=toolbar,
        )
        gui = ScarajectoryGUI(bundle=gui_bundle)

        return GUIProvides(gui=gui)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
