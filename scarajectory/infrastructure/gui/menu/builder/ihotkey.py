# -*- coding: UTF-8 -*-

'''
Module
    ihotkey.py
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
    Defines structural protocol interface IMenuHotkeyBinder.
'''

from __future__ import annotations

from tkinter import Tk
from typing import Protocol, runtime_checkable

from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.infrastructure.gui.menu.imenu_bar import IAppMenuBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMenuHotkeyBinder(Protocol):
    '''
        Interface defining contract for application menu hotkey binders.

        It defines:

            :methods:
                | bind_hotkeys - Registers shortcut key combinations to actions.
                | get_version - Returns component version string.
    '''

    def bind_hotkeys(
        self,
        root: Tk,
        menu_bar: IAppMenuBar,
        bundle: MenuBundle,
    ) -> None:
        '''
            Binds application-wide keyboard shortcuts to the root window.

            :param root: Application root Tk window.
            :param menu_bar: IAppMenuBar interface instance.
            :param bundle: Injected MenuBundle collaborator instance.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Component version string.
        '''
