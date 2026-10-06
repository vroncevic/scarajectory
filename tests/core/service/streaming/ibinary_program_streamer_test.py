# -*- coding: UTF-8 -*-

'''
Module
    ibinary_program_streamer_test.py
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
    Unit testing for IBinaryProgramStreamer protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.infrastructure.streaming.ibinary_program_streamer import IBinaryProgramStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryProgramStreamerStub:
    '''Structural test stub satisfying IBinaryProgramStreamer protocol.'''

    def stream_binary_program(self, program: BinaryProgram) -> bool:
        '''Streams binary program.'''
        _ = program
        return True

    def is_busy(self) -> bool:
        '''Checks streaming status.'''
        return False


class IncompleteBinaryProgramStreamerStub:
    '''Incomplete test stub missing required stream_binary_program method.'''

    def abort(self) -> None:
        '''Aborts stream.'''

    def is_busy(self) -> bool:
        '''Checks streaming status.'''
        return False


class BinaryProgramStreamerTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IBinaryProgramStreamer.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IBinaryProgramStreamer protocol.'''
        stub = BinaryProgramStreamerStub()
        self.assertIsInstance(stub, IBinaryProgramStreamer)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IBinaryProgramStreamer protocol check.'''
        incomplete = IncompleteBinaryProgramStreamerStub()
        self.assertNotIsInstance(incomplete, IBinaryProgramStreamer)


if __name__ == '__main__':
    main()
