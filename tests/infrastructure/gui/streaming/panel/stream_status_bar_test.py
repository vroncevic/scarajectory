# -*- coding: UTF-8 -*-

'''
Module
    stream_status_bar_test.py
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
    Unit testing for StreamStatusBar component.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Label, Progressbar
from unittest import TestCase, main

from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.streaming.panel.stream_status_bar import StreamStatusBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamStatusBarTestCase(TestCase):
    '''
        Unit tests for StreamStatusBar widget.

        It defines:

            :methods:
                | setUp - Initializes headless Tk root.
                | tearDown - Destroys Tk root.
                | test_set_status_text - Verifies label text update.
                | test_update_progress - Verifies progress bar and status text formatting.
    '''

    def setUp(self) -> None:
        '''Initializes headless Tk instance before each test.'''
        self.root: Tk = Tk()
        self.root.withdraw()

    def tearDown(self) -> None:
        '''Destroys Tk instance after each test.'''
        self.root.destroy()

    def test_set_status_text(self) -> None:
        '''Verifies set_status_text configures status label.'''
        status_bar = StreamStatusBar(self.root)
        status_bar.set_status_text('Custom Status')
        labels = [w for w in status_bar.winfo_children() if isinstance(w, Label)]
        self.assertIn('Custom Status', str(labels[0].cget('text')))

    def test_update_progress(self) -> None:
        '''Verifies update_progress updates progress bar and summary formatting.'''
        status_bar = StreamStatusBar(self.root)
        progress_bars = [
            w for w in status_bar.winfo_children() if isinstance(w, Progressbar)
        ]
        labels = [w for w in status_bar.winfo_children() if isinstance(w, Label)]

        progress1 = StreamProgress(
            state=StreamState.STREAMING,
            total_waypoints=10,
            sent_waypoints=5,
            completed_waypoints=5,
            failed_waypoints=0,
            current_line='G1 X10 Y20',
            error_message='',
            elapsed_seconds=1.5,
            percentage=50.0,
        )
        status_bar.update_progress(progress1)
        self.assertEqual(float(progress_bars[0]['value']), 50.0)
        self.assertIn('5/10', str(labels[0].cget('text')))
        self.assertNotIn('failed', str(labels[0].cget('text')))

        progress2 = StreamProgress(
            state=StreamState.STREAMING,
            total_waypoints=10,
            sent_waypoints=8,
            completed_waypoints=6,
            failed_waypoints=2,
            current_line='G1 X20 Y30',
            error_message='Limit hit',
            elapsed_seconds=2.5,
            percentage=80.0,
        )
        status_bar.update_progress(progress2)
        self.assertEqual(float(progress_bars[0]['value']), 80.0)
        self.assertIn('2 failed', str(labels[0].cget('text')))


if __name__ == '__main__':
    main()
