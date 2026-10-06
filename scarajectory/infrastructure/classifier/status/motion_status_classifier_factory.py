# -*- coding: UTF-8 -*-

'''
Module
    motion_status_classifier_factory.py
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
    Factory service constructing MotionStatusClassifier instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.classifier.iresponse_parser import IResponseParser
from scarajectory.infrastructure.classifier.response_parser_factory import ResponseParserFactory
from scarajectory.infrastructure.classifier.status.motion_status_classifier import MotionStatusClassifier

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionStatusClassifierFactory:
    '''
        Factory providing creation of MotionStatusClassifier instances.

        It defines:

            :methods:
                | create - Constructs and returns a MotionStatusClassifier instance.
                | create_with_parser - Constructs with explicit response parser.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> MotionStatusClassifier:
        '''
            Constructs and returns a MotionStatusClassifier instance.

            :return: MotionStatusClassifier instance.
        '''
        return cls.create_with_parser(
            response_parser=ResponseParserFactory.create()
        )

    @classmethod
    def create_with_parser(
        cls,
        *,
        response_parser: IResponseParser,
    ) -> MotionStatusClassifier:
        '''
            Constructs and returns a MotionStatusClassifier instance with explicit parser.

            :param response_parser: Injected IResponseParser instance.
            :return: MotionStatusClassifier instance.
        '''
        return MotionStatusClassifier(response_parser=response_parser)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
