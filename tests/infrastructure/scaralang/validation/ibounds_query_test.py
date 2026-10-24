# -*- coding: UTF-8 -*-

'''
Module
    ibounds_query_test.py
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
    Unit tests for IWorkspaceBoundsQuery protocol.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope
from scarajectory.infrastructure.scaralang.validation.ibounds_query import IWorkspaceBoundsQuery

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyBoundsQuery:
    '''
        Dummy implementation satisfying IWorkspaceBoundsQuery protocol.

        It defines:

            :methods:
                | bounds - Returns dummy manipulator kinematic bounds model.
                | envelope - Returns dummy workspace envelope provider.
                | r_min - Returns dummy inner workspace reach radius.
                | r_max - Returns dummy outer workspace reach radius.
    '''

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns dummy bounds model.

            :return: Mock ScaraBounds.
            :exceptions: None.
        '''
        return MagicMock(spec=ScaraBounds)

    @property
    def envelope(self) -> IWorkspaceEnvelope:
        '''
            Returns dummy envelope.

            :return: Mock IWorkspaceEnvelope.
            :exceptions: None.
        '''
        return MagicMock(spec=IWorkspaceEnvelope)

    @property
    def r_min(self) -> float:
        '''
            Returns dummy inner reach radius.

            :return: Minimum reach radius float.
            :exceptions: None.
        '''
        return 10.0

    @property
    def r_max(self) -> float:
        '''
            Returns dummy outer reach radius.

            :return: Maximum reach radius float.
            :exceptions: None.
        '''
        return 270.0


class TestIWorkspaceBoundsQuery(TestCase):
    '''
        Test cases for IWorkspaceBoundsQuery protocol.

        It defines:

            :methods:
                | test_conformance - Verifies protocol structural conformance.
    '''

    def test_conformance(self) -> None:
        '''
            Verifies protocol structural conformance.

            :exceptions: None.
        '''
        dummy = DummyBoundsQuery()
        self.assertIsInstance(dummy, IWorkspaceBoundsQuery)


if __name__ == '__main__':
    main()
