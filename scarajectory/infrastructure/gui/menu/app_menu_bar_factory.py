# -*- coding: UTF-8 -*-

'''
Module
    app_menu_bar_factory.py
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
    Factory service constructing AppMenuBar instances.
'''

from __future__ import annotations

from tkinter import Tk

from scarajectory.infrastructure.gui.menu.app_menu_bar import AppMenuBar
from scarajectory.infrastructure.gui.menu.builders_bundle import MenuBuildersBundle
from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.infrastructure.gui.menu.menu_hotkey_binder_factory import MenuHotkeyBinderFactory
from scarajectory.infrastructure.gui.menu.menu_layout_builder_factory import MenuLayoutBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppMenuBarFactory:
    '''
        Factory providing instantiation of AppMenuBar components.

        It defines:

            :methods:
                | create - Creates an AppMenuBar with injected dependencies.
                | create_default - Creates an AppMenuBar with default builders.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        root: Tk,
        bundle: MenuBundle,
        builders: MenuBuildersBundle,
    ) -> AppMenuBar:
        '''
            Creates an AppMenuBar with injected dependencies.

            :param root: Application root Tk window.
            :param bundle: Injected MenuBundle container instance.
            :param builders: Injected MenuBuildersBundle container instance.
            :return: AppMenuBar instance.
            :exceptions: None.
        '''
        return AppMenuBar(
            root=root,
            bundle=bundle,
            builders=builders,
        )

    @classmethod
    def create_default(
        cls,
        root: Tk,
        bundle: MenuBundle,
    ) -> AppMenuBar:
        '''
            Creates an AppMenuBar with default builders.

            :param root: Application root Tk window.
            :param bundle: Injected MenuBundle container instance.
            :return: AppMenuBar instance.
            :exceptions: None.
        '''
        builders: MenuBuildersBundle = MenuBuildersBundle(
            layout_builder=MenuLayoutBuilderFactory.create(),
            hotkey_binder=MenuHotkeyBinderFactory.create(),
        )

        return cls.create(
            root=root,
            bundle=bundle,
            builders=builders,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
