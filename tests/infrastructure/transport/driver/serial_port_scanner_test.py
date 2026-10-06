# -*- coding: UTF-8 -*-

'''
Module
    serial_port_scanner_test.py
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
    Unit testing for SerialPortScanner utility component.
'''

from __future__ import annotations

from types import SimpleNamespace
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.transport.driver.serial_port_scanner import SerialPortScanner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPortScannerTestCase(TestCase):
    '''Unit tests validating SerialPortScanner platform detection and hardware scan.'''

    def test_default_ports_by_os(self) -> None:
        '''Verifies default port fallbacks across supported operating systems.'''
        self.assertEqual(
            SerialPortScanner.get_default_ports_for_os('linux'),
            SerialPortScanner.LINUX_DEFAULT_PORTS,
        )
        self.assertEqual(
            SerialPortScanner.get_default_ports_for_os('windows'),
            SerialPortScanner.WINDOWS_DEFAULT_PORTS,
        )
        self.assertEqual(
            SerialPortScanner.get_default_ports_for_os('darwin'),
            SerialPortScanner.DARWIN_DEFAULT_PORTS,
        )
        self.assertEqual(
            SerialPortScanner.get_default_ports_for_os('freebsd'),
            SerialPortScanner.LINUX_DEFAULT_PORTS,
        )

    @patch('scarajectory.infrastructure.transport.driver.serial_port_scanner.comports')
    def test_scan_ports_with_detected_hardware(self, mock_comports: MagicMock) -> None:
        '''Verifies filtering of dummy ttyS ports and formatting of active device descriptions.'''
        port_usb = SimpleNamespace(device='/dev/ttyUSB0', description='FTDI USB Serial')
        port_acm = SimpleNamespace(device='/dev/ttyACM0', description='')
        port_dummy = SimpleNamespace(device='/dev/ttyS0', description='n/a')

        mock_comports.return_value = [port_usb, port_acm, port_dummy]

        detected: list[str] = SerialPortScanner.scan_ports()
        self.assertIn('/dev/ttyUSB0 - FTDI USB Serial', detected)
        self.assertIn('/dev/ttyACM0', detected)
        self.assertNotIn('/dev/ttyS0', detected)

    @patch('scarajectory.infrastructure.transport.driver.serial_port_scanner.comports')
    def test_scan_ports_exception_and_empty_fallbacks(
        self, mock_comports: MagicMock
    ) -> None:
        '''Verifies fallback to OS default ports on OSError or empty scan.'''
        mock_comports.side_effect = OSError('Hardware enum failed')
        detected_err: list[str] = SerialPortScanner.scan_ports()
        self.assertTrue(len(detected_err) > 0)

        mock_comports.side_effect = None
        mock_comports.return_value = []
        detected_empty: list[str] = SerialPortScanner.scan_ports()
        self.assertTrue(len(detected_empty) > 0)


if __name__ == '__main__':
    main()
