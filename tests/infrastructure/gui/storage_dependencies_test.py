# -*- coding: UTF-8 -*-

'''
Module
    storage_dependencies_test.py
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
    Unit tests for StorageDependencies data container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.gui.storage_dependencies import StorageDependencies
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStorageDependencies(TestCase):
    '''
        Tests StorageDependencies construction and immutability.

        It defines:

            :methods:
                | test_bundle_creation - Verifies bundle attributes assignment.
                | test_bundle_immutability - Verifies frozen dataclass behavior.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies bundle attributes assignment.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IPlanLoader)
        mock_storer = MagicMock(spec=IPlanStorer)
        mock_workspace = MagicMock(spec=IWorkspaceManager)

        bundle = StorageDependencies(
            loader=mock_loader,
            storer=mock_storer,
            workspace=mock_workspace,
        )

        self.assertIs(bundle.loader, mock_loader)
        self.assertIs(bundle.storer, mock_storer)
        self.assertIs(bundle.workspace, mock_workspace)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies frozen dataclass behavior.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IPlanLoader)
        mock_storer = MagicMock(spec=IPlanStorer)
        mock_workspace = MagicMock(spec=IWorkspaceManager)

        bundle = StorageDependencies(
            loader=mock_loader,
            storer=mock_storer,
            workspace=mock_workspace,
        )

        with self.assertRaises(FrozenInstanceError):
            bundle.loader = mock_loader  # type: ignore[misc]


if __name__ == '__main__':
    main()
