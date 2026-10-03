# -*- coding: UTF-8 -*-

'''
Module
    istream_control_delegate.py
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
    Defines structural protocol IStreamControlDelegate for stream execution actions.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamControlDelegate(Protocol):
    '''
        Structural protocol defining trajectory stream execution control actions.

        It defines:

            :methods:
                | on_start_stream - Initiates trajectory streaming transmission.
                | on_pause_resume_stream - Toggles stream pause and resume states.
                | on_stop_stream - Aborts stream transmission and stops motion.
    '''

    def on_start_stream(self) -> None:
        '''
            Initiates trajectory streaming transmission.
        '''

    def on_pause_resume_stream(self) -> None:
        '''
            Toggles stream pause and resume states.
        '''

    def on_stop_stream(self) -> None:
        '''
            Aborts stream transmission and stops motion.
        '''
