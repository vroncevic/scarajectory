# -*- coding: UTF-8 -*-

'''
Module
    config_command_formatter_test.py
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
    Unit testing for ConfigCommandFormatter component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.infrastructure.formatter.command.config_command_formatter import ConfigCommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigCommandFormatterTestCase(TestCase):
    '''Unit tests for ConfigCommandFormatter formatting routines.'''

    def test_format_get_config(self) -> None:
        '''Verifies format_get_config outputs expected query packet.'''
        cmd: str = ConfigCommandFormatter.format_get_config()
        self.assertEqual(cmd, '<CMD:GET_CONFIG>')

    def test_format_save_config(self) -> None:
        '''Verifies format_save_config outputs expected save packet.'''
        cmd: str = ConfigCommandFormatter.format_save_config()
        self.assertEqual(cmd, '<CMD:SAVE_CONFIG>')

    def test_format_set_config(self) -> None:
        '''Verifies format_set_config renders bounds attributes accurately.'''
        bounds = ScaraBounds(
            l1=225.0,
            l2=175.0,
            z_min=0.0,
            z_max=150.0,
            min_speed=5.0,
            max_speed=250.0,
            default_speed=50.0,
            default_accel=100.0,
            max_accel=500.0,
            j1_min_rad=-1.57,
            j1_max_rad=1.57,
            j2_min_rad=-2.61,
            j2_max_rad=2.61,
            singularity_outer_margin_mm=10.0,
            singularity_inner_margin_mm=5.0,
            singularity_theta2_min_rad=0.05,
            deadzone_r_min=50.0,
        )
        cmd: str = ConfigCommandFormatter.format_set_config(bounds)
        expected: str = (
            '<CMD:SET_CONFIG#L1=225.00#L2=175.00#Z_MIN=0.00#Z_MAX=150.00#MIN_SPEED=5.0#MAX_SPEED=250.0>'
        )
        self.assertEqual(cmd, expected)


if __name__ == '__main__':
    main()
