# -*- coding: UTF-8 -*-

'''
Module
    scara_transmission_loader.py
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
    Infrastructure adapter for loading TransmissionParameters settings.
'''

from __future__ import annotations

from collections.abc import Mapping

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters

from scarajectory.infrastructure.settings.isettings_reader import ISettingsReader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraTransmissionLoader:
    '''
        Settings adapter loading and constructing TransmissionParameters domain models.

        It defines:

            :attributes:
                | _reader - Injected ISettingsReader providing configuration key-values.

            :methods:
                | __init__ - Initializes ScaraTransmissionLoader with injected ISettingsReader.
                | load_transmission - Constructs TransmissionParameters with default configuration.
                | load_transmission_with_options - Constructs TransmissionParameters with options.
    '''

    _reader: ISettingsReader

    def __init__(self, *, reader: ISettingsReader) -> None:
        '''
            Initializes ScaraTransmissionLoader with injected ISettingsReader.

            :param reader: ISettingsReader instance.
        '''
        self._reader = reader

    def load_transmission(self) -> TransmissionParameters:
        '''
            Constructs and returns TransmissionParameters instance from base configuration.

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
        cfg: dict[str, float] = self._reader.read_settings()

        return TransmissionParameters(
            steps_per_rev=float(options.get('steps_per_rev', cfg.get('steps_per_rev', 200.0))),
            microstepping=float(options.get('microstepping', cfg.get('microstepping', 16.0))),
            gear_ratio_j1=float(options.get('gear_ratio_j1', cfg.get('gear_ratio_j1', 4.0))),
            gear_ratio_j2=float(options.get('gear_ratio_j2', cfg.get('gear_ratio_j2', 4.0))),
            gear_ratio_j4=float(options.get('gear_ratio_j4', cfg.get('gear_ratio_j4', 1.0))),
            leadscrew_pitch_z=float(options.get('leadscrew_pitch_z', cfg.get('leadscrew_pitch_z', 8.0))),
        )
