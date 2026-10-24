# -*- coding: UTF-8 -*-

'''
Module
    hotkey.py
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
    Dedicated hotkey binder component for application shortcut key bindings.
'''

from __future__ import annotations

from tkinter import Tk
from typing import ClassVar

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


class MenuHotkeyBinder:
    '''
        Binds application-wide keyboard shortcuts to Tkinter root window.

        It defines:

            :constants:
                | KEY_NEW - Clear / new plan shortcut key combination.
                | KEY_OPEN - Open JSON dialog shortcut key combination.
                | KEY_SAVE - Save JSON dialog shortcut key combination.
                | KEY_UNDO - Undo mutation history shortcut key combination.
                | KEY_REDO - Redo mutation history shortcut key combination.
                | KEY_DELETE - Delete selected waypoint key combination.
                | KEY_BACKSPACE - Backspace selected waypoint key combination.
            :methods:
                | bind_hotkeys - Registers shortcut key combinations to actions.
                | get_version - Returns the component version string.
    '''

    KEY_NEW: ClassVar[str] = '<Control-n>'
    KEY_OPEN: ClassVar[str] = '<Control-o>'
    KEY_SAVE: ClassVar[str] = '<Control-s>'
    KEY_UNDO: ClassVar[str] = '<Control-z>'
    KEY_REDO: ClassVar[str] = '<Control-y>'
    KEY_DELETE: ClassVar[str] = '<Delete>'
    KEY_BACKSPACE: ClassVar[str] = '<BackSpace>'

    def bind_hotkeys(
        self,
        root: Tk,
        menu_bar: IAppMenuBar,
        bundle: MenuBundle,
    ) -> None:
        '''
            Binds keyboard shortcuts to window.

            :param root: Application root Tk window.
            :param menu_bar: IAppMenuBar interface instance.
            :param bundle: Injected MenuBundle collaborator instance.
            :exceptions: None.
        '''
        root.bind(self.KEY_NEW, lambda e: bundle.mutation.clear())
        root.bind(self.KEY_OPEN, lambda e: menu_bar.open_json_dialog())
        root.bind(self.KEY_SAVE, lambda e: menu_bar.save_json_dialog())
        root.bind(self.KEY_UNDO, lambda e: bundle.history.undo())
        root.bind(self.KEY_REDO, lambda e: bundle.history.redo())
        root.bind(self.KEY_DELETE, lambda e: bundle.table.delete_selected())
        root.bind(self.KEY_BACKSPACE, lambda e: bundle.table.delete_selected())

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component version string.
            :exceptions: None.
        '''
        return __version__
