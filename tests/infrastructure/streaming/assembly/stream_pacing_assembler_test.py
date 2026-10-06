# -*- coding: UTF-8 -*-

'''
Module
    stream_pacing_assembler_test.py
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
    Unit tests for StreamPacingAssembler.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.streaming.assembly.stream_pacing_assembler import StreamPacingAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamPacingAssembler(TestCase):
    '''
        Test cases verifying StreamPacingAssembler behavior.
    '''

    def test_assemble_flow_pacing_bundle(self) -> None:
        '''
            Tests assembly of FlowPacingBundle with specified capacity.
        '''
        bundle: FlowPacingBundle = StreamPacingAssembler.assemble(
            queue_capacity=32
        )
        self.assertIsInstance(bundle, FlowPacingBundle)
        self.assertEqual(bundle.pacing_controller.capacity, 32)
        self.assertTrue(bundle.barrier_coordinator.is_barrier_clear())

    def test_get_version(self) -> None:
        '''
            Tests get_version returns string.
        '''
        self.assertIsInstance(StreamPacingAssembler.get_version(), str)


if __name__ == '__main__':
    main()
