# -*- coding: UTF-8 -*-

'''
Module
    gui_factory_test.py
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
    Unit tests for ScarajectoryGUIFactory presentation factory.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main
from unittest.mock import MagicMock

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.infrastructure.gui.gui_factory import ScarajectoryGUIFactory
from scarajectory.infrastructure.gui.engine import ScarajectoryGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScarajectoryGUIFactory(TestCase):
    '''
        Test cases for ScarajectoryGUIFactory.

        It defines:

            :methods:
                | test_factory_structure - Verifies factory exists and callable.
    '''

    def test_factory_structure(self) -> None:
        '''
            Verifies ScarajectoryGUIFactory create signature.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(ScarajectoryGUIFactory, 'create'))
        self.assertTrue(callable(ScarajectoryGUIFactory.create))

    def test_factory_version(self) -> None:
        '''
            Verifies ScarajectoryGUIFactory get_version method.

            :exceptions: None.
        '''
        self.assertEqual(ScarajectoryGUIFactory.get_version(), '1.0.3')



if __name__ == '__main__':
    main()
