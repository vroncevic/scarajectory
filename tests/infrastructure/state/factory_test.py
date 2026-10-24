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
    Unit tests for StateFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.infrastructure.state.dependencies import StateDependencies
from scarajectory.infrastructure.state.factory import StateFactory
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.state.provides import StateProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStateFactory(TestCase):
    '''
        Test cases for StateFactory component.

        It defines:

            :methods:
                | test_factory_create_default - Verifies default construction returns StateProvides.
                | test_factory_create_with_dependencies - Verifies construction with custom dependencies.
                | test_factory_version - Verifies get_version returns semantic version string.
    '''

    def test_factory_create_default(self) -> None:
        '''
            Verifies default factory construction returning StateProvides with IStreamStateMachine.

            :exceptions: None.
        '''
        provides = StateFactory.create(StateDependencies())
        self.assertIsInstance(provides, StateProvides)
        self.assertIsInstance(provides.stream_state_machine, IStreamStateMachine)
        self.assertEqual(provides.stream_state_machine.state, StreamState.IDLE)

    def test_factory_create_with_dependencies(self) -> None:
        '''
            Verifies factory construction with custom StateDependencies.

            :exceptions: None.
        '''
        deps = StateDependencies(initial_state=StreamState.STREAMING)
        provides = StateFactory.create(deps)
        self.assertIsInstance(provides, StateProvides)
        self.assertIsInstance(provides.stream_state_machine, IStreamStateMachine)
        self.assertEqual(provides.stream_state_machine.state, StreamState.STREAMING)

    def test_factory_version(self) -> None:
        '''
            Verifies factory version string retrieval.
        '''
        version = StateFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
