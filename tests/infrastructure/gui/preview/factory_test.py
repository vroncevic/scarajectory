# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit testing for PreviewTabFactory component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.preview.dependencies import PreviewDependencies
from scarajectory.infrastructure.gui.preview.factory import PreviewTabFactory
from scarajectory.infrastructure.gui.preview.tab import PreviewTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreviewTabFactoryTestCase(TestCase):
    '''
        Unit tests for PreviewTabFactory.

        It defines:

            :methods:
                | setUp - Initializes headless Tk instance before each test.
                | tearDown - Destroys Tk instance after each test.
                | test_create - Verifies PreviewTabFactory creates a valid PreviewTab.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def setUp(self) -> None:
        '''
            Initializes headless Tk instance before each test.

            :exceptions: None.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()

    def tearDown(self) -> None:
        '''
            Destroys Tk instance after each test.

            :exceptions: None.
        '''
        self.root.destroy()

    def test_create(self) -> None:
        '''
            Verifies PreviewTabFactory creates a valid PreviewTab instance.

            :exceptions: None.
        '''
        mock_plan = MagicMock()
        mock_exporter = MagicMock()
        deps = PreviewDependencies(plan=mock_plan, exporter=mock_exporter)
        tab = PreviewTabFactory.create(self.root, dependencies=deps)
        self.assertIsInstance(tab, PreviewTab)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(PreviewTabFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
