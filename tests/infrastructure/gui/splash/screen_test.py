# -*- coding: UTF-8 -*-

'''
Module
    screen_test.py
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
    Unit tests for SplashScreen component.
'''

from __future__ import annotations

from tkinter import Tk, Toplevel
from tkinter.ttk import Style
from unittest import TestCase, main
from unittest.mock import patch

from scarajectory.infrastructure.gui.splash.iscreen import ISplashScreen
from scarajectory.infrastructure.gui.splash.screen import SplashScreen

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSplashScreen(TestCase):
    '''
        Tests verifying SplashScreen widget instantiation and lifecycle.

        It defines:

            :methods:
                | setUpClass - Sets up test class fixture.
                | tearDownClass - Tears down test class fixture.
                | test_splash_screen_conformance - Verifies protocol conformance.
                | test_set_progress_and_close - Verifies progress updates and close.
                | test_splash_screen_theme_exception - Verifies theme error handling.
                | test_splash_screen_update_exception - Verifies update error handling.
                | test_splash_screen_destroy_exception - Verifies destroy error handling.
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

    def test_splash_screen_conformance(self) -> None:
        '''
            Verifies that SplashScreen conforms to ISplashScreen protocol.

            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        self.assertIsInstance(splash, ISplashScreen)
        splash.close()

    def test_set_progress_and_close(self) -> None:
        '''
            Verifies set_progress updates progress value and close dismisses window.

            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        splash.set_progress(50, 'Loading workspace...')
        self.assertEqual(splash.progress, 50)
        self.assertEqual(splash.status, 'Loading workspace...')

        splash.set_progress(150, 'Clamped max')
        self.assertEqual(splash.progress, 100)

        splash.set_progress(-20, 'Clamped min')
        self.assertEqual(splash.progress, 0)

        splash.close()
        # Closing already destroyed window handles exception gracefully
        splash.close()

    @patch.object(Style, 'theme_use', side_effect=Exception('Theme error'))
    def test_splash_screen_theme_exception(self, _mock_theme: object) -> None:
        '''
            Verifies splash screen initializes cleanly when theme_use fails.

            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        self.assertIsInstance(splash, ISplashScreen)
        splash.close()

    @patch.object(Toplevel, 'update', side_effect=Exception('Update error'))
    def test_splash_screen_update_exception(self, _mock_update: object) -> None:
        '''
            Verifies splash screen update exceptions are handled cleanly.

            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        splash.set_progress(30, 'Testing error path')
        splash.close()

    @patch.object(Toplevel, 'destroy', side_effect=Exception('Destroy error'))
    def test_splash_screen_destroy_exception(self, _mock_destroy: object) -> None:
        '''
            Verifies close handles destroy exception gracefully.

            :exceptions: None.
        '''
        splash = SplashScreen(self.root)
        splash.close()


if __name__ == '__main__':
    main()
