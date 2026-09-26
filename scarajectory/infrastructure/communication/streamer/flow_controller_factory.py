# -*- coding: UTF-8 -*-

'''
Module
    flow_controller_factory.py
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
    Factory service constructing FlowController instances with injected protocol parser.
'''

from __future__ import annotations

from scarajectory.core.service.communication.protocol.iprotocol_parser import IProtocolParser
from scarajectory.infrastructure.communication.protocol.ascii.parser.protocol_parser_factory import ProtocolParserFactory
from scarajectory.infrastructure.communication.streamer.flow_controller import FlowController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowControllerFactory:
    '''
        Factory providing creation of FlowController instances.

        It defines:

            :methods:
                | create - Constructs FlowController with configured capacity.
                | create_with_parser - Constructs FlowController with injected protocol parser.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        capacity: int = FlowController.DEFAULT_QUEUE_CAPACITY,
    ) -> FlowController:
        '''
            Constructs and returns a configured FlowController instance.

            :param capacity: Microcontroller ring buffer capacity (default 16).
            :return: FlowController instance.
        '''
        return FlowController(capacity=capacity, parser=ProtocolParserFactory.create())

    @classmethod
    def create_with_parser(
        cls,
        *,
        parser: IProtocolParser,
        capacity: int = FlowController.DEFAULT_QUEUE_CAPACITY,
    ) -> FlowController:
        '''
            Constructs FlowController with injected protocol parser.

            :param parser: IProtocolParser instance.
            :param capacity: Microcontroller ring buffer capacity (default 16).
            :return: FlowController instance.
        '''
        return FlowController(capacity=capacity, parser=parser)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__

