# -*- coding: UTF-8 -*-

'''
Module
    connection_repository_factory.py
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
    Factory module for assembling and instantiating ConnectionRepository instances.
'''

from __future__ import annotations

from pathlib import Path

from ats_utilities.context.bundle import ContextBundle

from scarajectory.infrastructure.preferences.connection_repository import ConnectionRepository

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionRepositoryFactory:
    '''
        Factory responsible for creating ConnectionRepository instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a ConnectionRepository with default configuration file path.
                | create_with_path - Assembles ConnectionRepository with explicit configuration file path.
                | get_version - Returns factory module semantic version string.
    '''

    @classmethod
    def create(cls, context_bundle: ContextBundle) -> ConnectionRepository:
        '''
            Assembles and instantiates a ConnectionRepository instance with default path.

            :param context_bundle: ATS ContextBundle instance.
            :return: Fully assembled ConnectionRepository instance.
        '''
        return cls.create_with_path(
            context_bundle=context_bundle,
            config_file=ConnectionRepository.DEFAULT_CONFIG_FILE,
        )

    @classmethod
    def create_with_path(
        cls,
        *,
        context_bundle: ContextBundle,
        config_file: Path,
    ) -> ConnectionRepository:
        '''
            Assembles and instantiates a ConnectionRepository instance with explicit config path.

            :param context_bundle: ATS ContextBundle instance.
            :param config_file: Path to configuration storage file.
            :return: Fully assembled ConnectionRepository instance.
        '''
        return ConnectionRepository(
            context_bundle=context_bundle,
            config_file=config_file,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__
