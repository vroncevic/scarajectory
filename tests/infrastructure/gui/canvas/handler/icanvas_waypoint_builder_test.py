# -*- coding: UTF-8 -*-

'''
Module
    icanvas_waypoint_builder_test.py
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
    Unit testing for ICanvasWaypointBuilder protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.gui.canvas.handler.icanvas_waypoint_builder import ICanvasWaypointBuilder
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingCanvasWaypointBuilderStub:
    '''Conforming stub implementation satisfying ICanvasWaypointBuilder.'''

    def create_waypoint_at(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> Waypoint:
        '''Creates waypoint at given world coordinates.'''
        _ = (wx, wy, settings)
        return Waypoint(
            x=0.0,
            y=0.0,
            z=0.0,
            phi=0.0,
            speed=10.0,
            name='TEST',
            command='G1',
        )

    def create_relocated_waypoint(
        self,
        current: Waypoint,
        wx: float,
        wy: float,
    ) -> Waypoint:
        '''Creates relocated waypoint with preserved attributes.'''
        _ = (current, wx, wy)
        return Waypoint(
            x=wx,
            y=wy,
            z=0.0,
            phi=0.0,
            speed=10.0,
            name='RELOCATED',
            command='G1',
        )


class NonConformingCanvasWaypointBuilderStub:
    '''Non-conforming stub missing create_relocated_waypoint method.'''

    def create_waypoint_at(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> Waypoint:
        '''Creates waypoint at given world coordinates.'''
        _ = (wx, wy, settings)
        return Waypoint(
            x=0.0,
            y=0.0,
            z=0.0,
            phi=0.0,
            speed=10.0,
            name='TEST',
            command='G1',
        )

    def get_supported_format(self) -> str:
        '''Returns format string.'''
        return 'G1'


class CanvasWaypointBuilderTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for ICanvasWaypointBuilder.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies conforming stub satisfies ICanvasWaypointBuilder protocol.'''
        stub = ConformingCanvasWaypointBuilderStub()
        self.assertIsInstance(stub, ICanvasWaypointBuilder)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-conforming stub fails ICanvasWaypointBuilder protocol check.'''
        incomplete = NonConformingCanvasWaypointBuilderStub()
        self.assertNotIsInstance(incomplete, ICanvasWaypointBuilder)


if __name__ == '__main__':
    main()
