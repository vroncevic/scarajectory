# -*- coding: UTF-8 -*-

'''
Module
    iscara_bounds_parser.py
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
    Defines abstract interface for parsing SCARA kinematics and boundary options.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraBoundsParser(Protocol):
    '''
        Protocol defining contract for parsing SCARA kinematics configuration options.

        It defines:

            :methods:
                | parse_geometry - Parses link arm lengths and vertical limits.
                | parse_motion - Parses speed and acceleration limit parameters.
                | parse_joints - Parses angular joint limit parameters in radians.
                | parse_singularities - Parses kinematic singularity margin parameters.
    '''

    def parse_geometry(
        self,
        *,
        options: Mapping[str, object],
        cfg: Mapping[str, float],
    ) -> dict[str, float]:
        '''
            Parses link arm lengths and vertical limit parameters.

            :param options: Runtime override options.
            :param cfg: Default configuration mapping.
            :return: Dictionary containing geometry parameter values.
        '''

    def parse_motion(
        self,
        *,
        options: Mapping[str, object],
        cfg: Mapping[str, float],
    ) -> dict[str, float]:
        '''
            Parses speed and acceleration limit parameters.

            :param options: Runtime override options.
            :param cfg: Default configuration mapping.
            :return: Dictionary containing motion parameter values.
        '''

    def parse_joints(
        self,
        *,
        options: Mapping[str, object],
        cfg: Mapping[str, float],
    ) -> dict[str, float]:
        '''
            Parses angular joint limit parameters in radians.

            :param options: Runtime override options.
            :param cfg: Default configuration mapping.
            :return: Dictionary containing joint limit parameter values.
        '''

    def parse_singularities(
        self,
        *,
        options: Mapping[str, object],
        cfg: Mapping[str, float],
    ) -> dict[str, float]:
        '''
            Parses kinematic singularity margin boundary parameters.

            :param options: Runtime override options.
            :param cfg: Default configuration mapping.
            :return: Dictionary containing singularity parameter values.
        '''
