# -*- coding: UTF-8 -*-

'''
Module
    istream_playback_controller_test.py
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
    Unit testing for IStreamPlaybackController protocol specification.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPlaybackControllerStub:
    '''Structural test stub satisfying IStreamPlaybackController protocol.'''

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


class IncompleteStreamPlaybackControllerStub:
    '''Incomplete test stub missing playback methods.'''

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''Starts streaming.'''
        _ = waypoints
        return True

    def stop_streaming(self) -> None:
        '''Stops streaming.'''


class StreamPlaybackControllerTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IStreamPlaybackController.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamPlaybackController protocol.'''
        stub = StreamPlaybackControllerStub()
        self.assertIsInstance(stub, IStreamPlaybackController)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IStreamPlaybackController protocol check.'''
        incomplete = IncompleteStreamPlaybackControllerStub()
        self.assertNotIsInstance(incomplete, IStreamPlaybackController)


if __name__ == '__main__':
    main()
