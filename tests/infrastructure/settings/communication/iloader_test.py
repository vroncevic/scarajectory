# -*- coding: UTF-8 -*-

'''
Module
    iloader_test.py
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
    Unit testing for ICommunicationSettingsLoader protocol conformance.
'''

from __future__ import annotations

from collections.abc import Mapping
from unittest import TestCase, main

from scarajectory.core.model.streaming.config import StreamConfig
from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.infrastructure.settings.communication.iloader import ICommunicationSettingsLoader


class ConformingCommunicationLoaderStub:
    '''Conforming stub implementation satisfying ICommunicationSettingsLoader protocol.'''

    def read_settings(self) -> dict[str, object]:
        '''Reads settings dictionary.'''
        return {'port': '/dev/ttyUSB0'}

    def load_stream_config(self) -> StreamConfig:
        '''Loads stream config.'''
        return StreamConfig(port='/dev/ttyUSB0', baudrate=115200, timeout=0.1, queue_capacity=16)

    def load_stream_config_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> StreamConfig:
        '''Loads stream config with custom options.'''
        _ = options
        return self.load_stream_config()

    def load_pacing_config(self) -> StreamPacingConfig:
        '''Loads pacing config.'''
        return StreamPacingConfig(send_delay=0.005, throttle_delay=0.01, poll_delay=0.02)

    def load_pacing_config_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> StreamPacingConfig:
        '''Loads pacing config with custom options.'''
        _ = options
        return self.load_pacing_config()


class IncompleteCommunicationLoaderStub:
    '''Non-conforming stub implementation missing pacing methods.'''

    def read_settings(self) -> dict[str, object]:
        '''Reads settings dictionary.'''
        return {}

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class CommunicationLoaderProtocolTestCase(TestCase):
    '''
        Tests ICommunicationSettingsLoader runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies ICommunicationSettingsLoader protocol.

            :exceptions: None.
        '''
        stub = ConformingCommunicationLoaderStub()
        self.assertIsInstance(stub, ICommunicationSettingsLoader)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-compliant class fails ICommunicationSettingsLoader protocol check.

            :exceptions: None.
        '''
        stub = IncompleteCommunicationLoaderStub()
        self.assertNotIsInstance(stub, ICommunicationSettingsLoader)


if __name__ == '__main__':
    main()
