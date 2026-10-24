# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory service constructing ControlTransmitter instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.streaming.control.dependencies import ControlDependencies
from scarajectory.infrastructure.streaming.control.provides import ControlProvides
from scarajectory.infrastructure.streaming.control.transmitter import ControlTransmitter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlFactory:
    '''
    Factory providing instantiation of ControlTransmitter components.

    It defines:

        :methods:
            | create - Constructs ControlProvides containing configured transmitter.
            | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ControlDependencies) -> ControlProvides:
        '''
        Constructs and wires ControlTransmitter using provided dependencies.

        :param dependencies: Injected ControlDependencies container.
        :return: ControlProvides containing configured transmitter.
        '''
        transmitter = ControlTransmitter(
            raw_transceiver=dependencies.raw_transceiver,
            system_builder=dependencies.system_builder,
            frame_packer=dependencies.frame_packer,
        )

        return ControlProvides(control_transmitter=transmitter)

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns factory version string.

        :return: Version string.
        '''
        return __version__
