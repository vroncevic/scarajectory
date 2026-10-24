# -*- coding: UTF-8 -*-

'''
Module
    bootstrap.py
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
    Bootstrap byte receiver implementation satisfying IStreamBytesReceiver.
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BootstrapBytesReceiver:
    '''
        Bootstrap byte receiver implementation satisfying IStreamBytesReceiver.

        It defines:

            :methods:
                | handle_incoming_bytes - Discards bytes received prior to worker attachment.
                | is_running - Returns False indicating inactive bootstrap state.
                | get_version - Returns component version string.
    '''

    def handle_incoming_bytes(self, data: bytes) -> None:
        '''
            Discards bytes received prior to worker attachment.

            :param data: Inbound bytes payload.
            :exceptions: None.
        '''
        _ = data

    def is_running(self) -> bool:
        '''
            Returns False indicating inactive bootstrap state.

            :return: False.
            :exceptions: None.
        '''
        return False

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
