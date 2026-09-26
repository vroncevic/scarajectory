# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_dispatcher.py
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
    Dispatches parsed binary wire frames to registered handler callbacks.
'''

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from scaralang.core.model.protocol.binary_frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameDispatcher:
    '''
        Dispatches parsed binary wire frames to registered handler callbacks.

        It defines:

            :attributes:
                | _handlers - Internal mapping of message IDs to list of handler callbacks.
            :methods:
                | __init__ - Initializes empty handler registry.
                | register_handler - Registers callback handler for specific message ID.
                | dispatch - Routes binary frame payload to registered handlers.
    '''

    _handlers: dict[int, list[Callable[[Any], None]]]

    def __init__(self) -> None:
        '''
            Initializes empty handler registry.

            :exceptions: None.
        '''
        self._handlers = {}

    def register_handler(self, message_id: int, handler: Callable[[Any], None]) -> None:
        '''
            Registers callback handler for specific message ID.

            :param message_id: Numerical message opcode identifier.
            :param handler: Callable handler accepting payload.
            :exceptions: None.
        '''
        key = int(message_id)

        if key not in self._handlers:
            self._handlers[key] = []

        self._handlers[key].append(handler)

    def dispatch(self, payload: Any) -> bool:
        '''
            Routes binary frame payload to registered handlers.

            :param payload: Parsed binary wire frame or event object.
            :return: True if payload was dispatched, False otherwise.
            :exceptions: None.
        '''
        if isinstance(payload, BinaryFrame):
            key = int(payload.msg_id)

            if key in self._handlers:
                for handler in self._handlers[key]:
                    handler(payload)

                return True

        return False
