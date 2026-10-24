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
    Unit tests for SCARAjectoryBundleOptionsValidator.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions import ATSValueError, ATSTypeError

from scarajectory.setup.keys import SCARAjectoryBundleKeys
from scarajectory.setup.options import SCARAjectoryBundleOptions
from scarajectory.setup.opt_validator import SCARAjectoryBundleOptionsValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSCARAjectoryBundleOptionsValidator(TestCase):
    '''
        Test cases for SCARAjectoryBundleOptionsValidator.

        It defines:

            :methods:
                | test_validate_valid_options - Tests validation of valid options.
                | test_validate_invalid_options - Tests validation failures on invalid options.
                | test_is_valid_success_and_failure - Tests is_valid boolean check.
    '''

    def test_validate_valid_options(self) -> None:
        '''
            Tests validation of empty and populated valid options.

            :exceptions: None.
        '''
        empty_opts = SCARAjectoryBundleOptions({})
        SCARAjectoryBundleOptionsValidator.validate(empty_opts)
        self.assertTrue(SCARAjectoryBundleOptionsValidator.is_valid(empty_opts))

        populated_opts = SCARAjectoryBundleOptions({
            SCARAjectoryBundleKeys.OPTION_L1: 150.0,
            SCARAjectoryBundleKeys.OPTION_L2: 120.0,
            SCARAjectoryBundleKeys.OPTION_Z_MIN: 0.0,
            SCARAjectoryBundleKeys.OPTION_Z_MAX: 100.0,
        })
        SCARAjectoryBundleOptionsValidator.validate(populated_opts)
        self.assertTrue(SCARAjectoryBundleOptionsValidator.is_valid(populated_opts))

    def test_validate_invalid_options(self) -> None:
        '''
            Tests validation errors on None, invalid type, and invalid option value type.

            :exceptions: None.
        '''
        with self.assertRaises(ATSValueError):
            SCARAjectoryBundleOptionsValidator.validate(None)  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            SCARAjectoryBundleOptionsValidator.validate('not_a_mapping')  # type: ignore[arg-type]

        invalid_type_opts = SCARAjectoryBundleOptions({
            SCARAjectoryBundleKeys.OPTION_L1: 'not_a_float',
        })
        with self.assertRaises(ATSTypeError):
            SCARAjectoryBundleOptionsValidator.validate(invalid_type_opts)

    def test_is_valid_success_and_failure(self) -> None:
        '''
            Tests is_valid method on valid and invalid inputs.

            :exceptions: None.
        '''
        valid_opts = SCARAjectoryBundleOptions({
            SCARAjectoryBundleKeys.OPTION_L1: 150.0,
        })
        self.assertTrue(SCARAjectoryBundleOptionsValidator.is_valid(valid_opts))
        self.assertFalse(SCARAjectoryBundleOptionsValidator.is_valid(None))  # type: ignore[arg-type]
        self.assertFalse(SCARAjectoryBundleOptionsValidator.is_valid('bad_opts'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
