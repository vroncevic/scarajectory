# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Provision dataclass exposing public interfaces provided by storage subsystem.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.infrastructure.storage.config_io.provides import ConfigIOProvides
from scarajectory.infrastructure.storage.plan.provides import PlanProvides
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class StorageProvides:
    '''
        Subsystem provision dataclass exposing public interfaces of storage subsystem.

        It defines:

            :attributes:
                | plan_loader - Injected IPlanLoader protocol implementation.
                | plan_storer - Injected IPlanStorer protocol implementation.
                | workspace_manager - Injected IWorkspaceManager protocol implementation.
                | config_io_provides - Injected ConfigIOProvides subsystem provision dataclass.
                | plan_storage_provides - Injected PlanProvides subsystem provision dataclass.
    '''

    plan_loader: IPlanLoader
    plan_storer: IPlanStorer
    workspace_manager: IWorkspaceManager
    config_io_provides: ConfigIOProvides
    plan_storage_provides: PlanProvides
