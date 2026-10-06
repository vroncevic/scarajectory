# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for CLIBundleValidator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions import ATSValueError, ATSTypeError

from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.infrastructure.cli.setup.options import CLIBundleOptions
from scarajectory.infrastructure.cli.setup.factory import CLIBundleFactory
from scarajectory.infrastructure.cli.setup.bundle import CLIBundle
from scarajectory.infrastructure.cli.setup.validator import CLIBundleValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleValidator(TestCase):
    '''
        Test cases for CLIBundleValidator.

        It defines:

            :methods:
                | test_validate_valid_bundle - Tests validation of valid CLI bundle.
                | test_validate_invalid_bundle - Tests validation failures on invalid input.
                | test_is_valid_success_and_failure - Tests is_valid boolean check.
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

    def test_validate_valid_bundle(self) -> None:
        '''
            Tests validation of a valid CLI bundle.

            :exceptions: None.
        '''
        cli_bundle = self._create_sample_cli_bundle()
        CLIBundleValidator.validate(cli_bundle)
        self.assertTrue(CLIBundleValidator.is_valid(cli_bundle))

    def test_validate_invalid_bundle(self) -> None:
        '''
            Tests validation failures when invalid CLI bundle or types are provided.

            :exceptions: None.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleValidator.validate(None)  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            CLIBundleValidator.validate('not_a_bundle')  # type: ignore[arg-type]

        cli_bundle = self._create_sample_cli_bundle()
        invalid_cli_bundle = CLIBundle(
            service='not_a_service',  # type: ignore[arg-type]
            parser=cli_bundle.parser,
            commands=cli_bundle.commands,
        )
        with self.assertRaises(ATSTypeError):
            CLIBundleValidator.validate(invalid_cli_bundle)

    def test_is_valid_success_and_failure(self) -> None:
        '''
            Tests is_valid method on valid and invalid inputs.

            :exceptions: None.
        '''
        cli_bundle = self._create_sample_cli_bundle()
        self.assertTrue(CLIBundleValidator.is_valid(cli_bundle))
        self.assertFalse(CLIBundleValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(CLIBundleValidator.is_valid('bad_bundle'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
