# -*- coding: UTF-8 -*-

'''
Module
    irunner_test.py
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
    Unit tests for IValvePulseRunner protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.tool.iactuator import IPurgeValveActuator
from scarajectory.infrastructure.tool.worker.irunner import IValvePulseRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyRunner:
    '''
        Dummy runner implementing IValvePulseRunner contract structurally.

        It defines:

            :methods:
                | schedule_deactivation - Schedules delayed deactivation.
                | is_active - Checks whether pulse execution is active.
    '''

    def schedule_deactivation(
        self,
        *,
        actuator: IPurgeValveActuator,
        delay_sec: float,
    ) -> None:
        '''
            Schedules delayed deactivation.

            :param actuator: Injected IPurgeValveActuator collaborator.
            :param delay_sec: Delay duration in seconds.
            :exceptions: None.
        '''

    def is_active(self) -> bool:
        '''
            Checks whether pulse execution is active.

            :return: True if active, False otherwise.
            :exceptions: None.
        '''
        return False


class TestIValvePulseRunner(TestCase):
    '''
        Test cases verifying IValvePulseRunner protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies structural protocol matching.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies DummyRunner satisfies IValvePulseRunner protocol.

            :exceptions: None.
        '''
        dummy = DummyRunner()
        self.assertIsInstance(dummy, IValvePulseRunner)


if __name__ == '__main__':
    main()
