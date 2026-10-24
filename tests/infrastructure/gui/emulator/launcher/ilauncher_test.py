# -*- coding: UTF-8 -*-

'''
Module
    ilauncher_test.py
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
    Unit tests for IEmulatorLauncher interface and protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.emulator.launcher.ilauncher import IEmulatorLauncher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingLauncherStub:
    '''
        Conforming stub implementation satisfying IEmulatorLauncher.

        It defines:

            :methods:
                | is_available - Simulates availability check.
                | launch_preview - Simulates emulator process launch.
                | get_version - Returns version string.
    '''

    def is_available(self) -> bool:
        '''
            Simulates availability check.

            :return: True always for test stub.
            :exceptions: None.
        '''
        return True

    def launch_preview(self, *, dsl_code: str) -> tuple[bool, str]:
        '''
            Simulates emulator process launch.

            :param dsl_code: SCARA DSL source text to preview.
            :return: Tuple of (success_boolean, status_or_error_message).
            :exceptions: None.
        '''
        _ = dsl_code
        return True, 'Success'

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.0'


class IncompleteLauncherStub:
    '''
        Non-conforming stub missing protocol methods.

        It defines:

            :methods:
                | get_version - Returns version string.
                | dummy_action - Dummy action method.
    '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.0'

    def dummy_action(self) -> None:
        '''
            Dummy action method.

            :exceptions: None.
        '''


class TestIEmulatorLauncher(TestCase):
    '''
        Tests verifying IEmulatorLauncher protocol definition and subtyping.

        It defines:

            :methods:
                | test_protocol_methods - Verifies methods declared on protocol.
                | test_conforming_stub_subtyping - Verifies stub satisfies protocol.
                | test_incomplete_stub_failure - Verifies incomplete stub fails protocol check.
    '''

    def test_protocol_methods(self) -> None:
        '''
            Verifies methods declared on IEmulatorLauncher protocol.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(IEmulatorLauncher, 'is_available'))
        self.assertTrue(hasattr(IEmulatorLauncher, 'launch_preview'))
        self.assertTrue(hasattr(IEmulatorLauncher, 'get_version'))

    def test_conforming_stub_subtyping(self) -> None:
        '''
            Verifies conforming stub satisfies IEmulatorLauncher structurally.

            :exceptions: None.
        '''
        stub = ConformingLauncherStub()
        self.assertIsInstance(stub, IEmulatorLauncher)

    def test_incomplete_stub_failure(self) -> None:
        '''
            Verifies incomplete stub fails protocol check.

            :exceptions: None.
        '''
        stub = IncompleteLauncherStub()
        self.assertNotIsInstance(stub, IEmulatorLauncher)


if __name__ == '__main__':
    main()
