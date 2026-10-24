# -*- coding: UTF-8 -*-

'''
Module
    runner_test.py
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
    Unit tests for ValvePulseRunner class.
'''

from __future__ import annotations

from time import sleep
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.tool.iactuator import IPurgeValveActuator
from scarajectory.infrastructure.tool.worker.irunner import IValvePulseRunner
from scarajectory.infrastructure.tool.worker.runner import ValvePulseRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestValvePulseRunner(TestCase):
    '''
        Test cases verifying ValvePulseRunner execution and protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies structural protocol matching.
                | test_initial_state - Verifies runner is inactive upon creation.
                | test_schedule_deactivation - Verifies delayed actuator execution.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies ValvePulseRunner satisfies IValvePulseRunner protocol.

            :exceptions: None.
        '''
        runner = ValvePulseRunner()
        self.assertIsInstance(runner, IValvePulseRunner)

    def test_initial_state(self) -> None:
        '''
            Verifies newly created runner reports inactive state.

            :exceptions: None.
        '''
        runner = ValvePulseRunner()
        self.assertFalse(runner.is_active())

    def test_schedule_deactivation(self) -> None:
        '''
            Verifies scheduling deactivation triggers actuator and updates state.

            :exceptions: None.
        '''
        mock_actuator = MagicMock(spec=IPurgeValveActuator)
        runner = ValvePulseRunner()

        runner.schedule_deactivation(
            actuator=mock_actuator,
            delay_sec=0.01,
        )
        sleep(0.05)
        self.assertFalse(runner.is_active())
        mock_actuator.deactivate_purge_valve.assert_called_once()


if __name__ == '__main__':
    main()
