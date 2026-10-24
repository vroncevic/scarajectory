# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for StoreProvides container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.store.bulk_mutator.ibulk_mutator import IWaypointBulkMutator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.plan.store.mutator.imutator import IWaypointMutator
from scarajectory.core.service.trajectory.plan.store.provides import StoreProvides
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStoreProvides(TestCase):
    '''
        Test cases for StoreProvides container.

        It defines:

            :methods:
                | test_container_initialization - Verifies StoreProvides attributes and types.
    '''

    def test_container_initialization(self) -> None:
        '''
            Verifies StoreProvides attributes and types.

            :exceptions: None.
        '''
        store = MagicMock(spec=IWaypointStore)
        query = MagicMock(spec=IWaypointQuery)
        mutator = MagicMock(spec=IWaypointMutator)
        bulk_mutator = MagicMock(spec=IWaypointBulkMutator)

        provides = StoreProvides(
            waypoint_store=store,
            waypoint_query=query,
            waypoint_mutator=mutator,
            waypoint_bulk_mutator=bulk_mutator,
        )

        self.assertIs(provides.waypoint_store, store)
        self.assertIs(provides.waypoint_query, query)
        self.assertIs(provides.waypoint_mutator, mutator)
        self.assertIs(provides.waypoint_bulk_mutator, bulk_mutator)


if __name__ == '__main__':
    main()
