# -*- coding: UTF-8 -*-

'''
Module
    scara_bounds_loader.py
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
    Infrastructure adapter for loading ScaraBounds workspace settings.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.service.kinematics.iscara_deadzone_calculator import IScaraDeadzoneCalculator
from scarajectory.core.service.settings.iscara_bounds_parser import IScaraBoundsParser
from scarajectory.infrastructure.settings.isettings_reader import ISettingsReader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraBoundsLoader:
    '''
        Settings adapter loading and constructing ScaraBounds domain models.

        It defines:

            :attributes:
                | _reader - Injected ISettingsReader providing configuration key-values.
                | _deadzone_calculator - Injected domain calculator for kinematic deadzones.
                | _parser - Injected parser component for bounds options.

            :methods:
                | __init__ - Initializes ScaraBoundsLoader with injected collaborators.
                | load_bounds - Constructs ScaraBounds domain model with default configuration.
                | load_bounds_with_options - Constructs ScaraBounds with custom override options.
                | get_version - Returns adapter version string.
    '''

    _reader: ISettingsReader
    _deadzone_calculator: IScaraDeadzoneCalculator
    _parser: IScaraBoundsParser

    def __init__(
        self,
        *,
        reader: ISettingsReader,
        deadzone_calculator: IScaraDeadzoneCalculator,
        parser: IScaraBoundsParser,
    ) -> None:
        '''
            Initializes ScaraBoundsLoader with injected collaborators.

            :param reader: ISettingsReader instance.
            :param deadzone_calculator: Domain kinematic deadzone calculator instance.
            :param parser: Bounds options parser component implementing IScaraBoundsParser.
            :exceptions: None.
        '''
        self._reader: Final[ISettingsReader] = reader
        self._deadzone_calculator: Final[IScaraDeadzoneCalculator] = (
            deadzone_calculator
        )
        self._parser: Final[IScaraBoundsParser] = parser

    def load_bounds(self) -> ScaraBounds:
        '''
            Constructs and returns ScaraBounds instance from base configuration.

            :return: Configured ScaraBounds domain model.
            :exceptions: None.
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
            :exceptions: None.
        '''
        cfg: dict[str, float] = self._reader.read_settings()
        geom: dict[str, float] = self._parser.parse_geometry(
            options=options, cfg=cfg
        )
        motion: dict[str, float] = self._parser.parse_motion(
            options=options, cfg=cfg
        )
        joints: dict[str, float] = self._parser.parse_joints(
            options=options, cfg=cfg
        )
        sings: dict[str, float] = self._parser.parse_singularities(
            options=options, cfg=cfg
        )
        deadzone_r: float = self._deadzone_calculator.calculate_deadzone_radius(
            geom['l1'], geom['l2'], joints['j2_max_rad']
        )

        return ScaraBounds(
            l1=geom['l1'],
            l2=geom['l2'],
            z_min=geom['z_min'],
            z_max=geom['z_max'],
            min_speed=motion['min_speed'],
            max_speed=motion['max_speed'],
            default_speed=motion['default_speed'],
            default_accel=motion['default_accel'],
            max_accel=motion['max_accel'],
            j1_min_rad=joints['j1_min_rad'],
            j1_max_rad=joints['j1_max_rad'],
            j2_min_rad=joints['j2_min_rad'],
            j2_max_rad=joints['j2_max_rad'],
            singularity_outer_margin_mm=sings['singularity_outer_margin_mm'],
            singularity_inner_margin_mm=sings['singularity_inner_margin_mm'],
            singularity_theta2_min_rad=sings['singularity_theta2_min_rad'],
            deadzone_r_min=deadzone_r,
        )

    def get_version(self) -> str:
        '''
            Returns the adapter version string.

            :return: Adapter version string.
            :exceptions: None.
        '''
        return __version__
