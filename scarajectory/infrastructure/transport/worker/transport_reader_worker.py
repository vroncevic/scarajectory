# -*- coding: UTF-8 -*-

'''
Module
    transport_reader_worker.py
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
    Dedicated background reader loop worker for hardware communication transports.
'''

from __future__ import annotations

from threading import Event
from time import sleep

from scarajectory.infrastructure.transport.driver.ichannel import IChannelDriver
from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransportReaderWorker:
    '''
        Dedicated background worker handling byte streaming and newline packet assembly.

        It defines:

            :attributes:
                | _stop_event - Event signaling reader loop termination.
                | _driver - Low-level I/O channel driver.
                | _listener - Inbound transport event listener.

            :methods:
                | __init__ - Initializes TransportReaderWorker instance with driver and listener.
                | is_running - Checks if reader loop termination event is not set.
                | run - Executes background read loop until stopped or disconnect detected.
    '''

    _stop_event: Event
    _driver: IChannelDriver
    _listener: ITransportListener

    def __init__(
        self,
        stop_event: Event,
        driver: IChannelDriver,
        listener: ITransportListener,
    ) -> None:
        '''
            Initializes TransportReaderWorker with synchronization event, driver, and listener.

            :param stop_event: Event signaling termination request.
            :param driver: Injected IChannelDriver instance.
            :param listener: Injected ITransportListener instance.
        '''
        self._stop_event = stop_event
        self._driver = driver
        self._listener = listener

    def is_running(self) -> bool:
        '''
            Checks if reader loop termination event is not set.

            :return: True if running, False otherwise.
        '''
        return not self._stop_event.is_set()

    def run(self) -> None:
        '''
            Executes background polling loop assembling incoming lines and forwarding byte chunks.
        '''
        buffer: str = ''
        abnormal_disconnect: bool = False

        while not self._stop_event.is_set():
            if not self._driver.is_open():
                break

            try:
                data: bytes = self._driver.read_bytes(64)
                if not data:
                    sleep(0.01)
                    continue

                try:
                    self._listener.on_bytes_received(data)
                except Exception as b_exc:
                    self._listener.on_log_emitted(
                        f'[ERR]: Byte callback error: {b_exc}', False
                    )

                buffer += data.decode('utf-8', errors='ignore')

                while '\n' in buffer:
                    line: str
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()

                    if line:
                        try:
                            self._listener.on_line_received(line)
                        except Exception as cb_exc:
                            self._listener.on_log_emitted(
                                f'[ERR]: Packet callback error: {cb_exc}', False
                            )
            except Exception:
                if not self._stop_event.is_set():
                    abnormal_disconnect = True
                break

        if abnormal_disconnect:
            self._driver.close_channel()
            self._listener.on_log_emitted(
                '[HOST]: Connection lost (device disconnected / unplugged)', False
            )
