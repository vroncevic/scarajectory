# -*- coding: UTF-8 -*-

'''
Module
    validation_tab_test.py
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
    Unit testing for ValidationTab and ValidationTabFactory components.
'''

from __future__ import annotations

from tkinter import END, Text, Tk
from tkinter.ttk import Button, Frame
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.validation.validation_tab import ValidationTab
from scarajectory.infrastructure.gui.validation.validation_tab_factory import ValidationTabFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidationTabTestCase(TestCase):
    '''Unit tests for ValidationTab and ValidationTabFactory.'''

    def setUp(self) -> None:
        '''Initializes headless Tk instance before each test.'''
        self.root: Tk = Tk()
        self.root.withdraw()

    def tearDown(self) -> None:
        '''Destroys Tk instance after each test.'''
        self.root.destroy()

    def test_validation_tab_creation_and_layout(self) -> None:
        '''Verifies ValidationTab builds expected frame, button, and text area.'''
        mock_plan = MagicMock()
        mock_validator = MagicMock()
        tab = ValidationTab(self.root, plan=mock_plan, validator=mock_validator)

        frames = [w for w in tab.winfo_children() if isinstance(w, Frame)]
        self.assertEqual(len(frames), 1)

        buttons = [w for w in frames[0].winfo_children() if isinstance(w, Button)]
        self.assertEqual(len(buttons), 1)

        text_widgets = [w for w in tab.winfo_children() if isinstance(w, Text)]
        self.assertEqual(len(text_widgets), 1)

    def test_validation_tab_run_validation(self) -> None:
        '''Verifies run_validation calls validator and populates formatted lines.'''
        mock_plan = MagicMock()
        mock_validator = MagicMock()
        mock_validator.validate_plan.return_value = (
            False,
            [
                'Reachability limit PASSED',
                'Singularity zone FAILED',
                'WARNING: speed near singularity',
            ],
        )

        tab = ValidationTab(self.root, plan=mock_plan, validator=mock_validator)
        tab.run_validation()

        mock_validator.validate_plan.assert_called_once_with(mock_plan)
        text_widgets = [w for w in tab.winfo_children() if isinstance(w, Text)]
        output_text = text_widgets[0].get('1.0', END).strip()
        self.assertIn('✅ Reachability limit PASSED', output_text)
        self.assertIn('❌ Singularity zone FAILED', output_text)
        self.assertIn('⚠️ WARNING: speed near singularity', output_text)

    def test_validation_tab_run_validation_error(self) -> None:
        '''Verifies run_validation handles unexpected validation exceptions.'''
        mock_plan = MagicMock()
        mock_validator = MagicMock()
        mock_validator.validate_plan.side_effect = RuntimeError('Validator failure')

        tab = ValidationTab(self.root, plan=mock_plan, validator=mock_validator)
        tab.run_validation()

        text_widgets = [w for w in tab.winfo_children() if isinstance(w, Text)]
        output_text = text_widgets[0].get('1.0', END).strip()
        self.assertIn('❌ Validation error: Validator failure', output_text)

    def test_validation_tab_factory_create(self) -> None:
        '''Verifies ValidationTabFactory creates a valid ValidationTab instance.'''
        mock_plan = MagicMock()
        mock_validator = MagicMock()
        tab = ValidationTabFactory.create(
            self.root,
            plan=mock_plan,
            validator=mock_validator,
        )
        self.assertIsInstance(tab, ValidationTab)

    def test_validation_tab_factory_version(self) -> None:
        '''Verifies factory returns semantic version string.'''
        self.assertEqual(ValidationTabFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
