# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for WorkerFactory in tool worker subpackage.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.tool.worker.factory import WorkerFactory
from scarajectory.infrastructure.tool.worker.irunner import IValvePulseRunner
from scarajectory.infrastructure.tool.worker.provides import WorkerProvides
from scarajectory.infrastructure.tool.worker.runner import ValvePulseRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkerFactory(TestCase):
    '''
        Test cases verifying WorkerFactory construction and version reporting.

        It defines:

            :methods:
                | test_create_runner - Verifies construction of ValvePulseRunner.
                | test_get_version - Verifies version string.
    '''

    def test_create_runner(self) -> None:
        '''
            Verifies factory constructs WorkerProvides wrapping ValvePulseRunner.

            :exceptions: None.
        '''
        provides: WorkerProvides = WorkerFactory.create()

        self.assertIsInstance(provides, WorkerProvides)
        self.assertIsInstance(provides.pulse_runner, ValvePulseRunner)
        self.assertIsInstance(provides.pulse_runner, IValvePulseRunner)

    def test_get_version(self) -> None:
        '''
            Verifies factory version query.

            :exceptions: None.
        '''
        self.assertEqual(WorkerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
