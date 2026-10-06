# -*- coding: UTF-8 -*-

'''
Module
    stream_pacing_assembler.py
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
    Assembles flow barrier and pacing controller into a FlowPacingBundle for streaming.
'''

from __future__ import annotations

from scarajectory.infrastructure.barrier.flow_barrier import FlowBarrier
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPacingAssembler:
    '''
        Sub-assembler for flow barrier and flow pacing controller.

        It defines:

            :methods:
                | assemble - Constructs configured FlowPacingBundle.
                | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble(
        cls,
        *,
        queue_capacity: int = 16,
    ) -> FlowPacingBundle:
        '''
            Constructs and returns configured FlowPacingBundle instance.

            :param queue_capacity: Queue depth limit integer.
            :return: FlowPacingBundle instance.
            :exceptions: None.
        '''
        barrier: FlowBarrier = FlowBarrierFactory.create()

        return FlowPacingBundleFactory.create(
            barrier=barrier,
            capacity=queue_capacity,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
