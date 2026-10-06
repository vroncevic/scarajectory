# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
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
    Unit tests for CLIBundleDependenciesValidator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions import ATSValueError, ATSTypeError

from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.infrastructure.cli.setup.options import CLIBundleOptions
from scarajectory.infrastructure.cli.setup.factory import CLIBundleFactory
from scarajectory.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from scarajectory.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleDependenciesValidator(TestCase):
    '''
        Test cases for CLIBundleDependenciesValidator.

        It defines:

            :methods:
                | test_validate_valid_dependencies - Tests validation of valid CLI bundle dependencies.
                | test_validate_invalid_dependencies - Tests validation failures on invalid dependencies.
                | test_is_valid_success_and_failure - Tests is_valid boolean check.
    '''

    def _create_sample_deps(self) -> CLIBundleDependencies:
        '''Creates a valid CLIBundleDependencies instance for testing.'''
        sample_bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        opts = CLIBundleOptions(
            service=sample_bundle.service,
            parser=sample_bundle.base.option_manager,
            gui=sample_bundle.gui,
        )
        cli_bundle = CLIBundleFactory.create_bundle(options=opts)
        return CLIBundleDependencies(
            service=cli_bundle.service,
            parser=cli_bundle.parser,
            commands=cli_bundle.commands,
        )

    def test_validate_valid_dependencies(self) -> None:
        '''
            Tests validation of complete and valid CLI dependencies.

            :exceptions: None.
        '''
        deps = self._create_sample_deps()
        CLIBundleDependenciesValidator.validate(deps)
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(deps))

    def test_validate_invalid_dependencies(self) -> None:
        '''
            Tests validation errors on None, invalid type, and missing/invalid dependency.

            :exceptions: None.
        '''
        with self.assertRaises(ATSValueError):
            CLIBundleDependenciesValidator.validate(None)  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            CLIBundleDependenciesValidator.validate('not_a_mapping')  # type: ignore[arg-type]

        deps = self._create_sample_deps()
        deps_missing = CLIBundleDependencies(
            service=None,  # type: ignore[arg-type]
            parser=deps['parser'],
            commands=deps['commands'],
        )
        with self.assertRaises(ATSValueError):
            CLIBundleDependenciesValidator.validate(deps_missing)

        deps_wrong_type = CLIBundleDependencies(
            service='not_a_service',  # type: ignore[arg-type]
            parser=deps['parser'],
            commands=deps['commands'],
        )
        with self.assertRaises(ATSTypeError):
            CLIBundleDependenciesValidator.validate(deps_wrong_type)

    def test_is_valid_success_and_failure(self) -> None:
        '''
            Tests is_valid method on valid and invalid inputs.

            :exceptions: None.
        '''
        deps = self._create_sample_deps()
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(deps))
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(CLIBundleDependenciesValidator.is_valid('bad_deps'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
