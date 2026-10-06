# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for CLIBundle data container.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.infrastructure.cli.setup.options import CLIBundleOptions
from scarajectory.infrastructure.cli.setup.factory import CLIBundleFactory
from scarajectory.infrastructure.cli.setup.bundle import CLIBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundle(TestCase):
    '''
        Test cases for CLIBundle container.

        It defines:

            :methods:
                | test_bundle_attributes - Tests attribute access on CLI bundle.
                | test_to_dict - Tests dictionary conversion of CLI bundle.
    '''

    def _create_sample_cli_bundle(self) -> CLIBundle:
        '''Creates a valid CLIBundle instance for testing.'''
        sample_bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        opts = CLIBundleOptions(
            service=sample_bundle.service,
            parser=sample_bundle.base.option_manager,
            gui=sample_bundle.gui,
        )
        return CLIBundleFactory.create_bundle(options=opts)

    def test_bundle_attributes(self) -> None:
        '''
            Tests bundle attribute values.

            :exceptions: None.
        '''
        cli_bundle = self._create_sample_cli_bundle()
        self.assertIsNotNone(cli_bundle.service)
        self.assertIsNotNone(cli_bundle.parser)
        self.assertIsNotNone(cli_bundle.commands)

    def test_to_dict(self) -> None:
        '''
            Tests dictionary conversion of CLI bundle.

            :exceptions: None.
        '''
        cli_bundle = self._create_sample_cli_bundle()
        data = cli_bundle.to_dict()
        self.assertIsInstance(data, dict)
        self.assertIn('service', data)
        self.assertIn('parser', data)
        self.assertIn('commands', data)


if __name__ == '__main__':
    main()
