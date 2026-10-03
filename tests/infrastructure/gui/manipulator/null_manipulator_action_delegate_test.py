# -*- coding: UTF-8 -*-

'''
Module
    null_manipulator_action_delegate_test.py
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
    Unit tests for NullManipulatorActionDelegate component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.manipulator.imanipulator_action_delegate import IManipulatorActionDelegate
from scarajectory.infrastructure.gui.manipulator.null_manipulator_action_delegate import NullManipulatorActionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestNullManipulatorActionDelegate(TestCase):
    '''
        Test cases verifying NullManipulatorActionDelegate contract and no-op behavior.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Tests structural protocol conformance against IManipulatorActionDelegate.
        '''
        delegate = NullManipulatorActionDelegate()
        self.assertIsInstance(delegate, IManipulatorActionDelegate)

    def test_actions_noop(self) -> None:
        '''
            Tests that all delegate actions execute safely as no-ops.
        '''
        delegate = NullManipulatorActionDelegate()
        try:
            delegate.on_home_robot()
            delegate.on_toggle_pump()
            delegate.on_purge_valve()
            delegate.on_override_change(100)
        except Exception as exc:  # noqa: BLE001
            self.fail(f'action raised unexpected exception: {exc}')


if __name__ == '__main__':
    main()
