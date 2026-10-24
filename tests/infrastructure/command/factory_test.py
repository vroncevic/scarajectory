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
    Unit testing for CommandFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.command.dependencies import CommandDependencies
from scarajectory.infrastructure.command.factory import CommandFactory
from scarajectory.infrastructure.command.provides import CommandProvides
from scarajectory.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandFactoryTestCase(TestCase):
    '''
        Unit tests for CommandFactory.

        It defines:

            :methods:
                | test_create_command_provides - Verifies creation of CommandProvides container.
                | test_get_version - Verifies factory version query.
    '''

    def test_create_command_provides(self) -> None:
        '''
            Verifies CommandFactory create method builds valid CommandProvides.

            :exceptions: None.
        '''
        mock_gui = MagicMock(spec=IGUI)
        provides = CommandFactory.create(CommandDependencies(gui=mock_gui))

        self.assertIsInstance(provides, CommandProvides)
        self.assertEqual(len(provides.commands), 1)
        self.assertIs(provides.commands[0], provides.studio_command)
        self.assertEqual(provides.studio_command.definition.name, 'studio')

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(CommandFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
