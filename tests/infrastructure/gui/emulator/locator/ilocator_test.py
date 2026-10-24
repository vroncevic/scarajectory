# -*- coding: UTF-8 -*-

'''
Module
    ilocator_test.py
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
    Unit testing for IEmulatorLocator protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.emulator.locator.ilocator import IEmulatorLocator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingLocatorStub:
    '''Conforming stub satisfying IEmulatorLocator protocol.'''

    def is_available(self) -> bool:
        '''Checks availability.'''
        return True

    def build_command(self, *, file_path: str) -> list[str]:
        '''Builds command.'''
        _ = file_path
        return ['scaraemu']

    def build_environment(self) -> dict[str, str]:
        '''Builds environment.'''
        return {}

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'


class IncompleteLocatorStub:
    '''Non-conforming stub missing protocol methods.'''

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'

    def dummy_action(self) -> None:
        '''Dummy method for public method threshold.'''


class EmulatorLocatorProtocolTestCase(TestCase):
    '''
        Tests IEmulatorLocator runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_methods - Verifies methods declared on protocol.
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_methods(self) -> None:
        '''
            Verifies methods declared on IEmulatorLocator protocol.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(IEmulatorLocator, 'is_available'))
        self.assertTrue(hasattr(IEmulatorLocator, 'build_command'))
        self.assertTrue(hasattr(IEmulatorLocator, 'build_environment'))
        self.assertTrue(hasattr(IEmulatorLocator, 'get_version'))

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies IEmulatorLocator protocol.

            :exceptions: None.
        '''
        stub = ConformingLocatorStub()
        self.assertIsInstance(stub, IEmulatorLocator)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-compliant class fails IEmulatorLocator protocol check.

            :exceptions: None.
        '''
        stub = IncompleteLocatorStub()
        self.assertNotIsInstance(stub, IEmulatorLocator)


if __name__ == '__main__':
    main()
