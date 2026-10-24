# -*- coding: UTF-8 -*-

'''
Module
    bulk_mutation.py
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
    Concrete implementation of bulk plan waypoint clearing and replacement.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar, Final

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.saver.isaver import IPlanHistorySaver
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


class PlanBulkMutator:
    '''
        Concrete implementation of bulk plan operations coordinating store, history, and selection.

        It defines:

            :constants:
                | EMPTY_COUNT - Threshold count representing an empty waypoint store.
            :attributes:
                | _waypoint_store - Injected IWaypointStore collaborator.
                | _plan_history_saver - Injected IPlanHistorySaver collaborator.
                | _plan_selection_navigator - Injected IPlanSelectionNavigator collaborator.
                | _plan_observer_dispatcher - Injected IPlanObserverDispatcher collaborator.
            :methods:
                | __init__ - Initializes the bulk mutator with injected collaborators.
                | clear - Clears all waypoints from the plan.
                | set_waypoints - Replaces all waypoints with a new sequence.
    '''

    EMPTY_COUNT: ClassVar[int] = 0

    _waypoint_store: IWaypointStore
    _plan_history_saver: IPlanHistorySaver
    _plan_selection_navigator: IPlanSelectionNavigator
    _plan_observer_dispatcher: IPlanObserverDispatcher

    def __init__(
        self,
        waypoint_store: IWaypointStore,
        plan_history_saver: IPlanHistorySaver,
        plan_selection_navigator: IPlanSelectionNavigator,
        plan_observer_dispatcher: IPlanObserverDispatcher,
    ) -> None:
        '''
            Initializes the bulk mutator with injected collaborators.

            :param waypoint_store: Injected IWaypointStore instance.
            :param plan_history_saver: Injected IPlanHistorySaver instance.
            :param plan_selection_navigator: Injected IPlanSelectionNavigator instance.
            :param plan_observer_dispatcher: Injected IPlanObserverDispatcher instance.
            :exceptions: None.
        '''
        self._waypoint_store: Final[IWaypointStore] = waypoint_store
        self._plan_history_saver: Final[IPlanHistorySaver] = plan_history_saver
        self._plan_selection_navigator: Final[IPlanSelectionNavigator] = (
            plan_selection_navigator
        )
        self._plan_observer_dispatcher: Final[IPlanObserverDispatcher] = (
            plan_observer_dispatcher
        )

    def clear(self) -> None:
        '''
            Clears all waypoints from the plan.

            :exceptions: None.
        '''
        if self._waypoint_store.count > self.EMPTY_COUNT:
            self._plan_history_saver.save_state(list(self._waypoint_store.waypoints))
            self._waypoint_store.clear()
            self._plan_selection_navigator.reset()
            self._plan_observer_dispatcher.notify_change()

    def set_waypoints(self, waypoints: Sequence[TrajectoryWaypoint]) -> None:
        '''
            Replaces all waypoints with a new sequence.

            :param waypoints: New sequence of TrajectoryWaypoint instances.
            :exceptions: None.
        '''
        self._plan_history_saver.save_state(list(self._waypoint_store.waypoints))
        self._waypoint_store.replace(list(waypoints))
        self._plan_selection_navigator.select_first_or_none(self._waypoint_store.count)
        self._plan_observer_dispatcher.notify_change()
