# -*- coding: UTF-8 -*-

'''
Module
    ieditor_test.py
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
    Unit tests for IWaypointEditor interface and protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.editor.ieditor import IWaypointEditor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingWaypointEditorStub:
    '''
        Conforming stub implementation satisfying IWaypointEditor.

        It defines:

            :methods:
                | delete_selected - Simulates deleting selected waypoint.
                | refresh_table - Simulates refreshing table.
                | apply_point_edit - Simulates applying point edit.
                | on_trajectory_updated - Simulates trajectory update callback.
                | get_version - Returns version string.
    '''

    def delete_selected(self) -> None:
        '''
            Simulates deleting selected waypoint.
        '''

    def refresh_table(self) -> None:
        '''
            Simulates refreshing table.
        '''

    def apply_point_edit(self) -> None:
        '''
            Simulates applying point edit.
        '''

    def on_trajectory_updated(self) -> None:
        '''
            Simulates trajectory update callback.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
        '''
        return '1.0.0'


class IncompleteWaypointEditorStub:
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
        '''
        return '1.0.0'

    def dummy_method(self) -> None:
        '''
            Dummy test method.
        '''


class TestIWaypointEditor(TestCase):
    '''
        Tests verifying IWaypointEditor protocol definition and subtyping.

        It defines:

            :methods:
                | test_protocol_methods - Verifies methods declared on protocol.
                | test_conforming_stub_subtyping - Verifies stub satisfies protocol.
                | test_incomplete_stub_failure - Verifies incomplete stub fails protocol check.
    '''

    def test_protocol_methods(self) -> None:
        '''
            Verifies methods declared on IWaypointEditor protocol.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(IWaypointEditor, 'delete_selected'))
        self.assertTrue(hasattr(IWaypointEditor, 'refresh_table'))
        self.assertTrue(hasattr(IWaypointEditor, 'apply_point_edit'))
        self.assertTrue(hasattr(IWaypointEditor, 'on_trajectory_updated'))
        self.assertTrue(hasattr(IWaypointEditor, 'get_version'))

    def test_conforming_stub_subtyping(self) -> None:
        '''
            Verifies conforming stub satisfies IWaypointEditor structurally.

            :exceptions: None.
        '''
        stub = ConformingWaypointEditorStub()
        self.assertIsInstance(stub, IWaypointEditor)

    def test_incomplete_stub_failure(self) -> None:
        '''
            Verifies incomplete stub fails protocol check.

            :exceptions: None.
        '''
        stub = IncompleteWaypointEditorStub()
        self.assertNotIsInstance(stub, IWaypointEditor)


if __name__ == '__main__':
    main()
