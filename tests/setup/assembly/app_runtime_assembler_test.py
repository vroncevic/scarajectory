# -*- coding: UTF-8 -*-

'''
Module
    app_runtime_assembler_test.py
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
    Unit tests for AppRuntimeAssembler runtime infrastructure assembly.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.transport.bundle import TransportBundle
from scarajectory.infrastructure.transport.transport_factory import TransportFactory
from scarajectory.setup.assembly.app_runtime_assembler import AppRuntimeAssembler
from scarajectory.setup.assembly.app_runtime_bundle import AppRuntimeBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestAppRuntimeAssembler(TestCase):
    '''
        Test cases for AppRuntimeAssembler component construction.

        It defines:

            :methods:
                | setUp - Initializes context bundle fixture.
                | test_assemble_default - Tests default transport assembly.
                | test_assemble_with_transport - Tests explicit transport.
                | test_get_version - Tests assembler version query.
    '''

    def setUp(self) -> None:
        '''
            Initializes context bundle fixture.

            :exceptions: None.
        '''
        self.context_bundle: ContextBundle = (
            ContextBundleFactory.create_bundle()
        )

    def test_assemble_default(self) -> None:
        '''
            Tests default transport assembly.

            :exceptions: None.
        '''
        bundle: AppRuntimeBundle = AppRuntimeAssembler.assemble(
            context_bundle=self.context_bundle
        )
        self.assertIsInstance(bundle, AppRuntimeBundle)
        self.assertIsNotNone(bundle.connection_repo)
        self.assertIsNotNone(bundle.transport)
        self.assertIsNotNone(bundle.streamer)
        self.assertIsNotNone(bundle.storage)

    def test_assemble_with_transport(self) -> None:
        '''
            Tests explicit transport assembly.

            :exceptions: None.
        '''
        transport: TransportBundle = (
            TransportFactory.create_default_transport()
        )
        bundle: AppRuntimeBundle = AppRuntimeAssembler.assemble_with_transport(
            context_bundle=self.context_bundle,
            transport=transport,
        )
        self.assertIsInstance(bundle, AppRuntimeBundle)
        self.assertIs(bundle.transport, transport)
        self.assertIsNotNone(bundle.streamer)

    def test_get_version(self) -> None:
        '''
            Tests assembler version query.

            :exceptions: None.
        '''
        version: str = AppRuntimeAssembler.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
