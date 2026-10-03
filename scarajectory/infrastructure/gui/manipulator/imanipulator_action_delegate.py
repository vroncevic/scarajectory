# -*- coding: UTF-8 -*-

'''
Module
    imanipulator_action_delegate.py
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
    Defines structural protocol IManipulatorActionDelegate for manipulator override actions.
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
class IManipulatorActionDelegate(Protocol):
    '''
        Structural protocol defining manipulator actuator and override actions.

        It defines:

            :methods:
                | on_home_robot - Transmits homing calibration command.
                | on_toggle_pump - Toggles vacuum pump state.
                | on_purge_valve - Sends momentary purge valve pulse command.
                | on_override_change - Updates feedrate speed override percentage.
    '''

    def on_home_robot(self) -> None:
        '''
            Transmits homing calibration command.
        '''

    def on_toggle_pump(self) -> None:
        '''
            Toggles vacuum pump state.
        '''

    def on_purge_valve(self) -> None:
        '''
            Sends momentary purge valve pulse command.
        '''

    def on_override_change(self, pct: int) -> None:
        '''
            Updates feedrate speed override percentage.

            :param pct: Speed override percentage (10 to 200).
        '''
