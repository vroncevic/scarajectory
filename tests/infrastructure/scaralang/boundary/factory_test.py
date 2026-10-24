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
    Unit tests for WorkspaceBoundaryAdapterFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.scaralang.boundary.factory import WorkspaceBoundaryAdapterFactory
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceBoundaryAdapterFactory(TestCase):
    '''
        Unit test cases verifying WorkspaceBoundaryAdapterFactory behavior.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates instance implementing IWorkspaceBoundaryAdapter.

            :exceptions: None.
        '''
        adapter = WorkspaceBoundaryAdapterFactory.create()
        self.assertIsInstance(adapter, IWorkspaceBoundaryAdapter)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns version string.

            :exceptions: None.
        '''
        self.assertIsInstance(
            WorkspaceBoundaryAdapterFactory.get_version(), str
        )


if __name__ == '__main__':
    main()
