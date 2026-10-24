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
    Unit tests for DslDocumentManagerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.gui.dsl.document.factory import DslDocumentManagerFactory
from scarajectory.infrastructure.gui.dsl.document.manager import DslDocumentManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslDocumentManagerFactoryTestCase(TestCase):
    '''
        Unit test suite validating DslDocumentManagerFactory.

        It defines:

            :methods:
                | test_create - Tests factory construction with loader and storer.
                | test_get_version - Tests factory version string.
    '''

    def test_create(self) -> None:
        '''
            Tests factory create with explicit dependencies.

            :exceptions: None.
        '''
        loader = MagicMock(spec=IPlanLoader)
        storer = MagicMock(spec=IPlanStorer)
        manager = DslDocumentManagerFactory.create(
            loader=loader,
            storer=storer,
        )
        self.assertIsInstance(manager, DslDocumentManager)

    def test_get_version(self) -> None:
        '''
            Tests factory version getter.

            :exceptions: None.
        '''
        self.assertEqual(DslDocumentManagerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
