# -*- coding: UTF-8 -*-

'''
Module
    scara_bounds_parser_test.py
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
    Unit tests for ScaraBoundsParser and ScaraBoundsParserFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.settings.bounds.iscara_bounds_parser import IScaraBoundsParser
from scarajectory.infrastructure.settings.bounds.scara_bounds_parser_factory import ScaraBoundsParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraBoundsParser(TestCase):
    '''
        Unit test cases verifying ScaraBoundsParser parsing and factory.
    '''

    parser: IScaraBoundsParser

    def setUp(self) -> None:
        self.parser = ScaraBoundsParserFactory.create()

    def test_factory_interface(self) -> None:
        '''
            Verifies factory returns an instance implementing IScaraBoundsParser.
        '''
        self.assertIsInstance(self.parser, IScaraBoundsParser)

    def test_factory_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        self.assertIsInstance(ScaraBoundsParserFactory.get_version(), str)

    def test_parse_geometry(self) -> None:
        '''
            Verifies geometry parsing with defaults and overrides.
        '''
        cfg = {'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
        opts = {'l1': 180.0}
        geom = self.parser.parse_geometry(options=opts, cfg=cfg)
        self.assertEqual(geom['l1'], 180.0)
        self.assertEqual(geom['l2'], 120.0)
        self.assertEqual(geom['z_min'], 0.0)
        self.assertEqual(geom['z_max'], 100.0)

    def test_parse_motion(self) -> None:
        '''
            Verifies motion limit parsing with defaults and overrides.
        '''
        cfg = {
            'min_speed': 1.0,
            'max_speed': 250.0,
            'default_speed': 50.0,
            'default_accel': 300.0,
            'max_accel': 2000.0,
        }
        opts = {'default_speed': 80.0}
        motion = self.parser.parse_motion(options=opts, cfg=cfg)
        self.assertEqual(motion['min_speed'], 1.0)
        self.assertEqual(motion['max_speed'], 250.0)
        self.assertEqual(motion['default_speed'], 80.0)
        self.assertEqual(motion['default_accel'], 300.0)
        self.assertEqual(motion['max_accel'], 2000.0)

    def test_parse_joints(self) -> None:
        '''
            Verifies angular joint limit parsing.
        '''
        cfg = {
            'j1_min_rad': -2.6,
            'j1_max_rad': 2.6,
            'j2_min_rad': -2.5,
            'j2_max_rad': 2.5,
        }
        opts = {'j2_max_rad': 2.4}
        joints = self.parser.parse_joints(options=opts, cfg=cfg)
        self.assertEqual(joints['j1_min_rad'], -2.6)
        self.assertEqual(joints['j1_max_rad'], 2.6)
        self.assertEqual(joints['j2_min_rad'], -2.5)
        self.assertEqual(joints['j2_max_rad'], 2.4)

    def test_parse_singularities(self) -> None:
        '''
            Verifies kinematic singularity margin parsing.
        '''
        cfg = {
            'singularity_outer_margin_mm': 3.0,
            'singularity_inner_margin_mm': 3.0,
            'singularity_theta2_min_rad': 0.08,
        }
        opts = {'singularity_outer_margin_mm': 5.0}
        sings = self.parser.parse_singularities(options=opts, cfg=cfg)
        self.assertEqual(sings['singularity_outer_margin_mm'], 5.0)
        self.assertEqual(sings['singularity_inner_margin_mm'], 3.0)
        self.assertEqual(sings['singularity_theta2_min_rad'], 0.08)


if __name__ == '__main__':
    main()
