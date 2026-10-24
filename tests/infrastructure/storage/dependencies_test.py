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
    Unit testing for StorageDependencies parameter bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader
from scarajectory.infrastructure.storage.config_io.storer.istorer import IConfigStorer
from scarajectory.infrastructure.storage.dependencies import StorageDependencies
from scarajectory.infrastructure.storage.workspace.config import WorkspaceConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStorageDependencies(TestCase):
    '''Unit tests validating StorageDependencies parameter bundle.'''

    def test_frozen_immutability(self) -> None:
        '''Verifies StorageDependencies is frozen and immutable.'''
        deps = StorageDependencies(
            io_loader=MagicMock(spec=IConfigLoader),
            io_storer=MagicMock(spec=IConfigStorer),
            workspace_config=WorkspaceConfig(),
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'workspace_config', WorkspaceConfig())

    def test_custom_dependencies(self) -> None:
        '''Verifies construction with explicit parameters.'''
        mock_loader = MagicMock(spec=IConfigLoader)
        mock_storer = MagicMock(spec=IConfigStorer)
        custom_config = WorkspaceConfig(workspace_dir='/custom/ws')
        deps = StorageDependencies(
            io_loader=mock_loader,
            io_storer=mock_storer,
            workspace_config=custom_config,
        )
        self.assertIs(deps.io_loader, mock_loader)
        self.assertIs(deps.io_storer, mock_storer)
        self.assertIs(deps.workspace_config, custom_config)


if __name__ == '__main__':
    main()
