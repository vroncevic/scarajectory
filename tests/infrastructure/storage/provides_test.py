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
    Unit testing for StorageProvides dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.storage.config_io.provides import ConfigIOProvides
from scarajectory.infrastructure.storage.plan.provides import PlanProvides
from scarajectory.infrastructure.storage.provides import StorageProvides
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStorageProvides(TestCase):
    '''Unit tests validating StorageProvides dataclass.'''

    def test_provides_fields(self) -> None:
        '''
            Verifies all fields assigned correctly in StorageProvides.

            :exceptions: None.
        '''
        mock_loader = MagicMock(spec=IPlanLoader)
        mock_storer = MagicMock(spec=IPlanStorer)
        mock_workspace = MagicMock(spec=IWorkspaceManager)
        mock_config_io = MagicMock(spec=ConfigIOProvides)
        mock_plan = MagicMock(spec=PlanProvides)

        provides = StorageProvides(
            plan_loader=mock_loader,
            plan_storer=mock_storer,
            workspace_manager=mock_workspace,
            config_io_provides=mock_config_io,
            plan_storage_provides=mock_plan
        )

        self.assertIs(provides.plan_loader, mock_loader)
        self.assertIs(provides.plan_storer, mock_storer)
        self.assertIs(provides.workspace_manager, mock_workspace)
        self.assertIs(provides.config_io_provides, mock_config_io)
        self.assertIs(provides.plan_storage_provides, mock_plan)


if __name__ == '__main__':
    main()
