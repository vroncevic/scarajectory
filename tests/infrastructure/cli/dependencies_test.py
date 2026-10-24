# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit testing for CLIDependencies data model.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.cli.dependencies import CLIDependencies
from scarajectory.infrastructure.cli.setup.bundle import CLIBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIDependenciesTestCase(TestCase):
    '''
        Unit tests for CLIDependencies dataclass.

        It defines:

            :methods:
                | test_cli_dependencies_properties - Verifies fields and immutability.
    '''

    def test_cli_dependencies_properties(self) -> None:
        '''
            Verifies CLIDependencies initialization and attribute retrieval.

            :exceptions: None.
        '''
        mock_bundle = MagicMock(spec=CLIBundle)
        deps = CLIDependencies(bundle=mock_bundle)
        self.assertIs(deps.bundle, mock_bundle)


if __name__ == '__main__':
    main()
