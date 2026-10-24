# -*- coding: UTF-8 -*-

'''
Module
    istreamer_test.py
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
    Unit testing for IBinaryStreamer protocol specification.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.infrastructure.streaming.binary.istreamer import IBinaryStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamerStub:
    '''Structural test stub satisfying IBinaryStreamer protocol.'''

    def stream_binary_program(self, program: BinaryProgram) -> bool:
        '''Streams binary program.'''
        _ = program
        return True

    def is_streaming(self) -> bool:
        '''Checks streaming status.'''
        return False


class IncompleteBinaryStreamerStub:
    '''Incomplete test stub missing required methods.'''

    def abort(self) -> None:
        '''Aborts stream.'''

    def reset(self) -> None:
        '''Resets stub state.'''


class TestIBinaryStreamer(TestCase):
    '''
    Unit tests validating structural protocol runtime checks for IBinaryStreamer.

    It defines:

        :methods:
            | test_protocol_conformance_success - Verifies compliant class satisfies protocol.
            | test_protocol_conformance_failure - Verifies incomplete class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IBinaryStreamer protocol.'''
        stub = BinaryStreamerStub()
        self.assertIsInstance(stub, IBinaryStreamer)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IBinaryStreamer protocol check.'''
        incomplete = IncompleteBinaryStreamerStub()
        self.assertNotIsInstance(incomplete, IBinaryStreamer)
