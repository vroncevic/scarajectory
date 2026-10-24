# -*- coding: UTF-8 -*-

'''
Module
    iapplier_test.py
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
    Unit tests for IWaypointEditApplier interface and protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.editor.applier.iapplier import IWaypointEditApplier
from scarajectory.infrastructure.gui.editor.applier.inputs import WaypointCoordinateInputs
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingEditApplierStub:
    '''
        Conforming stub implementation satisfying IWaypointEditApplier.

        It defines:

            :methods:
                | apply_edit - Simulates coordinate application.
                | get_version - Returns version string.
    '''

    def apply_edit(
        self,
        *,
        inputs: WaypointCoordinateInputs,
        bundle: TableBundle,
    ) -> bool:
        '''
            Simulates coordinate application.

            :param inputs: Injected WaypointCoordinateInputs container.
            :param bundle: Injected TableBundle dependency container.
            :return: True always for test stub.
            :exceptions: None.
        '''
        _ = inputs
        _ = bundle
        return True

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.0'


class IncompleteEditApplierStub:
    '''
        Non-conforming stub missing protocol methods.

        It defines:

            :methods:
                | get_version - Returns version string.
                | dummy_method - Dummy test method.
    '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.0'

    def dummy_method(self) -> None:
        '''
            Dummy test method.

            :exceptions: None.
        '''


class TestIWaypointEditApplier(TestCase):
    '''
        Tests verifying IWaypointEditApplier protocol definition and subtyping.

        It defines:

            :methods:
                | test_protocol_methods - Verifies methods declared on protocol.
                | test_conforming_stub_subtyping - Verifies stub satisfies protocol.
                | test_incomplete_stub_failure - Verifies incomplete stub fails protocol check.
    '''

    def test_protocol_methods(self) -> None:
        '''
            Verifies methods declared on IWaypointEditApplier protocol.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(IWaypointEditApplier, 'apply_edit'))
        self.assertTrue(hasattr(IWaypointEditApplier, 'get_version'))

    def test_conforming_stub_subtyping(self) -> None:
        '''
            Verifies conforming stub satisfies IWaypointEditApplier structurally.

            :exceptions: None.
        '''
        stub = ConformingEditApplierStub()
        self.assertIsInstance(stub, IWaypointEditApplier)

    def test_incomplete_stub_failure(self) -> None:
        '''
            Verifies incomplete stub fails protocol check.

            :exceptions: None.
        '''
        stub = IncompleteEditApplierStub()
        self.assertNotIsInstance(stub, IWaypointEditApplier)


if __name__ == '__main__':
    main()
