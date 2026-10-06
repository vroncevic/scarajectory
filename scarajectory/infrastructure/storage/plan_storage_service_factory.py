# -*- coding: UTF-8 -*-

'''
Module
    plan_storage_service_factory.py
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
    Factory module for assembling and instantiating PlanStorageService instances.
'''

from __future__ import annotations

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.storage.config_io.config_io_factory import ConfigIOFactory
from scarajectory.infrastructure.storage.config_io.iconfig_io_factory import IConfigIOFactory
from scarajectory.infrastructure.storage.plan_loader import PlanLoader
from scarajectory.infrastructure.storage.plan_storer import PlanStorer
from scarajectory.infrastructure.storage.plan_storage_service import PlanStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanStorageServiceFactory:
    '''
        Factory responsible for creating PlanStorageService instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a PlanStorageService with default ContextBundle.
                | create_with_context - Assembles PlanStorageService with explicit ContextBundle.
                | create_with_io_factory - Assembles PlanStorageService with explicit IConfigIOFactory.
                | get_version - Returns factory module semantic version string.
    '''

    @classmethod
    def create(cls) -> PlanStorageService:
        '''
            Assembles and instantiates a PlanStorageService adapter.

            :return: Fully assembled PlanStorageService instance.
            :exceptions: None.
        '''
        return cls.create_with_context(ContextBundleFactory.create_bundle())

    @classmethod
    def create_with_context(cls, context_bundle: ContextBundle) -> PlanStorageService:
        '''
            Assembles and instantiates a PlanStorageService adapter with explicit context.

            :param context_bundle: ATS ContextBundle instance.
            :return: Fully assembled PlanStorageService instance.
            :exceptions: None.
        '''
        io_factory = ConfigIOFactory.create(context_bundle)
        return cls.create_with_io_factory(io_factory)

    @classmethod
    def create_with_io_factory(
        cls,
        io_factory: IConfigIOFactory,
    ) -> PlanStorageService:
        '''
            Assembles and instantiates a PlanStorageService adapter with explicit I/O factory.

            :param io_factory: IConfigIOFactory instance.
            :return: Fully assembled PlanStorageService instance.
            :exceptions: None.
        '''
        loader = PlanLoader(io_factory=io_factory)
        storer = PlanStorer(io_factory=io_factory)

        return PlanStorageService(loader=loader, storer=storer)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__
