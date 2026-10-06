# -*- coding: UTF-8 -*-

'''
Module
    valve_pulse_worker_factory.py
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
    Factory constructing ValvePulseWorker thread instances.
'''

from __future__ import annotations

from scarajectory.core.service.tool.ipurge_valve_actuator import IPurgeValveActuator
from scarajectory.infrastructure.tool.valve_pulse_worker import ValvePulseWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValvePulseWorkerFactory:
    '''
        Factory creating ValvePulseWorker thread instances.

        It defines:

            :methods:
                | create - Constructs ValvePulseWorker instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        delay_sec: float,
        actuator: IPurgeValveActuator,
    ) -> ValvePulseWorker:
        '''
            Constructs ValvePulseWorker instance with delay and actuator collaborator.

            :param delay_sec: Delay duration in seconds.
            :param actuator: Injected IPurgeValveActuator collaborator.
            :return: Instantiated ValvePulseWorker thread.
        '''
        return ValvePulseWorker(delay_sec=delay_sec, actuator=actuator)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
        '''
        return __version__
