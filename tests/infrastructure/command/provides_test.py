# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit testing for CommandProvides container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.command.bundle import CommandBundle
from scarajectory.infrastructure.command.provides import CommandProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandProvidesTestCase(TestCase):
    '''
        Unit tests for CommandProvides container.

        It defines:

            :methods:
                | test_command_provides_properties - Verifies fields and immutability.
    '''

    def test_command_provides_properties(self) -> None:
        '''
            Verifies CommandProvides initialization and attribute retrieval.

            :exceptions: None.
        '''
        mock_cmd = MagicMock(spec=CommandBundle)
        provides = CommandProvides(
            commands=(mock_cmd,),
            studio_command=mock_cmd,
        )

        self.assertEqual(provides.commands, (mock_cmd,))
        self.assertIs(provides.studio_command, mock_cmd)


if __name__ == '__main__':
    main()
