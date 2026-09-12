# -*- coding: UTF-8 -*-

'''
Module
    gui_event_mediator_test.py
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
    Unit tests for GuiEventMediator component.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.infrastructure.gui.gui_event_mediator import GuiEventMediator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockTrajectoryObserver:
    '''
        Mock observer recording event dispatches.

        It defines:

            :attributes:
                | updated_count - Number of trajectory update events.
                | selected_indices - History of selected indices dispatched.
            :methods:
                | __init__ - Initializes recording counters.
                | on_trajectory_updated - Records trajectory update.
                | on_point_selected - Records selected point index.
    '''

    updated_count: int
    selected_indices: list[int]

    def __init__(self) -> None:
        '''
            Initializes recording counters.
        '''
        self.updated_count = 0
        self.selected_indices = []

    def on_trajectory_updated(self) -> None:
        '''
            Records trajectory update.
        '''
        self.updated_count += 1

    def on_point_selected(self, index: int) -> None:
        '''
            Records selected point index.

            :param index: Selected index.
        '''
        self.selected_indices.append(index)


class TestGuiEventMediator(TestCase):
    '''
        Test cases for GuiEventMediator observer coordination.

        It defines:

            :methods:
                | setUp - Initializes mediator and mock observer.
                | test_initial_state - Tests default selection and state.
                | test_add_remove_observer - Tests observer registration lifecycle.
                | test_selection_dispatch - Tests selecting index and event dispatch.
                | test_selection_bounded - Tests selection clamping with total count.
                | test_trajectory_updated_dispatch - Tests trajectory update broadcasting.
                | test_clear_selection - Tests clearing selection state.
    '''

    def setUp(self) -> None:
        '''
            Initializes mediator and mock observer.

            :exceptions: None.
        '''
        self.mediator = GuiEventMediator()
        self.observer = MockTrajectoryObserver()

    def test_initial_state(self) -> None:
        '''
            Tests default selection and state.

            :exceptions: None.
        '''
        self.assertEqual(self.mediator.selected_index, -1)

    def test_add_remove_observer(self) -> None:
        '''
            Tests observer registration lifecycle.

            :exceptions: None.
        '''
        self.mediator.add_observer(self.observer)
        self.mediator.notify_trajectory_updated()
        self.assertEqual(self.observer.updated_count, 1)

        self.mediator.remove_observer(self.observer)
        self.mediator.notify_trajectory_updated()
        self.assertEqual(self.observer.updated_count, 1)

    def test_selection_dispatch(self) -> None:
        '''
            Tests selecting index and event dispatch.

            :exceptions: None.
        '''
        self.mediator.add_observer(self.observer)
        self.mediator.set_selected_index(2)

        self.assertEqual(self.mediator.selected_index, 2)
        self.assertEqual(self.observer.selected_indices, [2])

    def test_selection_bounded(self) -> None:
        '''
            Tests selection clamping with total count.

            :exceptions: None.
        '''
        self.mediator.add_observer(self.observer)

        self.mediator.set_selected_index(3, total_count=5)
        self.assertEqual(self.mediator.selected_index, 3)

        self.mediator.set_selected_index(10, total_count=5)
        self.assertEqual(self.mediator.selected_index, -1)

    def test_trajectory_updated_dispatch(self) -> None:
        '''
            Tests trajectory update broadcasting.

            :exceptions: None.
        '''
        obs2 = MockTrajectoryObserver()
        self.mediator.add_observer(self.observer)
        self.mediator.add_observer(obs2)

        self.mediator.notify_trajectory_updated()
        self.assertEqual(self.observer.updated_count, 1)
        self.assertEqual(obs2.updated_count, 1)

    def test_clear_selection(self) -> None:
        '''
            Tests clearing selection state.

            :exceptions: None.
        '''
        self.mediator.add_observer(self.observer)
        self.mediator.set_selected_index(1)
        self.assertEqual(self.mediator.selected_index, 1)

        self.mediator.clear_selection()
        self.assertEqual(self.mediator.selected_index, -1)
        self.assertEqual(self.observer.selected_indices, [1, -1])


if __name__ == '__main__':
    main()
