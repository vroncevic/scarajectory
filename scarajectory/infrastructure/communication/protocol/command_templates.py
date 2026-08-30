# -*- coding: UTF-8 -*-

'''
Module
    command_templates.py
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
    Declarative template registry for SCARA robot firmware commands.
'''

from __future__ import annotations

from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandTemplates:
    '''
        Declarative template registry for SCARA robot firmware commands.

        It defines:

            :attributes:
                | ENABLE - Command string enabling robot steppers.
                | DISABLE - Command string disabling robot steppers.
                | ESTOP - Command string triggering immediate emergency stop.
                | STATUS - Command string querying microcontroller telemetry.
                | PAUSE - Command string pausing trajectory execution.
                | RESUME - Command string resuming trajectory execution.
                | HOME - Command string triggering robot homing routine.
                | GET_CONFIG - Command querying persistent robot configuration.
                | SAVE_CONFIG - Command persisting runtime config to Flash.
                | RESET_CONFIG - Command resetting config to defaults.
                | PUMP_ON - Command turning vacuum pump on.
                | PUMP_OFF - Command turning vacuum pump off.
                | VALVE_ON - Command opening release valve.
                | VALVE_OFF - Command closing release valve.
                | MOVE_TEMPLATE - Interpolation template for waypoint motion command.
                | JOG_TEMPLATE - Interpolation template for manual jog step command.
                | SET_CONFIG_TEMPLATE - Interpolation template for runtime kinematics configuration.
            :methods:
                | get_template - Retrieves command template by action identifier.
                | list_actions - Returns tuple of supported command action keys.
    '''

    ENABLE: ClassVar[str] = '<CMD:ENABLE>'
    DISABLE: ClassVar[str] = '<CMD:DISABLE>'
    ESTOP: ClassVar[str] = '<CMD:ESTOP>'
    STATUS: ClassVar[str] = '<CMD:STATUS>'
    PAUSE: ClassVar[str] = '<CMD:PAUSE>'
    RESUME: ClassVar[str] = '<CMD:RESUME>'
    HOME: ClassVar[str] = '<CMD:HOME>'
    GET_CONFIG: ClassVar[str] = '<CMD:GET_CONFIG>'
    SAVE_CONFIG: ClassVar[str] = '<CMD:SAVE_CONFIG>'
    RESET_CONFIG: ClassVar[str] = '<CMD:RESET_CONFIG>'
    PUMP_ON: ClassVar[str] = '<CMD:PUMP#1>'
    PUMP_OFF: ClassVar[str] = '<CMD:PUMP#0>'
    VALVE_ON: ClassVar[str] = '<CMD:VALVE#1>'
    VALVE_OFF: ClassVar[str] = '<CMD:VALVE#0>'
    MOVE_TEMPLATE: ClassVar[str] = '<pt#{x:.2f}#{y:.2f}#{z:.2f}#{phi:.2f}#{speed:.1f}#end>'
    JOG_TEMPLATE: ClassVar[str] = '<CMD:JOG#{axis}#{step:.1f}>'
    SET_CONFIG_TEMPLATE: ClassVar[str] = (
        '<CMD:SET_CONFIG#L1={l1:.2f}#L2={l2:.2f}#Z_MIN={z_min:.2f}#Z_MAX={z_max:.2f}#MIN_SPEED={min_speed:.1f}#MAX_SPEED={max_speed:.1f}>'
    )

    _LOOKUP: ClassVar[dict[str, str]] = {
        'ENABLE': '<CMD:ENABLE>',
        'DISABLE': '<CMD:DISABLE>',
        'ESTOP': '<CMD:ESTOP>',
        'STATUS': '<CMD:STATUS>',
        'PAUSE': '<CMD:PAUSE>',
        'RESUME': '<CMD:RESUME>',
        'HOME': '<CMD:HOME>',
        'GET_CONFIG': '<CMD:GET_CONFIG>',
        'SAVE_CONFIG': '<CMD:SAVE_CONFIG>',
        'RESET_CONFIG': '<CMD:RESET_CONFIG>',
        'PUMP_ON': '<CMD:PUMP#1>',
        'PUMP_OFF': '<CMD:PUMP#0>',
        'VALVE_ON': '<CMD:VALVE#1>',
        'VALVE_OFF': '<CMD:VALVE#0>',
        'MOVE': '<pt#{x:.2f}#{y:.2f}#{z:.2f}#{phi:.2f}#{speed:.1f}#end>',
        'JOG': '<CMD:JOG#{axis}#{step:.1f}>',
        'SET_CONFIG': (
            '<CMD:SET_CONFIG#L1={l1:.2f}#L2={l2:.2f}#Z_MIN={z_min:.2f}#Z_MAX={z_max:.2f}#MIN_SPEED={min_speed:.1f}#MAX_SPEED={max_speed:.1f}>'
        )
    }

    @classmethod
    def get_template(cls, action: str) -> str:
        '''
            Retrieves command template by action identifier.

            :param action: Action name string.
            :return: Template string or empty string if not found.
            :exceptions: None.
        '''
        return cls._LOOKUP.get(action.upper(), '')

    @classmethod
    def list_actions(cls) -> tuple[str, ...]:
        '''
            Returns tuple of supported command action keys.

            :return: Tuple of action key strings.
            :exceptions: None.
        '''
        return tuple(cls._LOOKUP.keys())
