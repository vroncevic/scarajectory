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
    Unit tests for MutationProvides dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.mutation.provides import MutationProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMutationProvides(TestCase):
    '''
        Test cases for MutationProvides container.

        It defines:

            :methods:
                | test_initialization - Verifies attribute assignment and immutability.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies attribute assignment and immutability.

            :exceptions: None.
        '''
        point_mutator: IPlanPointMutator = MagicMock(spec=IPlanPointMutator)
        bulk_mutator: IPlanBulkMutator = MagicMock(spec=IPlanBulkMutator)

        provides = MutationProvides(
            plan_point_mutator=point_mutator,
            plan_bulk_mutator=bulk_mutator,
        )

        self.assertIs(provides.plan_point_mutator, point_mutator)
        self.assertIs(provides.plan_bulk_mutator, bulk_mutator)

        with self.assertRaises(AttributeError):
            provides.plan_point_mutator = point_mutator  # type: ignore[misc]


if __name__ == '__main__':
    main()
