# -*- coding: UTF-8 -*-

'''
Module
    stream_config_loader_factory.py
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
    Factory providing StreamConfigLoader instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.settings.isettings_reader import ISettingsReader
from scarajectory.infrastructure.settings.settings_reader_factory import SettingsReaderFactory
from scarajectory.infrastructure.settings.stream.stream_config_loader import StreamConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamConfigLoaderFactory:
    '''
        Factory providing StreamConfigLoader instances.

        It defines:

            :methods:
                | create - Instantiates StreamConfigLoader with default reader.
                | create_with_reader - Instantiates StreamConfigLoader with explicit reader.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> StreamConfigLoader:
        '''
            Creates and returns a StreamConfigLoader instance using default SettingsReader.

            :return: Fully configured StreamConfigLoader instance.
        '''
        return cls.create_with_reader(reader=SettingsReaderFactory.create())

    @classmethod
    def create_with_reader(
        cls,
        *,
        reader: ISettingsReader,
    ) -> StreamConfigLoader:
        '''
            Creates and returns a StreamConfigLoader instance with explicit ISettingsReader.

            :param reader: ISettingsReader providing configuration key-values.
            :return: Fully configured StreamConfigLoader instance.
        '''
        return StreamConfigLoader(reader=reader)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
