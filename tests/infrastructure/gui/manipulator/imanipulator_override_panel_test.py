# -*- coding: UTF-8 -*-

'''
Module
    imanipulator_override_panel_test.py
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
    Unit testing for IManipulatorOverridePanel protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.manipulator.imanipulator_override_panel import IManipulatorOverridePanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingManipulatorOverridePanelStub:
    '''Conforming stub implementation satisfying IManipulatorOverridePanel.'''

    def set_pump_active(self, active: bool) -> None:
        '''Updates pump active state.'''
        _ = active

    def set_override_label(self, pct: int) -> None:
        '''Updates override percentage label.'''
        _ = pct


class NonConformingManipulatorOverridePanelStub:
    '''Non-conforming stub missing set_override_label method.'''

    def set_pump_active(self, active: bool) -> None:
        '''Updates pump active state.'''
        _ = active

    def get_panel_title(self) -> str:
        '''Returns panel title.'''
        return 'Override'


class ManipulatorOverridePanelTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IManipulatorOverridePanel.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies conforming stub satisfies IManipulatorOverridePanel protocol.'''
        stub = ConformingManipulatorOverridePanelStub()
        self.assertIsInstance(stub, IManipulatorOverridePanel)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-conforming stub fails IManipulatorOverridePanel protocol check.'''
        incomplete = NonConformingManipulatorOverridePanelStub()
        self.assertNotIsInstance(incomplete, IManipulatorOverridePanel)


if __name__ == '__main__':
    main()
