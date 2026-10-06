# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
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
    Unit tests for CLIBundleOptionsValidator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions import ATSValueError, ATSTypeError

from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.infrastructure.cli.setup.options import CLIBundleOptions
from scarajectory.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleOptionsValidator(TestCase):
    '''
        Test cases for CLIBundleOptionsValidator.

        It defines:

            :methods:
                | test_validate_valid_options - Tests validation of valid CLI bundle options.
                | test_validate_invalid_options - Tests validation failures on invalid options.
                | test_is_valid_success_and_failure - Tests is_valid boolean check.
    '''

    def test_validate_valid_options(self) -> None:
        '''
            Tests validation of complete valid options.

            :exceptions: None.
        '''
        bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        opts = CLIBundleOptions(
            service=bundle.service,
            parser=bundle.base.option_manager,
            gui=bundle.gui,
        )
        CLIBundleOptionsValidator.validate(opts)
        self.assertTrue(CLIBundleOptionsValidator.is_valid(opts))

    def test_validate_invalid_options(self) -> None:
        '''
            Tests validation errors on None, invalid type, and missing/bad option.

            :exceptions: None.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleOptionsValidator.validate(None)  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            CLIBundleOptionsValidator.validate('not_a_mapping')  # type: ignore[arg-type]

        bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        opts_none_attr = CLIBundleOptions(
            service=None,  # type: ignore[arg-type]
            parser=bundle.base.option_manager,
            gui=bundle.gui,
        )
        with self.assertRaises(ATSValueError):
            CLIBundleOptionsValidator.validate(opts_none_attr)

        opts_wrong_type = CLIBundleOptions(
            service='not_a_service',  # type: ignore[arg-type]
            parser=bundle.base.option_manager,
            gui=bundle.gui,
        )
        with self.assertRaises(ATSTypeError):
            CLIBundleOptionsValidator.validate(opts_wrong_type)

    def test_is_valid_success_and_failure(self) -> None:
        '''
            Tests is_valid method on valid and invalid inputs.

            :exceptions: None.
        '''
        bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        opts = CLIBundleOptions(
            service=bundle.service,
            parser=bundle.base.option_manager,
            gui=bundle.gui,
        )
        self.assertTrue(CLIBundleOptionsValidator.is_valid(opts))
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(CLIBundleOptionsValidator.is_valid('bad_opts'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
