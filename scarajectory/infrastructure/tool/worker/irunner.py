# -*- coding: UTF-8 -*-

'''
Module
    irunner.py
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
    Defines structural protocol IValvePulseRunner for delayed purge valve deactivation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.service.tool.iactuator import IPurgeValveActuator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IValvePulseRunner(Protocol):
    '''
        Structural protocol defining delayed purge valve deactivation operations.

        It defines:

            :methods:
                | schedule_deactivation - Schedules delayed purge valve deactivation.
                | is_active - Checks whether pulse deactivation is actively running.
    '''

    def schedule_deactivation(
        self,
        *,
        actuator: IPurgeValveActuator,
        delay_sec: float,
    ) -> None:
        '''
            Schedules delayed purge valve deactivation on actuator.

            :param actuator: Injected IPurgeValveActuator collaborator.
            :param delay_sec: Delay duration in seconds before triggering deactivation.
        '''

    def is_active(self) -> bool:
        '''
            Checks whether pulse deactivation is actively running.

            :return: True if pulse worker is alive, False otherwise.
        '''
