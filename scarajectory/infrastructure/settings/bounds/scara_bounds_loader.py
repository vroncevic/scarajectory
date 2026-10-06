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

from scaralang.core.model.kinematics.joint_angle_bounds import JointAngleBounds
from scaralang.core.model.kinematics.link_dimensions import LinkDimensions
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.singularity_margins import SingularityMargins
from scaralang.core.model.kinematics.speed_limits import SpeedLimits
from scaralang.core.model.kinematics.vertical_bounds import VerticalBounds

from scarajectory.infrastructure.settings.bounds.iscara_bounds_parser import IScaraBoundsParser
from scarajectory.infrastructure.settings.isettings_reader import ISettingsReader

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
                | _reader - Injected ISettingsReader providing configuration key-values.
                | _parser - Injected parser component for bounds options.

            :methods:
                | __init__ - Initializes ScaraBoundsLoader with injected collaborators.
                | load_bounds - Constructs ScaraBounds domain model with default configuration.
                | load_bounds_with_options - Constructs ScaraBounds with custom override options.
                | get_version - Returns adapter version string.
    '''

    _reader: ISettingsReader
    _parser: IScaraBoundsParser

    def __init__(
        self,
        *,
        reader: ISettingsReader,
        parser: IScaraBoundsParser,
    ) -> None:
        '''
            Initializes ScaraBoundsLoader with injected collaborators.

            :param reader: ISettingsReader instance.
            :param parser: Bounds options parser component implementing IScaraBoundsParser.
            :exceptions: None.
        '''
        self._reader: Final[ISettingsReader] = reader
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

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the adapter version string.

            :return: Adapter version string.
            :exceptions: None.
        '''
        return __version__
