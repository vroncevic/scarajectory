# -*- coding: UTF-8 -*-

'''
Module
    iscara_transmission_loader.py
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
    Defines abstract interface for loading robot transmission parameters.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraTransmissionLoader(Protocol):
    '''
        Protocol defining contract for reading SCARA transmission settings.

        It defines:

            :methods:
                | load_transmission - Constructs TransmissionParameters from configuration.
                | load_transmission_with_options - Constructs TransmissionParameters with options.
    '''

    def load_transmission(self) -> TransmissionParameters:
        '''
            Constructs and returns TransmissionParameters domain model from configuration.

            :return: Configured TransmissionParameters domain model.
        '''

    def load_transmission_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> TransmissionParameters:
        '''
            Constructs and returns TransmissionParameters instance with custom override options.

            :param options: Key-value options overriding base configuration.
            :return: Configured TransmissionParameters domain model.
        '''
