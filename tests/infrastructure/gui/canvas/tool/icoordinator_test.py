# -*- coding: UTF-8 -*-

'''
Module
    icoordinator_test.py
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
    Unit testing for ICanvasToolModeCoordinator protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.canvas.tool.icoordinator import ICanvasToolModeCoordinator
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingCoordinatorStub:
    '''
        Conforming stub implementation satisfying ICanvasToolModeCoordinator.

        It defines:

            :methods:
                | set_tool_mode - Changes tool mode.
                | reset - Resets tool mode.
                | tool_mode - Returns tool mode.
    '''

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Changes tool mode.

            :param mode: CanvasToolMode enum.
            :exceptions: None.
        '''
        del mode

    def reset(self) -> None:
        '''
            Resets tool mode.

            :exceptions: None.
        '''

    @property
    def tool_mode(self) -> CanvasToolMode:
        '''
            Returns tool mode.

            :return: CanvasToolMode enum value.
            :exceptions: None.
        '''
        return CanvasToolMode.POINT


class NonConformingCoordinatorStub:
    '''
        Non-conforming stub missing tool_mode property.

        It defines:

            :methods:
                | set_tool_mode - Changes tool mode.
                | reset - Resets tool mode.
    '''

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Changes tool mode.

            :param mode: CanvasToolMode enum.
            :exceptions: None.
        '''
        del mode

    def reset(self) -> None:
        '''
            Resets tool mode.

            :exceptions: None.
        '''


class TestICanvasToolModeCoordinator(TestCase):
    '''
        Unit tests validating structural protocol runtime checks for ICanvasToolModeCoordinator.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming stub satisfies protocol.
                | test_protocol_conformance_failure - Verifies non-conforming stub fails protocol.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies conforming stub satisfies ICanvasToolModeCoordinator protocol.

            :exceptions: None.
        '''
        stub = ConformingCoordinatorStub()
        self.assertIsInstance(stub, ICanvasToolModeCoordinator)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-conforming stub fails ICanvasToolModeCoordinator protocol check.

            :exceptions: None.
        '''
        incomplete = NonConformingCoordinatorStub()
        self.assertNotIsInstance(incomplete, ICanvasToolModeCoordinator)


if __name__ == '__main__':
    main()
