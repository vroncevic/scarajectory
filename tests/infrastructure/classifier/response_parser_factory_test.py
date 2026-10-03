# -*- coding: UTF-8 -*-

'''
Module
    response_parser_factory_test.py
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
    Unit tests for ResponseParserFactory factory service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.classifier.response_classification_registry import (
    ResponseClassificationRegistry,
)
from scarajectory.infrastructure.classifier.response_parser import (
    ResponseParser,
)
from scarajectory.infrastructure.classifier.response_parser_factory import (
    ResponseParserFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseParserFactoryTestCase(TestCase):
    '''
        Tests ResponseParserFactory component instantiation.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and structure.
                | test_factory_create - Verifies default parser creation.
                | test_factory_create_with_registry - Verifies creation with custom registry.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''Verifies factory version string and create callable.'''
        self.assertEqual(ResponseParserFactory.get_version(), '1.0.4')
        self.assertTrue(hasattr(ResponseParserFactory, 'create'))
        self.assertTrue(callable(ResponseParserFactory.create))

    def test_factory_create(self) -> None:
        '''Verifies default parser construction and standard parsing.'''
        parser = ResponseParserFactory.create()
        self.assertIsInstance(parser, ResponseParser)
        parsed = parser.parse_response('<RESP:ACK;OK>')
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.response_type, 'ACK')

    def test_factory_create_with_registry(self) -> None:
        '''Verifies construction using injected registry.'''
        mock_registry = MagicMock(spec=ResponseClassificationRegistry)
        parser = ResponseParserFactory.create_with_registry(
            registry=mock_registry
        )
        self.assertIsInstance(parser, ResponseParser)


if __name__ == '__main__':
    main()
