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
    Factory constructing Plan subsystem components with collaborator injection.
'''

from __future__ import annotations

from scarajectory.infrastructure.storage.plan.dependencies import PlanDependencies
from scarajectory.infrastructure.storage.plan.loader import PlanLoader
from scarajectory.infrastructure.storage.plan.provides import PlanProvides
from scarajectory.infrastructure.storage.plan.storer import PlanStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanFactory:
    '''
        Factory providing creation of plan persistence subsystem.

        It defines:

            :methods:
                | create - Constructs PlanProvides assembling loader and storer.
                | get_version - Returns package version string.
    '''

    @classmethod
    def create(cls, dependencies: PlanDependencies) -> PlanProvides:
        '''
            Constructs plan persistence provides container with assembled components.

            :param dependencies: Parameter bundle containing loader and storer dependencies.
            :return: PlanProvides containing assembled loader and storer.
            :exceptions: None.
        '''
        loader = PlanLoader(config_loader=dependencies.config_loader)
        storer = PlanStorer(config_storer=dependencies.config_storer)

        return PlanProvides(
            plan_loader=loader,
            plan_storer=storer
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns package version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
