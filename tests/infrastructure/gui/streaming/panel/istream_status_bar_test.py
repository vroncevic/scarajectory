# -*- coding: UTF-8 -*-

'''
Module
    istream_status_bar_test.py
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
    Unit testing for IStreamStatusBar protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.streaming.panel.istream_status_bar import IStreamStatusBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingStreamStatusBarStub:
    '''Conforming stub implementation satisfying IStreamStatusBar.'''

    def set_status_text(self, text: str) -> None:
        '''Updates status bar text.'''
        _ = text

    def update_progress(self, progress: StreamProgress) -> None:
        '''Updates progress data model.'''
        _ = progress


class NonConformingStreamStatusBarStub:
    '''Non-conforming stub missing update_progress method.'''

    def set_status_text(self, text: str) -> None:
        '''Updates status bar text.'''
        _ = text

    def get_bar_height(self) -> int:
        '''Returns widget height.'''
        return 20


class StreamStatusBarTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IStreamStatusBar.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies conforming stub satisfies IStreamStatusBar protocol.'''
        stub = ConformingStreamStatusBarStub()
        self.assertIsInstance(stub, IStreamStatusBar)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-conforming stub fails IStreamStatusBar protocol check.'''
        incomplete = NonConformingStreamStatusBarStub()
        self.assertNotIsInstance(incomplete, IStreamStatusBar)


if __name__ == '__main__':
    main()
