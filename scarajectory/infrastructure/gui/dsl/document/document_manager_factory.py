# -*- coding: UTF-8 -*-

'''
Module
    document_manager_factory.py
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
    Factory service constructing DslDocumentManager instances with collaborator injection.
'''

from __future__ import annotations

from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.infrastructure.gui.dsl.document.document_manager import DslDocumentManager
from scarajectory.infrastructure.storage.plan_storage_service_factory import PlanStorageServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslDocumentManagerFactory:
    '''
        Factory providing creation of DslDocumentManager instances.

        It defines:

            :methods:
                | create - Constructs DslDocumentManager with explicit storage service.
                | create_default - Constructs DslDocumentManager with default storage service.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, storage: IPlanStorageService) -> DslDocumentManager:
        '''
            Constructs DslDocumentManager with explicit storage service.

            :param storage: Required IPlanStorageService implementation.
            :return: DslDocumentManager instance.
            :exceptions: None.
        '''
        return DslDocumentManager(storage=storage)

    @classmethod
    def create_default(cls) -> DslDocumentManager:
        '''
            Constructs DslDocumentManager with default storage service.

            :return: DslDocumentManager instance.
            :exceptions: None.
        '''
        return cls.create(storage=PlanStorageServiceFactory.create())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
