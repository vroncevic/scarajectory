# -*- coding: UTF-8 -*-

'''
Module
    scara_bounds_parser.py
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
    Infrastructure parser component for extracting SCARA kinematic boundary parameters.
'''

from __future__ import annotations

from collections.abc import Mapping
from math import cos, pi

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraBoundsParser:
    '''
        Extracts and converts SCARA bounds dictionary configurations into typed values.

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
            :exceptions: None.
        '''
        return {
            'l1': float(options.get('l1', cfg.get('l1', 150.0))),
            'l2': float(options.get('l2', cfg.get('l2', 120.0))),
            'z_min': float(options.get('z_min', cfg.get('z_min', 0.0))),
            'z_max': float(options.get('z_max', cfg.get('z_max', 100.0))),
        }

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
            :exceptions: None.
        '''
        return {
            'min_speed': float(
                options.get('min_speed', cfg.get('min_speed', 1.0))
            ),
            'max_speed': float(
                options.get('max_speed', cfg.get('max_speed', 250.0))
            ),
            'default_speed': float(
                options.get('default_speed', cfg.get('default_speed', 50.0))
            ),
            'default_accel': float(
                options.get('default_accel', cfg.get('default_accel', 300.0))
            ),
            'max_accel': float(
                options.get('max_accel', cfg.get('max_accel', 2000.0))
            ),
        }

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
            :exceptions: None.
        '''
        return {
            'j1_min_rad': float(
                options.get('j1_min_rad', cfg.get('j1_min_rad', -2.617994))
            ),
            'j1_max_rad': float(
                options.get('j1_max_rad', cfg.get('j1_max_rad', 2.617994))
            ),
            'j2_min_rad': float(
                options.get('j2_min_rad', cfg.get('j2_min_rad', -2.530727))
            ),
            'j2_max_rad': float(
                options.get('j2_max_rad', cfg.get('j2_max_rad', 2.530727))
            ),
        }

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
            :exceptions: None.
        '''
        j2_max: float = float(
            options.get('j2_max_rad', cfg.get('j2_max_rad', 2.530727))
        )
        l1: float = float(options.get('l1', cfg.get('l1', 150.0)))
        l2: float = float(options.get('l2', cfg.get('l2', 120.0)))
        computed_deadzone: float = (
            max(0.0, l1**2 + l2**2 - 2.0 * l1 * l2 * cos(pi - j2_max)) ** 0.5
        )
        return {
            'singularity_outer_margin_mm': float(
                options.get(
                    'singularity_outer_margin_mm',
                    cfg.get('singularity_outer_margin_mm', 3.0),
                )
            ),
            'singularity_inner_margin_mm': float(
                options.get(
                    'singularity_inner_margin_mm',
                    cfg.get('singularity_inner_margin_mm', 3.0),
                )
            ),
            'singularity_theta2_min_rad': float(
                options.get(
                    'singularity_theta2_min_rad',
                    cfg.get('singularity_theta2_min_rad', 0.087266),
                )
            ),
            'deadzone_r_min': float(
                options.get(
                    'deadzone_r_min',
                    cfg.get('deadzone_r_min', computed_deadzone),
                )
            ),
        }
