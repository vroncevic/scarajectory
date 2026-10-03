# -*- coding: UTF-8 -*-

'''
Module
    null_manipulator_action_delegate.py
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
    Null-object implementation of manipulator override action delegate.
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NullManipulatorActionDelegate:
    '''
        Null-object implementation of manipulator override action delegate.

        It defines:

            :methods:
                | on_home_robot - No-op manipulator homing trigger.
                | on_toggle_pump - No-op vacuum pump toggle trigger.
                | on_purge_valve - No-op purge valve pulse trigger.
                | on_override_change - No-op feedrate override change.
    '''

    def on_home_robot(self) -> None:
        '''
            No-op implementation of homing trigger.

            :exceptions: None.
        '''

    def on_toggle_pump(self) -> None:
        '''
            No-op implementation of pump toggle trigger.

            :exceptions: None.
        '''

    def on_purge_valve(self) -> None:
        '''
            No-op implementation of valve pulse trigger.

            :exceptions: None.
        '''

    def on_override_change(self, pct: int) -> None:
        '''
            No-op implementation of feedrate override change.

            :param pct: Speed override percentage.
            :exceptions: None.
        '''
