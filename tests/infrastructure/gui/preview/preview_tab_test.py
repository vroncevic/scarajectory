# -*- coding: UTF-8 -*-

'''
Module
    preview_tab_test.py
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
    Unit testing for PreviewTab and PreviewTabFactory components.
'''

from __future__ import annotations

from tkinter import END, Text, Tk
from tkinter.ttk import Button, Frame
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.preview.preview_tab import PreviewTab
from scarajectory.infrastructure.gui.preview.preview_tab_factory import PreviewTabFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreviewTabTestCase(TestCase):
    '''Unit tests for PreviewTab and PreviewTabFactory.'''

    def setUp(self) -> None:
        '''Initializes headless Tk instance before each test.'''
        self.root: Tk = Tk()
        self.root.withdraw()

    def tearDown(self) -> None:
        '''Destroys Tk instance after each test.'''
        self.root.destroy()

    def test_preview_tab_creation_and_layout(self) -> None:
        '''Verifies PreviewTab builds expected frame, button, and text area.'''
        mock_plan = MagicMock()
        mock_exporter = MagicMock()
        tab = PreviewTab(self.root, plan=mock_plan, exporter=mock_exporter)

        frames = [w for w in tab.winfo_children() if isinstance(w, Frame)]
        self.assertEqual(len(frames), 1)

        buttons = [w for w in frames[0].winfo_children() if isinstance(w, Button)]
        self.assertEqual(len(buttons), 1)

        text_widgets = [w for w in tab.winfo_children() if isinstance(w, Text)]
        self.assertEqual(len(text_widgets), 1)

    def test_preview_tab_generate_preview(self) -> None:
        '''Verifies generate_preview triggers exporter and populates text widget.'''
        mock_plan = MagicMock()
        mock_exporter = MagicMock()
        mock_exporter.export_plan.return_value = 'M100\nM101\n'

        tab = PreviewTab(self.root, plan=mock_plan, exporter=mock_exporter)
        tab.generate_preview()

        mock_exporter.export_plan.assert_called_once_with(plan=mock_plan)
        text_widgets = [w for w in tab.winfo_children() if isinstance(w, Text)]
        self.assertEqual(text_widgets[0].get('1.0', END).strip(), 'M100\nM101')

    def test_preview_tab_generate_preview_error(self) -> None:
        '''Verifies generate_preview handles export failure gracefully.'''
        mock_plan = MagicMock()
        mock_exporter = MagicMock()
        mock_exporter.export_plan.side_effect = RuntimeError('Export failure')

        tab = PreviewTab(self.root, plan=mock_plan, exporter=mock_exporter)
        tab.generate_preview()

        text_widgets = [w for w in tab.winfo_children() if isinstance(w, Text)]
        self.assertIn('[ERROR] Plan export failed', text_widgets[0].get('1.0', END))

    def test_preview_tab_factory_create(self) -> None:
        '''Verifies PreviewTabFactory creates a valid PreviewTab instance.'''
        mock_plan = MagicMock()
        with patch('scarajectory.infrastructure.gui.preview.preview_tab_factory.ScaraPlanExporterFactory.create') as mock_factory_create:
            mock_factory_create.return_value = MagicMock()
            tab = PreviewTabFactory.create(self.root, plan=mock_plan)
            self.assertIsInstance(tab, PreviewTab)

    def test_preview_tab_factory_version(self) -> None:
        '''Verifies factory returns semantic version string.'''
        self.assertEqual(PreviewTabFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
