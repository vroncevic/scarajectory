# -*- coding: UTF-8 -*-

'''
Module
    response_classification_registry_factory_test.py
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
    Unit tests for ResponseClassificationRegistryFactory factory service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.classifier.response_classification_registry import (
    ResponseClassificationRegistry,
)
from scarajectory.infrastructure.classifier.response_classification_registry_factory import (
    ResponseClassificationRegistryFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ResponseClassificationRegistryFactoryTestCase(TestCase):
    '''
        Tests ResponseClassificationRegistryFactory component instantiation.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and structure.
                | test_factory_create - Verifies registry populated with protocol rules.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''Verifies factory version string and create callable.'''
        self.assertEqual(
            ResponseClassificationRegistryFactory.get_version(), '1.0.4'
        )
        self.assertTrue(
            hasattr(ResponseClassificationRegistryFactory, 'create')
        )
        self.assertTrue(
            callable(ResponseClassificationRegistryFactory.create)
        )

    def test_factory_create(self) -> None:
        '''Verifies registry is populated with protocol rules.'''
        registry = ResponseClassificationRegistryFactory.create()
        self.assertIsInstance(registry, ResponseClassificationRegistry)
        resp_ack = registry.classify('<RESP:ACK;OK>')
        self.assertEqual(resp_ack.response_type, 'ACK')
        self.assertTrue(resp_ack.is_success)

        resp_full = registry.classify('BUFFER_FULL')
        self.assertEqual(resp_full.response_type, 'FULL')
        self.assertFalse(resp_full.is_success)


if __name__ == '__main__':
    main()
