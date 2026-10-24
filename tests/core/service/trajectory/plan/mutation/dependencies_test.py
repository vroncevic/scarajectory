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
    Unit tests for MutationDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.history.saver.isaver import IPlanHistorySaver
from scarajectory.core.service.trajectory.plan.mutation.dependencies import MutationDependencies
from scarajectory.core.service.trajectory.plan.observer.idispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.navigator.inavigator import IPlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMutationDependencies(TestCase):
    '''
        Test cases for MutationDependencies parameter bundle.

        It defines:

            :methods:
                | test_initialization - Verifies attribute assignment and immutability.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies attribute assignment and immutability.

            :exceptions: None.
        '''
        store: IWaypointStore = MagicMock(spec=IWaypointStore)
        history: IPlanHistorySaver = MagicMock(spec=IPlanHistorySaver)
        navigator: IPlanSelectionNavigator = MagicMock(
            spec=IPlanSelectionNavigator
        )
        dispatcher: IPlanObserverDispatcher = MagicMock(
            spec=IPlanObserverDispatcher
        )

        deps = MutationDependencies(
            waypoint_store=store,
            plan_history_saver=history,
            plan_selection_navigator=navigator,
            plan_observer_dispatcher=dispatcher,
        )

        self.assertIs(deps.waypoint_store, store)
        self.assertIs(deps.plan_history_saver, history)
        self.assertIs(deps.plan_selection_navigator, navigator)
        self.assertIs(deps.plan_observer_dispatcher, dispatcher)

        with self.assertRaises(AttributeError):
            deps.waypoint_store = store  # type: ignore[misc]


if __name__ == '__main__':
    main()
