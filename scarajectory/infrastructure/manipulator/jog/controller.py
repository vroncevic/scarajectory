# -*- coding: UTF-8 -*-

'''
Module
    controller.py
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
    Dedicated controller adapter for manual robot axis jogging and feedrate override.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogController:
    '''
        Dedicated controller adapter for manual axis jogging and feedrate override.

        It defines:

            :attributes:
                | _dispatcher - Injected IChannelDispatcher communication adapter.
                | _system_builder - Injected IBinarySystemFrameBuilder frame encoder.
            :methods:
                | __init__ - Initializes JogController with dispatcher and builder.
                | is_connected - Checks if communication transport is active.
                | jog - Jogs specific robot axis by relative displacement.
                | set_feedrate_override - Sets execution speed override percentage.
    '''

    _dispatcher: IChannelDispatcher
    _system_builder: IBinarySystemFrameBuilder

    def __init__(
        self,
        *,
        dispatcher: IChannelDispatcher,
        system_builder: IBinarySystemFrameBuilder,
    ) -> None:
        '''
            Initializes JogController with dispatcher and system frame builder.

            :param dispatcher: IChannelDispatcher transport and sequence manager.
            :param system_builder: IBinarySystemFrameBuilder builder instance.
        '''
        self._dispatcher: Final[IChannelDispatcher] = dispatcher
        self._system_builder: Final[IBinarySystemFrameBuilder] = system_builder

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently active.

            :return: True if connected, False otherwise.
        '''
        return self._dispatcher.is_connected()

    def jog(self, axis: str, step: float) -> bool:
        '''
            Jogs specific robot axis by relative displacement.

            :param axis: Axis identifier string ('X', 'Y', 'Z', 'Phi', etc.).
            :param step: Relative displacement step value.
            :return: True if command transmitted successfully, False otherwise.
        '''
        joint_map: dict[str, int] = {
            'X': 0, 'J1': 0,
            'Y': 1, 'J2': 1,
            'Z': 2,
            'PHI': 3, 'J4': 3,
        }
        joint_id: int = joint_map.get(axis.upper(), 0)
        frame: BinaryFrame = self._system_builder.build_jog_frame(
            seq_num=self._dispatcher.next_seq(),
            joint_id=joint_id,
            step=int(step),
        )

        return self._dispatcher.send_frame(frame)

    def set_feedrate_override(self, pct: int) -> bool:
        '''
            Sets execution speed override percentage.

            :param pct: Speed override percentage between 10 and 200.
            :return: True if command transmitted successfully, False otherwise.
        '''
        frame: BinaryFrame = self._system_builder.build_override_frame(
            seq_num=self._dispatcher.next_seq(),
            pct=pct,
        )

        return self._dispatcher.send_frame(frame)
