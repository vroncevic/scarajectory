# -*- coding: UTF-8 -*-

'''
Module
    bundle_factory_test.py
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
    Unit tests for SCARAjectoryBundleFactory and SCARAjectory top-level engine.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.setup.keys import SCARAjectoryBundleKeys
from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.engine import SCARAjectory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBundleFactory(unittest.TestCase):
    '''
        Test cases for SCARAjectoryBundleFactory and SCARAjectory life cycle.

        It defines:

            :methods:
                | test_factory_creation - Tests creating bundle and verifying engine components.
                | test_factory_custom_geometry - Tests bundle creation with custom kinematic options.
                | test_engine_lifecycle - Tests SCARAjectory initialization status.
    '''

    def test_factory_creation(self) -> None:
        '''
            Tests default bundle assembly.

            :exceptions: None.
        '''
        bundle = SCARAjectoryBundleFactory.create_bundle()
        self.assertIsNotNone(bundle)
        self.assertIsNotNone(bundle.service)
        self.assertIsNotNone(bundle.gui)
        self.assertIsNotNone(bundle.cli)

    def test_factory_custom_geometry(self) -> None:
        '''
            Tests custom kinematic parameter injection.

            :exceptions: None.
        '''
        options = {
            SCARAjectoryBundleKeys.OPTION_L1: 160.0,
            SCARAjectoryBundleKeys.OPTION_L2: 130.0,
            SCARAjectoryBundleKeys.OPTION_Z_MIN: -10.0,
            SCARAjectoryBundleKeys.OPTION_Z_MAX: 90.0
        }
        bundle = SCARAjectoryBundleFactory.create_bundle(options=options)
        self.assertIsNotNone(bundle)
        self.assertEqual(bundle.service.get_validator().bounds.l1, 160.0)
        self.assertEqual(bundle.service.get_validator().bounds.l2, 130.0)

    def test_engine_lifecycle(self) -> None:
        '''
            Tests engine instantiation.

            :exceptions: None.
        '''
        bundle = SCARAjectoryBundleFactory.create_bundle()
        app = SCARAjectory(bundle)
        self.assertTrue(app.is_initialized())


if __name__ == '__main__':
    unittest.main()
