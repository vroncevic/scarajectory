# -*- coding: UTF-8 -*-

'''
Module
    gui_event_mediator.py
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
    Mediator coordinating waypoint selection and UI event notifications across views.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.itrajectory_observer import ITrajectoryObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiEventMediator:
    '''
        Mediator managing UI selection state and observer notifications across GUI components.

        It defines:

            :attributes:
                | _observers - Registered observer components.
                | _selected_index - Index of currently selected waypoint.
            :methods:
                | __init__ - Initializes mediator with empty observer list and no selection.
                | selected_index - Returns currently selected waypoint index.
                | set_selected_index - Updates selected waypoint index and dispatches notifications.
                | add_observer - Registers an observer for GUI events.
                | remove_observer - Unregisters an observer from GUI events.
                | notify_trajectory_updated - Dispatches trajectory updated event to all observers.
                | notify_point_selected - Dispatches point selected event to all observers.
                | clear_selection - Clears selection and notifies observers.
    '''

    _observers: list[ITrajectoryObserver]
    _selected_index: int

    def __init__(self) -> None:
        '''
            Initializes mediator with empty observer list and no selection.

            :exceptions: None.
        '''
        self._observers = []
        self._selected_index = -1

    @property
    def selected_index(self) -> int:
        '''
            Returns currently selected waypoint index.

            :return: Selected waypoint index or -1.
            :exceptions: None.
        '''
        return self._selected_index

    def set_selected_index(self, index: int, total_count: int = -1) -> None:
        '''
            Updates selected waypoint index and dispatches notifications.

            :param index: Target waypoint index (-1 to deselect).
            :param total_count: Optional upper bound limit check.
            :exceptions: None.
        '''
        if total_count >= 0:
            if -1 <= index < total_count:
                self._selected_index = index
            else:
                self._selected_index = -1
        else:
            self._selected_index = index

        self.notify_point_selected(self._selected_index)

    def add_observer(self, observer: ITrajectoryObserver) -> None:
        '''
            Registers an observer for GUI events.

            :param observer: ITrajectoryObserver instance.
            :exceptions: None.
        '''
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: ITrajectoryObserver) -> None:
        '''
            Unregisters an observer from GUI events.

            :param observer: ITrajectoryObserver instance.
            :exceptions: None.
        '''
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_trajectory_updated(self) -> None:
        '''
            Dispatches trajectory updated event to all observers.

            :exceptions: None.
        '''
        for obs in self._observers:
            obs.on_trajectory_updated()

    def notify_point_selected(self, index: int) -> None:
        '''
            Dispatches point selected event to all observers.

            :param index: Selected waypoint index.
            :exceptions: None.
        '''
        for obs in self._observers:
            obs.on_point_selected(index)

    def clear_selection(self) -> None:
        '''
            Clears selection and notifies observers.

            :exceptions: None.
        '''
        self.set_selected_index(-1)
