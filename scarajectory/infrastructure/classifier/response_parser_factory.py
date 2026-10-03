# -*- coding: UTF-8 -*-

'''
Module
    response_parser_factory.py
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
    Factory service constructing ResponseParser instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.classifier.response_classification_registry import ResponseClassificationRegistry
from scarajectory.infrastructure.classifier.response_classification_registry_factory import ResponseClassificationRegistryFactory
from scarajectory.infrastructure.classifier.response_parser import ResponseParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseParserFactory:
    '''
        Factory providing creation of ResponseParser instances.

        It defines:

            :methods:
                | create - Constructs and returns a ResponseParser instance.
                | create_with_registry - Constructs ResponseParser with explicit registry.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ResponseParser:
        '''
            Constructs and returns a ResponseParser instance.

            :return: ResponseParser instance.
        '''
        registry: ResponseClassificationRegistry = (
            ResponseClassificationRegistryFactory.create()
        )
        return cls.create_with_registry(registry=registry)

    @classmethod
    def create_with_registry(
        cls,
        *,
        registry: ResponseClassificationRegistry,
    ) -> ResponseParser:
        '''
            Constructs and returns a ResponseParser instance with explicit registry.

            :param registry: Injected ResponseClassificationRegistry instance.
            :return: ResponseParser instance.
        '''
        return ResponseParser(registry=registry)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
