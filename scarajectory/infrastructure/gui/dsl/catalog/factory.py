# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory service constructing DslExampleCatalog instances.
'''

from __future__ import annotations

from pathlib import Path

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.infrastructure.gui.dsl.catalog.catalog import DslExampleCatalog
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslExampleCatalogFactory:
    '''
        Factory providing creation of DslExampleCatalog instances.

        It defines:

            :methods:
                | create - Constructs DslExampleCatalog with explicit directory and loader.
                | create_default - Constructs DslExampleCatalog with workspace directory.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        examples_dir: Path,
        loader: IPlanLoader,
    ) -> DslExampleCatalog:
        '''
            Constructs DslExampleCatalog with explicit directory and loader.

            :param examples_dir: Path to directory containing example files.
            :param loader: Required IPlanLoader implementation.
            :return: DslExampleCatalog instance.
            :exceptions: None.
        '''
        return DslExampleCatalog(examples_dir=examples_dir, loader=loader)

    @classmethod
    def create_default(
        cls,
        *,
        loader: IPlanLoader,
        workspace: IWorkspaceManager,
    ) -> DslExampleCatalog:
        '''
            Constructs DslExampleCatalog with default user workspace directory.

            :param loader: Required IPlanLoader implementation.
            :param workspace: Required IWorkspaceManager implementation.
            :return: DslExampleCatalog instance.
            :exceptions: None.
        '''
        workspace_dir: Path = Path(workspace.ensure_workspace())
        return cls.create(examples_dir=workspace_dir, loader=loader)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
