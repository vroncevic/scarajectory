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
    Factory service assembling configuration I/O loader and storer subsystems.
'''

from __future__ import annotations

from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.loader.dependencies import LoaderDependencies
from scarajectory.infrastructure.storage.config_io.loader.factory import LoaderFactory
from scarajectory.infrastructure.storage.config_io.loader.provides import LoaderProvides
from scarajectory.infrastructure.storage.config_io.provides import ConfigIOProvides
from scarajectory.infrastructure.storage.config_io.storer.dependencies import StorerDependencies
from scarajectory.infrastructure.storage.config_io.storer.factory import StorerFactory
from scarajectory.infrastructure.storage.config_io.storer.provides import StorerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigIOFactory:
    '''
        Factory providing creation of unified configuration I/O subsystem.

        It defines:

            :methods:
                | create - Constructs ConfigIOProvides assembling loader and storer subsystems.
                | get_version - Returns package version string.
    '''

    @classmethod
    def create(cls, dependencies: ConfigIODependencies) -> ConfigIOProvides:
        '''
            Constructs configuration I/O provides container with assembled loader and storer.

            :param dependencies: Parameter bundle containing ATS context.
            :return: ConfigIOProvides with loader and storer interfaces.
            :exceptions: None.
        '''
        loader_provides: LoaderProvides = LoaderFactory.create(
            LoaderDependencies(context_bundle=dependencies.context_bundle)
        )
        storer_provides: StorerProvides = StorerFactory.create(
            StorerDependencies(context_bundle=dependencies.context_bundle)
        )

        return ConfigIOProvides(
            config_loader=loader_provides.config_loader,
            config_storer=storer_provides.config_storer
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns package version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
