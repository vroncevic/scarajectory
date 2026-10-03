# -*- coding: UTF-8 -*-

'''
Module
    imotion_streamer_test.py
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
    Unit testing for IMotionStreamer composite protocol specification.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.streaming.imotion_streamer import IMotionStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionStreamerStub:
    '''Structural test stub satisfying IMotionStreamer composite protocol.'''

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''Starts trajectory streaming.'''
        _ = waypoints
        return True

    def pause_streaming(self) -> None:
        '''Pauses streaming.'''

    def resume_streaming(self) -> None:
        '''Resumes streaming.'''

    def stop_streaming(self) -> None:
        '''Stops streaming.'''

    def stream_binary_program(self, program: BinaryProgram) -> bool:
        '''Streams pre-compiled binary program.'''
        _ = program
        return True


class IncompleteMotionStreamerStub:
    '''Incomplete test stub missing binary streaming capabilities.'''

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''Starts streaming.'''
        _ = waypoints
        return True

    def stop_streaming(self) -> None:
        '''Stops streaming.'''


class MotionStreamerTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IMotionStreamer.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies fully compliant class satisfies composite IMotionStreamer protocol.'''
        stub = MotionStreamerStub()
        self.assertIsInstance(stub, IMotionStreamer)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails composite IMotionStreamer protocol check.'''
        incomplete = IncompleteMotionStreamerStub()
        self.assertNotIsInstance(incomplete, IMotionStreamer)


if __name__ == '__main__':
    main()
