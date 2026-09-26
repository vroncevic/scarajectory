# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_builder_factory.py
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
    Factory instantiating and providing IBinaryFrameBuilder component.
'''

from __future__ import annotations

from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder import BinaryFrameBuilder
from scarajectory.core.service.communication.protocol.ibinary_frame_builder import IBinaryFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameBuilderFactory:
    '''
        Factory providing IBinaryFrameBuilder component instantiation.

        It defines:

            :methods:
                | create - Builds and returns a new IBinaryFrameBuilder instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IBinaryFrameBuilder:
        '''
            Builds and returns an IBinaryFrameBuilder instance.

            :return: IBinaryFrameBuilder protocol instance.
            :exceptions: None.
        '''
        return BinaryFrameBuilder()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
