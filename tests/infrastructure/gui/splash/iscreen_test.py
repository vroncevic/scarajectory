# -*- coding: UTF-8 -*-

'''
Module
    iscreen_test.py
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
    Unit tests for ISplashScreen interface and protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.splash.iscreen import ISplashScreen

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingSplashScreenStub:
    '''
        Conforming stub implementation satisfying ISplashScreen.

        It defines:

            :methods:
                | set_progress - Updates progress percentage and message.
                | close - Closes splash screen.
    '''

    def set_progress(self, progress: int, status: str) -> None:
        '''
            Updates progress percentage and message.

            :param progress: Integer percentage value.
            :param status: Descriptive status message string.
            :exceptions: None.
        '''
        del progress, status

    def close(self) -> None:
        '''
            Closes splash screen.

            :exceptions: None.
        '''


class TestISplashScreen(TestCase):
    '''
        Tests verifying ISplashScreen protocol definition and subtyping.

        It defines:

            :methods:
                | test_protocol_methods - Verifies methods declared on ISplashScreen.
                | test_conforming_stub_subtyping - Verifies stub satisfies protocol.
    '''

    def test_protocol_methods(self) -> None:
        '''
            Verifies methods declared on ISplashScreen protocol.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(ISplashScreen, 'set_progress'))
        self.assertTrue(hasattr(ISplashScreen, 'close'))

    def test_conforming_stub_subtyping(self) -> None:
        '''
            Verifies conforming stub satisfies ISplashScreen protocol structurally.

            :exceptions: None.
        '''
        stub = ConformingSplashScreenStub()
        self.assertIsInstance(stub, ISplashScreen)


if __name__ == '__main__':
    main()
