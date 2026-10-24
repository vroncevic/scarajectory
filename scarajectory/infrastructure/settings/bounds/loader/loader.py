# -*- coding: UTF-8 -*-

'''
Module
    loader.py
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

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scarajectory.infrastructure.settings.bounds.parser.iparser import IScaraBoundsParser
from scarajectory.infrastructure.settings.reader.ireader import ISettingsReader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraBoundsLoader:
    '''
        Settings adapter loading and constructing ScaraBounds domain models.

        It defines:

            :attributes:
                | _settings_reader - Injected ISettingsReader providing configuration key-values.
                | _bounds_parser - Injected parser component for bounds options.

            :methods:
                | __init__ - Initializes ScaraBoundsLoader with injected collaborators.
                | load_bounds - Constructs ScaraBounds domain model with default configuration.
                | load_bounds_with_options - Constructs ScaraBounds with custom override options.
    '''

    _settings_reader: ISettingsReader
    _bounds_parser: IScaraBoundsParser

    def __init__(
        self,
        *,
        settings_reader: ISettingsReader,
        bounds_parser: IScaraBoundsParser,
    ) -> None:
        '''
            Initializes ScaraBoundsLoader with injected collaborators.

            :param settings_reader: ISettingsReader instance.
            :param bounds_parser: Bounds options parser component implementing IScaraBoundsParser.
            :exceptions: None.
        '''
        self._settings_reader: Final[ISettingsReader] = settings_reader
        self._bounds_parser: Final[IScaraBoundsParser] = bounds_parser

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
        cfg: dict[str, float] = self._settings_reader.read_settings()
        geom: dict[str, float] = self._bounds_parser.parse_geometry(
            options=options, cfg=cfg
        )
        motion: dict[str, float] = self._bounds_parser.parse_motion(
            options=options, cfg=cfg
        )
        joints: dict[str, float] = self._bounds_parser.parse_joints(
            options=options, cfg=cfg
        )
        sings: dict[str, float] = self._bounds_parser.parse_singularities(
            options=options, cfg=cfg
        )

        return ScaraBounds(
            links=LinkDimensions(l1=geom['l1'], l2=geom['l2']),
            vertical=VerticalBounds(z_min=geom['z_min'], z_max=geom['z_max']),
            speeds=SpeedLimits(
                min_speed=motion['min_speed'],
                max_speed=motion['max_speed'],
                default_speed=motion['default_speed'],
                default_accel=motion['default_accel'],
                max_accel=motion['max_accel'],
            ),
            joints=JointAngleBounds(
                j1_min_rad=joints['j1_min_rad'],
                j1_max_rad=joints['j1_max_rad'],
                j2_min_rad=joints['j2_min_rad'],
                j2_max_rad=joints['j2_max_rad'],
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=sings['singularity_outer_margin_mm'],
                singularity_inner_margin_mm=sings['singularity_inner_margin_mm'],
                singularity_theta2_min_rad=sings['singularity_theta2_min_rad'],
                deadzone_r_min=sings['deadzone_r_min'],
            ),
        )
