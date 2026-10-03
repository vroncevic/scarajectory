# -*- coding: UTF-8 -*-

'''
Module
    flow_status_classifier_factory.py
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
    Factory service constructing FlowStatusClassifier instances.
'''

from __future__ import annotations

from scarajectory.core.service.classifier.iresponse_parser import IResponseParser
from scarajectory.infrastructure.classifier.response_parser_factory import ResponseParserFactory
from scarajectory.infrastructure.classifier.status.flow_status_classifier import FlowStatusClassifier

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowStatusClassifierFactory:
    '''
        Factory providing creation of FlowStatusClassifier instances.

        It defines:

            :methods:
                | create - Constructs and returns a FlowStatusClassifier instance.
                | create_with_parser - Constructs FlowStatusClassifier with explicit parser.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> FlowStatusClassifier:
        '''
            Constructs and returns a FlowStatusClassifier instance.

            :return: FlowStatusClassifier instance.
        '''
        return cls.create_with_parser(
            response_parser=ResponseParserFactory.create()
        )

    @classmethod
    def create_with_parser(
        cls,
        *,
        response_parser: IResponseParser,
    ) -> FlowStatusClassifier:
        '''
            Constructs and returns a FlowStatusClassifier instance with explicit parser.

            :param response_parser: Injected IResponseParser instance.
            :return: FlowStatusClassifier instance.
        '''
        return FlowStatusClassifier(response_parser=response_parser)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
