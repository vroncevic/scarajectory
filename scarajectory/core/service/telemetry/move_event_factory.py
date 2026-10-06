# -*- coding: UTF-8 -*-

'''
Module
    move_event_factory.py
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
    Factory service constructing MoveEvent models.
'''

from __future__ import annotations

from scarajectory.core.model.telemetry.move_event import MoveEvent

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MoveEventFactory:
    '''
        Factory service constructing MoveEvent models.

        It defines:

            :methods:
                | create - Constructs MoveEvent model with explicit parameters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, event_type: int, segment_id: int) -> MoveEvent:
        '''
            Constructs MoveEvent model instance.

            :param event_type: Event type identifier.
            :param segment_id: Monotonic trajectory segment counter.
            :return: MoveEvent model instance.
        '''
        return MoveEvent(event_type=event_type, segment_id=segment_id)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
