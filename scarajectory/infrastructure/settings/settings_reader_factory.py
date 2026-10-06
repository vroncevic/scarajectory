# -*- coding: UTF-8 -*-

'''
Module
    settings_reader_factory.py
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
    Factory providing SettingsReader instances for raw configuration ingestion.
'''

from __future__ import annotations

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.settings.settings_reader import SettingsReader
from scarajectory.infrastructure.storage.config_io.config_io_factory import ConfigIOFactory
from scarajectory.infrastructure.storage.config_io.iconfig_io_factory import IConfigIOFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SettingsReaderFactory:
    '''
        Factory providing SettingsReader instances.

        It defines:

            :methods:
                | create - Instantiates SettingsReader with default paths.
                | create_with_context - Instantiates SettingsReader with explicit context.
                | create_with_paths - Instantiates SettingsReader with explicit paths.
                | create_with_io_factory - Instantiates SettingsReader with explicit IConfigIOFactory.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> SettingsReader:
        '''
            Creates and returns a SettingsReader instance using default configuration paths.

            :return: Fully configured SettingsReader instance.
        '''
        return cls.create_with_context(
            context_bundle=ContextBundleFactory.create_bundle()
        )

    @classmethod
    def create_with_context(cls, context_bundle: ContextBundle) -> SettingsReader:
        '''
            Creates and returns a SettingsReader instance using default paths and explicit context bundle.

            :param context_bundle: ATS ContextBundle instance.
            :return: Fully configured SettingsReader instance.
        '''
        return cls.create_with_paths(
            config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
            scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            context_bundle=context_bundle,
        )

    @classmethod
    def create_with_paths(
        cls,
        *,
        config_path: str,
        scheme_path: str,
        context_bundle: ContextBundle,
    ) -> SettingsReader:
        '''
            Creates and returns a SettingsReader instance with explicit configuration paths.

            :param config_path: Absolute path to geometry configuration file.
            :param scheme_path: Absolute path to validation schema file.
            :param context_bundle: ATS ContextBundle instance.
            :return: Fully configured SettingsReader instance.
        '''
        io_factory: IConfigIOFactory = ConfigIOFactory.create(context_bundle)
        return cls.create_with_io_factory(
            config_path=config_path,
            scheme_path=scheme_path,
            io_factory=io_factory,
        )

    @classmethod
    def create_with_io_factory(
        cls,
        *,
        config_path: str,
        scheme_path: str,
        io_factory: IConfigIOFactory,
    ) -> SettingsReader:
        '''
            Creates and returns a SettingsReader instance with explicit I/O factory.

            :param config_path: Absolute path to geometry configuration file.
            :param scheme_path: Absolute path to validation schema file.
            :param io_factory: Injected IConfigIOFactory instance.
            :return: Fully configured SettingsReader instance.
        '''
        return SettingsReader(
            config_path=config_path,
            scheme_path=scheme_path,
            io_factory=io_factory,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
