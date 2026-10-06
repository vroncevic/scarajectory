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
    Unit tests for SCARAjectoryBundleDependenciesValidator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions import ATSValueError, ATSTypeError

from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.setup.bundle import SCARAjectoryBundle
from scarajectory.setup.dependencies import SCARAjectoryBundleDependencies
from scarajectory.setup.dep_validator import SCARAjectoryBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSCARAjectoryBundleDependenciesValidator(TestCase):
    '''
        Test cases for SCARAjectoryBundleDependenciesValidator.

        It defines:

            :methods:
                | test_validate_valid_dependencies - Tests validation of valid dependencies.
                | test_validate_invalid_dependencies - Tests validation failures on invalid dependencies.
                | test_is_valid_success_and_failure - Tests is_valid boolean check.
    '''

    def test_validate_valid_dependencies(self) -> None:
        '''
            Tests validation of complete and valid dependencies.

            :exceptions: None.
        '''
        bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        deps = SCARAjectoryBundleDependencies(
            base=bundle.base,
            service=bundle.service,
            gui=bundle.gui,
            streamer=bundle.streamer,
            cli=bundle.cli,
        )
        SCARAjectoryBundleDependenciesValidator.validate(deps)
        self.assertTrue(SCARAjectoryBundleDependenciesValidator.is_valid(deps))

    def test_validate_invalid_dependencies(self) -> None:
        '''
            Tests validation errors on None, invalid type, and missing/invalid dependency.

            :exceptions: None.
        '''
        with self.assertRaises(ATSValueError):
            SCARAjectoryBundleDependenciesValidator.validate(None)  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            SCARAjectoryBundleDependenciesValidator.validate('not_a_mapping')  # type: ignore[arg-type]

        bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        deps_missing = SCARAjectoryBundleDependencies(
            base=bundle.base,
            service=bundle.service,
            gui=bundle.gui,
            streamer=bundle.streamer,
            cli=None,  # type: ignore[arg-type]
        )
        with self.assertRaises(ATSValueError):
            SCARAjectoryBundleDependenciesValidator.validate(deps_missing)

    def test_is_valid_success_and_failure(self) -> None:
        '''
            Tests is_valid method on valid and invalid inputs.

            :exceptions: None.
        '''
        bundle: SCARAjectoryBundle = SCARAjectoryBundleFactory.create_bundle()
        deps = SCARAjectoryBundleDependencies(
            base=bundle.base,
            service=bundle.service,
            gui=bundle.gui,
            streamer=bundle.streamer,
            cli=bundle.cli,
        )
        self.assertTrue(SCARAjectoryBundleDependenciesValidator.is_valid(deps))
        self.assertFalse(SCARAjectoryBundleDependenciesValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(SCARAjectoryBundleDependenciesValidator.is_valid('bad_deps'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
