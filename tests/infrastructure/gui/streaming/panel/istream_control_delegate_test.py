# -*- coding: UTF-8 -*-

'''
Module
    istream_control_delegate_test.py
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
    Unit testing for IStreamControlDelegate protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.streaming.panel.istream_control_delegate import IStreamControlDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingControlDelegateStub:
    '''Conforming stub implementation satisfying IStreamControlDelegate.'''

    def on_start_stream(self) -> None:
        '''Starts streaming.'''

    def on_pause_resume_stream(self) -> None:
        '''Toggles pause/resume.'''

    def on_stop_stream(self) -> None:
        '''Stops streaming.'''


class IncompleteControlDelegateStub:
    '''Non-conforming stub implementation missing on_stop_stream.'''

    def on_start_stream(self) -> None:
        '''Starts streaming.'''

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class StreamControlDelegateProtocolTestCase(TestCase):
    '''
        Tests IStreamControlDelegate runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamControlDelegate protocol.'''
        stub = ConformingControlDelegateStub()
        self.assertIsInstance(stub, IStreamControlDelegate)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IStreamControlDelegate protocol check.'''
        stub = IncompleteControlDelegateStub()
        self.assertNotIsInstance(stub, IStreamControlDelegate)


if __name__ == '__main__':
    main()
