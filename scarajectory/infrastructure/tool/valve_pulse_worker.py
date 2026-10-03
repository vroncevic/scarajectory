# -*- coding: UTF-8 -*-

'''
Module
    valve_pulse_worker.py
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
    Dedicated background worker thread pulsing purge valve off after configured delay.
'''

from __future__ import annotations

from threading import Thread
from time import sleep
from typing import Final

from scarajectory.core.service.tool.ipurge_valve_actuator import IPurgeValveActuator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValvePulseWorker(Thread):
    '''
        Dedicated daemon worker executing delayed purge valve deactivation.

        It defines:

            :attributes:
                | _delay_sec - Delay duration in seconds before triggering actuator.
                | _actuator - Injected IPurgeValveActuator collaborator.
            :methods:
                | __init__ - Initializes worker with delay and actuator collaborator.
                | run - Pauses execution for duration and invokes actuator deactivation.
    '''

    _delay_sec: float
    _actuator: IPurgeValveActuator

    def __init__(
        self,
        *,
        delay_sec: float,
        actuator: IPurgeValveActuator,
    ) -> None:
        '''
            Initializes daemon worker thread with delay and actuator collaborator.

            :param delay_sec: Delay duration in seconds before triggering actuator.
            :param actuator: Injected IPurgeValveActuator collaborator.
        '''
        super().__init__(daemon=True)
        self._delay_sec: Final[float] = delay_sec
        self._actuator: Final[IPurgeValveActuator] = actuator

    def run(self) -> None:
        '''
            Pauses thread execution for configured duration and triggers actuator.
        '''
        sleep(self._delay_sec)
        self._actuator.deactivate_purge_valve()
