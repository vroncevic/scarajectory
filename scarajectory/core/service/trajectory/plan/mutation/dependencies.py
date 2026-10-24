# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Parameter bundle encapsulating inbound foreign dependencies for mutation subsystem.
'''

from __future__ import annotations

from dataclasses import dataclass

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


@dataclass(frozen=True, slots=True)
class MutationDependencies:
    '''
        Parameter bundle encapsulating collaborators required by mutation subsystem.

        It defines:

            :attributes:
                | waypoint_store - Injected IWaypointStore collaborator.
                | plan_history_saver - Injected IPlanHistorySaver collaborator.
                | plan_selection_navigator - Injected IPlanSelectionNavigator collaborator.
                | plan_observer_dispatcher - Injected IPlanObserverDispatcher collaborator.
    '''

    waypoint_store: IWaypointStore
    plan_history_saver: IPlanHistorySaver
    plan_selection_navigator: IPlanSelectionNavigator
    plan_observer_dispatcher: IPlanObserverDispatcher
