# -*- coding: UTF-8 -*-

'''
Module
    plan_storage_service_factory_test.py
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
    Unit tests for PlanStorageServiceFactory instantiation and assembly.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.storage.plan_storage_service import PlanStorageService
from scarajectory.infrastructure.storage.plan_storage_service_factory import (
    PlanStorageServiceFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanStorageServiceFactory(TestCase):
    '''
        Test cases verifying PlanStorageServiceFactory assembly operations.

        It defines:

            :methods:
                | test_create - Verifies factory creates PlanStorageService with default context.
                | test_create_with_context - Verifies assembly with explicit ContextBundle.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates a valid PlanStorageService instance.
        '''
        storage = PlanStorageServiceFactory.create()
        self.assertIsInstance(storage, PlanStorageService)

    def test_create_with_context(self) -> None:
        '''
            Verifies factory creates PlanStorageService with explicit ContextBundle.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        storage = PlanStorageServiceFactory.create_with_context(bundle)
        self.assertIsInstance(storage, PlanStorageService)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns semantic version string matching package.
        '''
        version = PlanStorageServiceFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.4')


if __name__ == '__main__':
    main()
