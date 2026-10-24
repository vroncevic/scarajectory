# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit testing for PreviewDependencies container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.exporter.scara.iexporter import IScaraPlanExporter
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.infrastructure.gui.preview.dependencies import PreviewDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreviewDependenciesTestCase(TestCase):
    '''
        Unit tests for PreviewDependencies container.

        It defines:

            :methods:
                | test_initialization - Verifies container properties initialization.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies container properties initialization.

            :exceptions: None.
        '''
        mock_plan = MagicMock(spec=IWaypointQuery)
        mock_exporter = MagicMock(spec=IScaraPlanExporter)

        deps = PreviewDependencies(
            plan=mock_plan,
            exporter=mock_exporter,
        )

        self.assertIs(deps.plan, mock_plan)
        self.assertIs(deps.exporter, mock_exporter)


if __name__ == '__main__':
    main()
