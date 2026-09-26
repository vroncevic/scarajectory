# -*- coding: UTF-8 -*-

'''
Module
    config_loader.py
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
    Infrastructure configuration adapter loading SCARA geometry and transmission using ATS Loader.
'''

from __future__ import annotations

from collections.abc import Mapping
from math import cos, sqrt
from os.path import abspath, dirname, exists, join

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.keys import ConfigIOBundleKeys
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.loader.engine import Loader

from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.communication.stream.stream_config import StreamConfig
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraConfigLoader:
    '''
        Configuration adapter reading robot parameters from JSON schema and config files.

        It defines:

            :attributes:
                | _config_path - Absolute path to scara_geometry.json.
                | _scheme_path - Absolute path to scheme.json.
                | _cached_config - Cached raw configuration dictionary.

            :methods:
                | load_raw_config - Loads and caches raw dictionary of settings.
                | load_bounds - Constructs ScaraBounds domain model.
                | load_bounds_with_options - Constructs ScaraBounds with override options.
                | load_transmission - Constructs TransmissionParameters domain model.
                | load_transmission_with_options - Constructs TransmissionParameters with options.
                | load_stream_config - Constructs StreamConfig domain model.
                | load_stream_config_with_options - Constructs StreamConfig with override options.
    '''

    def __init__(self) -> None:
        '''
            Initializes ScaraConfigLoader with configuration file paths.
        '''
        base_dir: str = join(dirname(dirname(abspath(__file__))), 'config')
        self._config_path: str = join(base_dir, 'scara_geometry.json')
        self._scheme_path: str = join(base_dir, 'scheme.json')
        self._cached_config: dict[str, float] = {}

    def load_raw_config(self) -> dict[str, float]:
        '''
            Reads and returns configuration parameters dictionary using ATS Loader.

            :return: Dictionary of configuration keys to float values.
        '''
        if self._cached_config:
            return self._cached_config

        if not exists(self._config_path):
            return {}

        context: ContextBundle = ContextBundleFactory.create_bundle()
        opts: dict[str, object] = {
            ConfigIOBundleKeys.OPTION_FILE_PATH: self._config_path,
            ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: context,
        }

        if exists(self._scheme_path):
            scheme_bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions({
                    ConfigIOBundleKeys.OPTION_FILE_PATH: self._scheme_path,
                    ConfigIOBundleKeys.OPTION_CONTEXT_BUNDLE: context,
                })
            )
            scheme: object = Loader(scheme_bundle).load_configuration()
            if scheme is not None:
                opts[ConfigIOBundleKeys.OPTION_SCHEME] = scheme

        config_bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(opts)
        )
        data: object = Loader(config_bundle).load_configuration()
        if isinstance(data, dict):
            self._cached_config = {
                str(k): float(v)
                for k, v in data.items()
                if isinstance(v, (int, float))
            }

        return self._cached_config

    def load_bounds(self) -> ScaraBounds:
        '''
            Constructs and returns ScaraBounds instance from configuration.

            :return: Configured ScaraBounds domain model.
        '''
        return self.load_bounds_with_options(options={})

    def load_bounds_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> ScaraBounds:
        '''
            Constructs and returns ScaraBounds instance from configuration and options.

            :param options: Key-value options overriding base configuration.
            :return: Configured ScaraBounds domain model.
        '''
        cfg: dict[str, float] = self.load_raw_config()

        l1: float = float(options.get('l1', cfg.get('l1', 150.0)))
        l2: float = float(options.get('l2', cfg.get('l2', 120.0)))
        z_min: float = float(options.get('z_min', cfg.get('z_min', 0.0)))
        z_max: float = float(options.get('z_max', cfg.get('z_max', 100.0)))
        min_spd: float = float(options.get('min_speed', cfg.get('min_speed', 1.0)))
        max_spd: float = float(options.get('max_speed', cfg.get('max_speed', 250.0)))
        def_spd: float = float(options.get('default_speed', cfg.get('default_speed', 50.0)))
        def_acc: float = float(options.get('default_accel', cfg.get('default_accel', 300.0)))
        max_acc: float = float(options.get('max_accel', cfg.get('max_accel', 2000.0)))
        j1_min: float = float(options.get('j1_min_rad', cfg.get('j1_min_rad', -2.617994)))
        j1_max: float = float(options.get('j1_max_rad', cfg.get('j1_max_rad', 2.617994)))
        j2_min: float = float(options.get('j2_min_rad', cfg.get('j2_min_rad', -2.530727)))
        j2_max: float = float(options.get('j2_max_rad', cfg.get('j2_max_rad', 2.530727)))
        s_out: float = float(options.get('singularity_outer_margin_mm', cfg.get('singularity_outer_margin_mm', 3.0)))
        s_in: float = float(options.get('singularity_inner_margin_mm', cfg.get('singularity_inner_margin_mm', 3.0)))
        s_th2: float = float(options.get('singularity_theta2_min_rad', cfg.get('singularity_theta2_min_rad', 0.087266)))

        r_dead_sq: float = l1 * l1 + l2 * l2 + 2.0 * l1 * l2 * cos(j2_max)
        deadzone_r: float = sqrt(max(0.0, r_dead_sq))

        return ScaraBounds(
            l1=l1,
            l2=l2,
            z_min=z_min,
            z_max=z_max,
            min_speed=min_spd,
            max_speed=max_spd,
            default_speed=def_spd,
            default_accel=def_acc,
            max_accel=max_acc,
            j1_min_rad=j1_min,
            j1_max_rad=j1_max,
            j2_min_rad=j2_min,
            j2_max_rad=j2_max,
            singularity_outer_margin_mm=s_out,
            singularity_inner_margin_mm=s_in,
            singularity_theta2_min_rad=s_th2,
            deadzone_r_min=deadzone_r,
        )

    def load_transmission(self) -> TransmissionParameters:
        '''
            Constructs and returns TransmissionParameters instance from configuration.

            :return: Configured TransmissionParameters domain model.
        '''
        return self.load_transmission_with_options(options={})

    def load_transmission_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> TransmissionParameters:
        '''
            Constructs and returns TransmissionParameters instance from configuration and options.

            :param options: Key-value options overriding base configuration.
            :return: Configured TransmissionParameters domain model.
        '''
        cfg: dict[str, float] = self.load_raw_config()

        return TransmissionParameters(
            steps_per_rev=float(options.get('steps_per_rev', cfg.get('steps_per_rev', 200.0))),
            microstepping=float(options.get('microstepping', cfg.get('microstepping', 16.0))),
            gear_ratio_j1=float(options.get('gear_ratio_j1', cfg.get('gear_ratio_j1', 4.0))),
            gear_ratio_j2=float(options.get('gear_ratio_j2', cfg.get('gear_ratio_j2', 4.0))),
            gear_ratio_j4=float(options.get('gear_ratio_j4', cfg.get('gear_ratio_j4', 1.0))),
            leadscrew_pitch_z=float(options.get('leadscrew_pitch_z', cfg.get('leadscrew_pitch_z', 8.0))),
        )

    def load_stream_config(self, *, port: str) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance from configuration for target port.

            :param port: Target serial device port or host string.
            :return: Configured StreamConfig domain model.
        '''
        return self.load_stream_config_with_options(port=port, options={})

    def load_stream_config_with_options(
        self,
        *,
        port: str,
        options: Mapping[str, object],
    ) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance from configuration and options.

            :param port: Target serial device port or host string.
            :param options: Key-value options overriding base configuration.
            :return: Configured StreamConfig domain model.
        '''
        cfg: dict[str, float] = self.load_raw_config()

        baudrate: int = int(options.get('baudrate', cfg.get('baudrate', 115200.0)))
        timeout: float = float(options.get('timeout', cfg.get('timeout', 0.1)))
        queue_capacity: int = int(options.get('queue_capacity', cfg.get('queue_capacity', 16.0)))

        mode_val = options.get('protocol_mode', 'binary')
        mode: ProtocolMode = (
            mode_val
            if isinstance(mode_val, ProtocolMode)
            else ProtocolMode(str(mode_val))
        )
        return StreamConfig(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
            queue_capacity=queue_capacity,
            protocol_mode=mode,
        )
