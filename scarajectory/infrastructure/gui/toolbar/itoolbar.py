# -*- coding: UTF-8 -*-

'''
Module
    itoolbar.py
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
    Defines interface IToolbar for CAD drawing and kinematic settings toolbar.
'''

from __future__ import annotations

from tkinter.ttk import Label
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
class IToolbar(Protocol):
    '''
        Interface for CAD drawing tool mode selection and toolbar status readout.

        It defines:

            :methods:
                | set_deadzone - Sets deadzone enforcement checkbox state.
                | get_cursor_label - Returns cursor info label widget.
    '''

    def set_deadzone(self, enabled: bool) -> None:
        '''
            Sets deadzone enforcement checkbox state.

            :param enabled: True to enforce deadzone protection.
        '''

    def get_cursor_label(self) -> Label:
        '''
            Returns cursor info label widget.

            :return: Label widget displaying coordinates.
        '''
