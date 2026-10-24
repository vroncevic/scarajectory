# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for WorkerProvides dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.tool.worker.irunner import IValvePulseRunner
from scarajectory.infrastructure.tool.worker.provides import WorkerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkerProvides(TestCase):
    '''
        Test cases verifying WorkerProvides immutability and attributes.

        It defines:

            :methods:
                | test_bundle_creation - Verifies valid attribute storage.
                | test_bundle_frozen - Verifies dataclass immutability.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies bundle correctly holds provided pulse runner instance.

            :exceptions: None.
        '''
        mock_runner = MagicMock(spec=IValvePulseRunner)
        provides = WorkerProvides(pulse_runner=mock_runner)
        self.assertIs(provides.pulse_runner, mock_runner)

    def test_bundle_frozen(self) -> None:
        '''
            Verifies that modifying attributes raises an error due to frozen dataclass.

            :exceptions: None.
        '''
        mock_runner = MagicMock(spec=IValvePulseRunner)
        provides = WorkerProvides(pulse_runner=mock_runner)
        with self.assertRaises(AttributeError):
            provides.pulse_runner = mock_runner  # type: ignore[misc]


if __name__ == '__main__':
    main()
