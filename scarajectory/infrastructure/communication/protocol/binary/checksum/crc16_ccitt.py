# -*- coding: UTF-8 -*-

'''
Module
    crc16_ccitt.py
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
    CRC-16-CCITT checksum calculation and verification engine.
'''

from __future__ import annotations

from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Crc16Ccitt:
    '''
        Computes and validates CRC-16-CCITT (poly 0x1021, seed 0xFFFF) checksums.

        It defines:

            :attributes:
                | INITIAL_SEED - Initial CRC accumulator seed (0xFFFF).
                | POLYNOMIAL - Generator polynomial (0x1021).
            :methods:
                | update - Updates running CRC accumulator with a single byte.
                | calculate - Computes 16-bit checksum over a sequence of bytes.
                | verify - Checks whether a byte sequence matches an expected checksum.
    '''

    INITIAL_SEED: ClassVar[int] = 0xFFFF
    POLYNOMIAL: ClassVar[int] = 0x1021

    @classmethod
    def update(cls, crc: int, byte: int) -> int:
        '''
            Updates running 16-bit CRC accumulator with a single input byte.

            :param crc: Current accumulator value.
            :param byte: Input byte value (0 - 255).
            :return: Updated 16-bit accumulator.
        '''
        current: int = (crc ^ ((byte & 0xFF) << 8)) & cls.INITIAL_SEED

        for _ in range(8):
            if current & 0x8000:
                current = ((current << 1) ^ cls.POLYNOMIAL) & cls.INITIAL_SEED
            else:
                current = (current << 1) & cls.INITIAL_SEED

        return current

    @classmethod
    def calculate(cls, data: bytes | bytearray) -> int:
        '''
            Calculates CRC-16-CCITT checksum over a contiguous memory buffer.

            :param data: Input raw byte sequence.
            :return: Calculated 16-bit integer checksum.
        '''
        crc: int = cls.INITIAL_SEED

        for b in data:
            crc = cls.update(crc, b)

        return crc

    @classmethod
    def verify(cls, data: bytes | bytearray, expected_crc: int) -> bool:
        '''
            Verifies that data computes to the given expected CRC-16 checksum.

            :param data: Input raw byte sequence.
            :param expected_crc: Expected 16-bit checksum value.
            :return: True if checksums match, False otherwise.
        '''
        return cls.calculate(data) == (expected_crc & cls.INITIAL_SEED)
