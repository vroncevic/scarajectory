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
    Unit tests for PlanHistoryFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.history.dependencies import HistoryStackDependencies
from scarajectory.core.service.trajectory.history.factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.history.navigator.inavigator import IPlanHistoryNavigator
from scarajectory.core.service.trajectory.history.provides import HistoryStackProvides
from scarajectory.core.service.trajectory.history.saver.isaver import IPlanHistorySaver
from scarajectory.core.service.trajectory.history.stack.factory import PlanHistoryStackFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanHistoryFactory(TestCase):
    '''
        Test cases for PlanHistoryFactory.

        It defines:

            :methods:
                | test_create - Tests instantiation of HistoryStackProvides via factory.
                | test_get_version - Tests factory version query.
    '''

    def test_create(self) -> None:
        '''
            Tests factory instantiation of HistoryStackProvides.

            :exceptions: None.
        '''
        stack = PlanHistoryStackFactory.create()
        deps = HistoryStackDependencies(stack=stack)
        provides = PlanHistoryFactory.create(deps)
        self.assertIsInstance(provides, HistoryStackProvides)
        self.assertIsInstance(provides.history, IPlanHistoryNavigator)
        self.assertIsInstance(provides.saver, IPlanHistorySaver)

    def test_get_version(self) -> None:
        '''
            Tests factory version string.

            :exceptions: None.
        '''
        version = PlanHistoryFactory.get_version()
        self.assertTrue(isinstance(version, str) and len(version) > 0)


if __name__ == '__main__':
    main()
