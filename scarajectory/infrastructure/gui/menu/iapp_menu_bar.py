# -*- coding: UTF-8 -*-

'''
Module
    iapp_menu_bar.py
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
    Defines interface IAppMenuBar for application top-level menu bar.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IAppMenuBar(Protocol):
    '''
        Interface for top-level menu bar dialog triggers and file operations.

        It defines:

            :methods:
                | open_json_dialog - Shows open file dialog and loads plan.
                | save_json_dialog - Shows save file dialog and saves plan.
                | import_dsl_dialog - Compiles selected SCARA DSL script into plan.
                | export_dsl_dialog - Exports active plan to SCARA DSL format.
    '''

    def open_json_dialog(self) -> None:
        '''
            Shows open file dialog and loads selected trajectory plan.
        '''

    def save_json_dialog(self) -> None:
        '''
            Shows save file dialog and saves current trajectory plan.
        '''

    def import_dsl_dialog(self) -> None:
        '''
            Shows open file dialog and compiles selected SCARA DSL script into plan.
        '''

    def export_dsl_dialog(self) -> None:
        '''
            Shows save file dialog and exports active trajectory plan to SCARA DSL format.
        '''
