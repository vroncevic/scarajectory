# -*- coding: UTF-8 -*-

'''
Module
    command_templates_test.py
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
    Unit tests for CommandTemplates template catalog.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.formatter.command_templates import CommandTemplates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandTemplates(TestCase):
    '''
        Test cases for CommandTemplates dictionary.

        It defines:

            :methods:
                | test_get_template - Tests template lookup by action name.
                | test_list_actions - Tests listing supported action names.
    '''

    def test_get_template(self) -> None:
        '''
            Tests template resolution for existing and non-existing actions.

            :exceptions: None.
        '''
        tpl = CommandTemplates.get_template('MOVE')
        self.assertTrue(isinstance(tpl, str) and len(tpl) > 0)

        empty_tpl = CommandTemplates.get_template('NON_EXISTENT_ACTION')
        self.assertEqual(empty_tpl, '')

    def test_list_actions(self) -> None:
        '''
            Tests listing all available action keys.

            :exceptions: None.
        '''
        actions = CommandTemplates.list_actions()
        self.assertIsInstance(actions, tuple)
        self.assertIn('MOVE', actions)
        self.assertIn('HOME', actions)


if __name__ == '__main__':
    main()
