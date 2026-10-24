# -*- coding: UTF-8 -*-

'''
Module
    igui_test.py
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
    Unit tests for IGUI protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingGUIStub:
    '''Conforming stub implementation satisfying IGUI.'''

    def is_initialized(self) -> bool:
        '''Checks initialization state.'''
        return True

    def start(self) -> None:
        '''Starts main event loop.'''

    def stop(self) -> None:
        '''Stops GUI window.'''

    def load_file(self, filepath: str) -> None:
        '''Loads trajectory file.'''
        _ = filepath

    def set_deadzone(self, enabled: bool) -> None:
        '''Sets deadzone state.'''
        _ = enabled


class IncompleteGUIStub:
    '''Non-conforming stub implementation missing methods.'''

    def is_initialized(self) -> bool:
        '''Checks initialization state.'''
        return True

    def start(self) -> None:
        '''Starts main event loop.'''


class IGUITestCase(TestCase):
    '''
        Tests IGUI runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
                | test_protocol_methods - Verifies protocol defines required methods.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IGUI protocol.'''
        stub = ConformingGUIStub()
        self.assertIsInstance(stub, IGUI)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IGUI protocol check.'''
        stub = IncompleteGUIStub()
        self.assertNotIsInstance(stub, IGUI)

    def test_protocol_methods(self) -> None:
        '''Verifies protocol defines all expected methods.'''
        for method_name in (
            'is_initialized', 'start', 'stop', 'load_file', 'set_deadzone'
        ):
            self.assertTrue(hasattr(IGUI, method_name))


if __name__ == '__main__':
    main()
