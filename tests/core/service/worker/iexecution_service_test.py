# -*- coding: UTF-8 -*-

'''
Module
    iexecution_service_test.py
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
    Unit testing for IExecutionService protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.worker.iexecution_service import IExecutionService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExecutionServiceStub:
    '''Structural test stub satisfying IExecutionService protocol.'''

    def start_streaming(self) -> bool:
        '''Starts hardware streaming.'''
        return True

    def stop_streaming(self) -> None:
        '''Stops hardware streaming.'''

    def pause_streaming(self) -> None:
        '''Pauses hardware streaming.'''

    def resume_streaming(self) -> None:
        '''Resumes hardware streaming.'''


class IncompleteExecutionServiceStub:
    '''Incomplete test stub missing required streaming control methods.'''

    def start_streaming(self) -> bool:
        '''Starts streaming.'''
        return True

    def stop_streaming(self) -> None:
        '''Stops streaming.'''


class ExecutionServiceTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IExecutionService.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IExecutionService protocol.'''
        stub = ExecutionServiceStub()
        self.assertIsInstance(stub, IExecutionService)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IExecutionService protocol check.'''
        incomplete = IncompleteExecutionServiceStub()
        self.assertNotIsInstance(incomplete, IExecutionService)


if __name__ == '__main__':
    main()
