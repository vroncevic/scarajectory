# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit testing for ShapePlanCoordinatorBundle container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.handler.coordinator.bundle import ShapePlanCoordinatorBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestShapePlanCoordinatorBundle(TestCase):
    '''
        Unit tests for ShapePlanCoordinatorBundle.

        It defines:

            :methods:
                | test_bundle_creation_and_attributes - Verifies bundle properties.
    '''

    def test_bundle_creation_and_attributes(self) -> None:
        '''
            Verifies ShapePlanCoordinatorBundle stores and exposes collaborators.

            :exceptions: None.
        '''
        mock_store = MagicMock()
        mock_point = MagicMock()
        mock_bulk = MagicMock()
        mock_avoidance = MagicMock()
        mock_planner = MagicMock()
        mock_validator = MagicMock()

        bundle = ShapePlanCoordinatorBundle(
            store=mock_store,
            point_mutator=mock_point,
            bulk_mutator=mock_bulk,
            avoidance_adapter=mock_avoidance,
            planner_adapter=mock_planner,
            validator=mock_validator,
        )

        self.assertIs(bundle.store, mock_store)
        self.assertIs(bundle.point_mutator, mock_point)
        self.assertIs(bundle.bulk_mutator, mock_bulk)
        self.assertIs(bundle.avoidance_adapter, mock_avoidance)
        self.assertIs(bundle.planner_adapter, mock_planner)
        self.assertIs(bundle.validator, mock_validator)


if __name__ == '__main__':
    main()
