# -*- coding: UTF-8 -*-

'''
Module
    valve_pulse_worker_test.py
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
    Unit tests for ValvePulseWorker and ValvePulseWorkerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.tool.valve_pulse_worker import ValvePulseWorker
from scarajectory.infrastructure.tool.valve_pulse_worker_factory import ValvePulseWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestValvePulseWorker(TestCase):
    '''Test cases for ValvePulseWorker.'''

    def test_worker_execution(self) -> None:
        '''Tests background thread execution and actuator deactivation.'''
        mock_actuator: MagicMock = MagicMock()

        worker: ValvePulseWorker = ValvePulseWorkerFactory.create(
            delay_sec=0.01,
            actuator=mock_actuator,
        )
        worker.start()
        worker.join()

        mock_actuator.deactivate_purge_valve.assert_called_once()

    def test_factory_version(self) -> None:
        '''Tests factory version string.'''
        self.assertEqual(ValvePulseWorkerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
