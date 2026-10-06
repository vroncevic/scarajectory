# -*- coding: UTF-8 -*-

'''
Module
    app_core_assembler_test.py
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
    Unit tests for AppCoreAssembler kinematics and validation assembly.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.factory import ContextBundleFactory
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds

from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory
from scarajectory.setup.assembly.app_core_assembler import AppCoreAssembler
from scarajectory.setup.assembly.app_core_bundle import AppCoreBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestAppCoreAssembler(TestCase):
    '''
        Test cases for AppCoreAssembler component construction.

        It defines:

            :methods:
                | setUp - Initializes test bounds fixture.
                | test_assemble_core_bundle - Tests assembly of core bundle.
                | test_get_version - Tests assembler version query.
    '''

    def setUp(self) -> None:
        '''
            Initializes test bounds fixture.

            :exceptions: None.
        '''
        self.bounds: ScaraBounds = (
            ScaraBoundsLoaderFactory.create().load_bounds()
        )

    def test_assemble_core_bundle(self) -> None:
        '''
            Tests assembly of core bundle.

            :exceptions: None.
        '''
        bundle: AppCoreBundle = AppCoreAssembler.assemble(
            bounds=self.bounds,
            context_bundle=ContextBundleFactory.create_bundle(),
        )
        self.assertIsInstance(bundle, AppCoreBundle)
        self.assertEqual(bundle.bounds.links.l1, self.bounds.links.l1)
        self.assertEqual(bundle.bounds.links.l2, self.bounds.links.l2)
        self.assertIsNotNone(bundle.transmission)
        self.assertIsNotNone(bundle.kinematics)
        self.assertIsNotNone(bundle.validator)
        self.assertEqual(bundle.validator.bounds.links.l1, self.bounds.links.l1)

    def test_get_version(self) -> None:
        '''
            Tests assembler version query.

            :exceptions: None.
        '''
        version: str = AppCoreAssembler.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
