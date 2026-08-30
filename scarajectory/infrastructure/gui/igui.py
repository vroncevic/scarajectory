# -*- coding: UTF-8 -*-

'''
Module
    igui.py
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
    Defines abstract interface IGUI for graphical user interface adapters.
'''

from __future__ import annotations

from abc import ABC, abstractmethod

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class IGUI(ABC):
    '''
        Abstract interface for GUI presentation adapters.

        It defines:

            :methods:
                | is_initialized - Checks if the GUI adapter is initialized.
                | start - Starts the GUI main event loop.
                | stop - Closes and destroys the GUI window.
                | load_file - Loads a trajectory plan file into the GUI.
    '''

    @abstractmethod
    def is_initialized(self) -> bool:
        '''
            Checks if the GUI adapter is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''

    @abstractmethod
    def start(self) -> None:
        '''
            Starts the GUI main event loop.

            :exceptions: None.
        '''

    @abstractmethod
    def stop(self) -> None:
        '''
            Closes and destroys the GUI window.

            :exceptions: None.
        '''

    @abstractmethod
    def load_file(self, filepath: str) -> None:
        '''
            Loads a trajectory plan file into the GUI.

            :param filepath: Path to the trajectory JSON file.
            :exceptions: None.
        '''
