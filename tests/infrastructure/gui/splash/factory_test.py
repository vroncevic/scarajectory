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
    Unit tests for SplashScreenFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main

from scarajectory.infrastructure.gui.splash.factory import SplashScreenFactory
from scarajectory.infrastructure.gui.splash.screen import SplashScreen

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSplashScreenFactory(TestCase):
    '''
        Tests verifying SplashScreenFactory creation methods.

        It defines:

            :methods:
                | setUpClass - Sets up test class fixture.
                | tearDownClass - Tears down test class fixture.
                | test_factory_version - Verifies factory version string.
                | test_create_returns_splash_screen - Verifies factory creation.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up test class fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down test class fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def test_factory_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(SplashScreenFactory.get_version(), '1.0.3')

    def test_create_returns_splash_screen(self) -> None:
        '''
            Verifies create returns active SplashScreen instance.

            :exceptions: None.
        '''
        splash = SplashScreenFactory.create(self.root)
        self.assertIsInstance(splash, SplashScreen)
        splash.close()


if __name__ == '__main__':
    main()
