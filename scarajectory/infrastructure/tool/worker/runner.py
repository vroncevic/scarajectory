# -*- coding: UTF-8 -*-

'''
Module
    runner.py
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
    Dedicated runner executing delayed purge valve deactivation using background worker.
'''

from __future__ import annotations

from threading import Thread

from scarajectory.core.service.tool.iactuator import IPurgeValveActuator
from scarajectory.infrastructure.tool.worker.worker import ValvePulseWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValvePulseRunner:
    '''
        Dedicated runner executing delayed purge valve deactivation using background worker.

        It defines:

            :attributes:
                | _worker_thread - Active background worker thread for pulse deactivation.
            :methods:
                | __init__ - Initializes ValvePulseRunner instance.
                | schedule_deactivation - Schedules delayed purge valve deactivation.
                | is_active - Checks whether pulse deactivation is actively running.
    '''

    _worker_thread: Thread

    def __init__(self) -> None:
        '''
            Initializes ValvePulseRunner with idle worker thread.

            :exceptions: None.
        '''
        self._worker_thread: Thread = Thread(target=tuple)

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
            :exceptions: None.
        '''
        self._worker_thread = ValvePulseWorker(
            delay_sec=delay_sec,
            actuator=actuator,
        )
        self._worker_thread.start()

    def is_active(self) -> bool:
        '''
            Checks whether pulse deactivation is actively running.

            :return: True if pulse worker is alive, False otherwise.
            :exceptions: None.
        '''
        return self._worker_thread.is_alive()
