# -*- coding: UTF-8 -*-

'''
Module
    serial_port_scanner.py
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
    Hardware serial port discovery and enumeration utility.
'''

from __future__ import annotations

from sys import platform
from typing import ClassVar

from serial.tools.list_ports import comports

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPortScanner:
    '''
        Hardware serial port scanner discovering available USB/COM communication endpoints.

        It defines:

            :attributes:
                | LINUX_DEFAULT_PORTS - Standard Linux serial device paths.
                | WINDOWS_DEFAULT_PORTS - Standard Windows COM port identifiers.
                | DARWIN_DEFAULT_PORTS - Standard macOS USB serial device paths.
            :methods:
                | scan_ports - Enumerates and returns list of detected serial port identifiers.
                | get_default_ports_for_os - Returns fallback port identifiers based on operating system.
    '''

    LINUX_DEFAULT_PORTS: ClassVar[list[str]] = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyUSB0', '/dev/ttyUSB1']
    WINDOWS_DEFAULT_PORTS: ClassVar[list[str]] = ['COM1', 'COM2', 'COM3', 'COM4']
    DARWIN_DEFAULT_PORTS: ClassVar[list[str]] = ['/dev/tty.usbmodem1', '/dev/tty.usbserial1']

    @classmethod
    def get_default_ports_for_os(cls, os_name: str | None = None) -> list[str]:
        '''
            Returns fallback port identifiers based on target operating system.

            :param os_name: Optional OS platform identifier (defaults to sys.platform).
            :return: List of default port paths or names.
            :exceptions: None.
        '''
        target_os: str = (os_name or platform).lower()

        if 'win' in target_os:
            return list(cls.WINDOWS_DEFAULT_PORTS)

        if 'darwin' in target_os:
            return list(cls.DARWIN_DEFAULT_PORTS)

        return list(cls.LINUX_DEFAULT_PORTS)

    @classmethod
    def scan_ports(cls) -> list[str]:
        '''
            Enumerates and returns list of detected serial port identifiers.

            :return: List of port device path strings.
            :exceptions: None.
        '''
        detected: list[str] = []

        try:
            ports = comports()

            for port in ports:
                if port.device.startswith('/dev/ttyS') and (not port.description or port.description == 'n/a'):
                    continue
                desc: str = f'{port.device} - {port.description}' if port.description else port.device
                detected.append(desc)

        except (OSError, AttributeError):
            pass

        return detected if detected else cls.get_default_ports_for_os()
