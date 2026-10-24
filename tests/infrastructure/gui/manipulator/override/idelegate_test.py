# -*- coding: UTF-8 -*-

'''
Module
    idelegate_test.py
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
    Unit testing for IManipulatorActionDelegate protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.manipulator.override.idelegate import IManipulatorActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingActionDelegateStub:
    '''Conforming stub implementation satisfying IManipulatorActionDelegate.'''

    def on_home_robot(self) -> None:
        '''Transmits homing calibration command.'''

    def on_toggle_pump(self) -> bool:
        '''Toggles vacuum pump state.'''
        return True

    def on_purge_valve(self) -> None:
        '''Sends momentary purge valve pulse command.'''

    def on_override_change(self, pct: int) -> None:
        '''Updates feedrate speed override percentage.'''
        _ = pct


class NonConformingActionDelegateStub:
    '''Non-conforming stub missing required delegate methods.'''

    def on_home_robot(self) -> None:
        '''Transmits homing calibration command.'''

    def auxiliary_action(self) -> None:
        '''Auxiliary action method to satisfy method count.'''


class TestIManipulatorActionDelegate(TestCase):
    '''Unit tests validating structural protocol runtime checks for IManipulatorActionDelegate.'''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies conforming stub satisfies IManipulatorActionDelegate protocol.

            :exceptions: None.
        '''
        stub = ConformingActionDelegateStub()
        self.assertIsInstance(stub, IManipulatorActionDelegate)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-conforming stub fails IManipulatorActionDelegate protocol check.

            :exceptions: None.
        '''
        incomplete = NonConformingActionDelegateStub()
        self.assertNotIsInstance(incomplete, IManipulatorActionDelegate)


if __name__ == '__main__':
    main()
