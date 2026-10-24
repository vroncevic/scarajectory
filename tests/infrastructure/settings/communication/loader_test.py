# -*- coding: UTF-8 -*-

'''
Module
    loader_test.py
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
    Unit tests for CommunicationSettingsLoader.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.streaming.config import StreamConfig
from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.config_factory import ConfigFactory
from scarajectory.core.service.streaming.pacing_config_factory import StreamPacingConfigFactory
from scarajectory.infrastructure.settings.communication.loader import CommunicationSettingsLoader
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommunicationSettingsLoaderTestCase(TestCase):
    '''
        Test cases verifying CommunicationSettingsLoader operations.

        It defines:

            :methods:
                | test_read_settings_cached - Verifies caching of loaded settings.
                | test_read_settings_nonexistent - Verifies empty dict when file does not exist.
                | test_load_stream_config_default_and_override - Verifies StreamConfig loading and override.
                | test_load_stream_config_with_options - Verifies options override StreamConfig.
                | test_load_pacing_config_default_and_override - Verifies StreamPacingConfig loading.
                | test_load_pacing_config_with_options - Verifies options override StreamPacingConfig.
    '''

    def test_read_settings_cached(self) -> None:
        '''
            Verifies reading settings caches results from config loader.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IConfigLoader)
        payload = {'port': '/dev/ttyUSB1', 'baudrate': 250000}
        mock_loader.load_validated.return_value = payload

        loader = CommunicationSettingsLoader(
            config_path=CommunicationSettingsLoader.DEFAULT_COMMUNICATION_CONFIG,
            scheme_path=CommunicationSettingsLoader.DEFAULT_SCHEME_CONFIG,
            config_loader=mock_loader,
        )

        res1 = loader.read_settings()
        res2 = loader.read_settings()
        self.assertEqual(res1, payload)
        self.assertEqual(res2, payload)
        self.assertEqual(mock_loader.load_validated.call_count, 1)

    def test_read_settings_nonexistent(self) -> None:
        '''
            Verifies reading settings returns empty dict when configuration file is absent.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IConfigLoader)
        loader = CommunicationSettingsLoader(
            config_path='/nonexistent/communication.json',
            scheme_path='/nonexistent/communication_scheme.json',
            config_loader=mock_loader,
        )
        res = loader.read_settings()
        self.assertEqual(res, {})
        mock_loader.load_validated.assert_not_called()

    def test_load_stream_config_default_and_override(self) -> None:
        '''
            Verifies load_stream_config falls back to factory defaults or applies config overrides.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IConfigLoader)
        loader_missing = CommunicationSettingsLoader(
            config_path='/nonexistent/communication.json',
            scheme_path='/nonexistent/communication_scheme.json',
            config_loader=mock_loader,
        )
        default_cfg: StreamConfig = loader_missing.load_stream_config()
        expected_default: StreamConfig = ConfigFactory.create_default()
        self.assertEqual(default_cfg, expected_default)

        mock_loader.load_validated.return_value = {
            'port': '/dev/ttyACM5',
            'baudrate': 57600,
            'timeout': 0.2,
            'queue_capacity': 32,
        }
        loader_present = CommunicationSettingsLoader(
            config_path=CommunicationSettingsLoader.DEFAULT_COMMUNICATION_CONFIG,
            scheme_path=CommunicationSettingsLoader.DEFAULT_SCHEME_CONFIG,
            config_loader=mock_loader,
        )
        custom_cfg: StreamConfig = loader_present.load_stream_config()
        self.assertEqual(custom_cfg.port, '/dev/ttyACM5')
        self.assertEqual(custom_cfg.baudrate, 57600)
        self.assertEqual(custom_cfg.timeout, 0.2)
        self.assertEqual(custom_cfg.queue_capacity, 32)

    def test_load_stream_config_with_options(self) -> None:
        '''
            Verifies load_stream_config_with_options overrides base config with runtime options.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IConfigLoader)
        mock_loader.load_validated.return_value = {
            'port': '/dev/ttyACM0',
            'baudrate': 115200,
        }
        loader = CommunicationSettingsLoader(
            config_path=CommunicationSettingsLoader.DEFAULT_COMMUNICATION_CONFIG,
            scheme_path=CommunicationSettingsLoader.DEFAULT_SCHEME_CONFIG,
            config_loader=mock_loader,
        )
        cfg: StreamConfig = loader.load_stream_config_with_options(
            options={'port': '/dev/ttyUSB9', 'baudrate': 9600}
        )
        self.assertEqual(cfg.port, '/dev/ttyUSB9')
        self.assertEqual(cfg.baudrate, 9600)

    def test_load_pacing_config_default_and_override(self) -> None:
        '''
            Verifies load_pacing_config falls back to binary defaults or applies config overrides.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IConfigLoader)
        loader_missing = CommunicationSettingsLoader(
            config_path='/nonexistent/communication.json',
            scheme_path='/nonexistent/communication_scheme.json',
            config_loader=mock_loader,
        )
        default_pacing: StreamPacingConfig = loader_missing.load_pacing_config()
        expected_default: StreamPacingConfig = StreamPacingConfigFactory.create_binary()
        self.assertEqual(default_pacing, expected_default)

        mock_loader.load_validated.return_value = {
            'send_delay': 0.001,
            'throttle_delay': 0.002,
            'poll_delay': 0.004,
        }
        loader_present = CommunicationSettingsLoader(
            config_path=CommunicationSettingsLoader.DEFAULT_COMMUNICATION_CONFIG,
            scheme_path=CommunicationSettingsLoader.DEFAULT_SCHEME_CONFIG,
            config_loader=mock_loader,
        )
        custom_pacing: StreamPacingConfig = loader_present.load_pacing_config()
        self.assertEqual(custom_pacing.send_delay, 0.001)
        self.assertEqual(custom_pacing.throttle_delay, 0.002)
        self.assertEqual(custom_pacing.poll_delay, 0.004)

    def test_load_pacing_config_with_options(self) -> None:
        '''
            Verifies load_pacing_config_with_options overrides base config with runtime options.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IConfigLoader)
        mock_loader.load_validated.return_value = {'send_delay': 0.005}
        loader = CommunicationSettingsLoader(
            config_path=CommunicationSettingsLoader.DEFAULT_COMMUNICATION_CONFIG,
            scheme_path=CommunicationSettingsLoader.DEFAULT_SCHEME_CONFIG,
            config_loader=mock_loader,
        )
        pacing: StreamPacingConfig = loader.load_pacing_config_with_options(
            options={'send_delay': 0.015, 'poll_delay': 0.05}
        )
        self.assertEqual(pacing.send_delay, 0.015)
        self.assertEqual(pacing.poll_delay, 0.05)


if __name__ == '__main__':
    main()
