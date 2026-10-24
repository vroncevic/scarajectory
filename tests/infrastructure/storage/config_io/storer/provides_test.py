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
    Unit tests for StorerProvides container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.infrastructure.storage.config_io.storer.istorer import IConfigStorer
from scarajectory.infrastructure.storage.config_io.storer.provides import StorerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStorerProvides(TestCase):
    '''
        Test cases verifying StorerProvides data structure.

        It defines:

            :methods:
                | test_provides_creation - Verifies proper instantiation of provides container.
    '''

    def test_provides_creation(self) -> None:
        '''Verifies storer collaborator is assigned correctly.'''
        mock_storer = MagicMock(spec=IConfigStorer)
        provides = StorerProvides(config_storer=mock_storer)
        self.assertEqual(provides.config_storer, mock_storer)
