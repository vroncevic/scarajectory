# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
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
    Unit tests for CLIBundleRegistry.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.infrastructure.cli.setup.options import CLIBundleOptions
from scarajectory.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from scarajectory.infrastructure.cli.setup.registry import CLIBundleRegistry
from scarajectory.infrastructure.cli.setup.factory import CLIBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleRegistry(TestCase):
    '''
        Test cases for CLIBundleRegistry.

        It defines:

            :methods:
                | test_create_bundle - Tests CLI bundle creation via registry.
                | test_get_version - Tests CLI bundle registry version query.
    '''

    def test_create_bundle(self) -> None:
        '''
            Tests bundle creation using dependencies.

            :exceptions: None.
        '''
        sample_bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        opts = CLIBundleOptions(
            service=sample_bundle.service,
            parser=sample_bundle.base.option_manager,
            gui=sample_bundle.gui,
        )
        cli_bundle = CLIBundleFactory.create_bundle(options=opts)
        deps = CLIBundleDependencies(
            service=cli_bundle.service,
            parser=cli_bundle.parser,
            commands=cli_bundle.commands,
        )
        bundle = CLIBundleRegistry.create_bundle(dependencies=deps)
        self.assertIsNotNone(bundle)
        self.assertEqual(bundle.service, sample_bundle.service)

    def test_get_version(self) -> None:
        '''
            Tests registry version string.

            :exceptions: None.
        '''
        version = CLIBundleRegistry.get_version()
        self.assertTrue(isinstance(version, str) and len(version) > 0)


if __name__ == '__main__':
    main()
